"""Adapt pinned official two-tower example, keeping upstream untouched."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "RelBenchGNN/upstream/examples/gnn_recommendation.py").read_text(encoding="utf-8")
prefix = source[:source.index('eval_loaders_dict:')]
prefix = prefix.replace('import argparse\n', 'import argparse\nimport sys\nimport gc\nimport time\nimport random\nimport hashlib\nimport subprocess\n')
prefix = prefix.replace('from model import Model', 'ROOT = Path(__file__).resolve().parents[1]\nsys.path.insert(0, str(ROOT / "RelBenchGNN/upstream/examples"))\nfrom model import Model\nfrom tracking import record')
prefix = prefix.replace('from text_embedder import GloveTextEmbedding', 'from local_text_embedder import GloveTextEmbedding')
prefix = prefix.replace('from relbench.modeling.loader import LinkNeighborLoader', 'from relbench.modeling.loader import LinkNeighborLoader, CustomNodeLoader')
prefix = prefix.replace('args = parser.parse_args()', '''parser.add_argument("--output_dir", required=True)
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
print("CONFIG", json.dumps(vars(args)), flush=True)''')
prefix = prefix.replace('load_dataset(args.dataset)', 'load_dataset(ROOT / "data/rel-hm")')
prefix = prefix.replace('train_table_input = get_link_train_table_input(\n    task.get_table("train"), task, n_dst_nodes\n)', '''del db
gc.collect()
train_table = task.get_table("train")
if args.smoke:
    train_table.df = train_table.df.iloc[:args.batch_size].copy().reset_index(drop=True)
train_table_input = get_link_train_table_input(train_table, task, n_dst_nodes)
del train_table
gc.collect()''')
model_train = source[source.index('model = Model('):source.index('@torch.no_grad()')]
model_train = model_train.replace('for batch in tqdm(train_loader, total=total_steps):', 'for batch in tqdm(train_loader, total=total_steps, mininterval=30):')
model_train = model_train.replace('loss.backward()', 'if not torch.isfinite(loss):\n            raise RuntimeError("Non-finite BPR loss")\n        loss.backward()')
model_train = model_train.replace('if steps > args.max_steps_per_epoch:', 'if steps >= args.max_steps_per_epoch:')
model_train = model_train.replace('steps += 1', '''steps += 1
        if steps % 100 == 0:
            record("two_tower_progress", f"Двухбашенная GNN: {steps}/{total_steps} шагов текущей эпохи", run_id, status="training", train_step=steps)''')
body = (ROOT / 'RelBenchGNN/two_tower_body.py').read_text(encoding="utf-8")
(ROOT / 'RelBenchGNN/run_two_tower.py').write_text(prefix + model_train + body, encoding="utf-8")
print('Generated run_two_tower.py')
