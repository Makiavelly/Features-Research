"""Explicitly synthetic generator smoke: verifies plumbing, not Llama quality."""
import json
from pathlib import Path
import shutil
import pandas as pd
import numpy as np
from runtime import search,final,write_json

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'data/kaggle_hm_llmfe_fulltrain_v2'
OUT=ROOT/'reports/kaggle_llmfe_validation/lightgbm_v5_preflight_synthetic_smoke'
DATA=OUT/'input'
DATA.mkdir(parents=True,exist_ok=True)
for name in ['articles.parquet','customers.parquet','manifest.json']:
    shutil.copy2(SOURCE/name,DATA/name)
train=pd.read_parquet(SOURCE/'train_pairs.parquet')
train=train[train.timestamp==train.timestamp.max()].head(2000).reset_index(drop=True)
train.to_parquet(DATA/'train_pairs.parquet',index=False)
pd.read_parquet(SOURCE/'history.parquet').head(10000).to_parquet(DATA/'history.parquet',index=False)
for split in ['search','confirm','val','test']:
    truth=pd.read_parquet(SOURCE/f'{split}_targets.parquet').head(8).reset_index(drop=True)
    truth.to_parquet(DATA/f'{split}_targets.parquet',index=False)
    pairs=pd.read_parquet(SOURCE/f'{split}_pairs.parquet')
    pairs[pairs.customer_id.isin(truth.customer_id)].reset_index(drop=True).to_parquet(DATA/f'{split}_pairs.parquet',index=False)
    if split in ['val','test']:
        for name in ['idgnn','manual_lightgbm','gnn_lightgbm']:
            np.save(DATA/f'{split}_{name}_reference.npy',np.load(SOURCE/f'{split}_{name}_reference.npy')[:8])
configuration={'smoke':True,'fake_generator':True,'target_successful_distinct':2,
               'max_llm_calls':10,'max_repairs_per_proposal':3,'cpu_threads':1,'train_pairs':len(train),
               'search_backend':'lightgbm',
               'evaluation_memory_gb':4,'evaluation_timeout_seconds':120}
program='''def modify_features(X, history):
    return pd.DataFrame({'f_fixture': X.raw_u_age.fillna(0) * 2}, index=X.index)
'''
calls=[]


def fake(prompt,seed):
    calls.append(seed)
    sequence=['invalid Python']*3+[program,program,program.replace('* 2','* 3')]
    text=sequence[len(calls)-1]
    return {'text':text,'truncated':False,'synthetic_fixture_not_llm':True}


selected=search(DATA,OUT/'run',configuration,fake)
result=final(DATA,OUT/'run',configuration)
trials=json.loads((OUT/'run/trials.json').read_text())
assert [t['status'] for t in trials]==['rejected','rejected','rejected','valid','duplicate','valid']
assert [t['repair'] for t in trials]==[0,1,2,3,0,1]
assert selected['search_budget']['target_met'] and selected['search_budget']['llm_calls']==6
def forbidden(*_):
    raise AssertionError('Resume must not generate again')
assert search(DATA,OUT/'run',configuration,forbidden)==selected
assert result['independent_full_replay']
assert all(t['metrics']['backend']=='lightgbm' for t in trials if t['status']=='valid')
assert all(t['preflight']['passed'] for t in trials if t['status']=='valid')
if selected['selected_raw_control']:
    assert not result['llm_feature_model_selected']
    assert 'LLM-FE LightGBM' not in result['metrics']
write_json(OUT/'verification.json',{'passed':True,'scope':'synthetic generation, tiny data, LightGBM search/confirmation/final +3 saved references, full replay, resume',
                                  'is_llm_experiment':False,'train_pairs':len(train),
                                  'gpu_or_llama_executed':False})
print('Synthetic integration smoke passed; NOT a Llama quality result.')
