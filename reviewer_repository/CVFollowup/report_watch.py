"""Generate interim and final reports as the independent experiment lanes finish."""
import argparse
import subprocess
import sys
import time
from common import ROOT,REPORT,read,write,record

def main(worker):
    REPORT.mkdir(parents=True,exist_ok=True)
    if not worker:
        with (REPORT/'report_watch.log').open('a') as log:
            p=subprocess.Popen([sys.executable,'-u',__file__,'--worker'],cwd=ROOT,
                stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        (REPORT/'report_watch.pid').write_text(str(p.pid));print('REPORT WATCH PID',p.pid);return
    deadline=time.monotonic()+48*3600
    while time.monotonic()<deadline:
        gnn=REPORT/'gnn_lane_status.json'
        if gnn.exists() and read(gnn).get('stage')=='verified':
            if not(REPORT/'gnn_corrected/comparison.json').exists():
                subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/report.py'),'gnn'],cwd=ROOT,check=True)
            flags=[REPORT/f'{name}_lane_status.json' for name in ['api','recformer']]
            if all(p.exists() and read(p).get('status')=='evaluated' for p in flags):
                subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/report.py'),'all'],cwd=ROOT,check=True)
                write(REPORT/'report_watch_status.json',{'status':'generated_pending_visual_review'});return
        time.sleep(30)
    record('followup_report_wait_limit','Report watcher ended after48h; inspect experiment lanes before resume.',
        'hm_medium_followup_report_watch_v1',status='interrupted')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--worker',action='store_true');main(p.parse_args().worker)
