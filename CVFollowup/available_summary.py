"""Close an explicitly incomplete grid using only completed inner-validation fits."""
import os
from pathlib import Path
import signal
import subprocess
import sys
from common import ROOT,OLD,OUT,REPORT,read,write,sha,record

LABELS=['baseline','lr1e6_w100','lr3e6_w300','lr1e5_w300']

def stop_waiter(filename,needle):
    path=REPORT/filename
    if not path.exists():return
    pid=int(path.read_text())
    try:command=Path(f'/proc/{pid}/cmdline').read_bytes()
    except FileNotFoundError:return
    assert needle.encode() in command,'PID reused; refuse to stop an unrelated process'
    os.kill(pid,signal.SIGTERM)

def main():
    assert read(REPORT/'api_lane_status.json')['status']=='evaluated'
    assert read(REPORT/'recformer_lane_status.json')['status'] in ['waiting_kaggle_imports','evaluating','evaluated']
    # Stop only obsolete idle waiters, leaving all trained files intact.
    stop_waiter('recformer_distributed.pid','recformer_distributed.py')
    stop_waiter('report_watch.pid','report_watch.py')
    rows=[]
    for label in LABELS:
        folders=[OLD/f'fold_{f}/recformer' if label=='baseline' else OUT/f'fold_{f}/recformer_grid'/label for f in range(3)]
        maps=[read(p/'training_summary.json')['best_trained_val_map'] for p in folders]
        rows.append({'label':label,'fold_search_maps':maps,'mean_search_map':sum(maps)/3})
    winner=max(rows,key=lambda x:x['mean_search_map']);chosen=winner['label']
    folders=[OLD/f'fold_{f}/recformer' if chosen=='baseline' else OUT/f'fold_{f}/recformer_grid'/chosen for f in range(3)]
    freeze={'selected_label':chosen,'selection':'maximum equal-fold mean inner validation among completed settings + existing baseline; stable ties baseline first',
        'validation_grid':rows,'checkpoints':{str(f):sha(p/'finetuned/best.pt') for f,p in enumerate(folders)},
        'test_used_for_selection':False,'scope':'available_three_of_four_new_settings',
        'excluded_unavailable':['lr3e6_w100'],'exclusion_reason':'User reports second Kaggle notebook cannot start; summarize available results',
        'protocol':'hm_medium_followup_available_summary_v1'}
    path=REPORT/'recformer_pretest_freeze.json'
    if path.exists():assert read(path)==freeze,'Preserve prior frozen selection'
    else:write(path,freeze)
    record('available_grid_selection_frozen',f'User requested summary without unavailable Kaggle setting. Selected {chosen} by completed three-fold inner validation only; no new training. Excluded lr3e6_w100 as unavailable, not poor quality.',
        'hm_medium_followup_available_summary_v1',status='evaluating',validation_grid=rows)
    if chosen!='baseline':
        for fold in range(3):
            write(REPORT/'recformer_lane_status.json',{'status':'evaluating','label':chosen,'fold':fold,'scope':freeze['scope']})
            print('EVALUATE',fold,chosen,flush=True)
            with (REPORT/f'recformer_f{fold}_{chosen}_evaluate.log').open('a') as log:
                subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/recformer_grid.py'),str(fold),chosen,'evaluate'],
                    cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    write(REPORT/'recformer_lane_status.json',{'status':'evaluated','selected_label':chosen,'scope':freeze['scope'],'excluded_unavailable':freeze['excluded_unavailable']})
    subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/report.py'),'all'],cwd=ROOT,check=True)
    subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/summary_figures.py')],cwd=ROOT,check=True)
    record('available_summary_generated','All available methods and API20/30/40 budgets evaluated; incomplete Recformer grid documented. Report/plots generated, visual review pending.',
        'hm_medium_followup_available_summary_v1',status='report_pending_visual_review',artifacts='reports/medium_followup_v1/final_comparison')

if __name__=='__main__':main()
