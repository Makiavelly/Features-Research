"""Exercise the revised allowance on synthetic state; no API or fitting."""
import json
from pathlib import Path
from toolbox import Toolbox, BASE, read, write
from budget_policy import research_caps

session = 'h011_budget300_preflight'
control = BASE / session / 'fold_0'
write(BASE / session / 'research_policy.json', {'research_caps': [100, 100, 100], 'research_total': 300})
assert research_caps(session) == [100, 100, 100]
write(control / 'research_budget.json', [99, 100, 100])
box = Toolbox(0, session, 0)
result = box.terminal("python -c 'print(300)'")
assert result['exit_code'] == 0 and result['output'].strip() == '300', result
assert read(control / 'research_budget.json') == [100, 100, 100]
assert 'error' in box.terminal('echo must-not-run')
assert read(control / 'research_budget.json') == [100, 100, 100]
assert 'error' in Toolbox(0, session, 1).terminal('echo must-not-run')
assert 'error' in Toolbox(0, session, 2).terminal('echo must-not-run')
assert box.call('status', {})['research_remaining_own_population'] == 0
assert research_caps('standalone_v2') == [14, 13, 13]
target = Path(__file__).with_name('budget300_verification.json')
write(target, {'passed': True, 'checks': ['hundredth_call_allowed', 'hundred_first_denied',
      'three_populations_total300', 'counter_not_reset_by_denial', 'remaining_reported_in_status',
      'other_sessions_unchanged'], 'real_API_requests': 0, 'feature_trainings': 0})
print(target.read_text())
