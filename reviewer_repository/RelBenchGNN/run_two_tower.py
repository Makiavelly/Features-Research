import argparse
import sys
import gc
import time
import random
import hashlib
import subprocess
import copy
import json
import os
import warnings
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import torch
import torch.nn.functional as F
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "RelBenchGNN/upstream/examples"))
from model import Model
from tracking import record
from local_text_embedder import GloveTextEmbedding
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
from relbench.modeling.loader import LinkNeighborLoader, CustomNodeLoader
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
parser.add_argument("--gnn", type=str, default="sage", choices=["sage", "gat"])
parser.add_argument("--gat_heads", type=int, default=4)
parser.add_argument("--gat_dropout", type=float, default=0.0)
parser.add_argument("--temporal_strategy", type=str, default="uniform")
# Use the same seed time across the mini-batch and share the negatives
parser.add_argument("--share_same_time", action="store_true", default=True)
parser.add_argument(
    "--no-share_same_time", dest="share_same_time", action="store_false"
)
# Whether to use shallow embedding on dst nodes or not.
parser.add_argument("--use_shallow", action="store_true", default=True)
parser.add_argument("--no-use_shallow", dest="use_shallow", action="store_false")
parser.add_argument("--max_steps_per_epoch", type=int, default=2000)
parser.add_argument("--num_workers", type=int, default=0)
parser.add_argument("--seed", type=int, default=42)
parser.add_argument(
    "--cache_dir",
    type=str,
    default=os.path.expanduser("~/.cache/relbench_examples"),
)
parser.add_argument("--pred_dir", type=str, default="/tmp/relbench_preds")
parser.add_argument("--output_dir", required=True)
parser.add_argument("--eval_batch_size", type=int, default=128)
parser.add_argument("--smoke", action="store_true")
parser.add_argument("--resume", action="store_true")
parser.add_argument("--inference-only", action="store_true")
args = parser.parse_args()
output_dir = Path(args.output_dir).resolve()
output_dir.mkdir(parents=True, exist_ok=True)
run_id = "hm_twotower_sage_seed_42_v1" if not args.smoke else "hm_twotower_sage_smoke_v1"
if args.inference_only:
    run_id += "_inference_v2"
started = time.time()
record("two_tower_start", "Начат двухбашенный GraphSAGE: отдельные forward пользователя и товара, общие веса, BPR loss", run_id, status="preparing", config=vars(args), artifacts=str(output_dir.relative_to(ROOT)))
def exception_hook(kind, error, tb):
    record("two_tower_error", "Ошибка двухбашенного запуска", run_id, status="failed", error=str(error))
    sys.__excepthook__(kind, error, tb)
sys.excepthook = exception_hook
if not args.inference_only:
    (output_dir / "config.json").write_text(json.dumps(vars(args), indent=2))
print("CONFIG", json.dumps(vars(args)), flush=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if torch.cuda.is_available():
    torch.set_num_threads(1)
seed_everything(args.seed)

dataset: Dataset = load_dataset(ROOT / "data/rel-hm")
task: RecommendationTask = dataset.load_task(args.task)
tune_metric = "map"
assert task.task_type == TaskType.RECOMMENDATION

# Dataset-level db: one cache per dataset; hidden columns are dropped after loading.
db = dataset.get_db()
n_dst_nodes = num_dst_nodes(db, task)

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

del db
gc.collect()
train_table = task.get_table("train")
if args.smoke:
    train_table.df = train_table.df.iloc[:args.batch_size].copy().reset_index(drop=True)
train_table_input = get_link_train_table_input(train_table, task, n_dst_nodes)
del train_table
gc.collect()
train_loader = LinkNeighborLoader(
    data=data,
    num_neighbors=num_neighbors,
    time_attr="time",
    src_nodes=train_table_input.src_nodes,
    dst_nodes=train_table_input.dst_nodes,
    num_dst_nodes=train_table_input.num_dst_nodes,
    src_time=train_table_input.src_time,
    share_same_time=args.share_same_time,
    batch_size=args.batch_size,
    temporal_strategy=args.temporal_strategy,
    # if share_same_time is True, we use sampler, so shuffle must be set False
    shuffle=not args.share_same_time,
    num_workers=args.num_workers,
)

model = Model(
    data=data,
    col_stats_dict=col_stats_dict,
    num_layers=args.num_layers,
    channels=args.channels,
    out_channels=args.channels,
    aggr=args.aggr,
    norm="layer_norm",
    shallow_list=[task.dst_entity_table] if args.use_shallow else [],
    gnn=args.gnn,
    gat_heads=args.gat_heads,
    gat_dropout=args.gat_dropout,
).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)


