"""Sequential GPU tuning; a single setting selected by3fold inner validation."""
import argparse
from pathlib import Path
import subprocess
import sys
from common import ROOT,OLD,OUT,REPORT,read,write,sha,record
from recformer_grid import GRID,build

def run_logged(fold,label,stage):
    with (REPORT/f'recformer_f{fold}_{label}_{stage}.log').open('a') as log:
        subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/recformer_grid.py'),str(fold),label,stage],
                       cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)

def main(worker):
    REPORT.mkdir(parents=True,exist_ok=True)
    if not worker:
        pidfile=REPORT/'recformer_lane.pid'
        if pidfile.exists():
            try:command=Path(f'/proc/{int(pidfile.read_text())}/cmdline').read_bytes()
            except FileNotFoundError:pass
            else:
                if b'CVFollowup/recformer_lane.py' in command:raise RuntimeError('Recformer lane active')
        with (REPORT/'recformer_lane.log').open('a') as stream:
            process=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),'--worker'],cwd=ROOT,
                 stdin=subprocess.DEVNULL,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
        pidfile.write_text(str(process.pid));print('RECFORMER TUNING PID',process.pid,flush=True);return
    try:
        assert read(REPORT/'recformer_grid_verification.json')['passed']
        files=['recformer_lane.py','recformer_grid.py','common.py','PROTOCOL.md']
        hashes={name:sha(ROOT/'CVFollowup'/name) for name in files}
        manifest=REPORT/'recformer_source_manifest.json'
        if manifest.exists():assert read(manifest)==hashes
        else:write(manifest,hashes)
        record('followup_recformer_grid_started','Four predeclared LR/warmup settings on3folds; only inner validation selects the setting.',
               'hm_medium_recformer_grid_seed42_v1',status='training')
        for label in GRID:
            for fold in range(3):
                write(REPORT/'recformer_lane_status.json',{'status':'training','label':label,'fold':fold})
                print('TRAIN',fold,label,flush=True);run_logged(fold,label,'train')
        rows=[]
        for label in ['baseline',*GRID]:
            paths=[OLD/f'fold_{f}/recformer' if label=='baseline' else OUT/f'fold_{f}/recformer_grid'/label for f in range(3)]
            maps=[read(p/'training_summary.json')['best_trained_val_map'] for p in paths]
            rows.append({'label':label,'fold_search_maps':maps,'mean_search_map':sum(maps)/3})
        winner=max(rows,key=lambda row:row['mean_search_map'])
        chosen=winner['label']
        folders=[OLD/f'fold_{f}/recformer' if chosen=='baseline' else OUT/f'fold_{f}/recformer_grid'/chosen for f in range(3)]
        write(REPORT/'recformer_pretest_freeze.json',{'selected_label':chosen,'selection':'maximum equal-fold mean of inner-search best-epoch MAP; stable ties baseline-first',
              'validation_grid':rows,'checkpoints':{str(f):sha(p/'finetuned/best.pt') for f,p in enumerate(folders)},
              'test_used_for_selection':False})
        record('followup_recformer_selected',f'LR/warmup grid selected {chosen} by inner validation only; checkpoints frozen.',
               'hm_medium_recformer_grid_seed42_v1',status='evaluating',validation_grid=rows)
        if chosen!='baseline':
            for fold in range(3):
                write(REPORT/'recformer_lane_status.json',{'status':'evaluating','label':chosen,'fold':fold})
                run_logged(fold,chosen,'evaluate')
        write(REPORT/'recformer_lane_status.json',{'status':'evaluated','selected_label':chosen})
        record('followup_recformer_evaluated','Validation-selected Recformer setting evaluated/replayed; comparison report pending.',
               'hm_medium_recformer_grid_seed42_v1',status='evaluated_pending_report')
    except BaseException as error:
        write(REPORT/'recformer_lane_failure.json',{'error':str(error)})
        record('followup_recformer_stopped',str(error),'hm_medium_recformer_grid_seed42_v1',status='interrupted')
        raise

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');main(parser.parse_args().worker)
