"""Keep a local WSL process alive after the interactive tool call returns."""
import os
import subprocess
import sys
from common import ROOT,REPORT

REPORT.mkdir(parents=True,exist_ok=True)
pidfile=REPORT/'pipeline.pid'
if pidfile.exists():
    pid=int(pidfile.read_text())
    try:os.kill(pid,0)
    except ProcessLookupError:pass
    else:raise RuntimeError(f'Existing pipeline PID{pid}; inspect before another launch')
with (REPORT/'pipeline.log').open('a') as log:
    child=subprocess.Popen([sys.executable,'-u',str(ROOT/'CVBenchmark/pipeline.py')],
        stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,cwd=ROOT)
pidfile.write_text(str(child.pid))
print('Pipeline PID',child.pid,flush=True)
