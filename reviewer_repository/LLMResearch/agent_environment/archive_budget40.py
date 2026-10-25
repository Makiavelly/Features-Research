"""Preserve the completed-turn state before the user-requested budget revision."""
import shutil
from pathlib import Path
from toolbox import ROOT, read, write

source = Path(__file__).resolve().parent
session = source / 'sessions/h011_codex_seed42_v1'
target = ROOT / 'reports/medium_h011_codex_v1/before_budget300'
assert not (target / 'snapshot.json').exists(), 'Original budget40 snapshot already exists; do not overwrite'
state = read(session / 'fold_0/budget.json')
turn = read(session / 'fold_0/next_turn.json')
assert turn['next_turn'] == len(state['accepted'])
target.mkdir(exist_ok=True)
shutil.copytree(session, target / 'session', dirs_exist_ok=True, symlinks=True,
                ignore=shutil.ignore_patterns('skills', '.tmp', 'tmp'))
(target / 'sources').mkdir(exist_ok=True)
for path in source.glob('*.py'):
    shutil.copy2(path, target / 'sources' / path.name)
shutil.copy2(source / 'H011_PROTOCOL.md', target / 'H011_PROTOCOL.md')
shutil.copy2(source / 'h011_verification.json', target / 'h011_verification.json')
for config in session.glob('fold_0/island_*/codex_home/config.toml'):
    text = config.read_text(encoding='utf-8')
    marker = '# Budget revision requested: stop at next completed-turn boundary.'
    assert marker in text
    config.write_text(text[:text.index(marker)].rstrip('\r\n') + '\n', encoding='utf-8')
write(target / 'snapshot.json', {'accepted': len(state['accepted']), 'next_turn': turn['next_turn'],
      'research_spent': read(session / 'fold_0/research_budget.json'),
      'actual_POST': len(list((session / 'fold_0/api_attempts').glob('attempt_*'))),
      'reason': 'User increased research budget40 to300/fold; stopped after completed native turn, no results discarded'})
print(read(target / 'snapshot.json'))
