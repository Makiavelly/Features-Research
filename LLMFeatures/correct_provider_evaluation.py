"""Correct a validator bug on the saved generation stream; never call the API.

Not an independent LLM run: prompts/proposals remain those actually generated
under v1. Re-evaluate the chronological first20 distinct valid programs, preserving
both the original run and any responses outside the corrected20-program budget.
"""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record


def main():
    current=json.loads((ROOT/'reports/provider_small_v1/current_run.json').read_text())
    assert current['status']=='finished','Wait for original generation stream to finish'
    original=Path(current['directory'])
    old_config=json.loads((original/'run_config.json').read_text())
    old_trials=json.loads((original/'gpt61sol_full_sql/search_state.json').read_text())['trials']
    modules={p.name:p.read_text() for p in (original/'runtime_sources').glob('*.py')}
    assert '\nNUMERIC_TYPE = ' in modules['full_sql.py']
    modules['full_sql.py']=modules['full_sql.py'].replace('\nNUMERIC_TYPE = ',
        "\n# SQLGlot models standard Boolean syntax as Func nodes. These are not external functions.\nFUNCTIONS.update({'AND','OR','NOT','IN','BETWEEN','IS'})\nNUMERIC_TYPE = ",1)
    modules['correct_provider_evaluation.py']=Path(__file__).read_text()
    code=ROOT/'LLMFeatures/provider_sql_corrected_runtime_v2'
    code.mkdir(exist_ok=True)
    for name,text in modules.items():(code/name).write_text(text,encoding='utf-8')
    sys.path.insert(0,str(code))
    import runtime
    from full_sql import parse,program_key
    # Binding regression: valid standard predicates must not be treated as functions.
    for predicate in ['days_ago<=7 AND sales_channel_id=1',
                      'days_ago<=7 OR sales_channel_id=1',
                      'NOT (days_ago>7)', 'days_ago BETWEEN 1 AND 7',
                      'sales_channel_id IN (1,2)', 'price IS NOT NULL']:
        parse('SELECT customer_id,count(*) FILTER(WHERE '+predicate+') AS f_count FROM history GROUP BY customer_id')
    config={**old_config,'protocol':'hm_small_gpt61sol_full_sql_corrected_eval_v2',
            'source_run':original.name,'evaluation_replay_only':True,'additional_api_requests':0,
            'source_api_attempts':len(list((original/'api_attempts').glob('attempt_*'))),
            'candidate_pool':'chronological first20 distinct valid from the original generation stream',
            'validator_patch':'Allow standard Boolean AND/OR/NOT/IN/BETWEEN/IS AST nodes; identified before v1 final test',
            'runtime_sha256':{n:hashlib.sha256(s.encode()).hexdigest() for n,s in modules.items()}}
    fingerprint=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()[:12]
    out=ROOT/'LLMFeatures/results'/(config['protocol']+'_'+fingerprint)
    if not out.exists():
        shutil.copytree(original,out,ignore=shutil.ignore_patterns('scratch'))
        shutil.copy2(out/'run_config.json',out/'original_generation_config.json')
        shutil.copy2(out/'gpt61sol_full_sql/search_state.json',out/'original_generation_state.json')
        shutil.copy2(out/'gpt61sol_full_sql/selected.json',out/'original_selected.json')
    runtime.write(out/'run_config.json',config)
    for name,text in modules.items():(out/'runtime_sources'/name).write_text(text,encoding='utf-8')
    data=ROOT/'data/kaggle_hm_small_sql_compare_v1'
    config_path=out/'run_config.json'
    arm=out/'gpt61sol_full_sql'
    trials,seen=[],set()
    for old in old_trials:
        folder=arm/'candidates'/f"candidate_{old['call']:03d}"
        trial=copy.deepcopy(old)
        trial.update(directory=str(folder),original_status=old['status'],evaluation_replayed=True)
        response=json.loads((folder/'response.json').read_text())
        stage='parse_and_validate'
        try:
            if response.get('truncated'):raise ValueError('Original output truncated')
            program=parse(response['text'])
            key=program_key(program)
            trial['program_key']=key
            runtime.write(folder/'program.json',program)
            if key in seen:
                trial.update(status='duplicate',failure_stage='deduplication',error='Duplicate under corrected validation')
            else:
                stage='preflight'
                runtime.evaluate(data,folder,'preflight',config_path)
                stage='training_and_search'
                metric=runtime.evaluate(data,folder,'search',config_path)
                trial.update(status='valid',program=program,score=metric['map'])
                (folder/'program.sql').write_text(runtime.render(program),encoding='utf-8')
                for name in ['error','failure_stage','diagnostic_queries']:trial.pop(name,None)
                if old['status']=='rejected':
                    for name in ['diagnostics.json','error.txt']:
                        path=folder/name
                        if path.exists():path.rename(folder/('original_'+name))
                seen.add(key)
        except Exception as error:
            trial.update(status='rejected',error=str(error),failure_stage=stage)
        runtime.write(folder/'trial.json',trial)
        trials.append(trial)
        if trial['status']!=old['status']:
            print('Reclassified call',trial['call'],old['status'],'->',trial['status'],flush=True)
        if len(seen)==20:break
    assert len(seen)==20
    valid=sorted([t for t in trials if t['status']=='valid'],key=lambda t:(-t['score'],t['call']))
    candidates=[{'directory':str(out/'raw_control'),'call':None}]+valid[:3]
    confirmation=[]
    for candidate in candidates:
        metric=runtime.evaluate(data,candidate['directory'],'confirm',config_path)
        confirmation.append(dict(directory=candidate['directory'],call=candidate['call'],confirmation_map=metric['map']))
    winner=max(confirmation,key=lambda t:t['confirmation_map'])
    chosen=Path(winner['directory'])
    selected={**winner,'selection':'top3 search plus raw -> disjoint confirmation88; corrected saved-stream evaluation',
              'program_sha256':runtime.sha(chosen/'program.json'),'model_sha256':runtime.sha(chosen/'model.txt'),
              'successful_distinct':20,'budget_complete':True,'llm_calls':len(trials),'confirmation':confirmation,
              'actual_original_api_requests':config['source_api_attempts'],'additional_api_requests':0}
    runtime.write(arm/'selected.json',selected)
    runtime.progress(arm,trials,config)
    runtime.write(out/'correction.json',{
        'source_run':original.name,'additional_api_requests':0,'independent_LLM_run':False,
        'original_statuses':dict(Counter(t['status'] for t in old_trials)),
        'corrected_statuses':dict(Counter(t['status'] for t in trials)),
        'reclassified_calls':[t['call'] for t in trials if t['status']!=t['original_status']],
        'unused_original_response_calls':[t['call'] for t in old_trials[len(trials):]],
        'policy':'First20 distinct valid after corrected validation; original prompts/repair history retained, not regenerated',
        'reused_models':'Unchanged previously trained SQL programs reuse exact saved models/search predictions; reclassified valid program is trained now',
        'regression_tests':'AND/OR/NOT/IN/BETWEEN/IS on past-only empty schema passed'})
    record('provider_corrected_evaluation_selected','Исправленныйsaved-streamreplay:первые20валидных,selectionпоvalidationзафиксирован. ДополнительныхAPIвызовов0;этоНЕнезависимыйLLMпрогон.',
           out.name,status='evaluating',artifacts=str(out.relative_to(ROOT)),source_run=original.name)
    runtime.finish(data,out,config_path)
    runtime.write(ROOT/'reports/provider_small_v1/corrected_run.json',{'run_id':out.name,'directory':str(out),'status':'finished'})
    print('Corrected evaluation finished:',out.name,flush=True)


if __name__=='__main__':main()
