"""Manual launch gate: preparation alone never starts the experiment."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from setup_windows import ROOT, BASE


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', action='store_true', help='Explicitly start the previously prepared H011 experiment')
    args = parser.parse_args()
    verification = json.loads((BASE / 'h011_verification.json').read_text(encoding='utf-8'))
    assert verification['passed']
    for name, digest in verification['sources_sha256'].items():
        assert hashlib.sha256((BASE / name).read_bytes()).hexdigest() == digest, f'Prepared source changed:{name}; recheck before launch'
    for name, digest in verification.get('profile_sha256', {}).items():
        path = BASE / 'sessions/h011_codex_seed42_v1' / name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, f'Prepared agent profile changed:{name}'
    if not args.start:
        print('H011 is prepared, NOT started. Later use this command with --start. The controller also refuses to run while another project experiment is alive.')
        return
    report = ROOT / 'reports/medium_h011_codex_v1'
    report.mkdir(parents=True, exist_ok=True)
    with (report / 'pipeline.log').open('ab') as log:
        child = subprocess.Popen([sys.executable, '-u', str(BASE / 'pipeline_windows.py')],
                    cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                    creationflags=subprocess.CREATE_NO_WINDOW)
    print('H011 controller spawned PID', child.pid, '; check pipeline.log/status for admission and progress.')


if __name__ == '__main__':
    main()
