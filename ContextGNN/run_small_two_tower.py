"""Reuse the project's two-tower Model on the frozen small H&M task."""
import argparse
import gc
import hashlib
import json
import math
from pathlib import Path
import random
import sys
import time
import numpy as np
import torch
import torch.nn.functional as F
from run_small import ROOT, CACHE, DATA
sys.path.insert(0, str(ROOT / "RelBenchGNN/upstream/examples"))
from model import Model
from relbench import load_dataset
from relbench.modeling.graph import make_pkey_fkey_graph, get_link_train_table_input
from relbench.modeling.utils import get_stype_proposal, to_unix_time
from relbench.modeling.nn import HeteroEncoder
from relbench.modeling.loader import LinkNeighborLoader, CustomNodeLoader
from torch_frame.config.text_embedder import TextEmbedderConfig
from torch_geometric.seed import seed_everything
from local_text_embedder import GloveTextEmbedding
from tracking import record

OUT = ROOT / "ContextGNN/results/hm_small_v1/two_tower"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    run_id = "hm_twotower_small_seed_42_v1" + ("_inference" if args.verify_only else "")
    record("small_twotower_start", "Двухбашенная Model из прежнего проекта подключена к малому H&M", run_id, status="preparing", artifacts=str(OUT.relative_to(ROOT)))
    def error_hook(kind, error, tb):
        record("small_twotower_error", "Ошибка малого двухбашенного запуска", run_id, status="failed", error=str(error))
        sys.__excepthook__(kind, error, tb)
    sys.excepthook = error_hook
    torch.set_num_threads(2)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dataset = load_dataset(DATA)
    task = dataset.load_task("user-item-purchase")
    db = dataset.get_db()
    data, stats = make_pkey_fkey_graph(db, col_to_stype_dict=get_stype_proposal(db),
        text_embedder_cfg=TextEmbedderConfig(text_embedder=GloveTextEmbedding(device="cpu"), batch_size=256),
        cache_dir=str(CACHE / "materialized"), remove_columns=task.hidden_columns())
    train_input = get_link_train_table_input(task.get_table("train"), task, 5000)
    class FullTimestampBatches:
        # Same-time in-batch negatives, including final partial groups: no train rows dropped.
        def __init__(self):
            times = train_input.src_time
            self.groups = [(times==stamp).nonzero().view(-1) for stamp in times.unique()]
        def __len__(self):
            return sum(math.ceil(len(group)/128) for group in self.groups)
        def __iter__(self):
            batches = []
            for group in self.groups:
                batches.extend(chunk.tolist() for chunk in group[torch.randperm(len(group))].split(128))
            random.shuffle(batches)
            yield from batches
    train_loader = LinkNeighborLoader(data=data, num_neighbors=[32,16], time_attr="time",
        src_nodes=train_input.src_nodes, dst_nodes=train_input.dst_nodes,
        num_dst_nodes=5000, src_time=train_input.src_time, temporal_strategy="last",
        share_same_time=False, batch_sampler=FullTimestampBatches(), num_workers=0)
    config = {"subset": "rel-hm-small-v1", "seed": 42, "channels": 64, "layers": 2,
        "encoder_channels": 64, "encoder_layers": 2, "neighbors": [32,16], "batch_size": 128,
        "max_epochs": 10, "patience": 3, "lr": .001, "temporal_strategy": "last",
        "shared_model": True, "shallow_item_embedding": True, "loss": "BPR with same-time in-batch negatives",
        "training_rows": 4804, "steps_per_epoch": len(train_loader),
        "partial_batch_policy": "keep remainders of every timestamp group, no training rows dropped",
        "source": "RelBenchGNN/upstream/examples/model.py, same Model as run_two_tower.py",
        "source_commit": "919fb8a61a4b4cb787283860597f45701895578d"}
    seed_everything(42)
    model = Model(data=data, col_stats_dict=stats, num_layers=2, channels=64, out_channels=64,
        aggr="sum", norm="layer_norm", shallow_list=[task.dst_entity_table], id_awareness=False)
    # Preserve two-tower architecture; align tabular encoder size with other small GNNs.
    model.encoder = HeteroEncoder(channels=64,
        node_to_col_names_dict={name:data[name].tf.col_names_dict for name in data.node_types},
        node_to_col_stats=stats, torch_frame_model_kwargs={"channels":64,"num_layers":2})
    model.reset_parameters()
    model = model.to(device)
    config["trainable_parameters"] = sum(value.numel() for value in model.parameters())
    with (DATA / "subset_manifest.json").open("rb") as file:
        config["subset_sha256"] = hashlib.file_digest(file, "sha256").hexdigest()
    (OUT / "config.json").write_text(json.dumps(config, indent=2))
    def validate_time(batch, root):
        for node_type, times in batch.time_dict.items():
            if (times > batch[root].seed_time[batch[node_type].batch]).any():
                raise RuntimeError("Future information reached two-tower encoder")
    @torch.no_grad()
    def evaluate(split, save=False):
        model.eval()
        seed_everything(42)
        table = task.get_table(split)
        stamp = int(table.df.timestamp.iloc[0].timestamp())
        sampler = train_loader.src_loader.node_sampler
        def encode(node_type, ids):
            loader = CustomNodeLoader(data, sampler, input_nodes=(node_type, ids),
                input_time=torch.full((len(ids),), stamp, dtype=torch.long), batch_size=128, shuffle=False, num_workers=0)
            outputs = []
            for batch in loader:
                batch = batch.to(device)
                validate_time(batch, node_type)
                outputs.append(model(batch, node_type).detach())
            return torch.cat(outputs)
        started = time.perf_counter()
        items = encode(task.dst_entity_table, torch.arange(5000))
        users = encode(task.src_entity_table, torch.from_numpy(table.df.customer_id.to_numpy()))
        scores = torch.cat([chunk@items.T for chunk in users.split(128)]).cpu().numpy()
        assert np.isfinite(scores).all()
        pred = torch.from_numpy(scores).topk(12, dim=1).indices.numpy()
        metrics = task.evaluate(pred, table) if split=="val" else task.evaluate(pred)
        if save:
            destination = OUT / ("inference" if args.verify_only else "embeddings")
            destination.mkdir(exist_ok=True)
            np.save(destination / f"{split}_user_embeddings.npy", users.cpu().numpy())
            np.save(destination / f"{split}_item_embeddings.npy", items.cpu().numpy())
            np.save(destination / f"{split}_user_ids.npy", table.df.customer_id.to_numpy())
        return pred, scores, metrics, time.perf_counter()-started
    if args.verify_only:
        best = torch.load(OUT / "best.pt", map_location=device)
        model.load_state_dict(best["model_state_dict"], strict=True)
        original = json.loads((OUT / "metrics.json").read_text())
        checks = {}
        for split in ["val", "test"]:
            pred, scores, metric, elapsed = evaluate(split, save=True)
            expected = np.load(OUT / f"{split}_predictions.npy")
            expected_scores = np.load(OUT / f"{split}_scores.npy")
            scores_close = np.allclose(scores, expected_scores, atol=1e-5, rtol=1e-5)
            ties_close = np.allclose(np.take_along_axis(scores,pred,axis=1),np.take_along_axis(scores,expected,axis=1),atol=1e-5,rtol=1e-5)
            map_diff = abs(metric["map"]-original[f"{split}_metrics"]["map"])
            valid_ids = pred.shape==expected.shape and ((pred>=0)&(pred<5000)).all() and (np.diff(np.sort(pred,axis=1),axis=1)!=0).all()
            checks[split] = {"passed":bool(scores_close and ties_close and valid_ids and map_diff<=1e-6),
                "predictions_identical":bool(np.array_equal(pred,expected)), "scores_close":bool(scores_close),
                "ranked_scores_close":bool(ties_close), "map_difference":map_diff,"seconds":elapsed}
        with (OUT / "best.pt").open("rb") as file:
            digest = hashlib.file_digest(file,"sha256").hexdigest()
        passed = all(value["passed"] for value in checks.values())
        (OUT / "verification.json").write_text(json.dumps({"passed":passed,"checks":checks,"checkpoint_sha256":digest},indent=2))
        record("small_twotower_verified","Двухбашенный независимый инференс малого набора проверен",run_id,status="verified" if passed else "failed",checks=checks)
        if not passed:
            raise RuntimeError("Two-tower small replay failed")
        return
    optimizer = torch.optim.Adam(model.parameters(),lr=.001)
    best_metric, best_epoch, stale = -1.,0,0
    history = []
    started = time.perf_counter()
    if device.type=="cuda":
        torch.cuda.reset_peak_memory_stats()
    for epoch in range(1,11):
        model.train()
        losses=[]
        seen=0
        epoch_start=time.perf_counter()
        for batches in train_loader:
            src,pos,neg=(batch.to(device) for batch in batches)
            for batch,root in [(src,task.src_entity_table),(pos,task.dst_entity_table),(neg,task.dst_entity_table)]:
                validate_time(batch,root)
            u=model(src,task.src_entity_table)
            p=model(pos,task.dst_entity_table)
            n=model(neg,task.dst_entity_table)
            loss=F.softplus(-((u*p).sum(dim=1)[:,None]-u@n.T)).mean()
            assert torch.isfinite(loss)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            losses.append(float(loss))
            seen+=len(u)
        assert seen==4804
        train_seconds=time.perf_counter()-epoch_start
        _,_,metric,val_seconds=evaluate("val")
        if metric["map"]>best_metric:
            best_metric,best_epoch,stale=metric["map"],epoch,0
            torch.save({"model_state_dict":model.state_dict(),"epoch":epoch,"config":config},OUT/"best.pt")
        else:
            stale+=1
        row={"epoch":epoch,"train_loss":float(np.mean(losses)),"val_metrics":metric,"train_seconds":train_seconds,"val_seconds":val_seconds,"train_rows":seen}
        history.append(row)
        (OUT/"history.json").write_text(json.dumps(history,indent=2))
        torch.save({"model_state_dict":model.state_dict(),"optimizer_state_dict":optimizer.state_dict(),"epoch":epoch,"config":config},OUT/"last.pt")
        record("small_twotower_epoch",f"Малая двухбашенная GNN: эпоха{epoch}/10, valMAP{metric['map']*100:.4f}%",run_id,status="training",**row)
        print(json.dumps(row),flush=True)
        if stale>=3:
            break
    best=torch.load(OUT/"best.pt",map_location=device)
    model.load_state_dict(best["model_state_dict"],strict=True)
    result={"model":"Two-tower GraphSAGE","seed":42,"best_epoch":best_epoch,"epochs_completed":len(history),
        "config":config,"training_and_validation_seconds":time.perf_counter()-started,
        "peak_cuda_bytes":torch.cuda.max_memory_allocated() if device.type=="cuda" else 0}
    for split in ["val","test"]:
        pred,scores,metric,elapsed=evaluate(split,save=True)
        np.save(OUT/f"{split}_predictions.npy",pred)
        np.save(OUT/f"{split}_scores.npy",scores)
        result[f"{split}_metrics"]=metric
        result[f"{split}_inference_seconds"]=elapsed
    (OUT/"metrics.json").write_text(json.dumps(result,indent=2))
    record("small_twotower_complete","Двухбашенная модель заново обучена и оценена на том же малом наборе",run_id,status="complete",val_metrics=result["val_metrics"],test_metrics=result["test_metrics"],config=result,artifacts=str(OUT.relative_to(ROOT)))


if __name__=="__main__":
    main()
