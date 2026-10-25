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
args.output_dir = str(ROOT / "baseline/results/gnn_embeddings_v1/extraction")
args.run_id = "hm_idgnn_embeddings_seed_42_v1"
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

loader_dict = {}

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




"""Appended to verified inference setup by prepare_embedding_export.py."""
import hashlib
import pyarrow as pa
import pyarrow.parquet as pq

FEATURES = [f"gnn_{index:03d}" for index in range(128)] + ["gnn_available"]
EXPORT = ROOT / "baseline/cache/gnn_embeddings_v1"
EXPORT.mkdir(parents=True, exist_ok=True)
manifest_path = EXPORT / "manifest.json"
model.load_state_dict(checkpoint["model_state_dict"], strict=True)
model.eval()
captured = {}
handle = model.head.register_forward_pre_hook(lambda module, inputs: captured.update(h=inputs[0].detach()))
with (checkpoint_dir / "best.pt").open("rb") as file:
    checkpoint_sha = hashlib.file_digest(file, "sha256").hexdigest()
manual_build = json.loads((ROOT / "baseline/cache/manual_v1/build_complete.json").read_text())
manifest = {"features": FEATURES, "checkpoint_sha256": checkpoint_sha, "seed": 42,
            "train_user_times": 50000, "files": {}, "counts": {},
            "missing_policy": "Zero vector plus gnn_available=0 for pairs outside sampled graph; no head logits in features"}

for split in ["train", "val", "test"]:
    loader_dict.clear()
    gc.collect()
    table = task.get_table(split)
    if split == "train":
        rng = np.random.default_rng(2026)
        selected_rows = np.sort(rng.choice(len(table.df), 50000, replace=False))
        table.df = table.df.iloc[selected_rows].copy().reset_index(drop=True)
    table.df = table.df.drop(columns=[task.dst_entity_col], errors="ignore")
    table_input = get_link_train_table_input(table, task, n_dst_nodes)
    loader_dict[split] = NeighborLoader(data, num_neighbors=num_neighbors,
        time_attr="time", input_nodes=table_input.src_nodes, input_time=table_input.src_time,
        subgraph_type="bidirectional", batch_size=128, temporal_strategy=args.temporal_strategy,
        shuffle=False, num_workers=0)
    if split == "train":
        pairs = pd.concat([pd.read_parquet(ROOT / name, columns=["customer_id", "article_id", "timestamp", "label"])
                           for name in manual_build["files"]["train"]], ignore_index=True)
        desired = {(int(user), int(pd.Timestamp(timestamp).timestamp())): (group.article_id.to_numpy(), group.label.to_numpy())
                   for (user, timestamp), group in pairs.groupby(["customer_id", "timestamp"], sort=False)}
        del pairs
    else:
        frame = pd.read_parquet(checkpoint_dir / f"inference/{split}_candidates.parquet")
        desired = {(int(row.customer_id), int(pd.Timestamp(row.timestamp).timestamp())): (np.asarray(row.candidates), None)
                   for row in frame.itertuples()}
        del frame
    folder = EXPORT / split
    folder.mkdir(exist_ok=True)
    files, buffers = [], []
    total = missing = users = 0
    original_predictions = np.load(checkpoint_dir / f"{split}_predictions.npy") if split != "train" else None
    row_offset = 0
    for batch_index, batch in enumerate(tqdm(loader_dict[split], mininterval=30)):
        batch = batch.to(device)
        with torch.no_grad():
            logits = model.forward_dst_readout(batch, task.src_entity_table, task.dst_entity_table).flatten()
        h = captured.pop("h").cpu().numpy()
        if h.shape[1] != 128 or not np.isfinite(h).all():
            raise RuntimeError("Invalid embeddings")
        count = batch[task.src_entity_table].batch_size
        dst_batch = batch[task.dst_entity_table].batch.cpu().numpy()
        dst_ids = batch[task.dst_entity_table].n_id.cpu().numpy()
        src_ids = batch[task.src_entity_table].n_id[:count].cpu().numpy()
        times = batch[task.src_entity_table].seed_time[:count].cpu().numpy()
        if split != "train":
            scores = torch.zeros(count, n_dst_nodes, device=device)
            scores[batch[task.dst_entity_table].batch, batch[task.dst_entity_table].n_id] = torch.sigmoid(logits)
            predictions = torch.topk(scores, k=12, dim=1).indices.cpu().numpy()
            if not np.array_equal(predictions, original_predictions[row_offset:row_offset+count]):
                raise RuntimeError(f"GNN reference predictions changed during {split} extraction")
            row_offset += count
        rows = []
        for index in range(count):
            user, timestamp = int(src_ids[index]), int(times[index])
            ids, labels = desired.pop((user, timestamp))
            selected = np.flatnonzero(dst_batch == index)
            positions = {int(dst_ids[pos]): pos for pos in selected}
            values = np.zeros((len(ids), 129), dtype=np.float32)
            for j, item in enumerate(ids):
                if int(item) in positions:
                    values[j, :128] = h[positions[int(item)]]
                    values[j, 128] = 1
            piece = pd.DataFrame(values, columns=FEATURES)
            piece["customer_id"] = user
            piece["article_id"] = ids.astype(np.int64)
            piece["timestamp"] = pd.to_datetime(timestamp, unit="s")
            if labels is not None:
                piece["label"] = labels.astype(np.int8)
            rows.append(piece)
            missing += int((values[:, 128] == 0).sum())
            total += len(ids)
        buffers.append(pd.concat(rows, ignore_index=True))
        users += count
        if len(buffers) == 10 or batch_index == len(loader_dict[split])-1:
            path = folder / f"part_{len(files):04d}.parquet"
            pq.write_table(pa.Table.from_pandas(pd.concat(buffers, ignore_index=True), preserve_index=False), path, compression="zstd")
            files.append(str(path.relative_to(ROOT)))
            buffers.clear()
            record("embedding_progress", f"Экспорт GNN {split}: {users} пользователь-время строк, {total} пар", run_id,
                   status=f"export_{split}", split=split, users=users, pairs=total, missing_embeddings=missing)
    if desired:
        raise RuntimeError(f"Missing source rows in {split}: {len(desired)}")
    manifest["files"][split] = files
    manifest["counts"][split] = {"user_times": users, "pairs": total, "missing_embeddings": missing}
    del desired
    gc.collect()
handle.remove()
manifest_path.write_text(json.dumps(manifest, indent=2))
record("embedding_export_complete", "128 представлений GNN экспортированы; пары обучения совпадают с ручным baseline, val/test сверены с предсказаниями GNN", run_id,
       status="complete", config=manifest, artifacts=str(manifest_path.relative_to(ROOT)))
