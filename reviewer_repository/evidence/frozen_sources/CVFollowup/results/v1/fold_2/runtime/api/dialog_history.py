"""Reconstruct exact per-island Chat Completions turns from immutable run files."""
import json
from pathlib import Path

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def completed_trials(config, out, number):
    folders = Path(out) / config['arm'] / 'candidates'
    trials = [read(path) for path in sorted(folders.glob('candidate_*/trial.json'))]
    trials = [t for t in trials if t['call'] < number]
    assert [t['call'] for t in trials] == list(range(1, number)), 'Missing completed trial in history'
    return trials

def next_island(config, trials):
    if not trials:
        return 0
    last = trials[-1]
    stop = (last['status'] == 'valid' or last['repair'] >= config['max_repairs_per_proposal']
            or last.get('unchanged_repair', False))
    proposal = last['proposal'] + int(stop)
    return proposal % config['islands']

def feedback(trial):
    result = {k: trial[k] for k in ['call', 'island', 'proposal', 'repair', 'status']}
    if trial['status'] == 'valid':
        result['search_map_fraction'] = trial['score']
    else:
        result['failure_stage'] = trial.get('failure_stage')
        result['error'] = trial['error']
    return 'EVALUATION_FEEDBACK_FOR_PREVIOUS_RESPONSE:\n' + json.dumps(result, ensure_ascii=False, sort_keys=True) + '\n\n'

def build_messages(config, out, prompt, seed):
    out = Path(out)
    number = seed - config['seed'] + 1
    assert number >= 1
    trials = completed_trials(config, out, number)
    island = next_island(config, trials)
    own = [t for t in trials if t['island'] == island]
    messages = [{'role': 'system', 'content': config['system_message']}]
    for trial in own:
        folder = out / config['arm'] / 'candidates' / f"candidate_{trial['call']:03d}"
        response = read(folder / 'response.json')
        request = read(out / 'api_attempts' / f"attempt_{response['api_attempt']:03d}" / 'request.json')
        previous_user = request['messages'][-1]
        assert previous_user['role'] == 'user'
        messages.append(previous_user)
        messages.append({'role': 'assistant', 'content': response['text']})
    content = (feedback(own[-1]) if own else '') + prompt
    messages.append({'role': 'user', 'content': content})
    assert [m['role'] for m in messages] == ['system'] + ['user', 'assistant']*len(own) + ['user']
    assert len(messages) == 2*len(own)+2
    return messages
