"""Publish verified H007 metrics to the persistent experiment registry."""
import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record

out = ROOT / 'reports/authored20_v1'
audit = json.loads((out / 'audit.json').read_text(encoding='utf-8'))
assert audit['status'] == 'passed'
with (out / 'comparison.csv').open(encoding='utf-8', newline='') as stream:
    row = next(r for r in csv.DictReader(stream) if r['model'] == 'CodexAuthored20')
metrics = {stage: {'map': float(row[stage + '_map_percent']) / 100}
           for stage in ['search', 'confirm', 'heldout_val', 'val', 'test']}
record('authored20_verified_metrics_registered',
       'H007 complete: 20 adaptive sets, 3 populations; confirmation selected set 9. '
       'Validation MAP@12 1.260603%, test 2.231032%. Audit passed. '
       'Generated features plus raw15; prior experiment history known, not a blind search.',
       audit['run_id'], status='complete', selected_call=audit['selected']['call'],
       authored_sets=20, api_requests=0, audit_status='passed',
       prior_experiment_history_known=True, automatic_raw_features=15,
       artifacts='reports/authored20_v1',
       **{stage + '_metrics': value for stage, value in metrics.items()})
print('Verified metrics recorded in experiment history.')
