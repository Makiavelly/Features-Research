"""Orchestrate independent frozen-inference folds without altering metric code."""
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import signal
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'CVFollowup'))
from common import record,read
import novelty_audit as audit

def fold_work(fold):
    for kind in ['raw15','manual','api']:
        log=audit.REP/f'fold_{fold}_{kind}.log'
        with log.open('a') as stream:
            subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/novelty_scores.py'),str(fold),kind],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True)
    return fold

def main():
    parent=int(sys.argv[1])
    cmd=Path(f'/proc/{parent}/cmdline').read_bytes()
    assert str(ROOT/'CVFollowup/novelty_audit.py').encode() in cmd
    assert b'run' in cmd
    # Parent currently waits for fold0's independent API-feature inference.
    # Keep its dispatch loop stopped until folds1/2 are finished, so it cannot
    # launch duplicate writers; its running fold0 child continues normally.
    os.kill(parent,signal.SIGSTOP)
    try:
        record('novelty_parallel_dispatch','Independent folds1/2 CPU inference scheduled in parallel (two threads per scorer); parent dispatch held to prevent duplicate writers, active fold0 worker and GPU TDM continue. No model/metric/source changes.',audit.RUN,status='scoring_parallel')
        with ThreadPoolExecutor(max_workers=2) as pool:
            tasks=[pool.submit(fold_work,f) for f in [1,2]]
            failures=[]
            for task in tasks:
                try:print('CPU_FOLD_DONE',task.result(),flush=True)
                except BaseException as error:failures.append(error)
        if failures:raise failures[0]
        record('novelty_parallel_dispatch_done','Independent CPU folds1/2 finished; parent dispatch resumes and reuses verified outputs.',audit.RUN,status='diagnosing')
    finally:
        os.kill(parent,signal.SIGCONT)

if __name__=='__main__':main()
