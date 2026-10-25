"""Read-only search-budget diagnostic; no candidate reselection or fitting."""
import json
from pathlib import Path
from h011_stage import OUT, REPORT, RUN, read, write, record
from report_h011 import response_usage

rows = []
for fold in range(3):
    folder = OUT / f'fold_{fold}'
    state = read(folder / 'budget.json')
    selected = read(folder / 'selected.json')
    usage = []
    incomplete = 0
    for attempt in sorted((folder / 'api_attempts').glob('attempt_*')):
        item, _ = response_usage(attempt / 'response.raw') if (attempt / 'response.raw').exists() else (None, None)
        if item:
            usage.append(item)
        else:
            incomplete += 1
    events = [json.loads(line) for path in folder.glob('island_*/tool_events.jsonl')
              for line in path.read_text(encoding='utf-8').splitlines()]
    denied = [e for e in events if 'exhausted its terminal/research budget' in json.dumps(e)]
    ranked = sorted(state['accepted'], key=lambda a: -a['search_map'])
    row = {'fold': fold, 'accepted': len(state['accepted']),
           'research_calls': read(folder / 'research_budget.json'), 'research_denials': len(denied),
           'API_attempts': len(list((folder / 'api_attempts').glob('attempt_*'))),
           'known_input_tokens': sum(u.get('input_tokens', 0) for u in usage),
           'known_output_tokens': sum(u.get('output_tokens', 0) for u in usage),
           'known_cached_input_tokens': sum(u.get('input_tokens_details', {}).get('cached_tokens', 0) for u in usage),
           'attempts_without_completed_usage': incomplete,
           'selected_call': selected['call'], 'confirmation': selected['confirmation'],
           'top3_search': [{'call': a['call'], 'search_map': a['search_map']} for a in ranked[:3]]}
    for split in ['heldout_val', 'val', 'test']:
        path = folder / f'{split}_metrics.json'
        if path.exists():
            row[split + '_map'] = read(path)['map']
    rows.append(row)
write(REPORT / 'search_budget_diagnostic.json', rows)
record('h011_search_budget_diagnostic',
       'Read-only audit of research denials, provider token usage, search and confirmation selection requested after low fold0 test. No fitting, reselection or budget changes.',
       RUN + '_search_budget_diagnostic', status='verified',
       artifacts=str((REPORT / 'search_budget_diagnostic.json').relative_to(REPORT.parents[1])))
print(json.dumps(rows, ensure_ascii=False, indent=2))
