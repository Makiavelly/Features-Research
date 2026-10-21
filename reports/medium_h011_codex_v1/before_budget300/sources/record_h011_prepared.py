"""Close preparation only: freeze readiness and explicitly retain deferred start."""
import hashlib
from pathlib import Path
import sys
from toolbox import ROOT, read, write

SOURCE = Path(__file__).resolve().parent
REPORT = ROOT / 'reports/medium_h011_codex_v1'
OUT = SOURCE / 'sessions/h011_codex_seed42_v1'
gateway = read(SOURCE / 'h011_verification.json')
tools = read(SOURCE / 'h011_tools_verification.json')
assert gateway['passed'] and tools['passed']
assert not (REPORT / 'pipeline.pid').exists()
assert not list(OUT.glob('fold_*/api_attempts/attempt_*'))
assert not list(OUT.glob('fold_*/evaluations/candidate_*'))
names = sorted(set(gateway['sources_sha256']) | {'check_h011.py', 'check_h011_tools.py',
               'launch_h011_windows.py', 'record_h011_prepared.py'})
gateway['sources_sha256'] = {name: hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() for name in names}
configs = {str(path.relative_to(OUT)): hashlib.sha256(path.read_bytes()).hexdigest()
           for path in OUT.glob('fold_*/island_*/codex_home/config.toml')}
assert len(configs) == 9
gateway.update(status='prepared_deferred_by_user', real_API_requests=0, feature_trainings=0,
               source_user_instruction='Prepare only; launch later to avoid interference with current runs.',
               population_tools_checks=tools['checks'], profile_sha256=configs,
               start_admission_test='Verified rejection while H010 controller was alive',
               actual_experiment_started=False, automatic_launch_watcher=False)
write(SOURCE / 'h011_verification.json', gateway)
write(REPORT / 'prepared.json', gateway)
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record
record('h011_prepared_launch_deferred',
       'User explicitly requested preparation only and later launch to avoid interference. H011 fully prepared: nine private profiles, bounded autonomous round-robin controller, original H009 evaluator, parent confirmation/freeze/replay/report, protected20 checks and gateway300-POST cap. Mock gateway and eleven tool/evaluator checks passed, admission guard rejected live H010. ZERO H011 API requests/trainings; no controller or automatic watcher started.',
       'hm_medium_h011_codex_seed42_v1', status='prepared_deferred_by_user',
       artifacts='LLMResearch/agent_environment/README.md', checks=tools['checks'],
       real_API_requests=0, feature_trainings=0)
print('H011 prepared and frozen; launch explicitly deferred;0 API requests,0 trainings.')
