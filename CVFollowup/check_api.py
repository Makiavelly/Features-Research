"""Validator regressions and exact inherited-history checks; no network calls."""
import sys
import numpy as np
import pandas as pd
from common import ROOT,OUT,REPORT,read,write,sha
from api_budgets import prepare,config

def main():
    folder,runtime=prepare(0,'h009');sys.path.insert(0,str(runtime))
    from python_features import parse,compile_function,construct,program_key
    source=(ROOT/'LLMFeatures/check_python_features.py').read_text(encoding='utf-8')
    body=source[source.index('    passed=[]'):source.index("    data=ROOT/'data/kaggle_hm_small_sql_compare_v1'")]
    scope=dict(globals(),parse=parse,compile_function=compile_function,construct=construct,program_key=program_key)
    exec(compile('def regression():\n'+body+'\n    return passed','<validator-regressions>','exec'),scope)
    checks=scope['regression']()
    from dialog_history import build_messages
    old=ROOT/'CVBenchmark/results/medium_v2/fold_0/h009'
    cfg,cfgpath=config(0,'h009',30,folder,runtime)
    oldcfg=read(old/'run_config.json')
    for number in [1,4,10,20]:
        trial=read(folder/cfg['arm']/'candidates'/f'candidate_{number:03d}'/'trial.json')
        candidate=folder/cfg['arm']/'candidates'/f'candidate_{number:03d}'
        response=read(candidate/'response.json');request=read(folder/'api_attempts'/f"attempt_{response['api_attempt']:03d}"/'request.json')
        prompt=(candidate/'prompt.txt').read_text(encoding='utf-8')
        assert build_messages(cfg,folder,prompt,42+number-1)==request['messages']
        assert sha(candidate/'response.json')==sha(old/cfg['arm']/'candidates'/f'candidate_{number:03d}'/'response.json')
    checks.append('inherited_messages_and_responses_byte_preserved')
    assert cfg['system_message']==oldcfg['system_message']
    assert cfg['train_pair_sha256']==oldcfg['train_pair_sha256']
    assert cfg['automatic_raw_features']==0 and cfg['max_llm_calls']==300
    assert {p.name:sha(p) for p in runtime.glob('*.py')}==oldcfg['runtime_sha256']
    checks.append('same_data_validator_model_and_original300_POST_cap')
    write(REPORT/'api_validator_verification.json',{'passed':True,'checks':checks,'real_api_calls':0,
          'runtime_sha256':{p.name:sha(p) for p in runtime.glob('*.py')}})
    print('FOLLOWUP API VALIDATOR:',len(checks),'checks passed;0 real API calls',flush=True)

if __name__=='__main__':main()
