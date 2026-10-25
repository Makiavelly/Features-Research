"""Explicitly migrate a completed-turn H011 state without resetting any counts."""
import hashlib
from pathlib import Path
import sys
from toolbox import ROOT, read, write
from h011_settings import SESSION, RUN, REPORT

source = Path(__file__).resolve().parent
session = source / 'sessions' / SESSION
previous = ROOT / 'reports/medium_h011_codex_v1'
snapshot = previous / 'before_budget300'
saved = read(snapshot / 'snapshot.json')
assert read(source / 'budget300_verification.json')['passed']
assert read(previous / 'pipeline_status.json')['status'] == 'interrupted'
assert saved['next_turn'] == read(session / 'fold_0/next_turn.json')['next_turn']
assert saved['accepted'] == len(read(session / 'fold_0/budget.json')['accepted'])
assert not list(session.glob('fold_*/selected.json')), 'Budget change must precede selection/test'
assert not REPORT.exists(), 'Revision already activated; do not overwrite its provenance'
REPORT.mkdir(parents=True)
policy = {'run_id': RUN, 'research_caps': [100, 100, 100], 'research_total': 300,
          'supersedes': 'hm_medium_h011_codex_seed42_v1', 'inherited': saved,
          'change': 'User explicitly increased research budget40 to300 per fold during search; retain all prior work and counts.'}
write(session / 'research_policy.json', policy)
for fold in range(3):
    folder = session / f'fold_{fold}'
    for name in ['evaluator_config.json', 'run_config.json']:
        path = folder / name
        if path.exists():
            cfg = read(path)
            assert cfg['protocol'] == f'hm_medium_h011_codex_seed42_v1_fold{fold}'
            cfg['protocol'] = f'{RUN}_fold{fold}'
            write(path, cfg)
    for island in range(3):
        work = folder / f'island_{island}/work'
        context = work / 'CONTEXT.md'
        with context.open('a', encoding='utf-8') as stream:
            stream.write('\n\nThe user increased the research terminal budget to100 calls per population,300 per fold.\n'
                         'This supersedes earlier14/13/13 instructions. Previously spent calls remain counted.\n'
                         'Feature-check budget remains20 shared per fold; API cap remains300 POSTs per fold.\n')
verification = read(source / 'h011_verification.json')
names = set(verification['sources_sha256']) | {'h011_settings.py', 'budget_policy.py',
        'check_budget300.py', 'activate_budget300.py'}
verification['sources_sha256'] = {name: hashlib.sha256((source / name).read_bytes()).hexdigest()
                                  for name in sorted(names)}
verification['profile_sha256'] = {str(p.relative_to(session)): hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in session.glob('fold_*/island_*/codex_home/config.toml')}
assert len(verification['profile_sha256']) == 9
verification.update(status='budget300_continuation_ready', run_id=RUN, budget_revision=policy,
                    revision_checks=read(source / 'budget300_verification.json'))
write(source / 'h011_verification.json', verification)
write(REPORT / 'launch_readiness.json', verification)
write(REPORT / 'continuation_provenance.json', policy)
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record
record('h011_budget40_superseded',
       'User increased research budget40 to300/fold. Controller stopped at a completed-turn boundary using its existing profile-integrity guard; original sources/state preserved in before_budget300. No paid response or candidate discarded. Continue under a new run ID; original run is incomplete, not a final result.',
       policy['supersedes'], status='superseded_budget_change', inherited=saved,
       artifacts=str(snapshot.relative_to(ROOT)))
record('h011_budget300_authorized',
       'User-requested research budget300/fold,100/population. Continue the same conversations and candidates with counters retained;20 accepted-program cap and300 API-POST cap unchanged. New run ID identifies changed protocol, not an independent restart. Six synthetic allowance tests passed without API or fitting.',
       RUN, status='resuming', inherited=saved, research_budget=300,
       artifacts=str(REPORT.relative_to(ROOT)))
print(policy)
