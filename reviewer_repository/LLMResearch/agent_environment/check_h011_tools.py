"""Population and external-budget checks; no feature training/model requests."""
import json
from pathlib import Path
import subprocess
import sys
from toolbox import ROOT, BASE, Toolbox, read, write
from h011_stage import prepare

boxes = [Toolbox(0, 'h011_preflight_tools', island) for island in range(3)]
control = boxes[0].control
checks = []
for island, box in enumerate(boxes):
    box.call('write_file', {'path': 'private.txt', 'content': str(island)})
    write(box.root / 'turn_allowance.json', {'island': island, 'starting_attempts': 2})
    try:
        box.call('write_file', {'path': '../../budget.json', 'content': '{}'})
    except ValueError:
        pass
    else:
        raise AssertionError('Budget state writable from agent file tool')
    try:
        box.call('read_file', {'path': f'../../island_{(island + 1) % 3}/work/private.txt'})
    except ValueError:
        pass
    else:
        raise AssertionError('Other population files exposed')
write(control / 'budget.json', {'accepted': [{'island': 0, 'search_map': .9}, {'island': 1, 'search_map': .1}],
                              'attempts': [{'status': 'accepted'}, {'status': 'accepted'}], 'target': 20})
assert boxes[0].call('status', {})['best_search_map'] == .9
assert boxes[1].call('status', {})['best_search_map'] == .1
assert boxes[2].call('status', {})['best_search_map'] is None
checks += ['other_population_files_denied', 'budget_outside_writable_workspace', 'no_other_population_search_feedback']
write(control / 'budget.json', {'accepted': [], 'attempts': [{'status': 'rejected'}] * 6, 'target': 20})
assert boxes[0].evaluate('not-a-file.py', '')['status'] == 'turn_budget_exhausted'
write(control / 'budget.json', {'accepted': [], 'attempts': [{'status': 'rejected'}] * 2 + [{'status': 'accepted'}], 'target': 20})
assert boxes[0].evaluate('not-a-file.py', '')['status'] == 'turn_budget_exhausted'
checks += ['four_submissions_per_turn_cap', 'one_success_per_turn_cap']
write(control / 'budget.json', {'accepted': [{'status': 'accepted'}] * 20, 'attempts': [], 'target': 20})
assert Toolbox(0, 'h011_preflight_tools').evaluate('not-a-file.py', '')['status'] == 'budget_exhausted'
checks.append('shared20_accepted_cap')
write(control / 'research_budget.json', [14, 13, 13])
assert all('error' in box.terminal('echo must-not-run') for box in boxes)
write(control / 'research_budget.json', [0, 0, 0])
result = boxes[0].terminal("python -c 'import os; assert not os.path.exists(\"/mnt/c\"); print(len(os.sched_getaffinity(0)))'")
assert result['exit_code'] == 0 and result['output'].strip() == '2', result
assert read(control / 'research_budget.json') == [1, 0, 0]
checks += ['14_13_13_research_cap', 'actual_isolated_terminal_CPU_affinity2']
for fold in range(3):
    folder, runtime, bundle, configpath, cfg = prepare(fold)
    original = read(ROOT / f'CVBenchmark/results/medium_v2/fold_{fold}/h009/run_config.json')
    for key in ['seed', 'train_pair_sha256', 'bundle_manifest_sha256', 'train_pairs',
                'lightgbm_rounds', 'cpu_threads', 'search_users', 'confirmation_users',
                'heldout_val_users', 'automatic_raw_features', 'max_python_features', 'runtime_sha256']:
        assert cfg[key] == original[key], key
    assert not (folder / 'budget.json').exists(), 'Actual H011 experiment unexpectedly submitted programs'
    assert not list(folder.glob('api_attempts/attempt_*')), 'Actual H011 made API requests'
checks += ['all_three_original_H009_evaluator_hashes', 'same_training_pairs_and_LightGBM', 'zero_actual_H011_API_or_checks']
target = Path(__file__).with_name('h011_tools_verification.json')
write(target, {'passed': True, 'checks': checks, 'real_API_requests': 0, 'feature_trainings': 0})
print(json.dumps(read(target), ensure_ascii=False, indent=2))
