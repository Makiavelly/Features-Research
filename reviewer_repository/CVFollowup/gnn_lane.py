"""Correct GNN validation selection on every fold before outer evaluation."""
import argparse
import fcntl
import subprocess
import sys
from pathlib import Path
from common import ROOT,OUT,REPORT,read,write,sha,record

def main(worker=False):
    REPORT.mkdir(parents=True,exist_ok=True)
    if not worker:
        pidfile=REPORT/'gpu_followup.pid'
        if pidfile.exists():
            try:cmd=Path(f'/proc/{int(pidfile.read_text())}/cmdline').read_bytes()
            except FileNotFoundError:pass
            else:
                if b'gnn_lane.py' in cmd:raise RuntimeError('GPU followup already running')
        with (REPORT/'gpu_followup.log').open('a') as log:
            p=subprocess.Popen([sys.executable,'-u',__file__,'--worker'],cwd=ROOT,
                stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        pidfile.write_text(str(p.pid));print('GPU FOLLOWUP PID',p.pid,flush=True);return
    try:
        assert read(REPORT/'graph_time_fix_verification.json')['passed']
        # Let any already running diagnostic finish before checking its cache.
        locks=OUT/'locks';locks.mkdir(parents=True,exist_ok=True)
        with (locks/'gpu.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
        for stage,folds in [('existing',[0]),('train',range(3)),('evaluate',range(3))]:
            if stage=='evaluate':
                checkpoints={str(p.relative_to(ROOT)):sha(p) for p in OUT.glob('fold_*/gnn_timefix_refit/*/best.pt')}
                assert len(checkpoints)==6
                frozen=REPORT/'gnn_timefix_pretest_freeze.json'
                if frozen.exists():assert read(frozen)['checkpoints']==checkpoints
                else:write(frozen,{'checkpoints':checkpoints,'selection':'unchanged inner validation rule, corrected timestamp units','test_used_for_selection':False})
            for fold in folds:
                write(REPORT/'gnn_lane_status.json',{'stage':stage,'fold':fold})
                with (REPORT/f'gnn_timefix_f{fold}_{stage}.log').open('a') as log:
                    subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/gnn_timefix.py'),str(fold),stage],
                        cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
        write(REPORT/'gnn_lane_status.json',{'stage':'verified'})
        record('followup_gnn_corrected','All six corrected GNN fits selected on inner validation, frozen, evaluated and replayed.',
            'hm_medium_gnn_timefix_v1',status='evaluated_pending_report')
        subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/recformer_lane.py'),'--worker'],cwd=ROOT,check=True)
    except BaseException as error:
        write(REPORT/'gpu_followup_failure.json',{'error':str(error)})
        record('followup_gpu_interrupted',str(error),'hm_medium_gpu_followup_v1',status='interrupted')
        raise

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--worker',action='store_true');main(p.parse_args().worker)
