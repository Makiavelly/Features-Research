"""Exact chat token budget for initial, repair and near-output-limit SQL scripts."""
import json
import os
from pathlib import Path
import sys
os.environ['USE_TORCH']='0'
os.environ['USE_TF']='0'
sys.path.insert(0,str(Path(__file__).resolve().parent))
from transformers import AutoTokenizer
from full_sql import parse,SQLProgramError
from prompting import make_prompt
from check_delivery import A

ROOT=Path(__file__).resolve().parents[3]
tokenizer=AutoTokenizer.from_pretrained('Qwen/Qwen2.5-Coder-7B-Instruct',
    revision='c03e6d358207e414f1eca0bb1891e29f1db0e242',cache_dir='/tmp/h003_context_tokenizer')
config=json.loads((ROOT/'reports/hm_small_llms_v1/exports/qwen_llama/run_config.json').read_text())


def count(prompt):
    messages=[{'role':'system','content':'Return only a complete DuckDB SQL script of SELECT/WITH queries following the user interface.'},
              {'role':'user','content':prompt}]
    return len(tokenizer.apply_chat_template(messages,tokenize=True,add_generation_prompt=True))


def script(features,padding=0):
    queries=[]
    for i in range(6):
        outputs=[f'count(*) FILTER(WHERE days_ago<={i*6+j+1})'+(' + 0'*padding)+f' AS f_window_{i}_{j}' for j in range(features)]
        queries.append('SELECT customer_id,'+','.join(outputs)+' FROM history GROUP BY customer_id')
    return ';\n'.join(queries)+';'


stress=script(6)
features=6
while len(tokenizer.encode(stress))>2048:
    # Keep all queries complete, remove one feature from every query.
    features-=1
    stress=script(features)
padding=0
while len(tokenizer.encode(script(features,padding+1)))<=2048:
    padding+=1
stress=script(features,padding)
program=parse(stress)
issues=[dict(query=i+1,reason='Binder Error: Referenced column f_missing does not exist in this query. '+('Check the CTE output schema. '*20),
             hint='Use only history and columns explicitly produced by your CTEs.') for i in range(6)]
error=str(SQLProgramError(issues))
samples={
    'initial':make_prompt(None,{'score':0.005555555555555556,'program':{'queries':[]}},None,config),
    'example_repair':make_prompt(None,{'score':0.01,'program':parse(A)},dict(text=A,error=error),config),
    'large_six_query_repair':make_prompt(None,{'score':0.01,'program':program},dict(text=stress,error=error),config),
    'large_duplicate_repair':make_prompt(None,{'score':0.01,'program':program},dict(text=stress,error='Duplicate of call10. Your Previous SQL response already contains the complete matching program. Change a time window/statistic/grouping.'),config),
}
result=dict(scope='Exact tokenizer on initial/example/stress prompts; no model weights or LLM generation',
            input_limit=6144,output_limit=2048,stress_response_tokens=len(tokenizer.encode(stress)),
            counts={n:count(p) for n,p in samples.items()})
assert max(result['counts'].values())<=6144,result
out=ROOT/'reports/kaggle_llmfe_validation/full_sql_small_v1/context_budget.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
