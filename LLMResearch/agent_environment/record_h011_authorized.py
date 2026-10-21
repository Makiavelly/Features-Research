"""Freeze prelaunch timeout handling after the user's explicit start instruction."""
import hashlib
from pathlib import Path
import sys
from toolbox import ROOT, read, write

SOURCE = Path(__file__).resolve().parent
OUT = SOURCE / 'sessions/h011_codex_seed42_v1'
REPORT = ROOT / 'reports/medium_h011_codex_v1'
verification = read(SOURCE / 'h011_verification.json')
assert verification['passed'] and read(SOURCE / 'h011_tools_verification.json')['passed']
assert not list(OUT.glob('fold_*/api_attempts/attempt_*'))
assert not list(OUT.glob('fold_*/evaluations/candidate_*'))
names = set(verification['sources_sha256']) | {'check_h011.py', 'check_h011_tools.py',
        'launch_h011_windows.py', 'record_h011_authorized.py'}
verification['sources_sha256'] = {name: hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()
                                  for name in sorted(names)}
verification['profile_sha256'] = {str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in OUT.glob('fold_*/island_*/codex_home/config.toml')}
assert len(verification['profile_sha256']) == 9
verification.update(status='authorized_ready_to_start', user_authorized_launch=True,
                    timeout_policy='3 retries before response headers only,5/15/30 seconds; each POST consumes300-fold cap; partial streams stop',
                    real_API_requests=0, feature_trainings=0)
write(SOURCE / 'h011_verification.json', verification)
write(REPORT / 'launch_readiness.json', verification)
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record
record('h011_launch_authorized',
       'User explicitly authorized H011 after H010 completion and requested timeout handling. Mocked connection failure recovers with separately counted POST; persistent failures stop after four attempts. Isolation/budget/evaluator checks passed again before paid work; sources/profiles refrozen. Previous launch deferral superseded.',
       'hm_medium_h011_codex_seed42_v1', status='authorized_ready_to_start',
       timeout_policy=verification['timeout_policy'], artifacts='reports/medium_h011_codex_v1')
print('H011 launch authorized and prelaunch sources frozen; no paid calls yet.')
