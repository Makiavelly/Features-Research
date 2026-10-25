"""Detached, bounded network recovery; all selected budgets precede outer scoring."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import time
from common import ROOT,OUT,REPORT,read,write,sha,record

def run_stage(fold,mode,stage):
    log=REPORT/f'api_f{fold}_{mode}_{stage}.log'
    for attempt in range(3):
        with log.open('a') as stream:
            result=subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/api_budgets.py'),str(fold),mode,stage],
                                  cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
        if result.returncode==0:return
        last=log.read_text(encoding='utf-8').strip().splitlines()[-1]
        transient='ProviderUnavailable:' in last and ('API transport failure:' in last or
                    any(f'API HTTP{code}:' in last for code in [408,429,500,502,503,504]))
        if not transient or attempt==2:raise RuntimeError(f'API {fold}/{mode}/{stage} stopped; see {log}')
        record('followup_api_network_retry',f'Fold{fold} {mode}: transient failure, resume{attempt+1}/2 in30s; saved response and300POST cap retained.',
               'hm_medium_followup_api_budget_v1',status='searching')
        time.sleep(30)

def main(worker):
    REPORT.mkdir(parents=True,exist_ok=True)
    if not worker:
        pidfile=REPORT/'api_lane.pid'
        if pidfile.exists():
            try:command=Path(f'/proc/{int(pidfile.read_text())}/cmdline').read_bytes()
            except FileNotFoundError:pass
            else:
                if b'CVFollowup/api_lane.py' in command:raise RuntimeError('API lane already active')
        with (REPORT/'api_lane.log').open('a') as stream:
            process=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),'--worker'],cwd=ROOT,
                 stdin=subprocess.DEVNULL,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
        pidfile.write_text(str(process.pid));print('FOLLOWUP API PID',process.pid,flush=True);return
    try:
        assert read(REPORT/'api_validator_verification.json')['passed']
        files=['api_lane.py','api_budgets.py','check_api.py','common.py','PROTOCOL.md']
        sources={name:sha(ROOT/'CVFollowup'/name) for name in files}
        manifest=REPORT/'api_source_manifest.json'
        if manifest.exists():assert read(manifest)==sources,'API sources changed after launch'
        else:write(manifest,sources)
        record('followup_api_started','Continuing six saved20-program streams to30/40; own-island memories only; no outer feedback.',
               'hm_medium_followup_api_budget_v1',status='searching')
        for fold in range(3):
            for mode in ['h008','h009']:
                write(REPORT/'api_lane_status.json',{'status':'searching','fold':fold,'mode':mode})
                print('SEARCH',fold,mode,flush=True);run_stage(fold,mode,'train')
        selected={str(p.relative_to(ROOT)):sha(p) for p in OUT.glob('fold_*/h00*/budgets/*/selected.json')}
        assert len(selected)==18
        write(REPORT/'api_pretest_freeze.json',{'selections':selected,'all_searches_complete':True,
              'previously_inspected_test':True,'protocol_sha256':sha(ROOT/'CVFollowup/PROTOCOL.md')})
        for fold in range(3):
            for mode in ['h008','h009']:
                write(REPORT/'api_lane_status.json',{'status':'evaluating','fold':fold,'mode':mode})
                print('EVALUATE',fold,mode,flush=True);run_stage(fold,mode,'evaluate')
        write(REPORT/'api_lane_status.json',{'status':'evaluated'})
        record('followup_api_evaluated','All20/30/40 budget selections evaluated and replayed; summary report pending.',
               'hm_medium_followup_api_budget_v1',status='evaluated_pending_report',artifacts=str(REPORT.relative_to(ROOT)))
    except BaseException as error:
        write(REPORT/'api_lane_failure.json',{'error':str(error)})
        record('followup_api_stopped',str(error),'hm_medium_followup_api_budget_v1',status='interrupted')
        raise

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true')
    main(parser.parse_args().worker)
