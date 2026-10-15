"""Synthetic SQL proposals, real LightGBM. These are NOT Llama quality results."""
import hashlib
import json
from pathlib import Path
import shutil
from check_sql import ROOT,SPEC
from runtime import search,final,evaluate,write_json,RAW

OUT=ROOT/'reports/kaggle_llmfe_validation/sql_v1_derived'
DATA=OUT/'smoke_input'
SOURCE=ROOT/'reports/kaggle_llmfe_validation/lightgbm_v5_preflight_synthetic_smoke/input'
DATA.mkdir(parents=True,exist_ok=True)
for file in SOURCE.iterdir():
    shutil.copy2(file,DATA/file.name)
config={'smoke':True,'fake_generator':True,'target_successful_distinct':2,
        'max_llm_calls':8,'max_repairs_per_proposal':3,'cpu_threads':4,'train_pairs':2000,
        'search_backend':'lightgbm','evaluation_memory_gb':4,'evaluation_timeout_seconds':1800}
second=json.loads(json.dumps(SPEC));second['aggregates'][0]['sql']='COUNT(*) FILTER (WHERE days_ago <= 7)'
responses=['invalid json',json.dumps(SPEC),json.dumps(SPEC),json.dumps(second)]
calls=[]
def fake(prompt,seed):
    calls.append(seed)
    return {'text':responses[len(calls)-1],'truncated':False,'synthetic_not_llm':True}
selected=search(DATA,OUT/'synthetic_run',config,fake)
report=final(DATA,OUT/'synthetic_run',config)
trials=json.loads((OUT/'synthetic_run/trials.json').read_text())
assert [t['status'] for t in trials]==['rejected','valid','duplicate','valid']
assert [t['repair'] for t in trials]==[0,1,0,1]
assert selected['search_budget']['evaluated_distinct']==2
assert selected['search_budget']['llm_calls']==4
assert report['independent_full_replay']
def forbidden(*_): raise AssertionError('Resume must not generate')
assert search(DATA,OUT/'synthetic_run',config,forbidden)==selected
print('Synthetic SQL end-to-end / repairs / duplicate / resume / final replay passed.',flush=True)
# Also check the new engine on ALL original training pairs, not just tiny data.
full_data=ROOT/'data/kaggle_hm_llmfe_fulltrain_v2'
full=OUT/'fulltrain_fixture';full.mkdir(exist_ok=True)
(full/'program.py').write_text(json.dumps(SPEC))
real_config={**config,'smoke':False,'train_pairs':803377}
metrics=evaluate(full_data,full,'search',real_config)
schema=json.loads((full/'schema.json').read_text())
assert schema['train_pairs']==803377 and len(schema['features'])==19
validation=evaluate(full_data,full,'val',real_config)
replay=evaluate(full_data,full,'replay_val',real_config)
assert replay['passed'] and replay['map']==validation['map']
write_json(OUT/'verification.json',{'passed':True,'tests':6,'synthetic_pipeline':True,
    'fulltrain_fixture_pairs':803377,'fulltrain_fixture_search_seconds':metrics['seconds'],
    'fulltrain_fixture_replay':True,'gpu_or_llama_executed':False,
    'quality_result':False,'note':'SQL programs are test fixtures, not Llama-generated features'})
print('SQL fixture full803377-pair fit and independent saved-model replay passed.',flush=True)
