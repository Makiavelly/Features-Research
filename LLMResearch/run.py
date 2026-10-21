"""Run a single fold in its own process; preserve original H009 evaluator."""
import argparse
import fcntl
from pathlib import Path
import sys
import time
import numpy as np
import pandas as pd
from common import ROOT, OUT, REPORT, RUN, read, write, sha, record
from prepare import prepare


def run(fold, stage):
    folder, runtime, bundle, cfg, cfgpath = prepare(fold)
    assert read(REPORT / 'verification.json')['passed']
    assert sha(folder / 'research.duckdb') == cfg['research_database_sha256']
    assert {p.name: sha(p) for p in runtime.glob('*.py')} == cfg['runtime_sha256']
    sys.path.insert(0, str(runtime))
    import runtime as api
    from python_features import RAW
    from agent import ResearchGenerator
    if stage == 'train':
        if (folder / 'trained.json').exists():
            return
        control = folder / 'raw_control'
        control.mkdir(exist_ok=True)
        write(control / 'program.json', {'code': RAW})
        (control / 'program.py').write_text(RAW)
        api.evaluate(bundle, control, 'search', cfgpath)
        generator = ResearchGenerator(cfg, folder, ROOT / '.env')
        original = api.progress
        def progress(directory, trials, config):
            valid = original(directory, trials, config)
            calls = len(list((folder / 'api_attempts').glob('attempt_*')))
            query_count = sum(generator.used(i) for i in range(3))
            write(REPORT / f'fold_{fold}_status.json', {'status': 'searching',
                  'accepted': len(valid), 'responses': len(trials), 'actual_POST': calls,
                  'queries': query_count, 'last_trial': {k: v for k, v in trials[-1].items()
                                                       if k not in ['program']}})
            record('h010_search_progress', f'H010 fold{fold}: {len(valid)}/20 accepted; {calls} POST; {query_count}/40 research queries.',
                   cfg['protocol'], status='searching', accepted=len(valid), actual_POST=calls,
                   research_queries=query_count, artifacts=str(folder.relative_to(ROOT)))
            return valid
        api.progress = progress
        started = time.perf_counter()
        selected = api.search(bundle, folder / cfg['arm'], generator, cfgpath)
        assert selected['budget_complete'] and selected['successful_distinct'] == 20
        write(folder / 'trained.json', {'selection': selected, 'seconds_this_segment': time.perf_counter() - started})
        record('h010_fold_selected', f'H010 fold{fold}:20 accepted programs, selection frozen before new outer evaluation.',
               cfg['protocol'], status='selected_pending_test')
    else:
        freeze = read(REPORT / 'pretest_freeze.json')['folds'][str(fold)]
        selected = read(folder / cfg['arm'] / 'selected.json')
        winner = Path(selected['directory'])
        assert sha(winner / 'program.json') == freeze['program_sha256'] == selected['program_sha256']
        assert sha(winner / 'model.txt') == freeze['model_sha256'] == selected['model_sha256']
        for split in ['heldout_val', 'val', 'test']:
            metric = api.evaluate(bundle, winner, split, cfgpath)
            replay = api.evaluate(bundle, winner, 'replay_' + split, cfgpath)
            assert replay['passed']
            pred = np.load(winner / f'{split}_predictions.npy')
            target = pd.read_parquet(bundle / ('test_targets.parquet' if split == 'test' else 'val_targets.parquet'))
            if split == 'heldout_val':
                target = target.iloc[read(bundle / 'selection.json')[split]].reset_index(drop=True)
            assert pred.shape == (len(target), 12)
            assert all(len(np.unique(p)) == 12 for p in pred)
            hits = np.array([np.isin(p, np.unique(t)) for p, t in zip(pred, target.article_id)])
            ap = (hits * np.cumsum(hits, axis=1) / np.arange(1, 13)).sum(1) / np.minimum(12, [len(np.unique(t)) for t in target.article_id])
            assert abs(float(ap.mean()) - metric['map']) < 1e-12
            np.save(folder / f'{split}_predictions.npy', pred)
            np.save(folder / f'{split}_ap.npy', ap)
            np.save(folder / f'{split}_users.npy', target.customer_id.to_numpy())
            write(folder / f'{split}_metrics.json', metric)
        write(folder / 'verification.json', {'passed': True, 'full_frozen_replays': True, 'independent_AP': True})
        record('h010_fold_verified', f'H010 fold{fold}: full frozen replays and independent AP passed.',
               cfg['protocol'], status='evaluated_verified', val_metrics=read(folder / 'val_metrics.json'),
               test_metrics=read(folder / 'test_metrics.json'), artifacts=str(folder.relative_to(ROOT)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fold', type=int, choices=range(3))
    parser.add_argument('stage', choices=['train', 'evaluate'])
    args = parser.parse_args()
    folder = OUT / f'fold_{args.fold}'
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / '.execution.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        run(args.fold, args.stage)
