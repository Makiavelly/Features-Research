"""Recover after the legacy API-efficiency report fails on a non-API run.

Only verifies completed scoring and updates the registry; no training, scoring,
program edits or changes to the frozen configuration are performed.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record

def read(p):
    return json.loads(p.read_text())
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

registry = ROOT / 'reports/authored20_v1/current_run.json'
source = Path(read(registry)['directory'])
state = read(source / 'state.json')
assert state['evaluated'] == state['committed'] == 20
selected = read(source / 'codex_authored20/selected.json')
for folder in [source / 'raw_control', Path(selected['directory'])]:
    for stage in ['heldout_val', 'val', 'test']:
        original = read(folder / f'{stage}_metrics.json')
        replay = read(folder / f'replay_{stage}_metrics.json')
        assert replay['passed']
        assert original['map'] == replay['map']
        assert original['predictions_sha256'] == replay['predictions_sha256'] == sha(folder / f'{stage}_predictions.npy')
        assert original['model_sha256'] == sha(folder / 'model.txt')
        assert original['program_sha256'] == sha(folder / 'program.json')
for name in ['comparison.csv', 'comparison.png', 'test_histograms.png', 'lightgbm_training.png']:
    assert (source / name).exists()
note = {'failure': "legacy efficiency_report requires target_successful_distinct; authored run uses planned_sets",
        'scope': 'postprocessing only, after scoring and all six frozen replays',
        'recovery': 'verify saved scoring outputs and mark ready for independent audit',
        'frozen_config_modified': False, 'additional_training': 0, 'additional_api_calls': 0}
(source / 'postprocessing_recovery.json').write_text(json.dumps(note, indent=2))
registry.write_text(json.dumps({'run_id': source.name, 'directory': str(source), 'status': 'finished'}, indent=2))
record('authored20_scoring_complete',
       'All 20 sets retained; confirmation selected set 9. Final scores and six frozen replays completed. '
       'Legacy API-efficiency report failed on a missing non-API config key; verified output-only recovery, frozen sources/config unchanged. Independent audit next.',
       source.name, status='completed_pending_audit', authored_sets=20, api_requests=0,
       artifacts='reports/authored20_v1')
print('Scoring verified; registry finalized without rerunning evaluation.')
