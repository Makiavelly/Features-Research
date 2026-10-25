"""Measure saved model inference vs features, without changing the live run."""
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
    selection = json.loads((OUT / "selected.json").read_text())
    directory = Path(selection["directory"])
    program = json.loads((directory / "program.json").read_text())
    model = lgb.Booster(model_file=str(directory / "model.txt"))
    table = load_dataset(ROOT / "data/rel-hm").load_task("user-item-purchase").get_table("val")
    users = table.df.customer_id.to_numpy()[:8]
    engine = FeatureEngine(CACHE / "benchmark")
    start = time.perf_counter()
    engine.prepare(table.df.timestamp.iloc[0], users, program)
    prepare_seconds = time.perf_counter()-start
    catalog = np.sort(engine.items.article_id.to_numpy())
    start = time.perf_counter()
    pairs = pd.DataFrame({"customer_id": np.repeat(users, len(catalog)), "article_id": np.tile(catalog, len(users))})
    pairs_seconds = time.perf_counter()-start
    start = time.perf_counter()
    values = engine.matrix(pairs)
    feature_seconds = time.perf_counter()-start
    predictions, times = {}, {}
    reference = None
    for threads in [2, 6, 12]:
        start = time.perf_counter()
        scores = model.predict(values, num_threads=threads).reshape(len(users), len(catalog))
        times[str(threads)] = time.perf_counter()-start
        if reference is None:
            reference = scores.copy()
        predictions[str(threads)] = bool(np.array_equal(scores, reference))
    start = time.perf_counter()
    result = np.stack([topk(scores, catalog) for scores in reference])
    topk_seconds = time.perf_counter()-start
    saved = np.load(directory / "final_val_predictions.npy", mmap_mode="r")[:len(users)]
    report = {"users": len(users), "catalog_size": len(catalog), "prepare_once_seconds": prepare_seconds,
              "pair_construction_seconds": pairs_seconds, "features_seconds": feature_seconds,
              "prediction_seconds_by_threads": times, "scores_identical_by_threads": predictions,
              "topk_seconds": topk_seconds, "predictions_match_live_saved": bool(np.array_equal(result, saved)),
              "concurrent_live_evaluator": True, "feature_matrix_megabytes": values.nbytes/1e6}
    atomic_json(OUT / "scoring_benchmark.json", report)
    engine.close()
    print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
