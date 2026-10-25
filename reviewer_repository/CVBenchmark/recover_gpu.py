"""Repair a failed GPU lane while preserving the original active API lane."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import time
from common import ROOT,REPORT,write,record

def main(original_pid,worker):
    pidfile=REPORT/'gpu_recovery.pid'
    if not worker:
        if pidfile.exists():
            try:os.kill(int(pidfile.read_text()),0)
            except ProcessLookupError:pass
            else:raise RuntimeError('GPU recovery process already alive')
        with (REPORT/'gpu_recovery.log').open('a') as stream:
            p=subprocess.Popen([sys.executable,'-u',str(Path(__file__)),str(original_pid),'--worker'],
                stdin=subprocess.DEVNULL,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True,cwd=ROOT)
        pidfile.write_text(str(p.pid));print('GPU recovery PID',p.pid,flush=True);return
    import pipeline
    try:
        record('medium_cv_gpu_recovery','Recovering GPU lane with required TDM CuBLAS deterministic setting; existing API lane kept running.',
               'hm_medium_temporal_cv_v2',status='training')
        pipeline.gpu_lane()
        while True:
            try:cmd=Path(f'/proc/{original_pid}/cmdline').read_bytes()
            except FileNotFoundError:break
            if b'CVBenchmark/pipeline.py' not in cmd:break
            time.sleep(30)
        print('Original controller ended; resuming completed-stage-aware orchestration',flush=True)
        pipeline.main()
    except BaseException as error:
        write(REPORT/'gpu_recovery_failure.json',{'error':str(error)})
        record('medium_cv_gpu_recovery_error',str(error),'hm_medium_temporal_cv_v2',status='interrupted')
        raise

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('original_pid',type=int);p.add_argument('--worker',action='store_true')
    a=p.parse_args();main(a.original_pid,a.worker)
