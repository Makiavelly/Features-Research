"""Build inference from the same model, graph and scoring code as training."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "RelBenchGNN/run_idgnn.py").read_text(encoding="utf-8")
source = source[:source.index('print("TRAINING_START", flush=True)')]
source = source.replace('args = parser.parse_args()', '''args = parser.parse_args()
checkpoint_dir = Path(args.output_dir)
checkpoint = torch.load(checkpoint_dir / "best.pt", map_location="cpu")
training_config = checkpoint["config"]
for key in ["seed", "channels", "aggr", "num_layers", "num_neighbors", "temporal_strategy", "eval_batch_size", "batch_size", "num_workers", "task", "dataset", "cache_dir"]:
    if key in training_config:
        setattr(args, key, training_config[key])
args.smoke = False
args.output_dir = str(checkpoint_dir / "inference")
args.run_id = args.run_id or f"hm_idgnn_{args.temporal_strategy}_{checkpoint_dir.name}_inference_v1"''')
source = source.replace('"Начат запуск RelBench ID-GNN"', '"Начата независимая проверка инференса из best.pt"')
source = source.replace('for split in ["train", "val", "test"]:', 'for split in ["val", "test"]:')
source = source.replace('optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)\ntrain_sparse_tensor = SparseTensor(train_dst_nodes, device=device)\n', '')
source = source[:source.index('def train()')] + source[source.index('@torch.no_grad()'):]
source = source.replace('batch_size = batch[task.src_entity_table].batch_size\n        scores', 'if not torch.isfinite(out).all():\n            raise RuntimeError("Non-finite inference logits")\n        batch_size = batch[task.src_entity_table].batch_size\n        scores')
source = source.replace('pred_list: list[Tensor] = []', 'pred_list: list[Tensor] = []\n    candidate_rows = []')
source = source.replace('pred_list.append(pred_mini)', '''pred_list.append(pred_mini)
        dst_batches = batch[task.dst_entity_table].batch.cpu().numpy()
        dst_ids = batch[task.dst_entity_table].n_id.cpu().numpy()
        top_ids = pred_mini.cpu().numpy()
        source_ids = batch[task.src_entity_table].n_id[:batch_size].cpu().numpy()
        source_times = batch[task.src_entity_table].seed_time[:batch_size].cpu().numpy()
        for row_index in range(batch_size):
            candidates = np.union1d(dst_ids[dst_batches == row_index], top_ids[row_index]).astype(np.int64)
            candidate_rows.append({"customer_id": int(source_ids[row_index]),
                                   "timestamp": pd.to_datetime(int(source_times[row_index]), unit="s"),
                                   "candidates": candidates.tolist()})''')
source = source.replace('return pred\n', '''frame = pd.DataFrame(candidate_rows)
    split = "val" if loader is loader_dict["val"] else "test"
    frame.to_parquet(output_dir / f"{split}_candidates.parquet", index=False)
    return pred
''')
source = source.replace('import numpy as np\n', 'import numpy as np\nimport pandas as pd\n')
source += '''
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
'''
(ROOT / "RelBenchGNN/run_inference.py").write_text(source, encoding="utf-8")
print("Generated run_inference.py")
