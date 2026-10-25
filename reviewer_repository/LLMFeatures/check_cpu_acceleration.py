"""Repeated CPU benchmarks and exact equivalence, with the live worker stopped."""
import hashlib
import json
from pathlib import Path
import time

import lightgbm as lgb
import numpy as np
import pandas as pd
from relbench import load_dataset

from features import FeatureEngine, ROOT
from evaluate import OUT, CACHE, topk, atomic_json


def main():
    directory = Path(json.loads((OUT / "selected.json").read_text())["directory"])
    model_file = directory / "model.txt"
    program_file = directory / "program.json"
    model = lgb.Booster(model_file=str(model_file))
    program = json.loads(program_file.read_text())
    table = load_dataset(ROOT / "data/rel-hm").load_task("user-item-purchase").get_table("val")
    completed = json.loads((directory / "final_val_progress.json").read_text())["completed_users"]
    rng = np.random.default_rng(42)
    indices = np.r_[np.arange(8), np.sort(rng.choice(np.arange(8, completed), 24, replace=False))]
    selected_users = table.df.customer_id.to_numpy()[indices]
    engine = FeatureEngine(CACHE / "cpu_acceleration_check")
    engine.prepare(table.df.timestamp.iloc[0], selected_users, program)
    catalog = np.sort(engine.items.article_id.to_numpy())
    saved = np.load(directory / "final_val_predictions.npy", mmap_mode="r")
    results = []
    for part in range(4):
        chosen = indices[part*8:part*8+8]
        users = table.df.customer_id.to_numpy()[chosen]
        pairs = pd.DataFrame({"customer_id": np.repeat(users, len(catalog)), "article_id": np.tile(catalog, len(users))})
        start = time.perf_counter()
        values = engine.matrix(pairs)
        feature_seconds = time.perf_counter()-start
        reference = model.predict(values, num_threads=2)
        pred = np.stack([topk(row, catalog) for row in reference.reshape(8, -1)])
        if not np.array_equal(pred, saved[chosen]):
            raise RuntimeError("Recomputed baseline differs from completed native predictions")
        for repeat in range(2):
            for threads in rng.permutation([2, 6, 8, 12]):
                started = time.perf_counter()
                scores = model.predict(values, num_threads=int(threads))
                seconds = time.perf_counter()-started
                identical = bool(np.array_equal(scores, reference))
                if not identical:
                    raise RuntimeError(f"Scores changed with {threads} threads")
                results.append({"batch": part, "repeat": repeat, "threads": int(threads),
                                "predict_seconds": seconds, "feature_seconds": feature_seconds,
                                "scores_bit_identical": identical})
            print(f"Checked batch {part+1}/4, repeat {repeat+1}/2", flush=True)
    medians = {str(threads): float(np.median([item["predict_seconds"] for item in results if item["threads"] == threads]))
               for threads in [2, 6, 8, 12]}
    chosen_threads = min(medians, key=medians.get)
    feature_median = float(np.median([item["feature_seconds"] for item in results]))
    report = {"passed": True, "users": len(indices), "pairs_per_pass": len(indices)*len(catalog),
              "catalog_size": len(catalog), "validation_indices": indices.tolist(),
              "repeats_per_setting": 8, "all_scores_bit_identical": True, "all_top12_match_saved": True,
              "live_evaluator_stopped_during_benchmark": True,
              "median_predict_seconds": medians, "median_feature_seconds": feature_median,
              "chosen_threads": int(chosen_threads),
              "prediction_speedup": medians["2"]/medians[chosen_threads],
              "estimated_batch_speedup": (medians["2"]+feature_median)/(medians[chosen_threads]+feature_median),
              "model_sha256": hashlib.sha256(model_file.read_bytes()).hexdigest(),
              "program_sha256": hashlib.sha256(program_file.read_bytes()).hexdigest(), "measurements": results}
    atomic_json(OUT / "cpu_acceleration_check.json", report)
    engine.close()
    print(json.dumps({key: value for key,value in report.items() if key != "measurements"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
