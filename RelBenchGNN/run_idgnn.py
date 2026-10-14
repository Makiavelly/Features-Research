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
output_dir = Path(args.output_dir)
output_dir.mkdir(parents=True, exist_ok=True)
started_at = time.time()
(output_dir / "config.json").write_text(json.dumps(vars(args), indent=2))
history = []
run_id = args.run_id or f"hm_idgnn_{args.temporal_strategy}_{output_dir.name}_v1"
record("run_start", "Начат запуск RelBench ID-GNN", run_id,
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
for split in ["train", "val", "test"]:
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

optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
train_sparse_tensor = SparseTensor(train_dst_nodes, device=device)


def train() -> float:
    model.train()

    loss_accum = count_accum = 0
    steps = 0
    total_steps = min(len(loader_dict["train"]), args.max_steps_per_epoch)
    for batch in tqdm(loader_dict["train"], total=total_steps, mininterval=30):
        batch = batch.to(device)
        out = model.forward_dst_readout(
            batch, task.src_entity_table, task.dst_entity_table
        ).flatten()

        batch_size = batch[task.src_entity_table].batch_size

        # Get ground-truth
        input_id = batch[task.src_entity_table].input_id
        src_batch, dst_index = train_sparse_tensor[input_id]

        # Get target label
        target = torch.isin(
            batch[task.dst_entity_table].batch
            + batch_size * batch[task.dst_entity_table].n_id,
            src_batch + batch_size * dst_index,
        ).float()

        # Optimization
        optimizer.zero_grad()
        loss = F.binary_cross_entropy_with_logits(out, target)
        loss.backward()

        optimizer.step()

        loss_accum += float(loss) * out.numel()
        count_accum += out.numel()

        steps += 1
        if steps > args.max_steps_per_epoch:
            break

    if count_accum == 0:
        warnings.warn(
            f"Did not sample a single '{task.dst_entity_table}' "
            f"node in any mini-batch. Try to increase the number "
            f"of layers/hops and re-try. If you run into memory "
            f"issues with deeper nets, decrease the batch size."
        )

    return loss_accum / count_accum if count_accum > 0 else float("nan")


@torch.no_grad()
def test(loader: NeighborLoader) -> np.ndarray:
    model.eval()

    pred_list: list[Tensor] = []
    for batch in tqdm(loader, mininterval=30):
        batch = batch.to(device)
        out = (
            model.forward_dst_readout(
                batch, task.src_entity_table, task.dst_entity_table
            )
            .detach()
            .flatten()
        )
        batch_size = batch[task.src_entity_table].batch_size
        scores = torch.zeros(batch_size, n_dst_nodes, device=out.device)
        scores[
            batch[task.dst_entity_table].batch, batch[task.dst_entity_table].n_id
        ] = torch.sigmoid(out)
        _, pred_mini = torch.topk(scores, k=task.eval_k, dim=1)
        pred_list.append(pred_mini)
    pred = torch.cat(pred_list, dim=0).cpu().numpy()
    return pred


print("TRAINING_START", flush=True)
record("training_start", "Начато обучение на GPU", run_id, status="training", epoch=0)
state_dict = None
best_val_metric = -math.inf
start_epoch = 1
elapsed_before_resume = 0.0
if args.resume and (output_dir / "last.pt").exists():
    checkpoint = torch.load(output_dir / "last.pt", map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    start_epoch = checkpoint["epoch"] + 1
    torch.set_rng_state(checkpoint["torch_rng"].cpu())
    np.random.set_state(checkpoint["numpy_rng"])
    import random
    random.setstate(checkpoint["python_rng"])
    if torch.cuda.is_available():
        torch.cuda.set_rng_state_all([state.cpu() for state in checkpoint["cuda_rng"]])
    if (output_dir / "history.json").exists():
        history = json.loads((output_dir / "history.json").read_text())
        elapsed_before_resume = history[-1]["elapsed_seconds"] if history else 0.0
    best = torch.load(output_dir / "best.pt", map_location=device)
    state_dict = best["model_state_dict"]
    best_val_metric = best["val_metrics"][tune_metric]
    print("RESUME_EPOCH", start_epoch, flush=True)
for epoch in range(start_epoch, args.epochs + 1):
    train_loss = train()
    if epoch % args.eval_epochs_interval == 0:
        val_pred = test(loader_dict["val"])
        val_metrics = task.evaluate(val_pred, val_table)
        print(
            f"Epoch: {epoch:02d}, Train loss: {train_loss}, "
            f"Val metrics: {val_metrics}"
        )

        if val_metrics[tune_metric] >= best_val_metric:
            best_val_metric = val_metrics[tune_metric]
            state_dict = copy.deepcopy(model.state_dict())
            torch.save({"model_state_dict": state_dict, "epoch": epoch,
                        "val_metrics": val_metrics, "config": vars(args)},
                       output_dir / "best.pt")

    history.append({"epoch": epoch, "train_loss": train_loss,
                    "val_metrics": val_metrics, "elapsed_seconds": elapsed_before_resume + time.time() - started_at})
    (output_dir / "history.json").write_text(json.dumps(history, indent=2))
    record("epoch", "Завершена эпоха ID-GNN", run_id, status="training", epoch=epoch,
           train_loss=train_loss, val_metrics=val_metrics,
           elapsed_seconds=elapsed_before_resume + time.time() - started_at)
    import random
    torch.save({"model_state_dict": model.state_dict(), "optimizer_state_dict": optimizer.state_dict(),
                "epoch": epoch, "config": vars(args), "torch_rng": torch.get_rng_state(),
                "numpy_rng": np.random.get_state(), "python_rng": random.getstate(),
                "cuda_rng": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else []},
               output_dir / "last.pt")

if state_dict is not None:
    model.load_state_dict(state_dict)
else:
    warnings.warn(
        "No best checkpoint was selected (state_dict is None); evaluating with current model weights."
    )
val_pred = test(loader_dict["val"])
val_metrics = task.evaluate(val_pred, val_table)
print(f"Best Val metrics: {val_metrics}")

test_pred = test(loader_dict["test"])
np.save(output_dir / "test_predictions.npy", test_pred)
np.save(output_dir / "val_predictions.npy", val_pred)
if args.smoke:
    test_table = task.get_table("test", mask_input_cols=False)
    test_table.df = test_table.df.iloc[:args.batch_size].copy()
    test_metrics = task.evaluate(test_pred, test_table)
else:
    test_metrics = task.evaluate(test_pred)
    write_prediction_table(task, test_pred, output_dir / "predictions.csv")
result = {"model": "RelBench ID-GNN", "dataset": "rel-hm", "task": args.task,
          "seed": args.seed, "smoke": args.smoke, "val_metrics": val_metrics,
          "test_metrics": test_metrics, "elapsed_seconds": elapsed_before_resume + time.time() - started_at,
          "config": vars(args)}
(output_dir / "metrics.json").write_text(json.dumps(result, indent=2))
record("run_complete", "Завершён запуск ID-GNN" if not args.smoke else "Завершена короткая техническая проверка ID-GNN",
       run_id, status="complete" if not args.smoke else "smoke_complete",
       val_metrics=val_metrics, test_metrics=test_metrics, epoch=args.epochs,
       smoke=args.smoke, elapsed_seconds=result["elapsed_seconds"])
print("RESULT", json.dumps(result), flush=True)
