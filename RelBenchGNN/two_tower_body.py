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
