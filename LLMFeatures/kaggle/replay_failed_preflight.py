"""Bounded replay of actual failed programs. Never repairs formulas or trains a model."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'hm_llmfe_llama31_8b_lightgbm_fulltrain_v3_3b338cf1f141_results'
DEST=ROOT/'reports/kaggle_llama_v3_audit/preflight_replay'
WORKER=Path(__file__).with_name('worker.py')
DATA=ROOT/'data/kaggle_hm_llmfe_fulltrain_v2'


def main():
    DEST.mkdir(parents=True,exist_ok=True)
    results=[]
    env={k:v for k,v in os.environ.items() if not any(s in k.upper() for s in ['TOKEN','SECRET','API_KEY'])}
    env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',CUDA_VISIBLE_DEVICES='')
    for source in sorted(SOURCE.glob('candidates/*/program.py')):
        destination=DEST/source.parent.name
        destination.mkdir(exist_ok=True)
        shutil.copy2(source,destination/'program.py')
        result_file=destination/'replay_result.json'
        if result_file.exists():
            result=json.loads(result_file.read_text())
        else:
            tick=time.perf_counter()
            with (destination/'preflight.log').open('w') as log:
                try:
                    proc=subprocess.run([sys.executable,str(WORKER),'--data',str(DATA),'--directory',str(destination),
                                         '--stage','preflight','--threads','1','--memory-gb','4','--backend','lightgbm'],
                                        stdout=log,stderr=subprocess.STDOUT,timeout=100,env=env)
                    code=proc.returncode
                except subprocess.TimeoutExpired:
                    code='timeout'
            result={'candidate':source.parent.name,'exit_code':code,'preflight_passed':code==0,
                    'seconds':time.perf_counter()-tick,'formulas_edited':False,
                    'full_training_performed':False,'log':str((destination/'preflight.log').relative_to(ROOT))}
            result_file.write_text(json.dumps(result,indent=2))
        results.append(result)
        print(json.dumps(result),flush=True)
    (DEST/'summary.json').write_text(json.dumps({'scope':'actual v3 programs, unchanged formulas, local CPU preflight only',
        'programs':len(results),'preflight_passed':sum(t['preflight_passed'] for t in results),
        'results':results},indent=2))


if __name__=='__main__':
    main()
