"""Official ContextGNN/IDGNN on a frozen, much smaller RelBench H&M task."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
import gc
import numpy as np
import torch
import torch.nn.functional as F

ROOT = Path('/mnt/c/Users/Мишаня/ml/projs/tbank/Features')
sys.path[:0] = [str(ROOT / "ContextGNN/upstream"), str(ROOT / "RelBenchGNN")]
from contextgnn.nn.models import ContextGNN, IDGNN
from contextgnn.utils import RHSEmbeddingMode
from local_text_embedder import GloveTextEmbedding
from tracking import record
from relbench import load_dataset
from cv_graph import make_pkey_fkey_graph, get_link_train_table_input
from relbench.modeling.utils import get_stype_proposal
from relbench.modeling.loader import SparseTensor
from torch_frame.config.text_embedder import TextEmbedderConfig
from torch_geometric.loader import NeighborLoader
from torch_geometric.seed import seed_everything

OUT = Path('/mnt/c/Users/Мишаня/ml/projs/tbank/Features/CVFollowup/results/v1/context_diagnostics/0')
CACHE = Path('/mnt/c/Users/Мишаня/ml/projs/tbank/Features/CVBenchmark/results/medium_v2/fold_0/cache/gnn_seeded_past_v2')
DATA = Path('/mnt/c/Users/Мишаня/ml/projs/tbank/Features/data/hm-cv-medium-v2/fold_0')


def sparse_ce(logits, src, dst):
    # PyG sparse_cross_entropy objective, without a dependency upgrade:
    # sum over positive edges of -log softmax, divided by batch size.
    return (logits.logsumexp(dim=-1)[src] - logits[src, dst]).sum() / logits.size(0)


def clear_rhs(model):
    if hasattr(model, "rhs_embedding"):
        model.rhs_embedding._cached_rhs_embedding = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--train-only", action="store_true")
    parser.add_argument("--evaluate-only", action="store_true")
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--export-idgnn", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    config = {"dataset": "rel-hm-small-v1", "seed": 42, "channels": 64,
              "encoder_channels": 64, "encoder_layers": 2, "layers": 2, "neighbors": [32, 16],
              "rhs_embedding_dim": 64, "rhs_mode": "FUSION", "batch_size": 128,
              "max_epochs": 10, "early_stopping_patience": 3, "lr": .001,
              "steps_per_epoch_cap": None, "temporal_strategy": "last",
              "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
              "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
              "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"}
    run_id = "hm_followup_context_f0_probe_gnn"
    record("small_context_start", "Малый ContextGNN пилот: подготовка графа" if not args.verify_only else "Малый ContextGNN: независимый инференс", run_id, status="preparing", config=config)
    def exception_hook(kind, error, tb):
        record("small_context_error", "Ошибка малого ContextGNN эксперимента", run_id, status="failed", error=str(error))
        sys.__excepthook__(kind, error, tb)
    sys.excepthook = exception_hook
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.set_num_threads(2)
    dataset = load_dataset(DATA)
    task = dataset.load_task("user-item-purchase")
    db = dataset.get_db()
    seed_everything(42)
    schema = get_stype_proposal(db.upto(__import__('pandas').Timestamp('2020-06-29 00:00:00')))
    (OUT/'stype_schema.json').write_text(json.dumps({t:{c:s.value for c,s in cols.items()} for t,cols in schema.items()},sort_keys=True,indent=2))
    data, stats = make_pkey_fkey_graph(db, col_to_stype_dict=schema,
        text_embedder_cfg=TextEmbedderConfig(text_embedder=GloveTextEmbedding(device="cpu"), batch_size=256),
        cache_dir=str(CACHE / "materialized"), remove_columns=task.hidden_columns())
    catalog_size = len(db.table_dict[task.dst_entity_table])
    tables = {split: task.get_table(split) for split in ["train", "val", "test"]}
    loaders = {}
    train_input = get_link_train_table_input(tables["train"], task, catalog_size)
    sparse_labels = SparseTensor(train_input.dst_nodes[1], device=device)
    for split in ["train", "val", "test"]:
        table = tables[split]
        loaders[split] = NeighborLoader(data, num_neighbors=[32, 16], time_attr="time",
            input_nodes=(task.src_entity_table, torch.from_numpy(table.df[task.src_entity_col].to_numpy())),
            input_time=torch.from_numpy(table.df.timestamp.astype("int64").to_numpy()//1_000_000_000),
            subgraph_type="bidirectional", batch_size=128, temporal_strategy="last",
            shuffle=split=="train", num_workers=0)
    (OUT / "config.json").write_text(json.dumps(config, indent=2))
    with (DATA / "subset_manifest.json").open("rb") as file:
        subset_sha = hashlib.file_digest(file, "sha256").hexdigest()

    def make_model(kind):
        seed_everything(42)
        kwargs = dict(data=data, col_stats_dict=stats, num_layers=2, channels=64, aggr="sum", norm="layer_norm",
                      torch_frame_model_kwargs={"channels": 64, "num_layers": 2})
        if kind == "contextgnn":
            model = ContextGNN(**kwargs, rhs_emb_mode=RHSEmbeddingMode.FUSION,
                               dst_entity_table=task.dst_entity_table, num_nodes=catalog_size, embedding_dim=64)
        else:
            model = IDGNN(**kwargs, out_channels=1)
        return model.to(device)

    def validate_time(batch):
        for node_type, times in batch.time_dict.items():
            if (times > batch[task.src_entity_table].seed_time[batch[node_type].batch]).any():
                raise RuntimeError("Future node reached the model")

    @torch.no_grad()
    def evaluate(model, kind, split):
        model.eval()
        clear_rhs(model)
        seed_everything(42)
        matrices = []
        started = time.perf_counter()
        for batch in loaders[split]:
            batch = batch.to(device)
            validate_time(batch)
            output = model(batch, task.src_entity_table, task.dst_entity_table)
            if not torch.isfinite(output).all():
                raise RuntimeError("Non-finite model output")
            if kind == "contextgnn":
                scores = output
            else:
                scores = torch.zeros(batch[task.src_entity_table].batch_size, catalog_size, device=device)
                scores[batch[task.dst_entity_table].batch, batch[task.dst_entity_table].n_id] = output.flatten().sigmoid()
            matrices.append(scores.cpu().numpy())
        scores = np.concatenate(matrices)
        pred = np.argsort(-scores,axis=1,kind='stable')[:,:12]
        if (np.diff(np.sort(pred, axis=1), axis=1) == 0).any():
            raise RuntimeError("Duplicate recommendations")
        metric = task.evaluate(pred, tables["val"]) if split == "val" else task.evaluate(pred)
        return pred, scores, metric, time.perf_counter()-started

    if args.export_idgnn:
        from export_small_features import export
        model = make_model("idgnn")
        checkpoint = torch.load(OUT / "idgnn/best.pt", map_location=device)
        model.load_state_dict(checkpoint["model_state_dict"], strict=True)
        export(model, loaders, task, device, validate_time, record)
        return
    checks = {}
    for kind in ["contextgnn"]:
        folder = OUT / kind
        folder.mkdir(exist_ok=True)
        model_run = f"hm_followup_context_f0_probe_{kind}"
        model = make_model(kind)
        if args.probe:
            batch = next(iter(loaders['train'])).to(device)
            validate_time(batch)
            model.train()
            output = model(batch, task.src_entity_table, task.dst_entity_table)
            loss = output.float().square().mean()
            assert torch.isfinite(loss)
            loss.backward()
            checks[kind] = {'passed':True,'shape':list(output.shape),'finite_loss':float(loss)}
            (OUT/'probe.json').write_text(json.dumps(checks,indent=2))
            del model,batch,output,loss
            gc.collect();torch.cuda.empty_cache()
            continue
        if args.evaluate_only:
            checkpoint = torch.load(folder / "best.pt", map_location=device)
            model.load_state_dict(checkpoint["model_state_dict"], strict=True)
            result = {"model": kind, "checkpoint_sha256": hashlib.sha256((folder/'best.pt').read_bytes()).hexdigest()}
            for split in ['val','test']:
                pred, scores, metric, elapsed = evaluate(model, kind, split)
                np.save(folder / f'{split}_predictions.npy', pred)
                np.save(folder / f'{split}_scores.npy', scores)
                result[f'{split}_metrics'] = metric
            (folder/'metrics.json').write_text(json.dumps(result,indent=2))
            continue
        if args.verify_only:
            checkpoint = torch.load(folder / "best.pt", map_location=device)
            model.load_state_dict(checkpoint["model_state_dict"], strict=True)
            reference = json.loads((folder / "metrics.json").read_text())
            checks[kind] = {}
            for split in ["val", "test"]:
                pred, scores, metrics, elapsed = evaluate(model, kind, split)
                original = np.load(folder / f"{split}_predictions.npy")
                old_scores = np.load(folder / f"{split}_scores.npy")
                shape_ok = pred.shape == original.shape
                scores_close = np.allclose(scores, old_scores, atol=1e-5, rtol=1e-5)
                ties_close = np.allclose(np.take_along_axis(scores, pred, axis=1), np.take_along_axis(scores, original, axis=1), atol=1e-5, rtol=1e-5)
                difference = abs(metrics["map"]-reference[f"{split}_metrics"]["map"])
                passed = bool(shape_ok and scores_close and ties_close and difference<=1e-6)
                checks[kind][split] = {"passed": passed, "predictions_identical": bool(np.array_equal(pred, original)),
                    "scores_close": bool(scores_close), "ranked_scores_close": bool(ties_close), "map_difference": difference, "seconds": elapsed}
            with (folder / "best.pt").open("rb") as file:
                checks[kind]["checkpoint_sha256"] = hashlib.file_digest(file, "sha256").hexdigest()
            record("small_model_verified", f"Независимая проверка {kind} на малом наборе", model_run+"_inference", status="verified" if all(checks[kind][s]["passed"] for s in ["val", "test"]) else "failed", checks=checks[kind])
        else:
            if (folder / "trained.json").exists():
                del model
                continue
            optimizer = torch.optim.Adam(model.parameters(), lr=.001)
            best_metric, best_epoch, stale = -1., 0, 0
            history = []
            if device.type == "cuda":
                torch.cuda.reset_peak_memory_stats()
            started = time.perf_counter()
            for epoch in range(1, 11):
                model.train()
                clear_rhs(model)
                losses = []
                epoch_started = time.perf_counter()
                for step, batch in enumerate(loaders["train"]):
                    if step >= 1000000:
                        break
                    batch = batch.to(device)
                    validate_time(batch)
                    src, dst = sparse_labels[batch[task.src_entity_table].input_id]
                    optimizer.zero_grad()
                    output = model(batch, task.src_entity_table, task.dst_entity_table)
                    if kind == "contextgnn":
                        loss = sparse_ce(output, src, dst)
                    else:
                        count = batch[task.src_entity_table].batch_size
                        target = torch.isin(batch[task.dst_entity_table].batch + count*batch[task.dst_entity_table].n_id, src+count*dst).float()
                        loss = F.binary_cross_entropy_with_logits(output.flatten(), target)
                    if not torch.isfinite(loss):
                        raise RuntimeError("Non-finite training loss")
                    loss.backward()
                    optimizer.step()
                    losses.append(float(loss))
                train_seconds = time.perf_counter()-epoch_started
                _, _, metric, eval_seconds = evaluate(model, kind, "val")
                improved = metric["map"] > best_metric
                if improved:
                    best_metric, best_epoch, stale = metric["map"], epoch, 0
                    torch.save({"model_state_dict": model.state_dict(), "epoch": epoch, "config": config}, folder / "best.pt")
                else:
                    stale += 1
                history.append({"epoch": epoch, "train_loss": float(np.mean(losses)), "val_metrics": metric,
                                "train_seconds": train_seconds, "val_seconds": eval_seconds, "steps": len(losses)})
                (folder / "history.json").write_text(json.dumps(history, indent=2))
                torch.save({"model_state_dict": model.state_dict(), "optimizer_state_dict": optimizer.state_dict(), "epoch": epoch, "config": config}, folder / "last.pt")
                record("small_epoch", f"Малый {kind}: эпоха {epoch}/10, validation MAP={metric['map']*100:.4f}%", model_run, status="training", **history[-1])
                print(kind, json.dumps(history[-1]), flush=True)
                if stale >= 3:
                    break
            checkpoint = torch.load(folder / "best.pt", map_location=device)
            model.load_state_dict(checkpoint["model_state_dict"], strict=True)
            if args.train_only:
                (folder/"trained.json").write_text(json.dumps({"best_epoch":best_epoch,"epochs":len(history),"seconds":time.perf_counter()-started}))
                del model,optimizer
                gc.collect()
                torch.cuda.empty_cache()
                continue
            result = {"model": kind, "seed": 42, "best_epoch": best_epoch, "epochs_completed": len(history), "subset_sha256": subset_sha,
                      "training_and_validation_seconds": time.perf_counter()-started,
                      "peak_cuda_bytes": torch.cuda.max_memory_allocated() if device.type=="cuda" else 0,
                      "config": config}
            for split in ["val", "test"]:
                pred, scores, metrics, elapsed = evaluate(model, kind, split)
                np.save(folder / f"{split}_predictions.npy", pred)
                np.save(folder / f"{split}_scores.npy", scores)
                result[f"{split}_metrics"] = metrics
                result[f"{split}_inference_seconds"] = elapsed
            (folder / "metrics.json").write_text(json.dumps(result, indent=2))
            record("small_model_complete", f"{kind} обучен и оценён на малом наборе", model_run, status="complete", val_metrics=result["val_metrics"], test_metrics=result["test_metrics"], config=result, artifacts=str(folder.relative_to(ROOT)))
        del model
        gc.collect()
        if device.type=="cuda":
            torch.cuda.empty_cache()
    if args.verify_only:
        passed = all(checks[k][s]["passed"] for k in checks for s in ["val", "test"])
        (OUT / "verification.json").write_text(json.dumps({"passed": passed, "checks": checks}, indent=2))
        if not passed:
            raise RuntimeError("Independent inference verification failed")


if __name__ == "__main__":
    main()
