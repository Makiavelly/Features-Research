"""Recording local Responses proxy with an immutable per-fold300-POST cap."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import time
import urllib.error
import urllib.request


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)


def server_for(root, provider, token, local_key, port=18736, opener=None, retry_delays=(5, 15, 30)):
    lock = threading.Lock()
    upstream = opener or urllib.request.urlopen
    root = Path(root)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def fail(self, status, message):
            raw = json.dumps({'error': {'message': message, 'type': 'agent_gateway'}}).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self):
            if self.path.endswith('/models'):
                raw = json.dumps({'object': 'list', 'data': [{'id': 'gpt-6.1-sol', 'object': 'model', 'owned_by': 'configured-provider'}]}).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
            else:
                self.fail(404, 'Only model listing and Responses are supported')

        def do_POST(self):
            if self.headers.get('Authorization') != 'Bearer ' + local_key:
                return self.fail(401, 'Invalid local agent credential')
            if self.path != '/v1/responses':
                return self.fail(400, 'Only /v1/responses is available; no compaction or external tools')
            try:
                fold, island = int(self.headers['X-HM-Fold']), int(self.headers['X-HM-Island'])
                assert fold in range(3) and island in range(3)
                length = int(self.headers.get('Content-Length', 0))
                assert 0 < length <= 8_000_000
                payload = json.loads(self.rfile.read(length))
                assert payload.get('model') == 'gpt-6.1-sol'
                # Native Codex tool definitions are retained; clamp only frozen
                # experimental model parameters. These are actual upstream logs.
                payload['reasoning'] = {**payload.get('reasoning', {}), 'effort': 'low'}
                payload['temperature'] = .8
                payload['max_output_tokens'] = 2048
                request = urllib.request.Request(provider.rstrip('/') + '/responses',
                    data=json.dumps(payload, ensure_ascii=False).encode(),
                    headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json',
                             'Accept': 'text/event-stream' if payload.get('stream') else 'application/json',
                             'User-Agent': 'HM-H011-Codex/1.0'}, method='POST')
                recovered = []
                for retry in range(len(retry_delays) + 1):
                    with lock:
                        attempts = root / f'fold_{fold}/api_attempts'
                        attempts.mkdir(parents=True, exist_ok=True)
                        number = len(list(attempts.glob('attempt_*'))) + 1
                        if number > 300:
                            return self.fail(429, 'Frozen300-POST fold budget exhausted')
                        folder = attempts / f'attempt_{number:03d}'
                        folder.mkdir()
                        write(folder / 'request.json', payload)
                        write(folder / 'origin.json', {'fold': fold, 'island': island, 'number': number,
                              'connection_retry': retry, 'prior_failed_attempts': recovered})
                    started = time.monotonic()
                    try:
                        response = upstream(request, timeout=240)
                        break
                    except Exception as error:
                        status = getattr(error, 'code', None)
                        detail = str(error).replace(token, '[REDACTED]')
                        transient = status in (429, 500, 502, 503, 504) or (
                            status is None and isinstance(error, (urllib.error.URLError, TimeoutError, ConnectionError)))
                        write(folder / 'failure.json', {'http_status': status, 'error': detail,
                              'phase': 'before_response_headers', 'seconds': time.monotonic() - started})
                        if not transient or retry == len(retry_delays):
                            raise
                        recovered.append(number)
                        write(folder / 'retry_scheduled.json', {'delay_seconds': retry_delays[retry],
                              'reason': 'Transient connection/HTTP failure before any response was forwarded; every POST consumes fold cap'})
                        time.sleep(retry_delays[retry])
                with response:
                    self.send_response(response.status)
                    self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    with (folder / 'response.raw').open('wb') as log:
                        while True:
                            block = response.read1(8192)
                            if not block:
                                break
                            log.write(block)
                            log.flush()
                            self.wfile.write(block)
                            self.wfile.flush()
                write(folder / 'transport.json', {'status': 'complete', 'seconds': time.monotonic() - started})
                for old in recovered:
                    write(attempts / f'attempt_{old:03d}/recovered.json', {'successful_transport_attempt': number})
            except urllib.error.HTTPError as error:
                detail = error.read().decode(errors='replace').replace(token, '[REDACTED]')[:1800]
                if 'folder' in locals():
                    write(folder / 'failure.json', {'http_status': error.code, 'error': detail})
                self.fail(error.code, detail)
            except Exception as error:
                detail = str(error).replace(token, '[REDACTED]')
                if 'folder' in locals():
                    write(folder / 'failure.json', {'error': detail})
                try:
                    self.fail(502, detail)
                except OSError:
                    pass

    return ThreadingHTTPServer(('127.0.0.1', port), Handler)
