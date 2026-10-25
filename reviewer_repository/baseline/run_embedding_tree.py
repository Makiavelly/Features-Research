"""Train a separate LightGBM head on frozen ID-GNN features; no test tuning."""
import sys
import json
from pathlib import Path
import time
import numpy as np
import pyarrow.dataset as pads
import lightgbm as lgb
from relbench import load_dataset
from run_manual_tree import predict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "RelBenchGNN"))
from tracking import record

RUN = "hm_idgnn_lightgbm_embeddings_seed_42_v1"
OUT = ROOT / "baseline/results/gnn_embeddings_v1"
OUT.mkdir(parents=True, exist_ok=True)
schema = json.loads((ROOT / "baseline/cache/gnn_embeddings_v1/manifest.json").read_text())
features = schema["features"]
task = load_dataset(ROOT / "data/rel-hm").load_task("user-item-purchase")
record("embedding_tree_start", "LightGBM обучается на замороженных представлениях ID-GNN; tuning только validation", RUN, status="tuning", config=schema)
train = pads.dataset([str(ROOT / name) for name in schema["files"]["train"]]).to_table().to_pandas()
values = train[features].to_numpy(dtype=np.float32)
labels = train.label.to_numpy(dtype=np.int8)
del train
dataset = lgb.Dataset(values, label=labels, feature_name=features, free_raw_data=False)
params = {"objective": "binary", "verbosity": -1, "num_threads": 2, "learning_rate": .05,
          "min_data_in_leaf": 100, "max_bin": 127, "feature_fraction": .9,
          "bagging_fraction": .8, "bagging_freq": 1, "deterministic": True, "force_col_wise": True, "seed": 42}
val = task.get_table("val")
tune = task.get_table("val")
rng = np.random.default_rng(2026)
tune.df = tune.df.iloc[np.sort(rng.choice(len(tune), 10000, replace=False))].copy()
trials = []
best_score = -1
for leaves in [15, 31]:
    model = lgb.train({**params, "num_leaves": leaves}, dataset, num_boost_round=150)
    pred, elapsed = predict(model, None, schema["files"]["val"], features, tune)
    score = task.evaluate(pred, tune)["map"]
    trials.append({"num_leaves": leaves, "val_tuning_map": score})
    record("embedding_tree_trial", f"LightGBM embeddings: num_leaves={leaves}, tuning MAP={score}", RUN, status="tuning", trial=trials[-1])
    if score > best_score:
        best_score, best_leaves = score, leaves
        model.save_model(str(OUT / "model.txt"))
model = lgb.Booster(model_file=str(OUT / "model.txt"))
result = {"model": "ID-GNN embeddings + LightGBM", "seed": 42, "feature_count": len(features),
          "features": features, "trials": trials, "best_num_leaves": best_leaves,
          "train_pairs": len(labels), "train_user_times": 50000, "rounds": 150,
          "checkpoint_sha256": schema["checkpoint_sha256"], "inference_from_saved_model": True,
          "embedding_counts": schema["counts"], "protocol": "Adaptation of RelBench Appendix C.2 to H&M ranking; 128 frozen embeddings plus availability flag; same pairs/budget as manual tree; in-sample GNN train representations"}
for split in ["val", "test"]:
    target = val if split == "val" else task.get_table("test", mask_input_cols=False)
    pred, elapsed = predict(model, None, schema["files"][split], features, target, split=split)
    metrics = task.evaluate(pred, target) if split == "val" else task.evaluate(pred)
    np.save(OUT / f"{split}_predictions.npy", pred)
    result[f"{split}_metrics"] = metrics
    result[f"{split}_inference_seconds"] = elapsed
(OUT / "metrics.json").write_text(json.dumps(result, indent=2))
record("embedding_tree_complete", "LightGBM на представлениях GNN обучен и оценён после загрузки сохранённой модели", RUN,
       status="complete", val_metrics=result["val_metrics"], test_metrics=result["test_metrics"], config=result, artifacts=str(OUT.relative_to(ROOT)))
print(json.dumps(result, indent=2), flush=True)
