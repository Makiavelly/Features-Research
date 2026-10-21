"""Train-only agent tools: isolated terminal plus externally enforced evaluation budget."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / 'CVBenchmark/results/medium_v2'
BASE = Path(__file__).resolve().parent / 'sessions'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp.replace(path)


class Toolbox:
    def __init__(self, fold, session, island=None):
        if fold not in range(3) or not session.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Invalid fold/session')
        self.fold = fold
        self.session = session
        self.island = island
        self.control = BASE / session / f'fold_{fold}'
        self.root = self.control if island is None else self.control / f'island_{island}'
        self.work = self.root / 'work'
        self.work.mkdir(parents=True, exist_ok=True)
        self.data = ROOT / f'LLMResearch/results/v2/fold_{fold}/research.duckdb'
        self.bundle = ROOT / f'data/hm-cv-medium-v2/fold_{fold}/bundle'
        assert self.data.exists()
        self.manifest = read(self.data.with_name('research_manifest.json'))

    def scoped(self, value):
        if not isinstance(value, str):
            raise ValueError('path must be text')
        if value.startswith('/work/'):
            value = value[6:]
        path = (self.work / value).resolve()
        if not path.is_relative_to(self.work.resolve()):
            raise ValueError('Only files inside /work are accessible')
        return path

    def state(self):
        path = self.control / 'budget.json'
        return read(path) if path.exists() else {'accepted': [], 'attempts': [], 'target': 20}

    def terminal(self, command):
        if not isinstance(command, str) or len(command) > 24000:
            raise ValueError('command must be text, max24000characters')
        if self.island is not None:
            with (self.control / '.research.lock').open('a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                path = self.control / 'research_budget.json'
                counts = read(path) if path.exists() else [0, 0, 0]
                if counts[self.island] >= [14, 13, 13][self.island]:
                    return {'error': 'This population exhausted its terminal/research budget. Use read_file/write_file and submit features.'}
                counts[self.island] += 1
                write(path, counts)
        runtime = ROOT / 'RelBenchGNN/.venv-wsl'
        args = ['bwrap', '--unshare-all', '--die-with-parent', '--new-session',
                '--ro-bind', '/usr', '/usr', '--symlink', 'usr/lib', '/lib',
                '--symlink', 'usr/lib64', '/lib64', '--symlink', 'usr/bin', '/bin',
                '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp',
                '--dir', '/opt', '--ro-bind', str(runtime), '/opt/runtime',
                '--dir', '/data', '--ro-bind', str(self.data), '/data/research.duckdb',
                '--bind', str(self.work), '/work', '--chdir', '/work', '--clearenv',
                '--setenv', 'HOME', '/work', '--setenv', 'PATH', '/opt/runtime/bin:/usr/bin:/bin',
                '--setenv', 'OMP_NUM_THREADS', '1', '--setenv', 'OPENBLAS_NUM_THREADS', '1',
                '--setenv', 'MKL_NUM_THREADS', '1', '--setenv', 'PYTHONDONTWRITEBYTECODE', '1',
                '/bin/bash', '-c', command]
        with tempfile.TemporaryFile() as log:
            started = time.monotonic()
            try:
                def affinity():
                    os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:2])
                result = subprocess.run(args, stdin=subprocess.DEVNULL, stdout=log,
                                        stderr=subprocess.STDOUT, timeout=60, preexec_fn=affinity)
                code = result.returncode
                timeout = False
            except subprocess.TimeoutExpired:
                code, timeout = None, True
            log.seek(0)
            output = log.read(24001)
        return {'exit_code': code, 'timed_out': timeout,
                'output': output[:24000].decode(errors='replace'), 'truncated': len(output) > 24000,
                'seconds': time.monotonic() - started,
                'filesystem': '/work writable; /data/research.duckdb and runtime read-only; host project absent; network isolated'}

    def evaluate(self, path, hypothesis):
        """Only this host-side tool can expose validation feedback or spend a check."""
        with (self.control / '.evaluation.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            state = self.state()
            if self.island is not None:
                allowance = read(self.root / 'turn_allowance.json')
                added = state['attempts'][allowance['starting_attempts']:]
                if len(added) >= 4 or any(a['status'] == 'accepted' for a in added):
                    return {'status': 'turn_budget_exhausted', 'message': 'Stop this turn now: one accepted program or four submissions reached. Parent rotates populations.'}
                assert allowance['island'] == self.island
                events = self.root / 'tool_events.jsonl'
                own_research = [json.loads(s) for s in events.read_text(encoding='utf-8').splitlines()] if events.exists() else []
                if not any(e['tool'] == 'terminal' and e['result'].get('exit_code') == 0 for e in own_research):
                    return {'status': 'research_required', 'message': 'Run at least one successful train-statistics terminal command of your choice first.'}
            if len(state['accepted']) >= 20:
                return {'status': 'budget_exhausted', 'accepted': 20, 'remaining': 0,
                        'message': 'All20 successful checks used. Stop and report; no extra evaluation allowed.'}
            if len(state['attempts']) >= 100:
                return {'status': 'attempt_cap', 'message': '100 submitted programs exhausted; no extra checks allowed'}
            code = self.scoped(path).read_text(encoding='utf-8')
            runtime = OLD / f'fold_{self.fold}/runtime/api'
            sys.path.insert(0, str(runtime))
            import runtime as api
            from python_features import parse, program_key
            number = len(state['attempts']) + 1
            output = self.control / f'evaluations/candidate_{number:03d}'
            output.mkdir(parents=True, exist_ok=True)
            attempt = {'call': number, 'island': self.island, 'hypothesis': hypothesis, 'code_sha256': hashlib.sha256(code.encode()).hexdigest()}
            try:
                program = parse(code)
                key = program_key(program)
                if any(a['program_key'] == key for a in state['accepted']):
                    attempt.update(status='duplicate')
                    state['attempts'].append(attempt)
                    write(self.control / 'budget.json', state)
                    return {'status': 'duplicate', 'accepted': len(state['accepted']), 'remaining': 20 - len(state['accepted'])}
                config = read(OLD / f'fold_{self.fold}/h009/run_config.json')
                config.update(protocol=f'codex_agent_{self.session}_fold{self.fold}',
                              test_previously_inspected=True,
                              standalone_agent_environment=True)
                configpath = self.control / 'evaluator_config.json'
                if not configpath.exists():
                    write(configpath, config)
                write(output / 'program.json', program)
                (output / 'program.py').write_text(program['code'], encoding='utf-8')
                api.evaluate(self.bundle, output, 'preflight', configpath)
                result = api.evaluate(self.bundle, output, 'search', configpath)
                attempt.update(status='accepted', program_key=key, search_map=result['map'],
                               directory=str(output))
                state['accepted'].append(attempt)
            except Exception as error:
                attempt.update(status='rejected', error=str(error)[-2000:])
            state['attempts'].append(attempt)
            write(self.control / 'budget.json', state)
            sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
            from tracking import record
            record('standalone_agent_feature_check',
                   f'Codex agent {self.session} fold{self.fold}: {attempt["status"]}; {len(state["accepted"])}/20 accepted checks.',
                   f'codex_agent_{self.session}_fold{self.fold}',
                   status='searching', accepted=len(state['accepted']), submissions=len(state['attempts']),
                   hypothesis=hypothesis, artifacts=str(self.root.relative_to(ROOT)))
            return {**{k: v for k, v in attempt.items() if k not in ['directory']},
                    'accepted': len(state['accepted']), 'remaining': 20 - len(state['accepted'])}

    def call(self, name, args):
        if name == 'status':
            state = self.state()
            return {'fold': self.fold, 'accepted': len(state['accepted']), 'remaining': 20 - len(state['accepted']),
                    'tables': self.manifest['tables'], 'training_cutoffs': self.manifest['history_cutoffs'],
                    'paths': {'work': '/work', 'train_database': '/data/research.duckdb'},
                    'best_search_map': max([a['search_map'] for a in state['accepted'] if a.get('island') == self.island], default=None),
                    'validation_labels_available': False, 'test_available': False}
        if name == 'terminal':
            return self.terminal(args['command'])
        if name == 'read_file':
            text = self.scoped(args['path']).read_text(encoding='utf-8')
            return {'text': text[:24000], 'truncated': len(text) > 24000}
        if name == 'write_file':
            if len(args['content']) > 24000:
                raise ValueError('Maximum24000characters')
            path = self.scoped(args['path'])
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(args['content'], encoding='utf-8')
            return {'written': True}
        if name == 'evaluate_features':
            return self.evaluate(args['path'], args.get('hypothesis', ''))
        raise ValueError('Unknown tool')


TOOLS = [
    {'name': 'status', 'description': 'Current fold training schema, time cutoffs and externally enforced20-program budget. No heldout/test access.', 'inputSchema': {'type': 'object', 'properties': {}}},
    {'name': 'terminal', 'description': 'Run bash/Python in an OS-isolated train-only workspace. pandas, NumPy, DuckDB available; no network, no host project.60second limit. Use for statistics and files, not fitting models; all model checks go through evaluate_features.', 'inputSchema': {'type': 'object', 'properties': {'command': {'type': 'string'}}, 'required': ['command']}},
    {'name': 'read_file', 'description': 'Read a UTF-8 file under your own /work only.', 'inputSchema': {'type': 'object', 'properties': {'path': {'type': 'string'}}, 'required': ['path']}},
    {'name': 'write_file', 'description': 'Write a file or notes under your own /work only.', 'inputSchema': {'type': 'object', 'properties': {'path': {'type': 'string'}, 'content': {'type': 'string'}}, 'required': ['path', 'content']}},
    {'name': 'evaluate_features', 'description': 'Submit a Python file defining modify_features(X,history). Original H009 validator, same train pairs and LightGBM, only search MAP feedback. Successful distinct checks spend one of20; validation/test labels and outer metrics never returned. Do not train models inside terminal.', 'inputSchema': {'type': 'object', 'properties': {'path': {'type': 'string'}, 'hypothesis': {'type': 'string'}}, 'required': ['path', 'hypothesis']}},
]
