# Adapted from pinned upstream examples/idgnn_recommendation.py.
import argparse
import gc
import time
import sys
import copy
import json
import math
import os
import warnings
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "RelBenchGNN/upstream/examples"))
from model import Model
from local_text_embedder import GloveTextEmbedding
from tracking import record
from torch import Tensor
from torch_frame import stype
from torch_frame.config.text_embedder import TextEmbedderConfig
from torch_geometric.loader import NeighborLoader
from torch_geometric.seed import seed_everything
from tqdm import tqdm

from relbench import load_dataset
from relbench.base import Dataset, RecommendationTask, TaskType
from relbench.modeling.graph import (
    get_link_train_table_input,
    make_pkey_fkey_graph,
    num_dst_nodes,
)
from relbench.modeling.loader import SparseTensor
from relbench.modeling.utils import get_stype_proposal
from relbench.submit import evaluate_task, write_prediction_table

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="rel-hm")
parser.add_argument("--task", type=str, default="user-item-purchase")
parser.add_argument("--lr", type=float, default=0.001)
parser.add_argument("--epochs", type=int, default=20)
parser.add_argument("--eval_epochs_interval", type=int, default=1)
parser.add_argument("--batch_size", type=int, default=512)
parser.add_argument("--channels", type=int, default=128)
parser.add_argument("--aggr", type=str, default="sum")
parser.add_argument("--num_layers", type=int, default=2)
parser.add_argument("--num_neighbors", type=int, default=128)
parser.add_argument("--temporal_strategy", type=str, default="last")
parser.add_argument("--max_steps_per_epoch", type=int, default=2000)
parser.add_argument("--num_workers", type=int, default=0)
parser.add_argument("--seed", type=int, default=42)
parser.add_argument(
    "--cache_dir", type=str, default=os.path.expanduser("~/.cache/relbench_examples")
)
parser.add_argument("--pred_dir", type=str, default="/tmp/relbench_preds")
parser.add_argument("--output_dir", required=True)
parser.add_argument("--run_id")
parser.add_argument("--eval_batch_size", type=int, default=128)
parser.add_argument("--smoke", action="store_true")
parser.add_argument("--resume", action="store_true")
args = parser.parse_args()
checkpoint_dir = Path(args.output_dir)
checkpoint = torch.load(checkpoint_dir / "best.pt", map_location="cpu")
training_config = checkpoint["config"]
for key in ["seed", "channels", "aggr", "num_layers", "num_neighbors", "temporal_strategy", "eval_batch_size", "batch_size", "num_workers", "task", "dataset", "cache_dir"]:
    if key in training_config:
        setattr(args, key, training_config[key])
args.smoke = False
args.output_dir = str(checkpoint_dir / "inference")
args.run_id = args.run_id or f"hm_idgnn_{args.temporal_strategy}_{checkpoint_dir.name}_inference_v1"
output_dir = Path(args.output_dir)
output_dir.mkdir(parents=True, exist_ok=True)
started_at = time.time()
(output_dir / "config.json").write_text(json.dumps(vars(args), indent=2))
history = []
run_id = args.run_id or f"hm_idgnn_{args.temporal_strategy}_{output_dir.name}_v1"
record("run_start", "Начата независимая проверка инференса из best.pt", run_id,
       status="preparing", config=vars(args), artifacts=str(output_dir.relative_to(ROOT)))
def report_exception(error_type, value, traceback):
    record("error", "Запуск ID-GNN завершился ошибкой", run_id,
           status="failed", error_type=error_type.__name__, error=str(value))
    sys.__excepthook__(error_type, value, traceback)
sys.excepthook = report_exception
print("CONFIG", json.dumps(vars(args)), flush=True)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if torch.cuda.is_available():
    torch.set_num_threads(1)
seed_everything(args.seed)

dataset: Dataset = load_dataset(ROOT / "data/rel-hm")
task: RecommendationTask = dataset.load_task(args.task)

# Dataset-level db: one cache per dataset; hidden columns are dropped after loading.
db = dataset.get_db()
n_dst_nodes = num_dst_nodes(db, task)
tune_metric = "map"
assert task.task_type == TaskType.RECOMMENDATION

