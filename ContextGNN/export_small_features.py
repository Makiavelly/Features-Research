"""Export frozen small ID-GNN features on shared tree train pairs/full catalog."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import torch
ROOT = Path(__file__).resolve().parents[1]


def export(model, loaders, task, device, validate_time, record):
    source = ROOT / "ContextGNN/cache/hm_small_v1/manual"
    out = ROOT / "ContextGNN/cache/hm_small_v1/idgnn_features"
    out.mkdir(exist_ok=True)
    if (out / "manifest.json").exists():
        return
    manual = json.loads((source / "manifest.json").read_text())
    names = [f"gnn_{i:03d}" for i in range(64)] + ["gnn_available"]
    model.eval()
    state = {}
    handle = model.head.register_forward_pre_hook(lambda module, values: state.update(h=values[0].detach()))
    report = {"files": {}, "features": names, "counts": {}, "train_pairs": manual["train_pairs"]}
    for split in ["train", "val", "test"]:
        wanted = None
        if split == "train":
            frame = pd.concat([pd.read_parquet(ROOT / name, columns=["customer_id", "article_id", "timestamp", "label"]) for name in manual["files"]["train"]], ignore_index=True)
            wanted = {(int(user), int(pd.Timestamp(time).timestamp())): group[["article_id", "label"]].to_numpy(dtype=np.int64)
                      for (user, time), group in frame.groupby(["customer_id", "timestamp"], sort=False)}
            del frame
        path = out / f"{split}.parquet"
        writer = None
        buffer = []
        total = missing = users = 0
        for batch in loaders[split]:
            batch = batch.to(device)
            validate_time(batch)
            with torch.no_grad():
                model(batch, task.src_entity_table, task.dst_entity_table)
            values = state.pop("h").cpu().numpy()
            dst_ids = batch[task.dst_entity_table].n_id.cpu().numpy()
            dst_batch = batch[task.dst_entity_table].batch.cpu().numpy()
            count = batch[task.src_entity_table].batch_size
            src = batch[task.src_entity_table].n_id[:count].cpu().numpy()
            times = batch[task.src_entity_table].seed_time[:count].cpu().numpy()
            for index in range(count):
                if split == "train":
                    pairs = wanted.pop((int(src[index]), int(times[index])))
                    ids, labels = pairs[:, 0], pairs[:, 1]
                else:
                    ids, labels = np.arange(5000), None
                x = np.zeros((len(ids), 65), dtype=np.float32)
                selected = np.flatnonzero(dst_batch==index)
                positions = {int(dst_ids[j]): j for j in selected}
                for j, item in enumerate(ids):
                    if int(item) in positions:
                        x[j, :64] = values[positions[int(item)]]
                        x[j, 64] = 1
                frame = pd.DataFrame(x, columns=names)
                frame["customer_id"] = int(src[index])
                frame["article_id"] = ids
                frame["timestamp"] = pd.to_datetime(int(times[index]), unit="s")
                if labels is not None:
                    frame["label"] = labels.astype(np.int8)
                buffer.append(frame)
                missing += int((x[:,64]==0).sum())
                total += len(ids)
                users += 1
                if len(buffer) == 8:
                    table = pa.Table.from_pandas(pd.concat(buffer, ignore_index=True), preserve_index=False)
                    if writer is None:
                        writer = pq.ParquetWriter(path, table.schema, compression="zstd")
                    writer.write_table(table)
                    buffer.clear()
        if buffer:
            table = pa.Table.from_pandas(pd.concat(buffer, ignore_index=True), preserve_index=False)
            if writer is None:
                writer = pq.ParquetWriter(path, table.schema, compression="zstd")
            writer.write_table(table)
        writer.close()
        if wanted:
            raise RuntimeError("Missing train user/time rows")
        report["files"][split] = [str(path.relative_to(ROOT))]
        report["counts"][split] = {"pairs": total, "missing_embeddings": missing, "user_times": users}
        record("small_idgnn_features", f"ID-GNN признаки малого {split} сохранены; всего{total}, без вектора{missing}", "hm_small_idgnn_features_v1", status="features", counts=report["counts"][split])
    handle.remove()
    (out / "manifest.json").write_text(json.dumps(report, indent=2))
