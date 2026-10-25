"""Real remote GPT feature search on the frozen small-v1 full-SQL protocol."""
import argparse
import ast
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import sys
import traceback
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'LLMFeatures/kaggle/full_sql_small'
DATA=ROOT/'data/kaggle_hm_small_sql_compare_v1'
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record
from provider_api import ProviderGenerator,ProviderUnavailable


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base-url',default='https://tooken.club/v1')
    parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args()
    modules={n:(SOURCE/n).read_text() for n in ['base_features.py','features.py','full_sql.py','prompting.py','runtime.py','worker.py']}
    modules['runtime.py']=modules['runtime.py'].replace('qwen_full_sql','gpt61sol_full_sql').replace('Qwen7B full SQL','GPT6.1 Sol full SQL')
    modules['provider_api.py']=(ROOT/'LLMFeatures/provider_api.py').read_text()
    modules['run_provider_small.py']=Path(__file__).read_text()
    hashes={n:hashlib.sha256(s.encode()).hexdigest() for n,s in modules.items()}
    code=ROOT/'LLMFeatures/provider_small_runtime_v1'
    code.mkdir(exist_ok=True)
    for name,source in modules.items():
        ast.parse(source)
        (code/name).write_text(source,encoding='utf-8')
    sys.path.insert(0,str(code))
    import runtime
    manifest=json.loads((DATA/'manifest.json').read_text())
    expected=json.loads((SOURCE/'delivery_manifest.json').read_text())['bundle_manifest_sha256']
    assert sha(DATA/'manifest.json')==expected
    for name,digest in manifest['files'].items():assert sha(DATA/name)==digest
    config={'protocol':'hm_small_gpt61sol_full_sql_seed42_v1','arms':['gpt61sol_full_sql'],
            'arm':'gpt61sol_full_sql','seed':42,'target_successful_distinct':20,
            'max_llm_calls':300,'max_repairs_per_proposal':3,'islands':3,'memory_programs_per_prompt':1,
            'model_id':'gpt-6.1-sol','model_source':'tooken_club_api','base_url':args.base_url.rstrip('/'),
            'reasoning_effort':'low','temperature':.8,'max_input_tokens':6144,'max_new_tokens':2048,
            'sampling_seed_requested':True,'seed_guarantee':'provider implementation not controlled',
            'lightgbm_rounds':150,'cpu_threads':4,'scoring_user_batch':16,'evaluation_timeout_seconds':1800,
            'feature_interface':'complete_SQL_SELECT_queries_with_host_joins','max_sql_queries':6,'max_sql_features':36,
            'search_users':128,'confirmation_users':88,'heldout_val_users':88,'validation_users':304,
            'test_users':250,'evaluation_catalog':5000,'test_previously_inspected':True,
            'train_pairs':manifest['train_pairs'],'train_pair_sha256':manifest['train_pair_sha256'],
            'bundle_manifest_sha256':expected,'runtime_sha256':hashes,
            'quantization':'remote API; provider implementation not controlled',
            'versions':{n:importlib.metadata.version(n) for n in ['numpy','pandas','pyarrow','duckdb','lightgbm','sqlglot']}}
    engine=runtime.FeatureEngine(ROOT/'reports/provider_small_v1/example_scratch',DATA)
    try:
        pairs=pd.read_parquet(DATA/'train_pairs.parquet')
        sample=pairs[pairs.timestamp==pairs.timestamp.min()].head(3)
        engine.prepare(sample.timestamp.iloc[0],sample.customer_id.values,{'queries':[]})
        config['training_examples']=engine.frame(sample).to_json(orient='records')
    finally:engine.close()
    fingerprint=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()[:12]
    out=ROOT/'LLMFeatures/results'/(config['protocol']+'_'+fingerprint)
    out.mkdir(parents=True,exist_ok=True)
    config_path=out/'run_config.json'
    if config_path.exists():assert json.loads(config_path.read_text())==config
    runtime.write(config_path,config)
    for name,source in modules.items():
        path=out/'runtime_sources'/name
        path.parent.mkdir(exist_ok=True)
        path.write_text(source,encoding='utf-8')
    for source,target in [('manifest.json','input_manifest.json'),('selection.json','validation_selection.json')]:
        shutil.copy2(DATA/source,out/target)
    models=json.loads((ROOT/'reports/tokenclub_probe_v1/models.json').read_text())['data']
    model=next(x for x in models if x['id']==config['model_id'])
    runtime.write(out/'provider_model.json',model)
    runtime.write(ROOT/'reports/provider_small_v1/current_run.json',{'run_id':out.name,'directory':str(out),'status':'prepared'})
    print('Run:',out.name,flush=True)
    if args.prepare_only:return
    raw=out/'raw_control'
    raw.mkdir(exist_ok=True)
    runtime.write(raw/'program.json',{'queries':[]})
    (raw/'program.sql').write_text('-- Raw15 control')
    record('provider_feature_search_started','Запущен реальный GPT-6.1-Sol через tookен.club: small-v1/fullSQL,20успехов/300calls,данныеиLightGBMпрежние. Токен только в памяти.',
           out.name,status='searching',artifacts=str(out.relative_to(ROOT)),model=config['model_id'])
    try:
        runtime.evaluate(DATA,raw,'search',config_path)
        generator=ProviderGenerator(config,out,ROOT/'.env')
        runtime.search(DATA,out/'gpt61sol_full_sql',generator,config_path)
        comparison=runtime.finish(DATA,out,config_path)
        assert len(list((out/'api_attempts').glob('attempt_*')))<=300
        runtime.write(ROOT/'reports/provider_small_v1/current_run.json',{'run_id':out.name,'directory':str(out),'status':'finished'})
        print(comparison.to_string(index=False),flush=True)
        print('Results ZIP:',runtime.archive_run(out),flush=True)
        record('provider_feature_search_finished','API поиск завершён,выборзафиксировандоtest,отчётсохранён. Требуетсялокальныйаудитпередитоговымвыводом.',
               out.name,status='completed_pending_audit',artifacts=str(out.relative_to(ROOT)))
    except BaseException as error:
        # ProviderUnavailable contains sanitized text only; never record headers/env.
        detail=str(error)
        (out/'failure.txt').write_text(detail+'\n'+traceback.format_exc())
        runtime.write(ROOT/'reports/provider_small_v1/current_run.json',{'run_id':out.name,'directory':str(out),'status':'interrupted','error':detail})
        record('provider_feature_search_interrupted','Запуск API остановлен: '+detail[:600],out.name,status='interrupted',artifacts=str(out.relative_to(ROOT)))
        runtime.archive_run(out)
        raise SystemExit(2)


if __name__=='__main__':main()
