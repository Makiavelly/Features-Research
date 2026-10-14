"""Keep upstream untouched; add local data, checkpoints and structured run records."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "RelBenchGNN/upstream/examples/idgnn_recommendation.py"


def main():
    source = SOURCE.read_text(encoding="utf-8")
    source = source.replace("import argparse\n", "import argparse\nimport gc\nimport time\nimport sys\n")
    source = source.replace("from text_embedder import GloveTextEmbedding", "from local_text_embedder import GloveTextEmbedding")
    source = source.replace("from local_text_embedder import GloveTextEmbedding", "from local_text_embedder import GloveTextEmbedding\nfrom tracking import record")
    source = source.replace(
        "from model import Model",
        'ROOT = Path(__file__).resolve().parents[1]\nsys.path.insert(0, str(ROOT / "RelBenchGNN/upstream/examples"))\nfrom model import Model',
    )
    source = source.replace(
        'args = parser.parse_args()',
        '''parser.add_argument("--output_dir", required=True)
parser.add_argument("--eval_batch_size", type=int, default=128)
parser.add_argument("--smoke", action="store_true")
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
print("CONFIG", json.dumps(vars(args)), flush=True)''',
    )
    source = source.replace('parser.add_argument("--output_dir", required=True)', 'parser.add_argument("--output_dir", required=True)\nparser.add_argument("--run_id")')
    source = source.replace('parser.add_argument("--smoke", action="store_true")', 'parser.add_argument("--smoke", action="store_true")\nparser.add_argument("--resume", action="store_true")')
    source = source.replace('load_dataset(args.dataset)', 'load_dataset(ROOT / "data/rel-hm")')
    source = source.replace('get_stype_proposal(db)', 'get_stype_proposal(db)')
    source = source.replace(
        'val_table = task.get_table("val")',
        'print("GRAPH_READY", data, flush=True)\nrecord("graph_ready", "Граф и признаки подготовлены", run_id, status="preparing_loaders", nodes=dict(data.num_nodes_dict))\ndel db\ngc.collect()\nval_table = task.get_table("val")',
    )
    source = source.replace('table = task.get_table(split)', 'table = task.get_table(split)\n    if args.smoke:\n        table.df = table.df.iloc[:args.batch_size].copy()\n        if split == "val":\n            val_table = table')
    source = source.replace('batch_size=args.batch_size,', 'batch_size=args.batch_size if split == "train" else args.eval_batch_size,')
    source = source.replace('for batch in tqdm(loader_dict["train"], total=total_steps):', 'for batch in tqdm(loader_dict["train"], total=total_steps, mininterval=30):')
    source = source.replace('for batch in tqdm(loader):', 'for batch in tqdm(loader, mininterval=30):')
    source = source.replace('state_dict = None', 'print("TRAINING_START", flush=True)\nrecord("training_start", "Начато обучение на GPU", run_id, status="training", epoch=0)\nstate_dict = None')
    source = source.replace('for epoch in range(1, args.epochs + 1):', '''start_epoch = 1
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
for epoch in range(start_epoch, args.epochs + 1):''')
    source = source.replace('state_dict = copy.deepcopy(model.state_dict())', '''state_dict = copy.deepcopy(model.state_dict())
            torch.save({"model_state_dict": state_dict, "epoch": epoch,
                        "val_metrics": val_metrics, "config": vars(args)},
                       output_dir / "best.pt")''')
    source = source.replace(
        '\n\nif state_dict is not None:',
        '''
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

if state_dict is not None:''',
    )
    start = source.index('os.makedirs(args.pred_dir, exist_ok=True)')
    source = source[:start] + '''np.save(output_dir / "test_predictions.npy", test_pred)
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
'''
    target = ROOT / "RelBenchGNN/run_idgnn.py"
    target.write_text('# Adapted from pinned upstream examples/idgnn_recommendation.py.\n' + source, encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
