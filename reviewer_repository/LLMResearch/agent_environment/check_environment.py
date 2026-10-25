"""Check actual OS isolation and MCP mechanics without calling a model."""
import json
from pathlib import Path
import subprocess
import sys
from toolbox import Toolbox, write


box = Toolbox(0, 'diagnostic')
code = '''import os, socket
import pandas as pd, numpy as np, duckdb
assert not os.path.exists('/mnt/c')
assert not os.path.exists('/home')
assert not os.environ.get('ACCESS_TOKEN')
con=duckdb.connect('/data/research.duckdb',read_only=True)
assert set(con.sql('SHOW TABLES').df()['name'])=={'train_pairs','train_history','history'}
print('train_pairs',con.sql('SELECT count(*) FROM train_pairs').fetchone()[0])
try:
    con.execute('CREATE TABLE forbidden AS SELECT 1')
except Exception:
    print('database read-only OK')
else:
    raise AssertionError('Database writable')
try:
    socket.create_connection(('1.1.1.1',443),timeout=1)
except OSError:
    print('network isolated OK')
else:
    raise AssertionError('Unexpected network access')
print('pandas',pd.__version__,'numpy',np.__version__)
'''
box.call('write_file', {'path': 'check.py', 'content': code})
result = box.terminal('python check.py')
assert result['exit_code'] == 0, result
for value in ['../../CONTEXT.md', '/etc/passwd']:
    try:
        box.scoped(value)
    except ValueError:
        pass
    else:
        raise AssertionError('Escaping path accepted')
messages = [
    {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05'}},
    {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
    {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'},
    {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {'name': 'status', 'arguments': {}}},
]
completed = subprocess.run([sys.executable, str(Path(__file__).with_name('mcp_server.py')), '--fold', '0', '--session', 'diagnostic'],
            input=''.join(json.dumps(m) + '\n' for m in messages), text=True, capture_output=True, check=True, timeout=20)
responses = [json.loads(line) for line in completed.stdout.splitlines()]
assert len(responses) == 3 and len(responses[1]['result']['tools']) == 5
assert json.loads(responses[2]['result']['content'][0]['text'])['remaining'] == 20
assert not box.state()['accepted']
verification = {'passed': True, 'os_isolation_verified': True, 'no_host_project': True,
                'network_disabled_in_terminal': True, 'train_database_read_only': True,
                'MCP_initialize_list_call': True, 'real_model_calls': 0, 'feature_evaluations': 0,
                'terminal_check': result}
write(Path(__file__).with_name('verification.json'), verification)
print(json.dumps(verification, ensure_ascii=False, indent=2))
