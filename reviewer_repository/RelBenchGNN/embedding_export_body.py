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
