"""CPU-only bounded feature alignment audit, no fitting and no repair of original results."""
import os
os.environ['CUDA_VISIBLE_DEVICES']=''
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[name]='1'
import json
from pathlib import Path
import resource
import signal
import numpy as np
import pandas as pd
from worker import Data,compile_program

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'reports/hm_llmfe_llama_v5_audit'
resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
def expired(*_):raise TimeoutError('Semantic probe exceeded30s for candidate')
signal.signal(signal.SIGALRM,expired)
data=Data(ROOT/'data/kaggle_hm_llmfe_fulltrain_v2')
pairs=pd.read_parquet(data.root/'search_pairs.parquet').head(128)
X,H=data.inputs(pairs,pairs.timestamp.iloc[0])
permutation=np.random.default_rng(42).permutation(len(X))
trials=json.loads((OUT/'export/trials.json').read_text());results=[]
for t in trials:
    if t['status']!='valid':continue
    directory=OUT/'export/candidates'/f"candidate_{t['sample']:03d}"
    try:
        signal.alarm(30)
        f=compile_program((directory/'program.py').read_text())
        full=f(X.copy(deep=True),H.copy(deep=True))
        shuffled=f(X.iloc[permutation].reset_index(drop=True).copy(deep=True),H.copy(deep=True))
        reordered=shuffled.iloc[np.argsort(permutation)].reset_index(drop=True)
        chunks=pd.concat([f(X.iloc[:64].reset_index(drop=True).copy(deep=True),H.copy(deep=True)),
                          f(X.iloc[64:].reset_index(drop=True).copy(deep=True),H.copy(deep=True))],ignore_index=True)
        a=full.to_numpy(dtype=float);b=reordered.to_numpy(dtype=float);c=chunks.to_numpy(dtype=float)
        result={'candidate':t['sample'],'permutation_invariant':bool(np.array_equal(a,b,equal_nan=True)),
                'batch_invariant':bool(np.array_equal(a,c,equal_nan=True)),'columns':list(full)}
        if t['sample']==151:
            recent=H[H.days_ago<=7]
            diagnostics=[]
            mapping=[('f_article_mean_price','article_id','price','mean'),
                     ('f_customer_mean_days_ago','customer_id','days_ago','mean'),
                     ('f_customer_mean_article_count','customer_id','article_id','count')]
            for feature,key,column,operation in mapping:
                expected=recent.groupby(key)[column].agg(operation).reindex(X[key]).to_numpy(dtype=float)
                actual=full[feature].to_numpy(dtype=float)
                equal=(actual==expected)|(np.isnan(actual)&np.isnan(expected))
                diagnostics.append({'feature':feature,'mismatched_pairs':int((~equal).sum()),'pairs':len(X),
                    'actual_missing':int(np.isnan(actual).sum()),'intended_missing':int(np.isnan(expected).sum())})
            result['correct_id_mapping_diagnostics']=diagnostics
        results.append(result)
    except Exception as error:results.append({'candidate':t['sample'],'probe_error':str(error)})
    finally:signal.alarm(0)
(OUT/'semantic_probes.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'candidates':len(results),'permutation_failed':sum(not r.get('permutation_invariant',False) for r in results),
    'batch_failed':sum(not r.get('batch_invariant',False) for r in results),
    'chosen':next(r for r in results if r['candidate']==151)},indent=2),flush=True)
