"""Record audited H009 outcome and memory/capability caveats."""
import csv
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/provider_history_v1'
audit=json.loads((OUT/'audit.json').read_text(encoding='utf-8'))
assert audit['status']=='passed' and audit['full_own_island_history_verified']
with (OUT/'comparison.csv').open(encoding='utf-8',newline='') as stream:
    row=next(r for r in csv.DictReader(stream) if r['model']=='GPT61Sol_FullHistory')
metrics={stage+'_metrics':{'map':float(row[stage+'_map_percent'])/100}
         for stage in ['search','confirm','heldout_val','val','test']}
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record
record('provider_history_verified_summary',
       'H009 complete:24 API POST,20 accepted programs,18 unordered numeric sets. '
       'Selected6:validation2.286989%,test0.721596% versus best-only H008test1.426760%. '
       'All own-island histories/search feedback verified, max18 messages/38143 input tokens, '
       '385823 total input tokens versus55261. Four rejections include one HOST hasattr limitation; '
       'diagnostic proves rejected15 equals accepted16 when only hasattr is enabled. '
       'Live runtime unchanged. One run does not establish a universal memory effect.',
       audit['run_id'],status='complete',audit_status='passed',api_requests=24,measured=20,
       numeric_distinct_sets=18,selected_call=audit['selected_call'],
       full_own_island_history_verified=True,input_tokens=385823,max_input_tokens_observed=38143,
       automatic_raw_features=0,host_builtin_limitations=1,
       artifacts='reports/provider_history_v1',**metrics)
print('H009 metrics and context outcome recorded.')
