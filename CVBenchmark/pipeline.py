"""Two resource lanes, then a global pretest barrier and frozen scoring/replay."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import traceback
from common import ROOT,DATA,OUT,REPORT,read,write,sha,record
from build_runtime import build

LOCK=threading.Lock()
STATUS={}

def step(name,args):
    folder=REPORT/'stages';folder.mkdir(parents=True,exist_ok=True)
    marker=folder/f'{name}.json'
    if marker.exists():
        assert read(marker)['status']=='complete';return
    with LOCK:
        STATUS[name]={'status':'running','started':time.time()};write(REPORT/'pipeline_status.json',STATUS)
    command=[sys.executable,'-u',*map(str,args)]
    log=folder/f'{name}.log';started=time.perf_counter()
    print('START',name,flush=True)
    env=os.environ.copy();env.update(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='4',TOKENIZERS_PARALLELISM='false')
    # Secret is read only by the explicit API adapter from .env, never put in args/env.
    with log.open('a') as stream:
        process=subprocess.run(command,env=env,stdout=stream,stderr=subprocess.STDOUT)
    result={'status':'complete' if process.returncode==0 else 'failed','returncode':process.returncode,
            'seconds':time.perf_counter()-started,'command':command,'log':str(log.relative_to(ROOT))}
    with LOCK:
        STATUS[name]=result;write(REPORT/'pipeline_status.json',STATUS)
    if process.returncode:
        raise RuntimeError(f'{name} failed; inspect {log}')
    write(marker,result);print('DONE',name,round(result['seconds'],1),flush=True)

def gpu_lane():
    for f in range(3):
        rt=OUT/f'fold_{f}/runtime'
        step(f'f{f}_gnn_train',[rt/'gnn.py','--train-only'])
        step(f'f{f}_tdm_train',[ROOT/'CVBenchmark/tdm.py',f,'train'])
        step(f'f{f}_recformer_train',[rt/'recformer.py','--variant','low_lr_warmup','--train-only'])

def cpu_lane():
    for f in range(3):
        for kind in ['manual','raw15']:step(f'f{f}_{kind}_train',[ROOT/'CVBenchmark/trees.py',f,kind,'train'])
        for mode in ['h008','h009']:step(f'f{f}_{mode}_search',[ROOT/'CVBenchmark/api.py',f,mode,'train'])

def main():
    REPORT.mkdir(parents=True,exist_ok=True)
    for f in range(3):build(f)
    fingerprint={str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'CVBenchmark').glob('*.py')}
    fingerprint['CVBenchmark/PROTOCOL.md']=sha(ROOT/'CVBenchmark/PROTOCOL.md')
    frozen=REPORT/'source_manifest.json'
    if frozen.exists():assert read(frozen)==fingerprint,'Source changed after pipeline launch; do not silently mix runs'
    else:write(frozen,fingerprint)
    record('medium_cv_resumed','Starting nine-method temporal CV; three reset folds; no Qwen/Llama. Outer scoring gated until all selections frozen.',
           'hm_medium_temporal_cv_v2',status='verifying',artifacts='reports/medium_cv_v2')
    try:
        for f in range(3):step(f'f{f}_validator',[ROOT/'CVBenchmark/check.py',f])
        rt=OUT/'fold_0/runtime'
        step('gpu_gnn_smoke',[rt/'gnn.py','--probe'])
        step('gpu_recformer_smoke',[rt/'recformer.py','--variant','low_lr_warmup','--probe'])
        record('medium_cv_running','Validator and GPU smoke checks passed. CPU/API and GPU lanes begin; no outer-test scores available.',
               'hm_medium_temporal_cv_v2',status='training')
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures=[executor.submit(gpu_lane),executor.submit(cpu_lane)]
            failures=[]
            for future in futures:
                try:future.result()
                except BaseException as e:failures.append(str(e))
            if failures:raise RuntimeError('; '.join(failures))
        write(REPORT/'selection_pretest.json',{'all_training_and_search_finished':True,'source_manifest_sha256':sha(frozen),
              'selected_files':{str(p.relative_to(ROOT)):sha(p) for p in OUT.rglob('*')
                                if p.is_file() and p.name in ['selected.json','trained.json','training_summary.json','best.pt']}})
        record('medium_cv_pretest_barrier','All nine methods on all three folds selected; outer scoring now permitted.',
               'hm_medium_temporal_cv_v2',status='evaluating')
        for f in range(3):
            rt=OUT/f'fold_{f}/runtime'
            step(f'f{f}_gnn_evaluate',[rt/'gnn.py','--evaluate-only'])
            step(f'f{f}_gnn_replay',[rt/'gnn.py','--verify-only'])
            step(f'f{f}_tdm_evaluate',[ROOT/'CVBenchmark/tdm.py',f,'evaluate'])
            step(f'f{f}_tdm_replay',[ROOT/'CVBenchmark/tdm.py',f,'verify'])
            step(f'f{f}_recformer_evaluate',[rt/'recformer.py','--variant','low_lr_warmup','--evaluate-only'])
            step(f'f{f}_recformer_replay',[rt/'recformer.py','--variant','low_lr_warmup','--verify-only'])
            for kind in ['manual','raw15']:step(f'f{f}_{kind}_evaluate',[ROOT/'CVBenchmark/trees.py',f,kind,'evaluate'])
            for mode in ['h008','h009']:step(f'f{f}_{mode}_evaluate',[ROOT/'CVBenchmark/api.py',f,mode,'evaluate'])
        step('report',[ROOT/'CVBenchmark/report.py'])
        record('medium_cv_complete','Temporal CV comparison and frozen replays completed. See report for per-fold results, uncertainty and limits.',
               'hm_medium_temporal_cv_v2',status='complete',artifacts='reports/medium_cv_v2/report.md')
    except BaseException as e:
        write(REPORT/'failure.json',{'error':str(e),'traceback':traceback.format_exc()})
        record('medium_cv_error',str(e),'hm_medium_temporal_cv_v2',status='interrupted',artifacts='reports/medium_cv_v2')
        raise

if __name__=='__main__':main()