def train() -> float:
    model.train()

    loss_accum = count_accum = 0
    steps = 0
    total_steps = min(len(train_loader), args.max_steps_per_epoch)
    for batch in tqdm(train_loader, total=total_steps, mininterval=30):
        src_batch, batch_pos_dst, batch_neg_dst = batch
        src_batch, batch_pos_dst, batch_neg_dst = (
            src_batch.to(device),
            batch_pos_dst.to(device),
            batch_neg_dst.to(device),
        )
        x_src = model(src_batch, task.src_entity_table)
        x_pos_dst = model(batch_pos_dst, task.dst_entity_table)
        x_neg_dst = model(batch_neg_dst, task.dst_entity_table)

        # [batch_size, ]
        pos_score = torch.sum(x_src * x_pos_dst, dim=1)
        if args.share_same_time:
            # [batch_size, batch_size]
            neg_score = x_src @ x_neg_dst.t()
            # [batch_size, 1]
            pos_score = pos_score.view(-1, 1)
        else:
            # [batch_size, ]
            neg_score = torch.sum(x_src * x_neg_dst, dim=1)
        optimizer.zero_grad()
        # BPR loss
        diff_score = pos_score - neg_score
        loss = F.softplus(-diff_score).mean()
        if not torch.isfinite(loss):
            raise RuntimeError("Non-finite BPR loss")
        loss.backward()
        optimizer.step()

        loss_accum += float(loss) * x_src.size(0)
        count_accum += x_src.size(0)

        steps += 1
        if steps % 100 == 0:
            record("two_tower_progress", f"Двухбашенная GNN: {steps}/{total_steps} шагов текущей эпохи", run_id, status="training", train_step=steps)
        if steps >= args.max_steps_per_epoch:
            break

    if count_accum == 0:
        warnings.warn(
            f"Did not sample a single '{task.dst_entity_table}' "
            f"node in any mini-batch. Try to increase the number "
            f"of layers/hops and re-try. If you run into memory "
            f"issues with deeper nets, decrease the batch size."
        )

    return loss_accum / count_accum if count_accum > 0 else float("nan")


"""Append to the official two-tower setup and BPR train function."""

@torch.no_grad()
def evaluate(split, save_embeddings=False):
    model.eval()
    # Replay the same sampling independently of preceding train/evaluation calls.
    seed_everything(args.seed + (0 if split == "val" else 1))
    table = task.get_table(split)
    if args.smoke:
        table.df = table.df.iloc[:32].copy().reset_index(drop=True)
    timestamp = int((dataset.val_timestamp if split == "val" else dataset.test_timestamp).timestamp())
    item_count = min(256, n_dst_nodes) if args.smoke else n_dst_nodes
    sampler = train_loader.src_loader.node_sampler
    def encode(node_type, ids):
        loader = CustomNodeLoader(data, sampler, input_nodes=(node_type, ids),
            input_time=torch.full((len(ids),), timestamp, dtype=torch.long),
            batch_size=args.eval_batch_size, shuffle=False, num_workers=0)
        values = []
        for batch_index, batch in enumerate(tqdm(loader, mininterval=30)):
            embedding = model(batch.to(device), node_type).detach().cpu()
            if not torch.isfinite(embedding).all():
                raise RuntimeError("Non-finite two-tower embeddings")
            values.append(embedding)
            if (batch_index+1) % 100 == 0:
                record("two_tower_encoding", f"Кодирование {split}/{node_type}: {batch_index+1}/{len(loader)} batches", run_id,
                       status="inference" if args.inference_only else "evaluating", split=split, node_type=node_type, batches=batch_index+1, total_batches=len(loader))
        return torch.cat(values)
    items = encode(task.dst_entity_table, torch.arange(item_count))
    users = encode(task.src_entity_table, torch.from_numpy(table.df[task.src_entity_col].values))
    item_gpu = items.to(device)
    predictions = []
    for chunk in users.split(128):
        scores = chunk.to(device) @ item_gpu.T
        predictions.append(scores.topk(12, dim=1).indices.cpu().numpy())
    pred = np.concatenate(predictions)
    if pred.shape != (len(table.df), 12) or (np.diff(np.sort(pred, axis=1), axis=1) == 0).any():
        raise RuntimeError("Invalid two-tower predictions")
    if save_embeddings:
        destination = output_dir / ("inference" if args.inference_only else "embeddings")
        destination.mkdir(exist_ok=True)
        np.save(destination / f"{split}_item_embeddings.npy", items.numpy())
        np.save(destination / f"{split}_user_embeddings.npy", users.numpy())
        np.save(destination / f"{split}_user_ids.npy", table.df[task.src_entity_col].values)
        (destination / f"{split}_metadata.json").write_text(json.dumps({"timestamp": timestamp,
            "item_count": item_count, "users": len(users), "channels": args.channels,
            "catalog_coverage": item_count / n_dst_nodes, "seed": args.seed, "smoke": args.smoke}, indent=2))
    if args.smoke:
        target = task.get_table(split, mask_input_cols=False)
        target.df = target.df.iloc[:32].copy().reset_index(drop=True)
        metrics = task.evaluate(pred, target)
    else:
        metrics = task.evaluate(pred, table) if split == "val" else task.evaluate(pred)
    return pred, metrics


