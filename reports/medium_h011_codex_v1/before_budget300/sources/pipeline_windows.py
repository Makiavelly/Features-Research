"""Actual autonomous Codex experiment: round-robin agents, cap, freeze and replay."""
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import threading
import time
from gateway import server_for, write
from setup_windows import ROOT, BASE, setup, wsl

SESSION = 'h011_codex_seed42_v1'
OUT = BASE / 'sessions' / SESSION
REPORT = ROOT / 'reports/medium_h011_codex_v1'
PORT = 18736


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def stage(name, fold=0, message=''):
    command = ['wsl.exe', '--exec', wsl(ROOT / 'RelBenchGNN/.venv-wsl/bin/python'),
               '-u', wsl(BASE / 'h011_stage.py'), name, '--fold', str(fold)]
    if message:
        command += ['--message', message]
    subprocess.run(command, check=True, cwd=ROOT)


def start_turn(fold, island, local_key):
    folder, work, home = setup(fold, SESSION, island, f'http://127.0.0.1:{PORT}/v1')
    budgetpath = OUT / f'fold_{fold}/budget.json'
    state = read(budgetpath) if budgetpath.exists() else {'attempts': [], 'accepted': []}
    write(folder / 'turn_allowance.json', {'island': island, 'starting_attempts': len(state['attempts'])})
    own = [a for a in state['accepted'] if a['island'] == island]
    best = max(own, key=lambda a: a['search_map']) if own else None
    prompt = f'''Autonomous H011 experiment, fold{fold}, population{island}. Work without asking the human.
You see only your own training-fold workspace and your own previous conversation.
Use MCP fold tools. Read FEATURE_INTERFACE.md using fold.read_file if not already known.
Research train data with Python/DuckDB in fold.terminal; choose your own questions and
write hypotheses/evidence into WORK_LOG.md. Do not fit models in terminal or access any
outside data. Research terminal budget is14/13/13 per population across the entire fold,
not per turn. Use read_file/write_file for ordinary documents to conserve research calls.
Join train_history.cutoff=train_pairs.timestamp for relationships to labels; sampled
negative pairs bias rates. Validation and test targets are unavailable.

THIS TURN: submit one new complete feature set through fold.evaluate_features.
If rejected/duplicate, correct it, at most4 submissions total (one proposal+3repairs).
After ONE accepted submission, stop this turn immediately and report its hypothesis.
If4 submissions fail, stop and report errors; the controller rotates populations.
The host enforces this quota and a shared20 accepted-program fold budget. Your own
best search MAP fraction is {best['search_map'] if best else None}; no other population's
solutions are supplied. {20-len(state['accepted'])} accepted checks remain globally.
You may inspect/improve your own files from earlier turns; do not read other workspaces.
Do not spend further tools after quota exhaustion, do not request test/confirmation.
The parent controller performs final selection/evaluation after all folds are frozen.
'''
    threadpath = folder / 'thread_id.txt'
    command = [shutil.which('codex') or read(BASE / 'tool_paths.json')['codex'], 'exec']
    if threadpath.exists():
        command += ['resume', '--json', '--skip-git-repo-check', threadpath.read_text().strip()]
    else:
        command += ['--json', '--color', 'never', '--skip-git-repo-check', '-C', str(work)]
    index = len(list((folder / 'turns').glob('turn_*.jsonl'))) + 1
    turn = folder / f'turns/turn_{index:03d}.jsonl'
    turn.parent.mkdir(parents=True, exist_ok=True)
    last = folder / f'turns/turn_{index:03d}_last.txt'
    command += ['-c', 'model_providers.hm_fold_api.stream_idle_timeout_ms=1200000', '-o', str(last), '-']
    env = dict(os.environ)
    env['CODEX_HOME'] = str(home)
    env['HM_AGENT_ACCESS_TOKEN'] = local_key
    with turn.open('wb') as log:
        child = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=log, stderr=log,
                                 env=env, cwd=work, creationflags=subprocess.CREATE_NO_WINDOW)
        child.stdin.write(prompt.encode('utf-8'))
        child.stdin.close()
        write(folder / 'active_turn.json', {'pid': child.pid, 'island': island, 'turn': index})
        try:
            code = child.wait(timeout=1800)
        except subprocess.TimeoutExpired:
            child.terminate()
            raise RuntimeError('Agent turn exceeded30minutes; inspect durable tool/API state')
    events = [json.loads(line) for line in turn.read_text(encoding='utf-8', errors='replace').splitlines() if line.startswith('{')]
    threads = [e['thread_id'] for e in events if e.get('type') == 'thread.started']
    if threads:
        if threadpath.exists():
            assert threadpath.read_text().strip() == threads[0], 'Resume unexpectedly changed population thread'
        else:
            threadpath.write_text(threads[0])
    assert code == 0, f'Codex turn failed code{code}; inspect{turn}'
    assert any(e.get('type') == 'turn.completed' for e in events), 'No completed native Codex turn'
    failures = [p for p in (OUT / f'fold_{fold}/api_attempts').glob('attempt_*/failure.json')
                if not (p.parent / 'recovered.json').exists()]
    assert not failures, 'Provider/gateway failure saved; inspect before any explicit resume'
    return read(budgetpath) if budgetpath.exists() else state


