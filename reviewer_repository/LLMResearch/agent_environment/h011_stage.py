"""Parent-only configuration, confirmation and frozen evaluation for H011."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import numpy as np
import pandas as pd
from toolbox import ROOT, BASE, Toolbox, read, write
from h011_settings import SESSION, RUN, REPORT

OUT = BASE / SESSION
OLD = ROOT / 'CVBenchmark/results/medium_v2'
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def prepare(fold):
    folder = OUT / f'fold_{fold}'
    folder.mkdir(parents=True, exist_ok=True)
    original = read(OLD / f'fold_{fold}/h009/run_config.json')
    runtime = OLD / f'fold_{fold}/runtime/api'
    assert original['runtime_sha256'] == {p.name: sha(p) for p in runtime.glob('*.py')}
    cfg = {**original, 'protocol': f'{RUN}_fold{fold}', 'test_previously_inspected': True,
           'standalone_agent_environment': True,
           'agent_protocol': 'Codex Responses native MCP terminal; three round-robin own-population sessions',
           'sampling_seed_requested': False, 'seed_guarantee': 'Codex does not expose proposal sampling seeds; evaluator/data remain42'}
    configpath = folder / 'evaluator_config.json'
    if configpath.exists():
        assert read(configpath) == cfg
    else:
        write(configpath, cfg)
    write(folder / 'run_config.json', cfg)
    manifest = read(ROOT / f'LLMResearch/results/v2/fold_{fold}/research_manifest.json')
    assert sha(ROOT / f'LLMResearch/results/v2/fold_{fold}/research.duckdb') == manifest['database_sha256']
    return folder, runtime, ROOT / f'data/hm-cv-medium-v2/fold_{fold}/bundle', configpath, cfg


def check_idle():
    markers = [b'LLMResearch/pipeline.py', b'LLMResearch/run.py', b'/worker.py', b'CVBenchmark/pipeline.py',
               b'CVFollowup/api_lane.py', b'CVFollowup/recformer_lane.py',
               b'CVFollowup/recformer_distributed.py', b'CVFollowup/gnn_lane.py',
               b'ContextGNN/run_small.py', b'Recformer/run_ablations.py', b'TDM/run_small.py']
    busy = []
    for path in Path('/proc').glob('[0-9]*/cmdline'):
        try:
            command = path.read_bytes()
        except (OSError, PermissionError):
            continue
        if str(ROOT).encode() in command and any(marker in command for marker in markers):
            busy.append({'pid': int(path.parent.name), 'command': command.replace(b'\0', b' ').decode(errors='replace')[:400]})
    if busy:
        print(json.dumps({'busy': busy, 'h011_started': False}, ensure_ascii=False), flush=True)
        raise SystemExit('Existing project run is alive; H011 remains prepared and unstarted')
    print('No conflicting project controller found', flush=True)


def select(fold):
    folder, runtime, data, configpath, cfg = prepare(fold)
    state = read(folder / 'budget.json')
    assert len(state['accepted']) == 20
    sys.path.insert(0, str(runtime))
    import runtime as api
    from python_features import RAW
    control = folder / 'raw_control'
    control.mkdir(exist_ok=True)
    write(control / 'program.json', {'code': RAW})
    (control / 'program.py').write_text(RAW)
    api.evaluate(data, control, 'search', configpath)
    valid = sorted(state['accepted'], key=lambda t: (-t['search_map'], t['call']))
    options = [{'directory': str(control), 'call': None}] + valid[:3]
    confirmation = []
    for entry in options:
        metric = api.evaluate(data, entry['directory'], 'confirm', configpath)
        confirmation.append({'directory': entry['directory'], 'call': entry['call'], 'confirmation_map': metric['map']})
    winner = max(confirmation, key=lambda t: t['confirmation_map'])
    directory = Path(winner['directory'])
    selected = {**winner, 'program_sha256': sha(directory / 'program.json'),
                'model_sha256': sha(directory / 'model.txt'), 'successful_distinct': 20,
                'budget_complete': True, 'confirmation': confirmation,
                'selection': 'top3 search + constant, disjoint confirmation; stable ties control then search/call'}
    target = folder / 'selected.json'
    if target.exists():
        assert read(target) == selected
    else:
        write(target, selected)
    record('h011_fold_selected', f'H011 autonomous Codex fold{fold}:20 accepted, original top3+constant confirmation selection frozen.',
           cfg['protocol'], status='selected_pending_test', artifacts=str(folder.relative_to(ROOT)))


def freeze():
    choices = {str(f): read(OUT / f'fold_{f}/selected.json') for f in range(3)}
    value = {'run_id': RUN, 'folds': choices, 'outer_metrics_used_for_selection': False,
             'test_previously_inspected': True, 'protocol_sha256': sha(Path(__file__).with_name('H011_PROTOCOL.md'))}
    target = REPORT / 'pretest_freeze.json'
    if target.exists():
        assert read(target) == value
    else:
        write(target, value)
    record('h011_all_selections_frozen', 'All three native Codex agent fold selections frozen before new outer scoring.', RUN, status='evaluating')


def evaluate(fold):
    folder, runtime, data, configpath, cfg = prepare(fold)
    selected = read(REPORT / 'pretest_freeze.json')['folds'][str(fold)]
    winner = Path(selected['directory'])
    assert sha(winner / 'program.json') == selected['program_sha256']
    assert sha(winner / 'model.txt') == selected['model_sha256']
    sys.path.insert(0, str(runtime))
    import runtime as api
    for split in ['heldout_val', 'val', 'test']:
        metric = api.evaluate(data, winner, split, configpath)
        assert api.evaluate(data, winner, 'replay_' + split, configpath)['passed']
        targets = pd.read_parquet(data / ('test_targets.parquet' if split == 'test' else 'val_targets.parquet'))
        if split == 'heldout_val':
            targets = targets.iloc[read(data / 'selection.json')[split]].reset_index(drop=True)
        pred = np.load(winner / f'{split}_predictions.npy')
        assert pred.shape == (len(targets), 12)
        assert all(len(np.unique(p)) == 12 and ((p >= 0) & (p < 10000)).all() for p in pred)
        hits = np.asarray([np.isin(p, np.unique(t)) for p, t in zip(pred, targets.article_id)])
        ap = (hits * np.cumsum(hits, 1) / np.arange(1, 13)).sum(1) / np.minimum(12, [len(np.unique(t)) for t in targets.article_id])
        assert abs(float(ap.mean()) - metric['map']) < 1e-12
        np.save(folder / f'{split}_predictions.npy', pred)
        np.save(folder / f'{split}_ap.npy', ap)
        np.save(folder / f'{split}_users.npy', targets.customer_id.to_numpy())
        write(folder / f'{split}_metrics.json', metric)
    write(folder / 'verification.json', {'passed': True, 'full_replays': True, 'independent_AP': True})
    record('h011_fold_verified', f'Autonomous Codex fold{fold}: full replays and independent AP passed.',
           cfg['protocol'], status='evaluated_verified', test_metrics=read(folder / 'test_metrics.json'),
           val_metrics=read(folder / 'val_metrics.json'), artifacts=str(folder.relative_to(ROOT)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['prepare', 'select', 'freeze', 'evaluate', 'record_start', 'record_stop', 'check_idle'])
    parser.add_argument('--fold', type=int, default=0)
    parser.add_argument('--message', default='')
    args = parser.parse_args()
    if args.stage == 'record_start':
        record('h011_started', 'User chose autonomous agent. Native Codex with GPT-6.1 Sol, three isolated populations/fold,20 accepted checks/fold, train-only OS-isolated tools, frozen original H009 evaluator; separate from H010.', RUN, status='searching', artifacts=str(REPORT.relative_to(ROOT)))
    elif args.stage == 'record_stop':
        record('h011_interrupted', args.message, RUN, status='interrupted')
    elif args.stage in ['freeze', 'check_idle']:
        globals()[args.stage]()
    else:
        globals()[args.stage](args.fold)
