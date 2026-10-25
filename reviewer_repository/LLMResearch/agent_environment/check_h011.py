"""No-network H011 preparation checks; never call the real provider or train."""
import hashlib
import io
import json
from pathlib import Path
import threading
import time
import urllib.error
import urllib.request
from gateway import server_for, write
from setup_windows import ROOT, BASE, setup

REPORT = ROOT / 'reports/medium_h011_codex_v1'
REPORT.mkdir(parents=True, exist_ok=True)
scratch = REPORT / f'preflight_scratch/check_{time.time_ns()}'
scratch.mkdir(parents=True)
captured = []


class MockResponse:
    status = 200
    headers = {'Content-Type': 'text/event-stream'}
    def __init__(self):
        self.buffer = io.BytesIO(b'data: {"type":"response.completed","response":{"usage":{"input_tokens":1,"output_tokens":1}}}\n\n')
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.buffer.close()
    def read1(self, n):
        return self.buffer.read(n)


def mock(request, timeout):
    captured.append(json.loads(request.data))
    assert request.get_header('Authorization') == 'Bearer mock-upstream-only'
    return MockResponse()


server = server_for(scratch, 'https://never-contact.invalid/v1', 'mock-upstream-only', 'local-only', 0, opener=mock)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
url = f'http://127.0.0.1:{server.server_port}/v1/responses'
payload = {'model': 'gpt-6.1-sol', 'input': 'mock', 'stream': True,
           'temperature': 0, 'max_output_tokens': 999999, 'reasoning': {'effort': 'high'}}


def request(key='local-only'):
    return urllib.request.Request(url, data=json.dumps(payload).encode(),
               headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json',
                        'X-HM-Fold': '0', 'X-HM-Island': '1'}, method='POST')


try:
    with urllib.request.urlopen(request(), timeout=5) as response:
        body = response.read()
    assert b'response.completed' in body
    assert captured[0]['reasoning']['effort'] == 'low'
    assert captured[0]['temperature'] == .8 and captured[0]['max_output_tokens'] == 2048
    attempt = scratch / 'fold_0/api_attempts/attempt_001'
    assert (attempt / 'request.json').exists() and (attempt / 'response.raw').exists()
    assert json.loads((attempt / 'origin.json').read_text())['island'] == 1
    assert 'mock-upstream-only' not in (attempt / 'request.json').read_text()
    try:
        urllib.request.urlopen(request('wrong-key'), timeout=5)
    except urllib.error.HTTPError as error:
        assert error.code == 401
    else:
        raise AssertionError('Unauthenticated gateway accepted')
    for i in range(2, 301):
        (scratch / f'fold_0/api_attempts/attempt_{i:03d}').mkdir()
    try:
        urllib.request.urlopen(request(), timeout=5)
    except urllib.error.HTTPError as error:
        assert error.code == 429
    else:
        raise AssertionError('Gateway cap not enforced')
    assert len(captured) == 1
finally:
    server.shutdown()
    server.server_close()

retry_calls = []


def flaky(request, timeout):
    retry_calls.append(1)
    if len(retry_calls) == 1:
        raise urllib.error.URLError(TimeoutError('synthetic provider timeout'))
    return MockResponse()


retryroot = scratch / 'retry_recovery'
server = server_for(retryroot, 'https://never-contact.invalid/v1', 'mock-upstream-only',
                    'local-only', 0, opener=flaky, retry_delays=(0, 0, 0))
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}/v1/responses'
try:
    with urllib.request.urlopen(request(), timeout=5) as response:
        assert b'response.completed' in response.read()
    assert len(retry_calls) == 2
    assert (retryroot / 'fold_0/api_attempts/attempt_001/failure.json').exists()
    assert (retryroot / 'fold_0/api_attempts/attempt_001/recovered.json').exists()
    assert (retryroot / 'fold_0/api_attempts/attempt_002/transport.json').exists()
finally:
    server.shutdown()
    server.server_close()


def unavailable(request, timeout):
    raise urllib.error.URLError(TimeoutError('synthetic persistent timeout'))


retryroot = scratch / 'retry_exhaustion'
server = server_for(retryroot, 'https://never-contact.invalid/v1', 'mock-upstream-only',
                    'local-only', 0, opener=unavailable, retry_delays=(0, 0, 0))
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}/v1/responses'
try:
    try:
        urllib.request.urlopen(request(), timeout=5)
    except urllib.error.HTTPError as error:
        assert error.code == 502
    else:
        raise AssertionError('Persistent timeout should stop after bounded retries')
    assert len(list(retryroot.glob('fold_0/api_attempts/attempt_*/failure.json'))) == 4
    assert not list(retryroot.glob('fold_0/api_attempts/attempt_*/recovered.json'))
finally:
    server.shutdown()
    server.server_close()

for fold in range(3):
    for island in range(3):
        setup(fold, 'h011_codex_seed42_v1', island, 'http://127.0.0.1:18736/v1')
files = ['H011_PROTOCOL.md', 'gateway.py', 'toolbox.py', 'mcp_server.py',
         'setup_windows.py', 'pipeline_windows.py', 'h011_stage.py', 'report_h011.py']
hashes = {name: hashlib.sha256((BASE / name).read_bytes()).hexdigest() for name in files}
value = {'passed': True, 'status': 'prepared_not_started', 'real_API_requests': 0,
         'feature_trainings': 0, 'checks': ['mocked_SSE_forwarding', 'upstream_parameters_clamped',
         'no_credential_in_saved_payload', 'gateway_origin_per_population',
         'gateway_authentication', 'hard300_POST_cap', 'nine_separate_Codex_profiles',
         'timeout_retry_separately_counted_and_recovered', 'persistent_timeout_four_attempt_bound'],
         'sources_sha256': hashes, 'os_isolation_verification': 'verification.json',
         'native_agent_smoke_verification': 'native_agent_verification.json'}
write(BASE / 'h011_verification.json', value)
write(REPORT / 'prepared.json', value)
print(json.dumps(value, ensure_ascii=False, indent=2))
