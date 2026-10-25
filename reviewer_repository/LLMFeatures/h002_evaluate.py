"""Train and score only the frozen shared candidate pools; no full-catalog calls."""
import argparse
import hashlib
import json
import time
from h002_common import OUT, CACHE, ROOT, RUN, OLD
import evaluate as ev
from features import FeatureEngine, validate_program
import lightgbm as lgb
import numpy as np
import pandas as pd
from relbench import load_dataset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True)
    parser.add_argument("--stage", choices=["search", "confirm", "final", "replay"], required=True)
    args = parser.parse_args()
    directory = __import__('pathlib').Path(args.directory)
    destination = directory / "replay" if args.stage == "replay" else directory
    destination.mkdir(exist_ok=True)
    program = validate_program(json.loads((directory / "program.json").read_text()))
    started = time.perf_counter()
    engine = FeatureEngine(CACHE / "scratch")
    task = load_dataset(ROOT / "data/rel-hm").load_task("user-item-purchase")
    if args.stage == "search" and not (directory / "model.txt").exists():
        model = ev.fit(engine, program, directory)
    else:
        model = lgb.Booster(model_file=str(directory / "model.txt"))
    if args.stage == "search" and directory.name == "raw_control":
        sample = ev.train_pairs().sort_values('timestamp').tail(2048)
        engine.prepare(sample.timestamp.iloc[0], sample.customer_id.values, program)
        values = engine.matrix(sample)
        control = lgb.Booster(model_file=str(OLD / "raw_control/model.txt"))
        old_scores = control.predict(values, num_threads=2)
        new_scores = model.predict(values, num_threads=8)
        identical = np.array_equal(old_scores, new_scores)
        ev.atomic_json(OUT / "training_threads_check.json", {"old_threads": 2, "new_threads": 8,
                       "checked_pairs": len(sample), "scores_bit_identical": identical,
                       "max_absolute_error": float(np.max(np.abs(old_scores-new_scores)))})
        if not identical:
            raise RuntimeError("Raw control changed with training threads; inspect before proceeding")
    if args.stage == "replay":
        ev.PREDICT_THREADS = 2
    result = {"stage": args.stage, "protocol": "saved ID-GNN candidate pools", "smoke": False,
              "model_sha256": hashlib.sha256((directory / "model.txt").read_bytes()).hexdigest(),
              "program_sha256": hashlib.sha256((directory / "program.json").read_bytes()).hexdigest(),
              "prediction_threads": ev.PREDICT_THREADS, "inference_from_saved_model": True}
    for split in (["val", "test"] if args.stage in ["final", "replay"] else ["val"]):
        table = task.get_table(split)
        indices = None
        if args.stage in ["search", "confirm"]:
            indices = np.load(OUT / "validation_selection.npz")[args.stage]
            table.df = table.df.iloc[indices].copy().reset_index(drop=True)
        tick = time.perf_counter()
        predictions = ev.shared_candidates(engine, program, model, table, destination, split, indices)
        pool_file = ROOT / f"RelBenchGNN/results/seed_42/inference/{split}_candidates.parquet"
        pool = pd.read_parquet(pool_file)
        if indices is not None:
            pool = pool.iloc[indices]
        if not all(len(np.unique(p)) == 12 and np.isin(p, c).all()
                   for p, c in zip(predictions, pool.candidates)):
            raise RuntimeError("Invalid shared top12")
        metrics = task.evaluate(predictions) if split == "test" else task.evaluate(predictions, table)
        result[split + "_metrics"] = metrics
        result[split + "_users"] = len(table.df)
        result[split + "_pairs"] = int(pool.candidates.map(len).sum())
        result[split + "_seconds"] = time.perf_counter() - tick
        if args.stage == "replay":
            reference = json.loads((directory / "final_metrics.json").read_text())
            if not np.array_equal(predictions, np.load(directory / f"shared_{split}_predictions.npy")):
                raise RuntimeError("Replay top12 mismatch")
            if metrics != reference[split + "_metrics"]:
                raise RuntimeError("Replay metrics mismatch")
    result["elapsed_seconds"] = time.perf_counter() - started
    result["passed"] = True
    ev.atomic_json(directory / ("verification.json" if args.stage == "replay" else args.stage + "_metrics.json"), result)
    engine.close()
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
