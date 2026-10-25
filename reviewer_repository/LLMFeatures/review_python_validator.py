"""Review saved model programs inside the existing restricted execution path.

No API calls or training. Uses only past training examples, never test targets.
"""
from collections import Counter
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/kaggle_hm_small_sql_compare_v1'


def main():
    current=json.loads((ROOT/'reports/provider_python_v1/current_run.json').read_text())
    source=Path(current['directory'])
    config=json.loads((source/'run_config.json').read_text())
    sys.path.insert(0,str(source/'runtime_sources'))
    from python_features import parse,compile_function,construct,FeatureEngine
    from worker import preflight
    arm=source/'gpt61sol_python'
    trials=json.loads((arm/'search_state.json').read_text())['trials']
    out=ROOT/'reports/gpt61sol_python_v1'
    out.mkdir(exist_ok=True)
    pairs=pd.read_parquet(DATA/'train_pairs.parquet')
    cutoff=pairs.timestamp.min()
    sample=pairs[pairs.timestamp==cutoff].head(96).copy()
    engine=FeatureEngine(out/'validator_review_scratch',DATA)
    records=[]
    try:
        for trial in trials:
            directory=arm/'candidates'/f"candidate_{trial['call']:03d}"
            response=json.loads((directory/'response.json').read_text())
            record={'call':trial['call'],'original_status':trial['status']}
            try:
                program=parse(response['text'])
            except ValueError as error:
                # Compilation does not execute model code: distinguish syntax from policy.
                text=response['text'].strip()
                if text.startswith('```'):
                    text='\n'.join(text.splitlines()[1:-1])
                try:compile(text,'<unrestricted-diagnostic>','exec')
                except SyntaxError as syntax:
                    reason='python_syntax_error';detail=f'{syntax.msg}, line {syntax.lineno}'
                else:
                    reason='documented_static_contract_restriction';detail=str(error)
                assert trial['status']=='rejected',trial
                record.update(classification=reason,reproduced=True,detail=detail)
                records.append(record)
                continue
            if trial['status']=='duplicate':
                record.update(classification='structural_AST_duplicate',reproduced=True)
            elif trial['status']=='rejected':
                # Independently inspect actual returned column sets, without
                # invoking the wrapper's expected-schema comparison.
                engine.prepare(cutoff,sample.customer_id.values,program)
                engine.names=None
                raw=super(FeatureEngine,engine).frame(sample)
                X=pd.concat([sample[['customer_id','article_id']].reset_index(drop=True),raw],axis=1)
                function=compile_function(program)
                try:
                    full=construct(function,X,engine.history)
                    empty=construct(function,X,engine.history.iloc[:0])
                except Exception:
                    full=empty=None
                if full is not None and set(full)!=set(empty):
                    record.update(classification='model_schema_changes_with_empty_history',reproduced=True,
                                  only_nonempty=sorted(set(full)-set(empty)),
                                  only_empty=sorted(set(empty)-set(full)),
                                  detail='Ordinary Python syntax is valid; returned feature names violate the documented fixed-schema contract. The actual dataset cutoffs have nonempty global history.')
                    records.append(record)
                    print('Reviewed call',trial['call'],record['classification'],flush=True)
                    continue
                # Re-run the exact failing worker stage under another output directory.
                destination=out/'rejection_replay'/directory.name
                destination.mkdir(parents=True,exist_ok=True)
                (destination/'program.json').write_text(json.dumps(program))
                stage='preflight' if trial['failure_stage']=='preflight' else 'search'
                env={k:v for k,v in os.environ.items() if not any(s in k.upper() for s in ['TOKEN','SECRET','API_KEY'])}
                env.update(CUDA_VISIBLE_DEVICES='',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
                command=[sys.executable,str(source/'runtime_sources/worker.py'),'--data',str(DATA),
                         '--directory',str(destination),'--stage',stage,'--config',str(source/'run_config.json')]
                with (destination/'reproduction.log').open('w') as log:
                    result=subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=1800)
                error=(destination/'reproduction.log').read_text()
                record.update(classification='runtime_failure_requires_manual_review',
                              reproduced=result.returncode!=0,detail=error[-3500:])
                if result.returncode==0:
                    record['classification']='possible_false_rejection_or_transient_host_failure'
            else:
                engine.prepare(cutoff,sample.customer_id.values,program)
                names=engine.names
                # Obtain X with exactly the host raw encodings.
                original_names=engine.names
                engine.names=None
                raw=super(FeatureEngine,engine).frame(sample)
                engine.names=original_names
                X=pd.concat([sample[['customer_id','article_id']].reset_index(drop=True),raw],axis=1)
                history=engine.history
                guarded=compile_function(program)
                normal=construct(guarded,X,history)
                schema=list(normal)
                empty=construct(guarded,X,history.iloc[:0],expected=schema)
                # Exercise absent groups and non-default row labels.
                unknown=X.iloc[:4].copy()
                unknown.index=pd.Index([91,7,28,3])
                unknown['customer_id']=1000000+np.arange(len(unknown))
                unknown['article_id']=2000000+np.arange(len(unknown))
                construct(guarded,unknown,history,expected=schema)
                preflight(engine,pairs,program)
                record.update(classification='accepted_extra_contract_checks_passed',reproduced=True,
                              features=len(schema),empty_history_passed=True,absent_groups_passed=True,
                              permutation_and_batch_passed=True)
            records.append(record)
            print('Reviewed call',trial['call'],record['classification'],flush=True)
    finally:engine.close()
    unresolved=[r for r in records if r['classification'] in {
        'runtime_failure_requires_manual_review','possible_false_rejection_or_transient_host_failure'}]
    result={'status':'requires_manual_review' if unresolved else 'passed',
            'calls_reviewed':len(records),'counts':dict(Counter(r['classification'] for r in records)),
            'records':records,'api_calls':0,
            'note':'Model code is only executed via the existing restricted wrapper. Unrestricted exec was rejected by automatic safety review and not performed. Numeric references are separately auditor-authored. Regression evidence cannot prove absence of every validator defect.'}
    (out/'validator_review.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))


if __name__=='__main__':main()
