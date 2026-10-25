"""Verify actual separate Codex tool events and persist the environment result."""
import json
from pathlib import Path
import sys
from toolbox import ROOT, BASE, Toolbox, read, write

folder = BASE / 'standalone_v2/fold_0'
events = [json.loads(line) for line in (folder / 'codex_events.jsonl').read_text(encoding='utf-8').splitlines() if line.startswith('{')]
calls = [e['item'] for e in events if e['type'] == 'item.completed' and e.get('item', {}).get('type') == 'mcp_tool_call']
assert any(c['tool'] == 'status' and c['status'] == 'completed' for c in calls)
terminal = next(c for c in calls if c['tool'] == 'terminal' and c['status'] == 'completed')
result = json.loads(terminal['result']['content'][0]['text'])
assert result['exit_code'] == 0 and 'train_pairs_count=190260' in result['output'] and 'mnt_c_exists=False' in result['output']
assert not any(c['tool'] == 'evaluate_features' for c in calls)
assert all(not Toolbox(fold, 'standalone_v2').state()['accepted'] for fold in range(3))
usage = next(e['usage'] for e in events if e['type'] == 'turn.completed')
value = {'passed': True, 'actual_codex_cli_agent': True, 'model_id_requested': 'gpt-6.1-sol',
         'provider_identity_independently_attested': False, 'separate_codex_home': True,
         'connected_train_folds': [0, 1, 2], 'native_agent_tools_verified_on_fold': 0,
         'successful_tools': ['fold.status', 'fold.terminal'], 'train_pairs': 190260,
         'feature_evaluations': 0, 'remaining_per_fold': 20, 'usage_successful_smoke': usage,
         'initial_smoke_profile': 'standalone_v1: tool approval configuration failed; preserved separately',
         'full_feature_experiment_started': False}
write(Path(__file__).with_name('native_agent_verification.json'), value)
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record
record('gpt61sol_codex_environment_ready',
       'Separate Codex CLI with configured gpt-6.1-sol provider actually called local train-fold MCP tools. OS-isolated terminal read190260 fold0 train pairs, imported pandas/NumPy/DuckDB, confirmed host project absent. Three fold profiles prepared;0 feature checks used. Original normal Codex/unsloth environments unchanged. Standalone agent smoke, not a completed feature experiment. Initial MCP approval-profile smoke failed and is retained separately.',
       'hm_gpt61sol_codex_environment_v1', status='complete', verification=value,
       artifacts='LLMResearch/agent_environment/README.md')
print(json.dumps(value, ensure_ascii=False, indent=2))
