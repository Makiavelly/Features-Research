"""Explicitly adapt frozen pilot implementations without changing old sources."""
from pathlib import Path
from common import ROOT,paths,frozen_source,write,sha,read

def build(fold):
    data,out=paths(fold);runtime=out/'runtime';runtime.mkdir(parents=True,exist_ok=True)
    root=f'ROOT = Path({str(ROOT)!r})'
    fit_cutoff=read(data/'subset_manifest.json')['splits']['train']['cutoffs'][0]
    graph=ROOT/'RelBenchGNN/upstream/relbench/modeling/graph.py'
    frozen_source(graph,runtime/'cv_graph.py',[
        ('        dataset = Dataset(\n            df=df,',
         f"        fit_df = df if table.time_col is None else df.loc[df[table.time_col] <= pd.Timestamp({fit_cutoff!r})]\n        assert len(fit_df)>0\n        dataset = Dataset(\n            df=fit_df,"),
        ('        tf, col_stats = dataset.tensor_frame, dataset.col_stats',
         '        tf, col_stats = dataset._get_tensorframe_converter()(df), dataset.col_stats\n        assert tf.num_rows==len(df)')])
    gnn=ROOT/'ContextGNN/run_small.py'
    text=gnn.read_text(encoding='utf-8')
    # Evaluation is a separate stage. Preserve the original official models/losses.
    insertion='''        if args.evaluate_only:
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
'''
    probe='''        if args.probe:
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
'''
    frozen_source(gnn,runtime/'gnn.py',[
        ('ROOT = Path(__file__).resolve().parents[1]',root),
        ('from relbench.modeling.graph import make_pkey_fkey_graph, get_link_train_table_input','from cv_graph import make_pkey_fkey_graph, get_link_train_table_input'),
        ('OUT = ROOT / "ContextGNN/results/hm_small_v1"',f'OUT = Path({str(out/"gnn")!r})'),
        ('CACHE = ROOT / "ContextGNN/cache/hm_small_v1"',f'CACHE = Path({str(out/"cache/gnn_seeded_past_v2")!r})'),
        ('DATA = ROOT / "data/rel-hm-small-v1"',f'DATA = Path({str(data)!r})'),
        ('    data, stats = make_pkey_fkey_graph(db, col_to_stype_dict=get_stype_proposal(db),',
         f"    seed_everything(42)\n    schema = get_stype_proposal(db.upto(__import__('pandas').Timestamp({fit_cutoff!r})))\n    (OUT/'stype_schema.json').write_text(json.dumps({{t:{{c:s.value for c,s in cols.items()}} for t,cols in schema.items()}},sort_keys=True,indent=2))\n    data, stats = make_pkey_fkey_graph(db, col_to_stype_dict=schema,"),
        ('parser.add_argument("--verify-only", action="store_true")','parser.add_argument("--verify-only", action="store_true")\n    parser.add_argument("--train-only", action="store_true")\n    parser.add_argument("--evaluate-only", action="store_true")\n    parser.add_argument("--probe", action="store_true")'),
        ('run_id = "hm_contextgnn_small_pipeline_v1"',f'run_id = "hm_medium_cv_v2_fold{fold}_gnn"'),
        ('model_run = f"hm_{kind}_small_seed_42_v1"',f'model_run = f"hm_medium_cv_v2_fold{fold}_{{kind}}"'),
        ('        if args.verify_only:\n            checkpoint',probe+insertion+'        if args.verify_only:\n            checkpoint'),
        ('            if (folder / "metrics.json").exists():','            if (folder / "trained.json").exists():'),
        ('                    if step >= 50:', '                    if step >= 1000000:'),
        ('            result = {"model": kind, "seed": 42,','            if args.train_only:\n                (folder/"trained.json").write_text(json.dumps({"best_epoch":best_epoch,"epochs":len(history),"seconds":time.perf_counter()-started}))\n                del model,optimizer\n                gc.collect()\n                torch.cuda.empty_cache()\n                continue\n            result = {"model": kind, "seed": 42,'),
        ('"steps_per_epoch_cap": 50','"steps_per_epoch_cap": None'),
        ('pred = torch.from_numpy(scores).topk(12, dim=1).indices.numpy()',"pred = np.argsort(-scores,axis=1,kind='stable')[:,:12]"),
        ('"all 5000 subset catalog items, all retained validation/test users"','"all 10000 items; original full-target evaluation including unretrievable positives"')])
    source=ROOT/'Recformer/run_ablations.py'
    text=source.read_text(encoding='utf-8')
    old_checks="    original_checks=json.loads((ROOT/'Recformer/results/hm_small_seed42_v1/data_checks.json').read_text())\n    assert hashlib.sha256(json.dumps(encoded,sort_keys=True).encode()).hexdigest()==original_checks['input_sha256']"
    old_zero="    original_zero=json.loads((ROOT/'Recformer/results/hm_small_seed42_v1/zero_shot/metrics.json').read_text())\n    assert abs(zero_metric['map']-original_zero['val_metrics']['map'])<1e-12"
    frozen_source(source,runtime/'recformer.py',[
        ('ROOT = Path(__file__).resolve().parents[1]',root),
        ("DATA = ROOT/'data/rel-hm-small-v1'",f'DATA = Path({str(data)!r})'),
        ("    OUT=ROOT/'Recformer/results'/('hm_small_'+args.variant+'_seed42_v1')",f'    OUT=Path({str(out/"recformer")!r})'),
        ("    RUN='hm_recformer_small_'+args.variant+'_seed42_v1'",f"    RUN='hm_medium_cv_v2_fold{fold}_recformer'"),
        (old_checks,"    assert all(len(encoded[s])==len(tables[s].df) for s in tables)"),
        (old_zero,"    assert np.isfinite(zero_metric['map'])"),
        ('    assert total_updates==1204','    assert total_updates>100'),
        ('5000','10000')])
    frozen_source(ROOT/'TDM/common.py',runtime/'tdm_common.py',[
        ("ROOT = Path(__file__).resolve().parents[1]",root),
        ("DATA = ROOT / 'data/rel-hm-small-v1'",f'DATA = Path({str(data)!r})'),
        ("OUT = ROOT / 'TDM/results/hm_small_v1'",f'OUT = Path({str(out/"tdm")!r})'),
        ('assert len(self.hashes)==10','assert len(self.hashes)>=10'),
        ("assert [len(self.tables[s].df) for s in self.tables]==[4804,304,250]","assert all(len(self.tables[s].df)>0 for s in self.tables)"),
        ('max_training_seconds=900','max_training_seconds=1800'),('5000','10000')])
    frozen_source(ROOT/'TDM/run_small.py',runtime/'tdm_train.py',[
        ('from common import (ROOT','from tdm_common import (ROOT'),
        ("PIPELINE='hm_tdm_small_pipeline_v1'",f"PIPELINE='hm_medium_cv_v2_fold{fold}_tdm'"),
        ("return f'hm_tdm_small_{variant}_seed42_v1'",f"return f'hm_medium_cv_v2_fold{fold}_tdm_{{variant}}'")])
    api=runtime/'api';api.mkdir(exist_ok=True)
    base=ROOT/'LLMFeatures/provider_generated_only_runtime_v1'
    for name in ['base_features.py','features.py','python_features.py','worker.py','runtime.py','prompting.py']:
        changes=[]
        if name=='python_features.py':changes=[("'len','list','map'","'hasattr','len','list','map'")]
        if name=='worker.py':changes=[('np.arange(5000)','np.arange(10000)'),("'full_catalog': 5000","'full_catalog': 10000"),
            ("    model = lgb.Booster(model_file=str(directory / 'model.txt'))\n    all_predictions = []",
             "    model = lgb.Booster(model_file=str(directory / 'model.txt'))\n    trained_names = model.feature_name()\n    assert trained_names == json.loads((directory / 'feature_schema.json').read_text())['features']\n    engine.names = list(trained_names)  # Align output by saved model schema, including fresh processes.\n    all_predictions = []")]
        if name=='runtime.py':
            changes=[("    return final\n","    return final\n")] # The API search is checkpointed per response; skip repetitive full archives.
            changes=[("        archive_run(out.parent)","        pass  # raw responses already persisted atomically"),
                     ("    archive_run(out.parent)","    pass  # archive only on explicit delivery"),
                     ('LightGBM training on72813 pairs','LightGBM training on configured fold pairs')]
        if name=='prompting.py':
            changes=[('frozen 5000-customer cohort','frozen 20000-customer cohort'),
                     ("{config['train_pairs']} unchanged pairs/4804 user-times/8cutoffs.","{config['train_pairs']} unchanged pairs/{config['train_user_times']} user-times/6cutoffs."),
                     ('Search128 users x all5000items.',"Search{config['search_users']} users x all10000items."),
                     ('disjoint confirmation88; heldout88/test250 never select programs.',"disjoint confirmation{config['confirmation_users']}; heldout/test never select programs. Original weekly targets include purchases outside the restricted catalog; they remain in MAP denominators.")]
        frozen_source(base/name,api/name,changes)
    # H009 and H008 use the same adapted validator, workers and prompts.
    for name in ['dialog_history.py']:
        frozen_source(ROOT/'LLMFeatures/provider_history_runtime_v1'/name,api/name)
    frozen_source(ROOT/'LLMFeatures/provider_history_runtime_v1/provider_api.py',api/'provider_history.py')
    frozen_source(ROOT/'LLMFeatures/provider_generated_only_runtime_v1/provider_api.py',api/'provider_best.py')
    manifest={str(p.relative_to(runtime)):sha(p) for p in sorted(runtime.rglob('*.py'))}
    write(out/'runtime_manifest.json',manifest)
    return runtime

if __name__=='__main__':
    import sys
    for f in map(int,sys.argv[1:] or range(3)):print(build(f),flush=True)
