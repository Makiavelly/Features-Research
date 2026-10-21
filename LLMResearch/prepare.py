"""Freeze original H009 runtime and construct train-only research tables."""
import sys
import duckdb
import pandas as pd
from common import ROOT, SOURCE, OLD, DATA, OUT, REPORT, RUN, read, write, sha, frozen


def prepare(fold):
    folder = OUT / f'fold_{fold}'
    runtime = folder / 'runtime'
    for source in (OLD / f'fold_{fold}/runtime/api').glob('*.py'):
        frozen(runtime / source.name, source.read_text(encoding='utf-8'))
    # Independent source snapshots allow audit/resume even after later code work.
    for name in ['agent.py', 'query_worker.py']:
        frozen(runtime / name, (SOURCE / name).read_text(encoding='utf-8'))
    sys.path.insert(0, str(runtime))
    bundle = DATA / f'fold_{fold}/bundle'
    cfg = read(OLD / f'fold_{fold}/h009/run_config.json')
    assert cfg['runtime_sha256'] == {p.name: sha(p) for p in runtime.glob('*.py')
                                   if p.name not in ['agent.py', 'query_worker.py']}
    assert read(OLD / f'fold_{fold}/validator_verification.json')['status'] == 'passed'
    dbpath = folder / 'research.duckdb'
    manifest_path = folder / 'research_manifest.json'
    if not manifest_path.exists():
        assert not dbpath.exists(), 'Incomplete research database; inspect before rebuilding'
        from base_features import FeatureEngine
        pairs = pd.read_parquet(bundle / 'train_pairs.parquet')
        val = pd.read_parquet(bundle / 'val_targets.parquet', columns=['timestamp'])
        assert pairs.timestamp.max() + pd.Timedelta(days=7) <= val.timestamp.min()
        assert sha(bundle / 'train_pairs.parquet') == cfg['train_pair_sha256']
        engine = FeatureEngine(folder / 'scratch/research_prepare', bundle)
        con = duckdb.connect(str(dbpath))
        try:
            engine.prepare(pairs.timestamp.min(), pairs.customer_id.unique(), {'aggregates': []})
            raw = engine.frame(pairs)
            train_pairs = pd.concat([pairs.reset_index(drop=True), raw], axis=1)
            assert len(train_pairs) == cfg['train_pairs']
            con.register('frame', train_pairs)
            con.execute('CREATE TABLE train_pairs AS SELECT * FROM frame')
            con.unregister('frame')
            cutoffs = sorted(pairs.timestamp.unique())
            rows = []
            for index, cutoff in enumerate(cutoffs):
                engine.prepare(cutoff, pairs.customer_id.unique(), {'aggregates': []})
                history = engine.con.sql('SELECT * FROM history').df()
                assert len(history) and history.days_ago.min() >= 0
                history['cutoff'] = pd.Timestamp(cutoff)
                con.register('frame', history)
                if index == 0:
                    con.execute('CREATE TABLE train_history AS SELECT * FROM frame')
                else:
                    con.execute('INSERT INTO train_history SELECT * FROM frame')
                con.unregister('frame')
                rows.append({'cutoff': str(pd.Timestamp(cutoff)), 'rows': len(history)})
            con.execute('CREATE TABLE history AS SELECT * EXCLUDE(cutoff) FROM train_history WHERE cutoff=(SELECT max(cutoff) FROM train_history)')
            tables = {name: con.execute(f'DESCRIBE {name}').fetchall()
                      for name in ['train_pairs', 'train_history', 'history']}
            sources = {n: sha(bundle / n) for n in ['train_pairs.parquet', 'transactions.parquet',
                                                     'article.parquet', 'customer.parquet']}
        finally:
            engine.close()
            con.close()
        write(manifest_path, {'tables': tables, 'history_cutoffs': rows,
                             'train_label_end': str(pairs.timestamp.max() + pd.Timedelta(days=7)),
                             'sources': sources, 'database_sha256': sha(dbpath),
                             'contains_validation_or_test': False})
    manifest = read(manifest_path)
    assert sha(dbpath) == manifest['database_sha256']
    for name, digest in manifest['sources'].items():
        assert sha(bundle / name) == digest
    cfg.update(protocol=f'{RUN}_fold{fold}', test_previously_inspected=True,
               research_protocol='text JSON query_train, train-only, full own-island history',
               research_query_budget=40, research_island_budgets=[14, 13, 13],
               research_queries_per_generation=4, research_query_timeout_seconds=20,
               research_database_sha256=manifest['database_sha256'],
               research_tables=manifest['tables'],
               research_history_cutoffs=manifest['history_cutoffs'],
               research_manifest_sha256=sha(manifest_path),
               source_h009_config_sha256=sha(OLD / f'fold_{fold}/h009/run_config.json'),
               runtime_sha256={p.name: sha(p) for p in runtime.glob('*.py')})
    cfgpath = folder / 'run_config.json'
    frozen(cfgpath, __import__('json').dumps(cfg, ensure_ascii=False, indent=2) + '\n')
    return folder, runtime, bundle, cfg, cfgpath


if __name__ == '__main__':
    if sys.argv[1] == '--refresh-unstarted':
        # Only preflight corrections BEFORE any real generation are allowed.
        for fold in range(3):
            folder = OUT / f'fold_{fold}'
            assert not list(folder.glob('api_attempts/attempt_*'))
            assert not (folder / 'generations').exists()
        for fold in range(3):
            folder = OUT / f'fold_{fold}'
            for name in ['agent.py', 'query_worker.py']:
                target = folder / 'runtime' / name
                if target.exists() and target.read_text(encoding='utf-8') != (SOURCE / name).read_text(encoding='utf-8'):
                    target.unlink()
                    (folder / 'run_config.json').unlink(missing_ok=True)
        (REPORT / 'verification.json').unlink(missing_ok=True)
    else:
        prepare(int(sys.argv[1]))
