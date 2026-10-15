"""Isolated downstream evaluator. The LLM never receives validation/test labels."""
import argparse
import gc
import hashlib
import json
import os
from pathlib import Path
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
import lightgbm as lgb
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from features import FeatureEngine, ROOT, USER_COLUMNS, ITEM_COLUMNS
sys.path.insert(0, str(ROOT / "RelBenchGNN"))
from tracking import record
from relbench import load_dataset

OUT = ROOT / "LLMFeatures/results/qwen25coder7b_seed42_v1"
CACHE = ROOT / "baseline/cache/llmfe_qwen25coder7b_v1"
RUN = "hm_llmfe_qwen25coder7b_seed42_v1"


def atomic_json(path, data):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    temporary.replace(path)


def train_pairs():
    """Reuse row selection/negatives only; no old feature values are read."""
    path = CACHE / "train_pairs.parquet"
    if path.exists():
        return pd.read_parquet(path)
    build = json.loads((ROOT / "baseline/cache/manual_v1/build_complete.json").read_text())
    frames = [pd.read_parquet(ROOT / file, columns=["customer_id", "article_id", "timestamp", "label"])
              for file in build["files"]["train"]]
    pairs = pd.concat(frames, ignore_index=True)
    if pairs.duplicated(["customer_id", "article_id", "timestamp"]).any():
        raise RuntimeError("Duplicate supervised pairs")
    CACHE.mkdir(parents=True, exist_ok=True)
    pairs.to_parquet(path, index=False)
    return pairs


def fit(engine, program, destination, smoke=False):
    pairs = train_pairs()
    if smoke:
        last_time = pairs.timestamp.max()
        pairs = pairs[pairs.timestamp == last_time].head(2000).copy()
    groups = list(pairs.groupby("timestamp", sort=True))
    parts = []
    # All train arrays fit in RAM (<250 MB at maximum supported program size).
    for index, (timestamp, frame) in enumerate(groups):
        engine.prepare(timestamp, frame.customer_id.values, program)
        parts.append((engine.matrix(frame), frame.label.to_numpy(dtype=np.int8)))
        if index % 10 == 0:
            print(f"TRAIN SNAPSHOT {index+1}/{len(groups)} {timestamp}", flush=True)
    values = np.concatenate([part[0] for part in parts])
    labels = np.concatenate([part[1] for part in parts])
    del parts
    gc.collect()
    categorical = [f"raw_u_{name}" for name in ["club_member_status", "fashion_news_frequency"]]
    categorical += [f"raw_i_{name}" for name in ITEM_COLUMNS]
    params = {"objective": "binary", "verbosity": -1, "num_threads": 2,
              "learning_rate": .05, "num_leaves": 31, "min_data_in_leaf": 100,
              "max_bin": 127, "feature_fraction": .9, "bagging_fraction": .8,
              "bagging_freq": 1, "deterministic": True, "force_col_wise": True,
              "seed": 42, "feature_fraction_seed": 42, "bagging_seed": 42,
              "data_random_seed": 42}
    dataset = lgb.Dataset(values, label=labels, feature_name=engine.feature_names,
                          categorical_feature=categorical)
    model = lgb.train(params, dataset, num_boost_round=10 if smoke else 150)
    model.save_model(str(destination / "model.txt"))
    schema = {"features": engine.feature_names, "categorical": categorical,
              "category_maps": engine.category_maps, "train_pairs": len(labels),
              "train_user_times": int(pairs[["customer_id", "timestamp"]].drop_duplicates().shape[0]),
              "params": params, "rounds": 10 if smoke else 150, "smoke": smoke}
    atomic_json(destination / "feature_schema.json", schema)
    del model, dataset, values, labels, pairs
    gc.collect()
    # Every reported result uses a reloaded model, including search scores.
    return lgb.Booster(model_file=str(destination / "model.txt"))


def topk(scores, item_ids, k=12):
    """Deterministic order, score descending then article_id ascending."""
    scores = np.asarray(scores)
    ids = np.asarray(item_ids)
    if len(ids) < k or not np.isfinite(scores).all() or len(np.unique(ids)) != len(ids):
        raise ValueError("Invalid scoring input")
    threshold = np.partition(scores, len(scores)-k)[len(scores)-k]
    above = np.flatnonzero(scores > threshold)
    tied = np.flatnonzero(scores == threshold)
    tied = tied[np.argsort(ids[tied], kind="stable")[:k-len(above)]]
    chosen = np.r_[above, tied]
    return ids[chosen[np.lexsort((ids[chosen], -scores[chosen]))]]