def main():
    REPORT.mkdir(parents=True, exist_ok=True)
    assert read(BASE / 'verification.json')['passed']
    assert read(BASE / 'h011_verification.json')['passed']
    assert read(BASE / 'h011_tools_verification.json')['passed']
    stage('check_idle')
    original = read(ROOT / 'CVBenchmark/results/medium_v2/fold_0/h009/run_config.json')
    token = None
    for line in (ROOT / '.env').read_text(encoding='utf-8-sig').splitlines():
        if '=' in line and line.split('=', 1)[0].strip() == 'ACCESS_TOKEN':
            token = line.split('=', 1)[1].strip().strip('"').strip("'")
    assert token
    local_key = secrets.token_urlsafe(24)
    server = server_for(OUT, original['base_url'], token, local_key, PORT)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    (REPORT / 'pipeline.pid').write_text(str(os.getpid()))
    try:
        stage('record_start')
        for fold in range(3):
            stage('prepare', fold)
            statepath = OUT / f'fold_{fold}/budget.json'
            state = read(statepath) if statepath.exists() else {'attempts': [], 'accepted': []}
            next_turn_path = OUT / f'fold_{fold}/next_turn.json'
            next_turn = read(next_turn_path)['next_turn'] if next_turn_path.exists() else 0
            while len(state['accepted']) < 20:
                island = next_turn % 3
                write(REPORT / 'pipeline_status.json', {'status': 'searching', 'fold': fold, 'island': island,
                      'accepted': len(state['accepted']), 'turn': next_turn})
                print('H011', fold, island, 'accepted', len(state['accepted']), '/20', flush=True)
                state = start_turn(fold, island, local_key)
                next_turn += 1
                write(next_turn_path, {'next_turn': next_turn})
                assert len(state['attempts']) < 100 or len(state['accepted']) == 20
            stage('select', fold)
        stage('freeze')
        for fold in range(3):
            write(REPORT / 'pipeline_status.json', {'status': 'evaluating', 'fold': fold})
            stage('evaluate', fold)
        subprocess.run(['wsl.exe', '--exec', wsl(ROOT / 'RelBenchGNN/.venv-wsl/bin/python'),
                        '-u', wsl(BASE / 'report_h011.py')], check=True, cwd=ROOT)
        write(REPORT / 'pipeline_status.json', {'status': 'report_pending_visual_review'})
    except BaseException as error:
        write(REPORT / 'pipeline_status.json', {'status': 'interrupted', 'error': str(error)[:1600]})
        stage('record_stop', message=str(error)[:1600])
        raise
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    main()
