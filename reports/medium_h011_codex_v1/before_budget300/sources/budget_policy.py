"""Research allowance is read outside the agent-writable workspace."""
import json
from pathlib import Path


def research_policy(session):
    path = Path(__file__).resolve().parent / 'sessions' / session / 'research_policy.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {
        'research_caps': [14, 13, 13], 'research_total': 40}


def research_caps(session):
    policy = research_policy(session)
    caps = policy['research_caps']
    assert len(caps) == 3 and all(isinstance(n, int) and n > 0 for n in caps)
    assert sum(caps) == policy['research_total']
    return caps
