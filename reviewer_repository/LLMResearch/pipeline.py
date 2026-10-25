"""Sequential API lane with a three-fold selection barrier."""
import fcntl
import subprocess
import sys
import traceback
from common import ROOT, SOURCE, OUT, REPORT, RUN, read, write, sha, record


def invoke(script, *args):
    subprocess.run([sys.executable, '-u', str(SOURCE / script), *map(str, args)], cwd=ROOT, check=True)


def pipeline():
    assert read(REPORT / 'verification.json')['passed']
    record('h010_started', 'H010 authorized: train-statistics tools added to matched H009,20 accepted programs/fold,40 research requests/fold,300 POST cap. Original test weeks already inspected.',
           RUN, status='searching', artifacts=str(REPORT.relative_to(ROOT)))
    for fold in range(3):
        write(REPORT / 'pipeline_status.json', {'status': 'searching', 'fold': fold})
        invoke('run.py', fold, 'train')
    folds = {}
    for fold in range(3):
        folder = OUT / f'fold_{fold}'
        cfg = read(folder / 'run_config.json')
        selected = read(folder / cfg['arm'] / 'selected.json')
        assert selected['budget_complete'] and selected['successful_distinct'] == 20
        folds[str(fold)] = {k: selected[k] for k in ['directory', 'call', 'program_sha256', 'model_sha256', 'confirmation_map']}
    freeze = REPORT / 'pretest_freeze.json'
    value = {'protocol': RUN, 'folds': folds, 'selection_uses_outer_test': False,
             'test_previously_inspected': True, 'protocol_sha256': sha(SOURCE / 'PROTOCOL.md')}
    if freeze.exists():
        assert read(freeze) == value
    else:
        write(freeze, value)
    record('h010_all_selections_frozen', 'All three H010 selections frozen before new outer scoring.', RUN, status='evaluating')
    for fold in range(3):
        write(REPORT / 'pipeline_status.json', {'status': 'evaluating', 'fold': fold})
        invoke('run.py', fold, 'evaluate')
    invoke('report.py')
    write(REPORT / 'pipeline_status.json', {'status': 'report_pending_visual_review'})
    record('h010_report_generated', 'H010 all60 accepted programs and all frozen replays complete; paired H009 comparison generated, visual review pending.',
           RUN, status='report_pending_visual_review', artifacts=str(REPORT.relative_to(ROOT)))


if __name__ == '__main__':
    REPORT.mkdir(parents=True, exist_ok=True)
    with (REPORT / '.pipeline.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            pipeline()
        except BaseException as error:
            write(REPORT / 'pipeline_status.json', {'status': 'interrupted', 'error': str(error)[:1600]})
            record('h010_interrupted', str(error)[:1600], RUN, status='interrupted')
            traceback.print_exc()
            raise