if args.inference_only:
    from two_tower_inference_checks import verify_replay
    inference_started = time.perf_counter()
    best = torch.load(output_dir / "best.pt", map_location=device)
    model.load_state_dict(best["model_state_dict"], strict=True)
    reference = json.loads((output_dir / "metrics.json").read_text())
    checks = {}
    for split in ["val", "test"]:
        pred, metrics = evaluate(split, save_embeddings=True)
        expected = np.load(output_dir / f"{split}_predictions.npy")
        np.save(output_dir / f"inference/{split}_predictions.npy", pred)
        checks[split] = verify_replay(output_dir, split, pred, expected, metrics, reference)
    with (output_dir / "best.pt").open("rb") as file:
        digest = hashlib.file_digest(file, "sha256").hexdigest()
    result = {"passed": all(check["passed"] for check in checks.values()), "checks": checks, "checkpoint_sha256": digest,
              "inference_seconds": time.perf_counter()-inference_started, "verification_protocol": "numerical_ties_v2"}
    (output_dir / "inference/inference_check.json").write_text(json.dumps(result, indent=2))
    record("two_tower_inference", "Независимый инференс двухбашенной GNN проверен; сравниваются векторы, оценки по рангам и MAP с допуском для численных ties", run_id,
           status="verified" if result["passed"] else "failed", checks=result, artifacts=str(output_dir.relative_to(ROOT)))
    if not result["passed"]:
        raise RuntimeError("Two-tower inference mismatch")
else:
    history = []
    start_epoch = 1
    best_metric = -1.0
    if args.resume and (output_dir / "last.pt").exists():
        saved = torch.load(output_dir / "last.pt", map_location=device)
        if saved["config"] != vars(args):
            raise RuntimeError("Changed configuration requires new run_id/output directory")
        model.load_state_dict(saved["model_state_dict"])
        optimizer.load_state_dict(saved["optimizer_state_dict"])
        start_epoch = saved["epoch"] + 1
        best_metric = saved["best_metric"]
        history = json.loads((output_dir / "history.json").read_text())
        torch.set_rng_state(saved["torch_rng"].cpu())
        torch.cuda.set_rng_state_all([state.cpu() for state in saved["cuda_rng"]])
        np.random.set_state(saved["numpy_rng"])
        random.setstate(saved["python_rng"])
    for epoch in range(start_epoch, args.epochs + 1):
        record("two_tower_epoch_start", f"Обучение двухбашенной GNN: эпоха {epoch}/{args.epochs}", run_id, status="training", current_epoch=epoch)
        loss = train()
        _, metrics = evaluate("val")
        if metrics["map"] >= best_metric:
            best_metric = metrics["map"]
            torch.save({"model_state_dict": model.state_dict(), "epoch": epoch, "val_metrics": metrics, "config": vars(args)}, output_dir / "best.pt")
        history.append({"epoch": epoch, "train_loss": loss, "val_metrics": metrics, "elapsed_seconds": time.time()-started})
        (output_dir / "history.json").write_text(json.dumps(history, indent=2))
        torch.save({"model_state_dict": model.state_dict(), "optimizer_state_dict": optimizer.state_dict(),
            "epoch": epoch, "best_metric": best_metric, "config": vars(args), "torch_rng": torch.get_rng_state(),
            "cuda_rng": torch.cuda.get_rng_state_all(), "numpy_rng": np.random.get_state(), "python_rng": random.getstate()}, output_dir / "last.pt")
        record("two_tower_epoch", "Завершена эпоха двухбашенной GNN", run_id, status="training", **history[-1])
        print("EPOCH", json.dumps(history[-1]), flush=True)
        if not args.smoke:
            subprocess.run([sys.executable, str(ROOT / "RelBenchGNN/report_two_tower.py")], check=True)
    best = torch.load(output_dir / "best.pt", map_location=device)
    model.load_state_dict(best["model_state_dict"], strict=True)
    result = {"model": "RelBench two-tower GraphSAGE", "seed": args.seed, "smoke": args.smoke,
              "best_epoch": best["epoch"], "config": vars(args), "shared_backbone": True,
              "published_graphsage_map_percent": {"val": .92, "test": .80},
              "protocol_differences": "batch 256; exactly 2000 steps rather than original 2001; fixed seed per eval split; one seed, paper five"}
    for split in ["val", "test"]:
        pred, metrics = evaluate(split, save_embeddings=True)
        np.save(output_dir / f"{split}_predictions.npy", pred)
        result[f"{split}_metrics"] = metrics
    (output_dir / "metrics.json").write_text(json.dumps(result, indent=2))
    record("two_tower_complete", "Двухбашенная GNN завершила обучение и полную оценку" if not args.smoke else "Двухбашенная GNN: smoke forward/backward/eval пройден, метрики не сопоставимы с полным тестом", run_id,
           status="complete" if not args.smoke else "smoke_complete", epoch=args.epochs,
           val_metrics=result["val_metrics"], test_metrics=result["test_metrics"], artifacts=str(output_dir.relative_to(ROOT)))
