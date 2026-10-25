"""RelBench popularity and past-visit baselines, evaluated on complete val/test."""
from collections import Counter
import json
from pathlib import Path
import time
import sys

import numpy as np
import pandas as pd
from relbench import load_dataset

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "RelBenchGNN"))
from tracking import record


def main():
    dataset = load_dataset(ROOT / "data/rel-hm")
    task = dataset.load_task("user-item-purchase")
    train = task.get_table("train").df
    val = task.get_table("val")
    test = task.get_table("test", mask_input_cols=False)
    out = ROOT / "baseline/results"
    out.mkdir(parents=True, exist_ok=True)
    results = {}
    started = time.time()
    for split, history, target in [("val", train, val), ("test", pd.concat([train, val.df], ignore_index=True), test)]:
        k = task.eval_k
        popularity = Counter()
        for items in history.article_id:
            popularity.update(items)
        top = [item for item, _ in popularity.most_common(k)]
        global_pred = np.tile(np.array(top, dtype=np.int64), (len(target), 1))
        needed = set(target.df.customer_id)
        relevant = history[history.customer_id.isin(needed)]

        def top_past(group):
            counts = Counter()
            for items in group:
                counts.update(items)
            top = [item for item, _ in counts.most_common(k)]
            return top + [-1] * (k - len(top))

        lookup = relevant.groupby("customer_id", sort=False).article_id.apply(top_past).to_dict()
        past_pred = np.array([lookup.get(user, [-1] * k) for user in target.df.customer_id], dtype=np.int64)
        results[split] = {}
        for name, pred in [("global_popularity", global_pred), ("past_visit", past_pred)]:
            metrics = task.evaluate(pred, target)
            results[split][name] = metrics
            np.save(out / f"{name}_{split}_predictions.npy", pred)
            print(split, name, metrics, flush=True)
    results["elapsed_seconds"] = time.time() - started
    (out / "simple_metrics.json").write_text(json.dumps(results, indent=2))
    for name in ["global_popularity", "past_visit"]:
        record("baseline_complete", f"Завершён baseline {name}", f"hm_{name}_v1", status="complete",
               val_metrics=results["val"][name], test_metrics=results["test"][name],
               artifacts="baseline/results/simple_metrics.json", elapsed_seconds=results["elapsed_seconds"])


if __name__ == "__main__":
    main()
