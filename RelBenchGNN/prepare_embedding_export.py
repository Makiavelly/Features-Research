"""Generate extraction from the verified graph/checkpoint setup, without training."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "RelBenchGNN/run_inference.py").read_text(encoding="utf-8")
source = source[:source.index('@torch.no_grad()')]
source = source.replace('args.output_dir = str(checkpoint_dir / "inference")', 'args.output_dir = str(ROOT / "baseline/results/gnn_embeddings_v1/extraction")')
source = source.replace('args.run_id = args.run_id or f"hm_idgnn_{args.temporal_strategy}_{checkpoint_dir.name}_inference_v1"', 'args.run_id = "hm_idgnn_embeddings_seed_42_v1"')
source = source.replace('for split in ["val", "test"]:', 'for split in ["train", "val", "test"]:')
source = source.replace('    if args.smoke:', '''    if split == "train":
        rng = np.random.default_rng(2026)
        selected = np.sort(rng.choice(len(table.df), 50000, replace=False))
        table.df = table.df.iloc[selected].copy().reset_index(drop=True)
        table.df = table.df.drop(columns=[task.dst_entity_col])
    if args.smoke:''')
source = source.replace('batch_size=args.batch_size if split == "train" else args.eval_batch_size', 'batch_size=args.eval_batch_size')
source = source.replace('shuffle=split == "train"', 'shuffle=False')
source = source.replace('    if split == "train":\n        train_dst_nodes = table_input.dst_nodes[1]\n', '')
source = source[:source.index('loader_dict:')] + 'loader_dict = {}\n\n' + source[source.index('model = Model('):]
source += '\n' + (ROOT / 'RelBenchGNN/embedding_export_body.py').read_text(encoding='utf-8')
(ROOT / 'RelBenchGNN/export_embeddings.py').write_text(source, encoding='utf-8')
print('Generated export_embeddings.py')
