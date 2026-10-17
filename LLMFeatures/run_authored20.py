"""H007: exactly20 adaptively authored Codex feature sets, three populations.

Feature decisions are supplied by the current assistant, not an external API or
an automated generator. Commit before fitness; never add a twenty-first model.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/kaggle_hm_small_sql_compare_v1'
REGISTRY=ROOT/'reports/authored20_v1/current_run.json'
FROZEN=ROOT/'LLMFeatures/provider_python_runtime_v2'
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record
from authored20_design import program as build_program


def read(path):return json.loads(Path(path).read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()
def write(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(path)


def prepare():
    modules={n:(FROZEN/n).read_text() for n in ['base_features.py','python_features.py','features.py','worker.py','runtime.py','prompting.py']}
    modules['authored20_design.py']=(ROOT/'LLMFeatures/authored20_design.py').read_text()
    modules['run_authored20.py']=Path(__file__).read_text()
    previous=read(ROOT/'reports/provider_python_v1/current_run.json')
    base=read(Path(previous['directory'])/'run_config.json')
    manifest=read(DATA/'manifest.json')
    assert sha(DATA/'manifest.json')==base['bundle_manifest_sha256']
    for name,digest_value in manifest['files'].items():assert sha(DATA/name)==digest_value
    config={k:base[k] for k in ['seed','train_pairs','train_pair_sha256','bundle_manifest_sha256',
        'lightgbm_rounds','cpu_threads','scoring_user_batch','evaluation_timeout_seconds','search_users',
        'confirmation_users','heldout_val_users','validation_users','test_users','evaluation_catalog','versions']}
    config.update(protocol='hm_small_codex_authored20_adaptive_seed42_v1',arms=['codex_authored20'],arm='codex_authored20',
                  planned_sets=20,islands=3,parent_rule='highest_search_MAP_in_own_island_or_raw; stable ties prefer earlier',
                  author='current Codex session; exact underlying model independently unverified',
                  provider_api_requests=0,feature_interface='same complete Python modify_features(X,history)',
                  max_python_features=36,feature_call_timeout_seconds=60,worker_address_space_gb=8,
                  test_previously_inspected=True,prior_experiment_results_known_to_author=True,
                  output_token_limit=None,assistant_context_not_matched_to_provider_prompt=True,
                  proposal_mode='assistant-authored adaptive decisions after observed search fitness; exactly20 total across3islands',
                  runtime_sha256={n:hashlib.sha256(s.encode()).hexdigest() for n,s in modules.items()},
                  raw_reference_run=Path(previous['directory']).name)
    out=ROOT/'LLMFeatures/results'/(config['protocol']+'_'+digest(config)[:12])
    out.mkdir(parents=True,exist_ok=True)
    if (out/'run_config.json').exists():assert read(out/'run_config.json')==config
    write(out/'run_config.json',config)
    code=out/'runtime_sources';code.mkdir(exist_ok=True)
    for name,text in modules.items():(code/name).write_text(text,encoding='utf-8')
    for name in ['manifest.json','selection.json']:shutil.copy2(DATA/name,out/('input_'+name))
    raw=out/'raw_control'
    if not raw.exists():shutil.copytree(Path(previous['directory'])/'raw_control',raw,ignore=shutil.ignore_patterns('scratch'))
    if not (out/'state.json').exists():
        write(out/'state.json',{'planned_sets':20,'trials':[],'committed':0,'evaluated':0,'api_requests':0})
        record('authored20_protocol_registered',
               'H007: пользователь поручил текущей сессии Codex самостоятельно написать и оценить ровно20 наборов. '
               'Адаптивный поиск по3популяциям, выбор родителей поsearch. Те же72813пары/LightGBM150/31/4CPU/seed42. '
               'Точная модель сессии не аттестована; сравнение не доказывает подмену провайдером. '
               'Текущая сессия знает историю, ограничение2048токенов к ней не применяется. '
               'Черновики не обучались; только20зафиксированных перед оценкой предложений будут оценены.',
               out.name,status='prepared',artifacts=str(out.relative_to(ROOT)),planned_sets=20,api_requests=0)
    write(REGISTRY,{'run_id':out.name,'directory':str(out),'status':'prepared'})
    print('Run:',out.name,flush=True)
    return out


def load():
    out=Path(read(REGISTRY)['directory'])
    config=read(out/'run_config.json')
    for name,value in config['runtime_sha256'].items():assert sha(out/'runtime_sources'/name)==value
    sys.path.insert(0,str(out/'runtime_sources'))
    import runtime
    return out,config,runtime


def parent(state,island,raw_score):
    best={'call':None,'score':raw_score,'directory':'raw_control'}
    for trial in state['trials']:
        if trial['island']==island and trial.get('status')=='valid' and trial['score']>best['score']:
            best=trial
    return best


def commit(proposal_path):
    out,config,runtime=load()
    state=read(out/'state.json')
    assert state['committed']==state['evaluated'],'Evaluate the previous committed set before proposing another'
    number=state['committed']+1
    assert number<=20,'Exactly20 authored sets; a twenty-first is forbidden'
    proposal=read(proposal_path)
    assert proposal['call']==number and proposal['island']==(number-1)%3
    raw_score=read(out/'raw_control/search_metrics.json')['map']
    best=parent(state,proposal['island'],raw_score)
    assert proposal['parent_call']==best['call'],('Wrong adaptive parent',best)
    outputs=proposal['features']
    assert 1<=len(outputs)<=36 and len(outputs)==len(set(outputs))
    # Always build from the frozen implementation, not a changing live helper.
    import authored20_design as implementation
    assert sha(Path(implementation.__file__))==config['runtime_sha256']['authored20_design.py']
    from python_features import validate_program,program_key
    source=implementation.program(outputs)
    value=validate_program({'code':source})
    key=program_key(value)
    assert all(t['program_key']!=key for t in state['trials'])
    directory=out/'codex_authored20/candidates'/f'candidate_{number:03d}'
    assert not directory.exists()
    directory.mkdir(parents=True)
    write(directory/'program.json',value)
    (directory/'program.py').write_text(source,encoding='utf-8')
    proposal.update(committed_utc=datetime.now(timezone.utc).isoformat(),
                    parent_search_map=best['score'],program_sha256=sha(directory/'program.json'),
                    program_key=key,source_sha256=sha(directory/'program.py'))
    write(directory/'proposal.json',proposal)
    previous=state.get('commit_chain_head','0'*64)
    chain=digest({'previous':previous,'proposal':proposal})
    entry={'previous':previous,'proposal':proposal,'hash':chain}
    with (out/'commit_chain.jsonl').open('a',encoding='utf-8') as handle:
        handle.write(json.dumps(entry,ensure_ascii=False)+'\n')
    state['committed']=number;state['commit_chain_head']=chain
    state['pending']={'call':number,'directory':str(directory),'proposal':proposal}
    write(out/'state.json',state)
    record('authored20_candidate_committed',
           f"Зафиксирован набор{number}/20, популяция{proposal['island']}, родитель{proposal['parent_call']}. "
           f"{len(outputs)} новых признаков. Решение записано до получения егоMAP. "+proposal['rationale'],
           out.name,status='searching',committed_sets=number,evaluated_sets=state['evaluated'],api_requests=0)
    print(json.dumps(proposal,ensure_ascii=False,indent=2),flush=True)


def matrix_check(out,directory,config,runtime):
    from python_features import FeatureEngine
    from worker import preflight
    pairs=pd.read_parquet(DATA/'train_pairs.parquet')
    program=read(directory/'program.json')
    engine=FeatureEngine(directory/'matrix_scratch',DATA)
    try:
        checks=preflight(engine,pairs,program)
        parts=[]
        for cutoff,group in pairs.groupby('timestamp',sort=True):
            engine.prepare(cutoff,group.customer_id.values,program)
            parts.append(engine.matrix(group))
        values=np.concatenate(parts)
        column_hashes=[hashlib.sha256(np.ascontiguousarray(values[:,i]).tobytes()).hexdigest() for i in range(values.shape[1])]
        signature=hashlib.sha256(''.join(sorted(column_hashes)).encode()).hexdigest()
        assert all(t.get('numeric_signature')!=signature for t in read(out/'state.json')['trials']), 'Numerically duplicate feature set'
        write(directory/'matrix_verification.json',{'status':'passed','preflight':checks,'rows':len(values),
              'columns':values.shape[1],'feature_names':engine.feature_names,'numeric_signature':signature,
              'ordered_sha256':hashlib.sha256(values.tobytes()).hexdigest(),'labels_used_for_verification':False})
        return signature
    finally:engine.close()


def evaluate_pending():
    out,config,runtime=load();state=read(out/'state.json')
    pending=state['pending'];directory=Path(pending['directory']);proposal=pending['proposal']
    assert sha(directory/'program.json')==proposal['program_sha256']
    if (directory/'matrix_verification.json').exists():
        signature=read(directory/'matrix_verification.json')['numeric_signature']
    else:signature=matrix_check(out,directory,config,runtime)
    metric=runtime.evaluate(DATA,directory,'search',out/'run_config.json')
    trial={'call':pending['call'],'island':proposal['island'],'parent_call':proposal['parent_call'],
           'repair':0,'seconds':0,'generated_tokens':0,'elapsed_seconds':metric['seconds'],
           'status':'valid','score':metric['map'],'program_key':proposal['program_key'],
           'directory':str(directory),'numeric_signature':signature,'description':proposal['description']}
    write(directory/'trial.json',trial)
    state['trials'].append(trial);state['evaluated']=len(state['trials']);state.pop('pending')
    write(out/'state.json',state)
    write(out/'codex_authored20/search_state.json',{'calls':len(state['trials']),'measured':len(state['trials']),
          'target':20,'trials':state['trials']})
    record('authored20_candidate_evaluated',
           f"Набор{trial['call']}/20 оценён: searchMAP@12 {100*trial['score']:.6f}%, популяция{trial['island']}. "
           'Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.',
           out.name,status='searching',evaluated_sets=state['evaluated'],committed_sets=state['committed'],api_requests=0)
    print('EVALUATED:',json.dumps(trial,ensure_ascii=False),flush=True)
    print('POPULATION BESTS:',json.dumps([parent(state,i,read(out/'raw_control/search_metrics.json')['map']) for i in range(3)],ensure_ascii=False),flush=True)


def finish():
    out,config,runtime=load();state=read(out/'state.json')
    assert state['committed']==state['evaluated']==20 and len(state['trials'])==20
    assert len({t['numeric_signature'] for t in state['trials']})==20
    arm=out/'codex_authored20'
    selected_path=arm/'selected.json'
    if not selected_path.exists():
        top=sorted(state['trials'],key=lambda t:(-t['score'],t['call']))[:3]
        confirmation=[]
        for trial in [{'call':None,'directory':str(out/'raw_control')}]+top:
            metric=runtime.evaluate(DATA,trial['directory'],'confirm',out/'run_config.json')
            confirmation.append({**trial,'confirmation_map':metric['map']})
        best=max(confirmation,key=lambda t:t['confirmation_map'])
        selected={**best,'confirmation':confirmation,'selection':'top3search plus raw -> disjointconfirmation88',
                  'program_sha256':sha(Path(best['directory'])/'program.json'),
                  'model_sha256':sha(Path(best['directory'])/'model.txt'),
                  'successful_distinct':20,'budget_complete':True,'llm_calls':0,'authored_sets':20}
        write(selected_path,selected)
        record('authored20_selection_frozen','Все20 наборов оценены. Победитель выбран поconfirmation88 до итоговой оценкиval/test.',
               out.name,status='evaluating',selected_call=best['call'],authored_sets=20,api_requests=0)
    frame=runtime.finish(DATA,out,out/'run_config.json')
    write(REGISTRY,{'run_id':out.name,'directory':str(out),'status':'finished'})
    record('authored20_finished_pending_audit','Ровно20 авторских наборов оценены, итоговаяоценка выполнена. Требуется независимыйаудит.',
           out.name,status='completed_pending_audit',authored_sets=20,api_requests=0,artifacts=str(out.relative_to(ROOT)))
    print(frame.to_string(index=False),flush=True)


def main():
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prepare',action='store_true')
    group.add_argument('--commit',type=Path)
    group.add_argument('--evaluate',action='store_true')
    group.add_argument('--finish',action='store_true')
    args=parser.parse_args()
    if args.prepare:prepare()
    elif args.commit:commit(args.commit)
    elif args.evaluate:evaluate_pending()
    else:finish()


if __name__=='__main__':main()
