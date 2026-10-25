"""Synthetic proposals plus real tree training/replay; never a real Llama result."""
import json
from pathlib import Path
import shutil
from check_structured import ROOT,SPEC
from runtime import search,final,evaluate,write_json

OUT=ROOT/'reports/kaggle_llmfe_validation/structured_v1'
DATA=OUT/'smoke_input'
SOURCE=ROOT/'reports/kaggle_llmfe_validation/lightgbm_v5_preflight_synthetic_smoke/input'
DATA.mkdir(parents=True,exist_ok=True)
for file in SOURCE.iterdir():shutil.copy2(file,DATA/file.name)
config={'smoke':True,'fake_generator':True,'target_successful_distinct':2,'max_llm_calls':8,
        'max_repairs_per_proposal':3,'cpu_threads':4,'train_pairs':2000,'search_backend':'lightgbm',
        'evaluation_memory_gb':4,'evaluation_timeout_seconds':1800}
second=json.loads(json.dumps(SPEC));second['aggregates'][0]['window']=7
sequence=['{"aggregates":[{"name":"f_bad","keys":["customer_id"],"op":"avg","column":"raw_u_active"}]}',
          json.dumps(SPEC),json.dumps(SPEC),json.dumps(second)]
calls=[]
def fake(prompt,seed):
    calls.append(seed)
    return {'text':sequence[len(calls)-1],'synthetic_not_llm':True,'truncated':False}
selected=search(DATA,OUT/'synthetic_run',config,fake)
report=final(DATA,OUT/'synthetic_run',config)
trials=json.loads((OUT/'synthetic_run/trials.json').read_text())
assert [t['status'] for t in trials]==['rejected','valid','duplicate','valid']
assert [t['repair'] for t in trials]==[0,1,0,1]
assert selected['search_budget']['llm_calls']==4 and selected['search_budget']['target_met']
assert report['independent_full_replay']
assert (OUT/'synthetic_run/candidates/candidate_002/compiled_sql.json').exists()
def forbidden(*_):raise AssertionError('Resume must not generate')
assert search(DATA,OUT/'synthetic_run',config,forbidden)==selected
print('Synthetic structured search/repair/duplicate/resume/final replay passed.',flush=True)
full=OUT/'fulltrain_fixture';full.mkdir(exist_ok=True)
(full/'program.py').write_text(json.dumps(SPEC))
full_data=ROOT/'data/kaggle_hm_llmfe_fulltrain_v2'
full_config={**config,'train_pairs':803377,'smoke':False}
metrics=evaluate(full_data,full,'search',full_config)
schema=json.loads((full/'schema.json').read_text())
assert schema['train_pairs']==803377 and len(schema['features'])==19
val=evaluate(full_data,full,'val',full_config)
replay=evaluate(full_data,full,'replay_val',full_config)
assert replay['passed'] and val['map']==replay['map']
write_json(OUT/'verification.json',{'passed':True,'interface_tests':7,'synthetic_pipeline':True,
    'fulltrain_fixture_pairs':803377,'fulltrain_fixture_seconds':metrics['seconds'],
    'independent_model_replay':True,'gpu_or_llama_executed':False,'quality_result':False})
print('Structured fixture803377-pair training and independent replay passed.',flush=True)
