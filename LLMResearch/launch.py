"""Launch exactly one detached H010 controller in WSL."""
import os
import subprocess
import sys
from pathlib import Path
from common import ROOT, SOURCE, REPORT, read

REPORT.mkdir(parents=True, exist_ok=True)
assert read(REPORT / 'verification.json')['passed']
pidpath = REPORT / 'pipeline.pid'
if pidpath.exists():
    pid = int(pidpath.read_text())
    try:
        command = Path(f'/proc/{pid}/cmdline').read_bytes()
    except FileNotFoundError:
        pass
    else:
        if b'LLMResearch/pipeline.py' in command:
            raise RuntimeError(f'H010 pipeline already running PID{pid}')
with (REPORT / 'pipeline.log').open('a') as log:
    child = subprocess.Popen([sys.executable, '-u', str(SOURCE / 'pipeline.py')],
               cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
               start_new_session=True)
pidpath.write_text(str(child.pid))
print('H010 pipeline PID', child.pid, flush=True)