def full_catalog(engine, program, model, table, destination, split, stage, resume=True):
    users = table.df.customer_id.to_numpy(dtype=np.int64)
    timestamp = table.df.timestamp.iloc[0]
    if not (table.df.timestamp == timestamp).all():
        raise ValueError("Evaluation split must have one snapshot")
    engine.prepare(timestamp, users, program)
    catalog = np.sort(engine.items.article_id.to_numpy(dtype=np.int64))
    array_path = destination / f"{stage}_{split}_predictions.npy"
    state_path = destination / f"{stage}_{split}_progress.json"
    user_order_sha256 = hashlib.sha256(users.tobytes()).hexdigest()
    start = 0
    if resume and state_path.exists():
        progress = json.loads(state_path.read_text())
        if progress["user_order_sha256"] != user_order_sha256:
            raise RuntimeError("Evaluation user order changed on resume")
        start = progress["completed_users"]
        predictions = np.lib.format.open_memmap(array_path, mode="r+")
    else:
        predictions = np.lib.format.open_memmap(array_path, mode="w+", dtype=np.int64, shape=(len(users), 12))
    started = time.perf_counter()
    for offset in range(start, len(users), 8):
        selected = users[offset:offset+8]
        pairs = pd.DataFrame({"customer_id": np.repeat(selected, len(catalog)),
                              "article_id": np.tile(catalog, len(selected))})
        values = engine.matrix(pairs)
        scores = model.predict(values, num_threads=2).reshape(len(selected), len(catalog))
        for index in range(len(selected)):
            predictions[offset+index] = topk(scores[index], catalog)
        predictions.flush()
        atomic_json(state_path, {"user_order_sha256": user_order_sha256, "total_users": len(users),
                                "completed_users": offset+len(selected),
                                "catalog_size": len(catalog), "elapsed_seconds_current_process": time.perf_counter()-started})
        if offset % 256 == 0 or offset+len(selected) == len(users):
            message = f"LLM-FE {stage}/{split}: {offset+len(selected)}/{len(users)} пользователей, полный каталог"
            print(message, flush=True)
            record("llmfe_scoring", message, RUN, status="evaluating", stage=stage, split=split,
                   scored_users=offset+len(selected), total_users=len(users), catalog_size=len(catalog))
        del pairs, values, scores
    return np.asarray(predictions), time.perf_counter()-started


def shared_candidates(engine, program, model, table, destination, split):
    candidates = pd.read_parquet(ROOT / f"RelBenchGNN/results/seed_42/inference/{split}_candidates.parquet")
    if not np.array_equal(candidates.customer_id.values, table.df.customer_id.values):
        raise RuntimeError("Candidate order differs from task")
    engine.prepare(table.df.timestamp.iloc[0], table.df.customer_id.values, program)
    predictions = np.empty((len(candidates), 12), dtype=np.int64)
    for start in range(0, len(candidates), 1000):
        frame = candidates.iloc[start:start+1000]
        counts = frame.candidates.map(len).to_numpy()
        pairs = pd.DataFrame({"customer_id": np.repeat(frame.customer_id.values, counts),
                              "article_id": np.concatenate(frame.candidates.values).astype(np.int64)})
        scores = model.predict(engine.matrix(pairs), num_threads=2)
        boundaries = np.r_[0, np.cumsum(counts)]
        for row, (left, right) in enumerate(zip(boundaries[:-1], boundaries[1:])):
            predictions[start+row] = topk(scores[left:right], pairs.article_id.values[left:right])
    np.save(destination / f"shared_{split}_predictions.npy", predictions)
    return predictions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True)
    parser.add_argument("--stage", choices=["smoke", "search", "confirm", "final"], required=True)
    args = parser.parse_args()
    destination = Path(args.directory)
    program = json.loads((destination / "program.json").read_text())
    started = time.perf_counter()
    engine = FeatureEngine(CACHE / "scratch")
    task = load_dataset(ROOT / "data/rel-hm").load_task("user-item-purchase")
    smoke = args.stage == "smoke"
    if args.stage in ["smoke", "search"] or not (destination / "model.txt").exists():
        model = fit(engine, program, destination, smoke)
    else:
        model = lgb.Booster(model_file=str(destination / "model.txt"))
    result = {"stage": args.stage, "smoke": smoke, "seed": 42,
              "inference_from_saved_model": True, "program_sha256": __import__('features').digest(program)}
    for split in (["val", "test"] if args.stage == "final" else ["val"]):
        table = task.get_table(split)  # test labels are masked
        if args.stage != "final":
            selection = np.load(OUT / "validation_selection.npz")
            indices = selection["search" if args.stage in ["search", "smoke"] else "confirm"]
            if smoke:
                indices = indices[:8]
            table.df = table.df.iloc[indices].copy().reset_index(drop=True)
        # Smoke scores the complete catalog for a few users, never a fake test.
        predictions, seconds = full_catalog(engine, program, model, table, destination, split, args.stage)
        if split == "test":
            metrics = task.evaluate(predictions)
        else:
            metrics = task.evaluate(predictions, table)
        result[f"{split}_metrics"] = metrics
        result[f"{split}_users"] = len(table.df)
        result[f"{split}_seconds"] = seconds
        if args.stage == "final":
            shared = shared_candidates(engine, program, model, table, destination, split)
            result[f"shared_{split}_metrics"] = task.evaluate(shared) if split == "test" else task.evaluate(shared, table)
    result["elapsed_seconds"] = time.perf_counter()-started
    result["features"] = engine.feature_names
    atomic_json(destination / f"{args.stage}_metrics.json", result)
    engine.close()
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
