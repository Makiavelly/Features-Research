"""Launch isolated Codex configuration using existing API credentials in memory."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from setup_windows import ROOT, BASE, setup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fold', type=int, default=0)
    parser.add_argument('--session', default='standalone_v2')
    parser.add_argument('--interactive', action='store_true')
    parser.add_argument('--smoke', action='store_true')
    parser.add_argument('--prompt-file')
    args = parser.parse_args()
    assert json.loads((BASE / 'verification.json').read_text())['passed']
    folder, work, home = setup(args.fold, args.session)
    env = dict(os.environ)
    token = None
    for line in (ROOT / '.env').read_text(encoding='utf-8-sig').splitlines():
        if '=' in line and line.split('=', 1)[0].strip() == 'ACCESS_TOKEN':
            token = line.split('=', 1)[1].strip().strip('"').strip("'")
    assert token, 'Existing provider token missing'
    env['HM_AGENT_ACCESS_TOKEN'] = token
    env['CODEX_HOME'] = str(home)
    binary = shutil.which('codex')
    assert binary, 'Existing Codex CLI not found'
    command = [binary]
    if args.interactive:
        command += ['-C', str(work)]
        raise SystemExit(subprocess.call(command, env=env))
    prompt = ('This is only an environment smoke check, NOT an experiment. '
              'Use fold.status. Then use fold.terminal to run Python, import pandas/numpy/duckdb, '
              'open /data/research.duckdb read-only and count train_pairs. '
              'Verify /mnt/c is absent. Do not call evaluate_features, do not train anything, '
              'do not use network. Report the observed row count and isolation briefly in Russian.'
              if args.smoke else None)
    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding='utf-8')
    if not prompt:
        raise SystemExit('Choose --interactive, --smoke or --prompt-file; no experiment starts implicitly')
    command += ['exec', '--skip-git-repo-check', '--json', '--color', 'never',
                '-C', str(work), '-o', str(folder / 'last_message.txt'), '-']
    with (folder / 'codex_events.jsonl').open('ab') as log:
        child = subprocess.Popen(command, env=env, stdin=subprocess.PIPE,
                                 stdout=log, stderr=log, creationflags=subprocess.CREATE_NO_WINDOW)
        child.stdin.write(prompt.encode('utf-8'))
        child.stdin.close()
        (folder / 'codex.pid').write_text(str(child.pid))
        print('Standalone GPT-6.1 Sol Codex PID', child.pid, flush=True)
        result = child.wait()
    # Never include env/auth in logs or error diagnostics.
    if result:
        raise SystemExit(result)


if __name__ == '__main__':
    main()
