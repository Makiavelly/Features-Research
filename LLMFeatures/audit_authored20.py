"""Independent audit: exactly20 decisions, adaptive parents, metrics and replay.

No training, provider requests or feature changes are performed here.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/kaggle_hm_small_sql_compare_v1'
OUT=ROOT/'reports/authored20_v1'


def read(path):return json.loads(Path(path).read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()


def main():
    info=read(OUT/'current_run.json');assert info['status']=='finished'
    source=Path(info['directory']);config=read(source/'run_config.json')
    assert source.name==config['protocol']+'_'+digest(config)[:12]
    state=read(source/'state.json')
    assert state['committed']==state['evaluated']==len(state['trials'])==20
    assert [t['call'] for t in state['trials']]==list(range(1,21))
    assert state['api_requests']==config['provider_api_requests']==0
    assert not (source/'api_attempts').exists()
    assert len(list((source/'codex_authored20/candidates').glob('*/model.txt')))==20
    assert len(list((source/'codex_authored20/candidates').glob('*/program.json')))==20
    for name,value in config['runtime_sha256'].items():assert sha(source/'runtime_sources'/name)==value
    for name in ['worker.py','python_features.py','base_features.py','features.py']:
        assert sha(source/'runtime_sources'/name)==sha(ROOT/'LLMFeatures/provider_python_runtime_v2'/name)
    old_config=read(ROOT/'LLMFeatures/results'/config['raw_reference_run']/'run_config.json')
    matched=['seed','train_pairs','train_pair_sha256','bundle_manifest_sha256','lightgbm_rounds',
             'cpu_threads','scoring_user_batch','search_users','confirmation_users','heldout_val_users',
             'validation_users','test_users','evaluation_catalog']
    assert all(config[k]==old_config[k] for k in matched)
    assert sha(DATA/'manifest.json')==config['bundle_manifest_sha256']
    manifest=read(DATA/'manifest.json')
    for name,value in manifest['files'].items():assert sha(DATA/name)==value
    sys.path.insert(0,str(source/'runtime_sources'))
    from worker import ap12
    from python_features import FeatureEngine,validate_program,program_key
    from authored20_design import program as build_program
    selection=read(DATA/'selection.json')
    targets={s:pd.read_parquet(DATA/f'{s}_targets.parquet') for s in ['val','test']}
    for name,indices in selection.items():targets[name]=targets['val'].iloc[indices].reset_index(drop=True)
    def metrics(directory,stage):
        value=read(directory/f'{stage}_metrics.json')
        assert value['program_sha256']==sha(directory/'program.json')
        assert value['model_sha256']==sha(directory/'model.txt')
        assert value['predictions_sha256']==sha(directory/f'{stage}_predictions.npy')
        pred=np.load(directory/f'{stage}_predictions.npy')
        assert ((pred>=0)&(pred<5000)).all()
        np.testing.assert_array_equal(np.load(directory/f'{stage}_users.npy'),targets[stage].customer_id)
        ap=ap12(pred,targets[stage].article_id)
        np.testing.assert_array_equal(ap,np.load(directory/f'{stage}_ap.npy'))
        assert float(ap.mean())==value['map']
        return value,ap
    pairs=pd.read_parquet(DATA/'train_pairs.parquet')
    chain=[json.loads(line) for line in (source/'commit_chain.jsonl').read_text().splitlines()]
    assert len(chain)==20
    previous='0'*64
    raw_score=metrics(source/'raw_control','search')[0]['map']
    parents=[{'call':None,'score':raw_score} for i in range(3)]
    numeric=[];programs=[];rows=[]
    engine=FeatureEngine(OUT/'audit_scratch',DATA)
    try:
        for trial,entry in zip(state['trials'],chain):
            number=trial['call'];island=(number-1)%3
            directory=source/'codex_authored20/candidates'/f'candidate_{number:03d}'
            proposal=read(directory/'proposal.json')
            assert entry['previous']==previous
            assert digest({'previous':previous,'proposal':proposal})==entry['hash']
            assert proposal==entry['proposal']
            previous=entry['hash']
            assert trial['island']==proposal['island']==island
            assert proposal['parent_call']==trial['parent_call']==parents[island]['call']
            assert proposal['parent_search_map']==parents[island]['score']
            assert proposal['program_sha256']==sha(directory/'program.json')
            assert proposal['source_sha256']==sha(directory/'program.py')
            program=validate_program(read(directory/'program.json'))
            assert program['code']==build_program(proposal['features'])==(directory/'program.py').read_text()
            assert program_key(program)==trial['program_key']
            programs.append(trial['program_key'])
            assert 1<=len(proposal['features'])<=36
            schema=read(directory/'feature_schema.json')
            assert schema['train_pairs']==72813 and schema['train_pair_sha256']==config['train_pair_sha256']
            assert all(schema['preflight'][k] for k in ['passed','row_permutation','batch_invariance','empty_history','absent_groups'])
            parts=[]
            for cutoff,frame in pairs.groupby('timestamp',sort=True):
                engine.prepare(cutoff,frame.customer_id.values,program)
                parts.append(engine.matrix(frame))
            matrix=np.concatenate(parts)
            columns=[hashlib.sha256(np.ascontiguousarray(matrix[:,i]).tobytes()).hexdigest() for i in range(matrix.shape[1])]
            signature=hashlib.sha256(''.join(sorted(columns)).encode()).hexdigest()
            assert signature==trial['numeric_signature']==read(directory/'matrix_verification.json')['numeric_signature']
            numeric.append(signature)
            assert engine.feature_names==schema['features']
            search,_=metrics(directory,'search');assert search['map']==trial['score']
            if trial['score']>parents[island]['score']:parents[island]=trial
            rows.append({'call':number,'island':island,'parent_call':trial['parent_call'],
                         'description':proposal['description'],'features':len(proposal['features']),
                         'search_map_percent':100*trial['score']})
            print('Audited candidate',number,'adaptive parent and numeric matrix verified',flush=True)
    finally:engine.close()
    assert previous==state['commit_chain_head'] and len(set(numeric))==len(set(programs))==20
    selected=read(source/'codex_authored20/selected.json')
    top3=sorted(state['trials'],key=lambda t:(-t['score'],t['call']))[:3]
    assert [c['call'] for c in selected['confirmation']]==[None]+[c['call'] for c in top3]
    def folder(path):return source/'raw_control' if Path(path).name=='raw_control' else source/'codex_authored20/candidates'/Path(path).name
    for trial in selected['confirmation']:
        value,_=metrics(folder(trial['directory']),'confirm')
        assert value['map']==trial['confirmation_map']
    assert max(selected['confirmation'],key=lambda t:t['confirmation_map'])['call']==selected['call']
    winner=folder(selected['directory'])
    assert sha(winner/'program.json')==selected['program_sha256'] and sha(winner/'model.txt')==selected['model_sha256']
    comparison=[];quality={}
    for label,directory in [('Raw15',source/'raw_control'),('CodexAuthored20',winner)]:
        row={'model':label,'source':str(directory.relative_to(ROOT))};quality[label]={}
        for stage in ['search','confirm','heldout_val','val','test']:
            value,ap=metrics(directory,stage);row[stage+'_map_percent']=100*value['map'];quality[label][stage]=ap.tolist()
        comparison.append(row)
        destination=OUT/'independent_replay'/label;destination.mkdir(parents=True,exist_ok=True)
        for name in ['program.json','model.txt','val_metrics.json','test_metrics.json']:shutil.copy2(directory/name,destination/name)
        for stage in ['val','test']:
            if not (destination/f'replay_{stage}_metrics.json').exists():
                env={k:v for k,v in os.environ.items() if not any(s in k.upper() for s in ['TOKEN','SECRET','API_KEY'])}
                env.update(CUDA_VISIBLE_DEVICES='',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
                command=[sys.executable,str(source/'runtime_sources/worker.py'),'--data',str(DATA),'--directory',str(destination),
                         '--stage','replay_'+stage,'--config',str(source/'run_config.json')]
                with (destination/f'{stage}.log').open('w') as handle:
                    completed=subprocess.run(command,env=env,stdout=handle,stderr=subprocess.STDOUT,timeout=1800)
                assert completed.returncode==0,(label,stage)
            replay=read(destination/f'replay_{stage}_metrics.json')
            assert replay['passed'] and replay['predictions_sha256']==sha(directory/f'{stage}_predictions.npy')
        print('Independent frozen replay passed:',label,flush=True)
    reference=ROOT/'LLMFeatures/results'/config['raw_reference_run']/'raw_control'
    for name in ['model.txt','search_predictions.npy','val_predictions.npy','test_predictions.npy']:
        assert sha(source/'raw_control'/name)==sha(reference/name)
    pd.DataFrame(rows).to_csv(OUT/'all20_search.csv',index=False)
    pd.DataFrame(comparison).to_csv(OUT/'comparison.csv',index=False)
    (OUT/'quality.json').write_text(json.dumps(quality,indent=2))
    result={'status':'passed','run_id':source.name,'source_directory':str(source),
            'exactly20_committed':True,'exactly20_models':True,'numeric_distinct_sets':20,
            'island_counts':[sum(t['island']==i for t in state['trials']) for i in range(3)],
            'adaptive_parents_verified':True,'commit_hash_chain_verified':True,'same_downstream_sources':True,
            'raw_control_identical':True,'independent_replays':True,'matched_fields':matched,
            'selected':selected,'api_requests':0,'kernel_verification':read(OUT/'kernel_verification.json'),
            'identity_attested':False,'test_previously_inspected':True,
            'limitations':['Assistant has prior experiment history','Assistant context/output budgets are not identical to provider calls',
                           'Results cannot establish provider model identity','One seed and previously inspected250-user test']}
    (OUT/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(pd.DataFrame(comparison).to_string(index=False))


if __name__=='__main__':main()