stypes_cache_path = Path(f"{args.cache_dir}/{args.dataset}/stypes.json")
try:
    with open(stypes_cache_path, "r") as f:
        col_to_stype_dict = json.load(f)
    for table, col_to_stype in col_to_stype_dict.items():
        for col, stype_str in col_to_stype.items():
            col_to_stype[col] = stype(stype_str)
except FileNotFoundError:
    col_to_stype_dict = get_stype_proposal(db)
    Path(stypes_cache_path).parent.mkdir(parents=True, exist_ok=True)
    with open(stypes_cache_path, "w") as f:
        json.dump(col_to_stype_dict, f, indent=2, default=str)

data, col_stats_dict = make_pkey_fkey_graph(
    db,
    col_to_stype_dict=col_to_stype_dict,
    text_embedder_cfg=TextEmbedderConfig(
        text_embedder=GloveTextEmbedding(device="cpu"), batch_size=256
    ),
    cache_dir=f"{args.cache_dir}/{args.dataset}/materialized",
    remove_columns=task.hidden_columns(),
)

num_neighbors = [int(args.num_neighbors // 2**i) for i in range(args.num_layers)]

print("GRAPH_READY", data, flush=True)
record("graph_ready", "Граф и признаки подготовлены", run_id, status="preparing_loaders", nodes=dict(data.num_nodes_dict))
del db
gc.collect()
val_table = task.get_table("val")  # hoisted: get_table is uncached

loader_dict: Dict[str, NeighborLoader] = {}
for split in ["val", "test"]:
    table = task.get_table(split)
    if args.smoke:
        table.df = table.df.iloc[:args.batch_size].copy()
        if split == "val":
            val_table = table
    table_input = get_link_train_table_input(table, task, n_dst_nodes)
    if split == "train":
        train_dst_nodes = table_input.dst_nodes[1]
    loader_dict[split] = NeighborLoader(
        data,
        num_neighbors=num_neighbors,
        time_attr="time",
        input_nodes=table_input.src_nodes,
        input_time=table_input.src_time,
        subgraph_type="bidirectional",
        batch_size=args.batch_size if split == "train" else args.eval_batch_size,
        temporal_strategy=args.temporal_strategy,
        shuffle=split == "train",
        num_workers=args.num_workers,
        persistent_workers=args.num_workers > 0,
    )

model = Model(
    data=data,
    col_stats_dict=col_stats_dict,
    num_layers=args.num_layers,
    channels=args.channels,
    out_channels=1,
    aggr=args.aggr,
    norm="layer_norm",
    id_awareness=True,
).to(device)



@torch.no_grad()
def test(loader: NeighborLoader) -> np.ndarray:
    model.eval()

    pred_list: list[Tensor] = []
    candidate_rows = []
    for batch in tqdm(loader, mininterval=30):
        batch = batch.to(device)
        out = (
            model.forward_dst_readout(
                batch, task.src_entity_table, task.dst_entity_table
            )
            .detach()
            .flatten()
        )
        if not torch.isfinite(out).all():
            raise RuntimeError("Non-finite inference logits")
        batch_size = batch[task.src_entity_table].batch_size
        scores = torch.zeros(batch_size, n_dst_nodes, device=out.device)
        scores[
            batch[task.dst_entity_table].batch, batch[task.dst_entity_table].n_id
        ] = torch.sigmoid(out)
        _, pred_mini = torch.topk(scores, k=task.eval_k, dim=1)
        pred_list.append(pred_mini)
        dst_batches = batch[task.dst_entity_table].batch.cpu().numpy()
        dst_ids = batch[task.dst_entity_table].n_id.cpu().numpy()
        top_ids = pred_mini.cpu().numpy()
        source_ids = batch[task.src_entity_table].n_id[:batch_size].cpu().numpy()
        source_times = batch[task.src_entity_table].seed_time[:batch_size].cpu().numpy()
        for row_index in range(batch_size):
            candidates = np.union1d(dst_ids[dst_batches == row_index], top_ids[row_index]).astype(np.int64)
            candidate_rows.append({"customer_id": int(source_ids[row_index]),
                                   "timestamp": pd.to_datetime(int(source_times[row_index]), unit="s"),
                                   "candidates": candidates.tolist()})
    pred = torch.cat(pred_list, dim=0).cpu().numpy()
    frame = pd.DataFrame(candidate_rows)
    split = "val" if loader is loader_dict["val"] else "test"
    frame.to_parquet(output_dir / f"{split}_candidates.parquet", index=False)
    return pred



import hashlib
model.load_state_dict(checkpoint["model_state_dict"], strict=True)
record("inference_start", "Веса загружены строго; запущен инференс полного validation/test", run_id, status="inference")
if device.type == "cuda":
    torch.cuda.synchronize()
infer_started = time.perf_counter()
val_pred = test(loader_dict["val"])
val_seconds = time.perf_counter() - infer_started
test_started = time.perf_counter()
test_pred = test(loader_dict["test"])
if device.type == "cuda":
    torch.cuda.synchronize()
test_seconds = time.perf_counter() - test_started
val_metrics = task.evaluate(val_pred, val_table)
test_metrics = task.evaluate(test_pred)
reference = json.loads((checkpoint_dir / "metrics.json").read_text())
checks = {}
passed = True
for split, pred, metrics in [("val", val_pred, val_metrics), ("test", test_pred, test_metrics)]:
    original = np.load(checkpoint_dir / f"{split}_predictions.npy")
    shape_ok = pred.shape == original.shape
    ids_valid = bool(((pred >= 0) & (pred < n_dst_nodes)).all())
    unique = bool((np.diff(np.sort(pred, axis=1), axis=1) != 0).all())
    difference = abs(float(metrics["map"]) - float(reference[f"{split}_metrics"]["map"]))
    identical = bool(np.array_equal(original, pred))
    checks[split] = {"shape": list(pred.shape), "shape_ok": shape_ok, "ids_valid": ids_valid,
                     "unique_ids_per_user": unique, "predictions_identical": identical,
                     "same_item_at_same_rank_fraction": float((original == pred).mean()) if shape_ok else 0.0,
                     "map_absolute_difference": difference, "map_tolerance": 1e-6,
                     "passed": bool(shape_ok and ids_valid and unique and difference <= 1e-6)}
    passed = passed and checks[split]["passed"]
    np.save(output_dir / f"{split}_predictions.npy", pred)
test_targets = task.get_table("test", mask_input_cols=False)
ap = []
for true_items, predicted in zip(test_targets.df[task.dst_entity_col], test_pred):
    relevant = np.isin(predicted, true_items)
    precision = np.cumsum(relevant) / np.arange(1, task.eval_k + 1)
    ap.append(float((precision * relevant).sum() / min(len(true_items), task.eval_k)))
np.save(output_dir / "test_ap_per_user.npy", np.asarray(ap))
with (checkpoint_dir / "best.pt").open("rb") as file:
    digest = hashlib.file_digest(file, "sha256").hexdigest()
result = {"passed": passed, "checkpoint": str(checkpoint_dir / "best.pt"), "checkpoint_sha256": digest,
          "best_epoch": checkpoint["epoch"], "val_metrics": val_metrics, "test_metrics": test_metrics,
          "checks": checks, "val_inference_seconds": val_seconds, "test_inference_seconds": test_seconds,
          "test_users_per_second": len(test_pred) / test_seconds,
          "total_seconds_including_preparation": time.time() - started_at}
(output_dir / "inference_check.json").write_text(json.dumps(result, indent=2))
record("inference_complete", "Проверка инференса пройдена" if passed else "Проверка инференса обнаружила расхождение",
       run_id, status="verified" if passed else "failed", val_metrics=val_metrics, test_metrics=test_metrics,
       checks=checks, artifacts=str(output_dir.relative_to(ROOT)))
print("INFERENCE_CHECK", json.dumps(result), flush=True)
if not passed:
    raise SystemExit("Inference check failed; inspect inference_check.json")
