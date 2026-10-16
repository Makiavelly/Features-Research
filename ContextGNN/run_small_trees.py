"""Retrain both LightGBM baselines on the SAME pilot train pairs/full catalog."""
import hashlib
import json
from pathlib import Path
import sys
import gc
import time
import numpy as np
import pandas as pd
import pyarrow.dataset as pads
import lightgbm as lgb
from relbench import load_dataset
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "baseline"), str(ROOT / "RelBenchGNN")]
from run_manual_tree import predict, dense
from tracking import record
BASE = ROOT / "ContextGNN"
OUT = BASE / "results/hm_small_v1"
task = load_dataset(ROOT / "data/rel-hm-small-v1").load_task("user-item-purchase")
manual_dir = BASE / "cache/hm_small_v1/manual"
manual = json.loads((manual_dir / "manifest.json").read_text())
schema = json.loads((manual_dir / "schema.json").read_text())
gnn = json.loads((BASE / "cache/hm_small_v1/idgnn_features/manifest.json").read_text())
key_reference = None
for kind, manifest, features, categorical in [
    ("lightgbm_manual", manual, schema["features"], schema["categorical_features"]),
    ("lightgbm_idgnn", gnn, gnn["features"], [])]:
    folder = OUT / kind
    folder.mkdir(exist_ok=True)
    if (folder / "verification.json").exists():
        key_reference = json.loads((folder / "metrics.json").read_text())["train_pair_sha256"]
        continue
    candidate_audit = {}
    for split in ["val", "test"]:
        columns = pads.dataset([str(ROOT / name) for name in manifest["files"][split]], format="parquet").to_table(columns=["customer_id", "article_id"]).to_pandas()
        actual_keys = columns.customer_id.to_numpy(dtype=np.int64)*5000 + columns.article_id.to_numpy(dtype=np.int64)
        wanted_users = np.sort(task.get_table(split).df.customer_id.to_numpy(dtype=np.int64))
        expected_keys = np.repeat(wanted_users, 5000)*5000 + np.tile(np.arange(5000), len(wanted_users))
        assert np.array_equal(np.sort(actual_keys), expected_keys), "Evaluation is not the full shared catalog"
        candidate_audit[split] = {"full_catalog": True, "users": len(wanted_users), "pairs": len(actual_keys)}
        del columns, actual_keys, expected_keys
    run_id = f"hm_small_{kind}_seed_42_v1"
    frame = pads.dataset([str(ROOT / name) for name in manifest["files"]["train"]], format="parquet").to_table().to_pandas()
    keys = frame[["timestamp", "customer_id", "article_id", "label"]].sort_values(["timestamp", "customer_id", "article_id"]).reset_index(drop=True)
    keys["timestamp"] = keys.timestamp.astype("datetime64[ns]")
    keys[["customer_id", "article_id", "label"]] = keys[["customer_id", "article_id", "label"]].astype(np.int64)
    digest = hashlib.sha256(pd.util.hash_pandas_object(keys, index=False).values.tobytes()).hexdigest()
    if key_reference is None:
        key_reference = digest
    assert digest == key_reference, "LightGBM train pairs/labels do not match"
    values, labels = dense(frame, features), frame.label.to_numpy(dtype=np.int8)
    del frame, keys
    gc.collect()
    params = {"objective": "binary", "verbosity": -1, "num_threads": 2, "learning_rate": .05,
        "min_data_in_leaf": 100, "max_bin": 127, "feature_fraction": .9, "bagging_fraction": .8,
        "bagging_freq": 1, "deterministic": True, "force_col_wise": True, "seed": 42}
    dataset = lgb.Dataset(values, label=labels, feature_name=features,
                          categorical_feature=[features.index(name) for name in categorical], free_raw_data=False)
    best, trials = -1, []
    started = time.perf_counter()
    for leaves in [15, 31]:
        model = lgb.train({**params, "num_leaves": leaves}, dataset, num_boost_round=150)
        pred, _ = predict(model, None, manifest["files"]["val"], features, task.get_table("val"), candidate_file=manual_dir / "val_candidates.parquet")
        metric = task.evaluate(pred, task.get_table("val"))["map"]
        trials.append({"num_leaves": leaves, "validation_map": metric})
        record("small_tree_trial", f"{kind}: leaves{leaves}, valMAP{metric*100:.4f}%", run_id, status="tuning", trial=trials[-1])
        if metric > best:
            best, best_leaves = metric, leaves
            model.save_model(str(folder / "model.txt"))
    model = lgb.Booster(model_file=str(folder / "model.txt"))
    result = {"model": kind, "seed": 42, "train_pairs": len(labels), "train_pair_sha256": digest,
              "train_user_times": 4804, "features": features, "categorical_features": categorical,
              "trials": trials, "selected_num_leaves": best_leaves, "rounds": 150,
              "training_and_tuning_seconds": time.perf_counter()-started, "inference_from_saved_model": True,
              "evaluation_catalog": 5000, "subset": "rel-hm-small-v1"}
    result["candidate_audit"] = candidate_audit
    if kind == "lightgbm_idgnn":
        result["embedding_coverage"] = gnn["counts"]
        result["missing_policy"] = "zero local vector plus availability flag; in-sample frozen ID-GNN train representations"
    checks = {}
    for split in ["val", "test"]:
        target = task.get_table(split, mask_input_cols=False)
        pred, elapsed = predict(model, None, manifest["files"][split], features, target,
                                split=split, candidate_file=manual_dir / f"{split}_candidates.parquet")
        metric = task.evaluate(pred, target)
        np.save(folder / f"{split}_predictions.npy", pred)
        result[f"{split}_metrics"] = metric
        result[f"{split}_inference_seconds"] = elapsed
        # Reload weights and repeat all predictions, independent of in-memory fitted model.
        replay = lgb.Booster(model_file=str(folder / "model.txt"))
        repeated, _ = predict(replay, None, manifest["files"][split], features, target,
                              split=split, candidate_file=manual_dir / f"{split}_candidates.parquet")
        checks[split] = {"passed": bool(np.array_equal(pred, repeated)), "rows": len(pred)}
        assert checks[split]["passed"]
    (folder / "metrics.json").write_text(json.dumps(result, indent=2))
    (folder / "verification.json").write_text(json.dumps({"passed": True, "checks": checks}, indent=2))
    record("small_tree_complete", f"{kind} пересчитан и проверен на общем малом каталоге", run_id, status="complete",
           val_metrics=result["val_metrics"], test_metrics=result["test_metrics"], config=result, artifacts=str(folder.relative_to(ROOT)))
    del model, dataset, values, labels
    gc.collect()
