"""Independent audit of remote full-SQL search; no training or API calls."""
from collections import Counter
import argparse
import ast
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import os
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/gpt61sol_small_v1'
DATA=ROOT/'data/kaggle_hm_small_sql_compare_v1'


def read(path):return json.loads(Path(path).read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    global OUT
    parser=argparse.ArgumentParser()
    parser.add_argument('--corrected',action='store_true')
    parser.add_argument('--python',action='store_true')
    args=parser.parse_args()
    if args.corrected:OUT=ROOT/'reports/gpt61sol_small_v2'
    if args.python:OUT=ROOT/'reports/gpt61sol_python_v1'
    tick=time.perf_counter()
    current=read(ROOT/('reports/provider_python_v1' if args.python else 'reports/provider_small_v1')/('corrected_run.json' if args.corrected else 'current_run.json'))
    assert current['status']=='finished',current
    source=Path(current['directory'])
    config=read(source/'run_config.json')
    OUT.mkdir(parents=True,exist_ok=True)
    sys.path.insert(0,str(source/'runtime_sources'))
    from worker import ap12,write
    if args.python:
        from python_features import program_key,validate_program,FeatureEngine,parse
    else:
        from full_sql import program_key,validate_program,FeatureEngine
    fingerprint=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()[:12]
    assert source.name==config['protocol']+'_'+fingerprint
    manifest=read(DATA/'manifest.json')
    assert config['bundle_manifest_sha256']==sha(DATA/'manifest.json')==sha(source/'input_manifest.json')
    for name,digest in manifest['files'].items():assert sha(DATA/name)==digest
    for name,digest in config['runtime_sha256'].items():assert sha(source/'runtime_sources'/name)==digest
    old_config=read(ROOT/'reports/hm_small_llms_v1/exports/qwen_llama/run_config.json')
    matched=['seed','train_pairs','train_pair_sha256','target_successful_distinct','max_llm_calls',
             'max_repairs_per_proposal','islands','memory_programs_per_prompt','temperature','lightgbm_rounds',
             'cpu_threads','scoring_user_batch','search_users','confirmation_users','heldout_val_users',
             'validation_users','test_users','evaluation_catalog','training_examples','max_new_tokens']
    assert all(config[k]==old_config[k] for k in matched)
    parent=read(ROOT/'LLMFeatures/kaggle/full_sql_small/delivery_manifest.json')
    for name in ['base_features.py','features.py','full_sql.py','prompting.py','worker.py']:
        if args.python:
            if name=='base_features.py':assert config['runtime_sha256'][name]==parent['modules'][name]
            if name=='worker.py':
                original=ast.parse((ROOT/'LLMFeatures/provider_small_runtime_v1/worker.py').read_text())
                actual=ast.parse((source/'runtime_sources/worker.py').read_text())
                for function in ['fit','predict','ap12','timed_frame']:
                    old=next(n for n in original.body if isinstance(n,ast.FunctionDef) and n.name==function)
                    new=next(n for n in actual.body if isinstance(n,ast.FunctionDef) and n.name==function)
                    assert ast.dump(old)==ast.dump(new),'Downstream function changed: '+function
            continue
        if args.corrected and name=='full_sql.py':
            old_source=(ROOT/'LLMFeatures/results'/config['source_run']/'runtime_sources/full_sql.py').read_text()
            expected=old_source.replace('\nNUMERIC_TYPE = ',
                "\n# SQLGlot models standard Boolean syntax as Func nodes. These are not external functions.\nFUNCTIONS.update({'AND','OR','NOT','IN','BETWEEN','IS'})\nNUMERIC_TYPE = ",1)
            assert (source/'runtime_sources/full_sql.py').read_text()==expected
        else:assert config['runtime_sha256'][name]==parent['modules'][name]
    versions={n:importlib.metadata.version(n) for n in ['numpy','pandas','pyarrow','duckdb','lightgbm','sqlglot']}
    assert versions==config['versions']
    selection=read(DATA/'selection.json')
    assert sorted(sum(selection.values(),[]))==list(range(304))
    targets={s:pd.read_parquet(DATA/f'{s}_targets.parquet') for s in ['val','test']}
    targets.update({s:targets['val'].iloc[ids].reset_index(drop=True) for s,ids in selection.items()})

    def metrics(folder,stage):
        metric=read(folder/f'{stage}_metrics.json')
        assert metric['program_sha256']==sha(folder/'program.json') and metric['model_sha256']==sha(folder/'model.txt')
        assert metric['predictions_sha256']==sha(folder/f'{stage}_predictions.npy')
        pred=np.load(folder/f'{stage}_predictions.npy')
        np.testing.assert_array_equal(np.load(folder/f'{stage}_users.npy'),targets[stage].customer_id.to_numpy())
        assert metric['full_catalog']==5000 and metric['pairs']==len(targets[stage])*5000
        assert ((pred>=0)&(pred<5000)).all()
        ap=ap12(pred,targets[stage].article_id)
        assert float(ap.mean())==metric['map']
        np.testing.assert_array_equal(ap,np.load(folder/f'{stage}_ap.npy'))
        return metric,ap

    arm=source/('gpt61sol_python' if args.python else 'gpt61sol_full_sql')
    trials=read(arm/'search_state.json')['trials']
    valid=[t for t in trials if t['status']=='valid']
    assert len(valid)==20
    seen={}
    rejection_review=[]
    for n,trial in enumerate(trials,1):
        assert trial['call']==n and trial['island']==trial['proposal']%3
        folder=arm/'candidates'/f'candidate_{n:03d}'
        response=read(folder/'response.json')
        assert response['seed']==42+n-1 and response['provider_model']==config['model_id']
        attempt=source/'api_attempts'/f"attempt_{response['api_attempt']:03d}"
        payload=read(attempt/'request.json')
        assert payload['model']==config['model_id'] and payload['max_tokens']==2048
        assert payload['temperature']==.8 and payload['seed']==response['seed'] and payload['reasoning_effort']=='low'
        assert payload['messages'][1]['content']==(folder/'prompt.txt').read_text()
        if trial['status']=='valid':
            program=validate_program(read(folder/'program.json'))
            key=program_key(program)
            assert key==trial['program_key'] and key not in seen
            seen[key]=n
            schema=read(folder/'feature_schema.json')
            assert schema['train_pairs']==72813 and schema['train_pair_sha256']==manifest['train_pair_sha256']
            assert schema['preflight']['passed'] and schema['preflight']['batch_invariance']
            if args.python:assert schema['preflight']['empty_history'] and schema['preflight']['absent_groups']
            metric,_=metrics(folder,'search')
            assert metric['map']==trial['score']
        elif trial['status']=='duplicate':assert trial['program_key'] in seen
        elif args.python and trial['status']=='rejected':
            stage=trial['failure_stage']
            review={'call':n,'stage':stage,'error':trial['error']}
            try:
                parse(response['text'])
            except (ValueError,SyntaxError) as error:
                assert stage=='parse_and_validate'
                review.update(classification='documented_static_contract_or_syntax',reproduced=True,
                              independent_parse_error=str(error))
            else:
                assert stage in {'preflight','training_and_search'}
                review.update(classification='requires_separate_reproduction',reproduced=False)
            rejection_review.append(review)
    attempts=list((source/'api_attempts').glob('attempt_*'))
    assert len(attempts)<=300
    if args.corrected:
        assert len(attempts)==config['source_api_attempts'] and config['additional_api_requests']==0
    elif args.python:
        assert len(attempts)==len(trials)+len(list((source/'api_attempts').glob('*/failure.json')))
    else:assert len(attempts)==len(trials)
    if not args.python:assert not list((source/'api_attempts').glob('*/failure.json'))
    selected=read(arm/'selected.json')
    top3=sorted(valid,key=lambda t:(-t['score'],t['call']))[:3]
    assert [t['call'] for t in selected['confirmation']]==[None]+[t['call'] for t in top3]
    def local(path):return source/'raw_control' if Path(path).name=='raw_control' else arm/'candidates'/Path(path).name
    for candidate in selected['confirmation']:
        metric,_=metrics(local(candidate['directory']),'confirm')
        assert metric['map']==candidate['confirmation_map']
    assert max(selected['confirmation'],key=lambda t:t['confirmation_map'])['directory']==selected['directory']
    folder=local(selected['directory'])
    assert sha(folder/'model.txt')==selected['model_sha256'] and sha(folder/'program.json')==selected['program_sha256']
    rows,quality=[],{}
    for label,where in [('Raw15',source/'raw_control'),('GPT61Sol',folder)]:
        row={'model':label,'source':str(where.relative_to(ROOT))}
        quality[label]={}
        for stage in ['search','confirm','heldout_val','val','test']:
            metric,ap=metrics(where,stage)
            row[stage+'_map_percent']=100*metric['map']
            quality[label][stage]=ap.tolist()
        rows.append(row)
        if label=='Raw15':
            oldraw=ROOT/'reports/hm_small_llms_v1/exports/qwen_llama/raw_control'
            assert sha(where/'model.txt')==sha(oldraw/'model.txt')
            for stage in ['val','test']:assert sha(where/f'{stage}_predictions.npy')==sha(oldraw/f'{stage}_predictions.npy')
        destination=OUT/'independent_replay'/label
        destination.mkdir(parents=True,exist_ok=True)
        for name in ['program.json','model.txt','val_metrics.json','test_metrics.json']:shutil.copy2(where/name,destination/name)
        for stage in ['val','test']:
            result=destination/f'replay_{stage}_metrics.json'
            if not result.exists():
                env={k:v for k,v in os.environ.items() if not any(s in k.upper() for s in ['TOKEN','SECRET','API_KEY'])}
                env.update(CUDA_VISIBLE_DEVICES='',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
                command=[sys.executable,str(source/'runtime_sources/worker.py'),'--data',str(DATA),'--directory',str(destination),
                         '--stage','replay_'+stage,'--config',str(source/'run_config.json')]
                with (destination/f'replay_{stage}.log').open('w') as log:
                    completed=subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=1800)
                assert completed.returncode==0,(destination,stage)
            replay=read(result)
            assert replay['passed'] and replay['predictions_sha256']==sha(where/f'{stage}_predictions.npy')
            np.testing.assert_array_equal(np.load(destination/f'replay_{stage}_predictions.npy'),np.load(where/f'{stage}_predictions.npy'))
        print('Independent replay passed:',label,flush=True)
    pd.DataFrame(rows).to_csv(OUT/'comparison.csv',index=False)
    write(OUT/'quality.json',quality)
    paid_responses=[read(p) for p in sorted((arm/'candidates').glob('*/response.json'))]
    assert len(paid_responses)==len(attempts)-(len(list((source/'api_attempts').glob('*/failure.json'))) if args.python else 0)
    assert all(r.get('prompt_tokens',0)<=6144 and r.get('generated_tokens',0)<=2048 for r in paid_responses)
    stats={'calls':len(attempts),'api_attempts':len(attempts),'evaluated_candidate_responses':len(trials),
           'outside_corrected_pool':len(attempts)-len(trials) if args.corrected else 0,'statuses':dict(Counter(t['status'] for t in trials)),
           'repairs':sum(t['repair']>0 for t in trials),'generation_minutes':sum(t.get('seconds',0) for t in paid_responses)/60,
           'prompt_tokens':sum(t.get('prompt_tokens',0) for t in paid_responses),'completion_tokens':sum(t.get('generated_tokens',0) for t in paid_responses),
           'max_input_tokens':max(t.get('prompt_tokens',0) for t in paid_responses),'max_completion_tokens':max(t.get('generated_tokens',0) for t in paid_responses),
           'truncated':sum(t.get('truncated',False) for t in trials),'selected_call':selected['call'],
           'failure_stages':dict(Counter(t.get('failure_stage') for t in trials if t['status']=='rejected'))}
    if args.python:
        stats['api_failures']=[read(p) for p in sorted((source/'api_attempts').glob('*/failure.json'))]
        stats['api_failures_count']=len(stats['api_failures'])
        write(OUT/'rejection_review_initial.json',rejection_review)
    audit={'status':'passed','run_id':source.name,'source_directory':str(source),'config':config,'matched_tree_fields':matched,
           'full_SQL_sources_match':not (args.corrected or args.python),'boolean_validator_patch_verified':args.corrected,
           'raw_control_identical':True,'all20_programs_checked':True,
           'top3_confirmation_selection_checked':True,'independent_replays_passed':True,'stats':stats,
           'selected':selected,'selected_SQL':(folder/('program.py' if args.python else 'program.sql')).read_text(),'test_previously_inspected':True,
           'scope':('API full Python compared with the same provider/model SQL and historical JSON models' if args.python else 'API full SQL; old Qwen7B/H003 used JSON DSL, actual Qwen full-SQL results not yet available'),
           'seconds':time.perf_counter()-tick}
    if args.python:
        audit['selected_Python']=audit.pop('selected_SQL')
        audit['validator_regression']=read(source/'validator_verification.json')
        audit['rejection_review_initial']=rejection_review
    write(OUT/'audit.json',audit)
    print(json.dumps(stats,indent=2),flush=True)
    print(pd.DataFrame(rows).to_string(index=False),flush=True)


if __name__=='__main__':main()
