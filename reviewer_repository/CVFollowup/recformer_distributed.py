"""Train local assignments and wait for validated Kaggle imports before selection."""
import argparse
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from common import ROOT,OUT,REPORT,read,write,sha,record

PLAN={'local':['lr1e6_w100','lr3e6_w300'],
      'kaggle_1':['lr3e6_w100'],'kaggle_2':['lr1e5_w300']}

def alive(pid,needle):
    try:return needle.encode() in Path(f'/proc/{pid}/cmdline').read_bytes()
    except FileNotFoundError:return False

def main(worker=False):
    REPORT.mkdir(parents=True,exist_ok=True)
    if not worker:
        pidfile=REPORT/'recformer_distributed.pid'
        if pidfile.exists() and alive(int(pidfile.read_text()),'recformer_distributed.py'):raise RuntimeError('Distributed controller active')
        old=REPORT/'recformer_lane.pid'
        if old.exists():
            pid=int(old.read_text())
            if alive(pid,'CVFollowup/recformer_lane.py'):
                # Terminate only scheduler. Its in-flight child training survives.
                os.kill(pid,signal.SIGTERM)
        active=[]
        for proc in Path('/proc').iterdir():
            if proc.name.isdigit():
                try:command=(proc/'cmdline').read_bytes().decode(errors='replace')
                except (FileNotFoundError,ProcessLookupError,PermissionError):continue
                if 'CVFollowup/recformer_grid.py' in command and '\x00train' in command:
                    active.append({'pid':int(proc.name),'command':command})
        file=REPORT/'recformer_distributed_plan.json'
        if file.exists():assert read(file)['assignments']==PLAN
        else:write(file,{'assignments':PLAN,'existing_training_to_wait_for':active,
            'same_hyperparameters':True,'cross_gpu_numeric_differences_expected':True,
            'global_selection':'unchanged: baseline + four settings, equal-fold mean inner validation; no test until all complete'})
        with (REPORT/'recformer_distributed.log').open('a') as stream:
            p=subprocess.Popen([sys.executable,'-u',__file__,'--worker'],cwd=ROOT,
                stdin=subprocess.DEVNULL,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
        pidfile.write_text(str(p.pid))
        print('DISTRIBUTED CONTROLLER PID',p.pid,'WAIT FOR',active,flush=True);return
    try:
        plan=read(REPORT/'recformer_distributed_plan.json')
        record('recformer_distributed_started','Local scheduler limited to LR1e-6/w100 and LR3e-6/w300; current in-flight job retained. Other two settings assigned to Kaggle, wait for verified imports before global validation selection.',
            'hm_medium_recformer_distributed_v1',status='training',assignments=PLAN)
        for proc in plan['existing_training_to_wait_for']:
            while alive(proc['pid'],'CVFollowup/recformer_grid.py'):time.sleep(15)
        for label in PLAN['local']:
            for fold in range(3):
                write(REPORT/'recformer_lane_status.json',{'status':'training','label':label,'fold':fold,'controller':'distributed'})
                with (REPORT/f'recformer_f{fold}_{label}_train.log').open('a') as log:
                    subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/recformer_grid.py'),str(fold),label,'train'],cwd=ROOT,
                        stdout=log,stderr=subprocess.STDOUT,check=True)
        labels=PLAN['kaggle_1']+PLAN['kaggle_2']
        while True:
            missing=[f'{f}/{label}' for label in labels for f in range(3)
                if not(OUT/f'fold_{f}/recformer_grid'/label/'external_import.json').exists()]
            if not missing:break
            write(REPORT/'recformer_lane_status.json',{'status':'waiting_kaggle_imports','missing':missing})
            time.sleep(30)
        # Original controller now skips all12 completed fits and performs unchanged selection/evaluation.
        subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/recformer_lane.py'),'--worker'],cwd=ROOT,check=True)
    except BaseException as error:
        write(REPORT/'recformer_distributed_failure.json',{'error':str(error)})
        record('recformer_distributed_interrupted',str(error),'hm_medium_recformer_distributed_v1',status='interrupted')
        raise

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--worker',action='store_true');main(p.parse_args().worker)
