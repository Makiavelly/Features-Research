"""H006: complete Python feature generation on frozen small-v1 data."""
import argparse
import ast
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import sys
import traceback
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/kaggle_hm_small_sql_compare_v1'
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record
from provider_api import ProviderGenerator


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_modules():
    source=ROOT/'LLMFeatures/provider_small_runtime_v1'
    modules={name:(source/name).read_text() for name in ['base_features.py','worker.py','runtime.py']}
    modules.update({name:(ROOT/'LLMFeatures'/name).read_text() for name in ['python_features.py','provider_api.py']})
    modules['prompting.py']=(ROOT/'LLMFeatures/python_prompting.py').read_text()
    modules['features.py']='from python_features import FeatureEngine, validate_program\n'
    runtime=modules['runtime.py']
    runtime=runtime.replace('from full_sql import parse, render, program_key, signature, SQLProgramError as DiagnosticError',
                            'from python_features import parse, render, program_key, signature, PythonProgramError as DiagnosticError')
    runtime=runtime.replace("{'queries': []}","{'code': __import__('python_features').RAW}")
    runtime=runtime.replace('program.sql','program.py').replace('gpt61sol_full_sql','gpt61sol_python')
    runtime=runtime.replace('SQL','Python').replace('SELECT/WITH','Python function')
    runtime=runtime.replace('Qwen7B returns complete SELECT scripts; NF4/FP16 loading matches the control.',
                             'GPT-6.1 Sol API returns complete Python functions; remote implementation is not controlled.')
    runtime=runtime.replace('Old local Qwen used Q4_K_M/Ollama: this is not byte-identical quantization.',
                             'Historical Qwen used a different feature interface and model implementation.')
    modules['runtime.py']=runtime
    worker=modules['worker.py'].replace("    source = directory / 'program.json'",
        "    import resource\n    resource.setrlimit(resource.RLIMIT_AS, (8 * 1024**3, 8 * 1024**3))\n    source = directory / 'program.json'")
    modules['worker.py']=worker
    modules['run_provider_python.py']=Path(__file__).read_text()
    return modules


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args()
    modules=build_modules()
    code=ROOT/'LLMFeatures/provider_python_runtime_v1'
    code.mkdir(exist_ok=True)
    for name,text in modules.items():
        ast.parse(text)
        (code/name).write_text(text,encoding='utf-8')
    sys.path.insert(0,str(code))
    import runtime
    from python_features import RAW
    manifest=json.loads((DATA/'manifest.json').read_text())
    sql_config=json.loads(next((ROOT/'LLMFeatures/results').glob('hm_small_gpt61sol_full_sql_seed42_v1_*/run_config.json')).read_text())
    assert sha(DATA/'manifest.json')==sql_config['bundle_manifest_sha256']
    for name,digest in manifest['files'].items(): assert sha(DATA/name)==digest
    config={**sql_config,
            'protocol':'hm_small_gpt61sol_python_seed42_v1','arms':['gpt61sol_python'],'arm':'gpt61sol_python',
            'feature_interface':'complete_Python_modify_features_X_history',
            'runtime_sha256':{n:hashlib.sha256(s.encode()).hexdigest() for n,s in modules.items()},
            'system_message':'Return only a complete Python program defining modify_features(X, history), following the documented input/output contract.',
            'max_python_features':36,'feature_call_timeout_seconds':60,'worker_address_space_gb':8,
            'validator_checks':'Python compile, no I/O, numeric/schema/index, real cutoff permutation and batch invariance',
            'deduplication':'conservative Python AST excluding whitespace/comments/docstrings; not matrix equivalence',
            'sql_comparison_run':sql_config['protocol'],
            'versions':{n:importlib.metadata.version(n) for n in ['numpy','pandas','pyarrow','duckdb','lightgbm','sqlglot']}}
    config.pop('max_sql_queries',None)
    config.pop('max_sql_features',None)
    fingerprint=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()[:12]
    out=ROOT/'LLMFeatures/results'/(config['protocol']+'_'+fingerprint)
    out.mkdir(parents=True,exist_ok=True)
    config_path=out/'run_config.json'
    if config_path.exists(): assert json.loads(config_path.read_text())==config
    runtime.write(config_path,config)
    for name,text in modules.items():
        path=out/'runtime_sources'/name
        path.parent.mkdir(exist_ok=True)
        path.write_text(text,encoding='utf-8')
    for source,target in [('manifest.json','input_manifest.json'),('selection.json','validation_selection.json')]:
        shutil.copy2(DATA/source,out/target)
    registry=ROOT/'reports/provider_python_v1/current_run.json'
    registry.parent.mkdir(exist_ok=True)
    runtime.write(registry,{'run_id':out.name,'directory':str(out),'status':'prepared'})
    print('Run:',out.name,flush=True)
    if args.prepare_only:return
    checks=json.loads((ROOT/'reports/provider_python_v1/validator_verification.json').read_text())
    assert checks['status']=='passed'
    assert checks['module_sha256']==sha(code/'python_features.py'), 'Validator changed since verification'
    shutil.copy2(ROOT/'reports/provider_python_v1/validator_verification.json',out/'validator_verification.json')
    raw=out/'raw_control'
    raw.mkdir(exist_ok=True)
    runtime.write(raw/'program.json',{'code':RAW})
    (raw/'program.py').write_text(RAW)
    record('provider_python_search_started',
           'H006: реальный GPT-6.1 Sol пишет полную Python функцию. '
           'Те же 72813 пар / LightGBM150/31 / seed42 / 20 наборов / 300 API вызовов. '
           'Предварительная проверка валидатора пройдена. Test не используется при отборе.',
           out.name,status='searching',artifacts=str(out.relative_to(ROOT)))
    try:
        runtime.evaluate(DATA,raw,'search',config_path)
        # Raw implementation must be identical to the preceding SQL experiment.
        sql_raw=next((ROOT/'LLMFeatures/results').glob('hm_small_gpt61sol_full_sql_seed42_v1_*/raw_control'))
        for file in ['model.txt','search_predictions.npy','search_ap.npy']:
            assert sha(raw/file)==sha(sql_raw/file), 'Raw control mismatch: '+file
        generator=ProviderGenerator(config,out,ROOT/'.env')
        runtime.search(DATA,out/'gpt61sol_python',generator,config_path)
        comparison=runtime.finish(DATA,out,config_path)
        runtime.write(registry,{'run_id':out.name,'directory':str(out),'status':'finished'})
        print(comparison.to_string(index=False),flush=True)
        print('Results ZIP:',runtime.archive_run(out),flush=True)
        record('provider_python_search_finished',
               'Python эксперимент завершён; требуется независимый аудит. Отбор заморожен до test.',
               out.name,status='completed_pending_audit',artifacts=str(out.relative_to(ROOT)))
    except BaseException as error:
        (out/'failure.txt').write_text(str(error)+'\n'+traceback.format_exc())
        runtime.write(registry,{'run_id':out.name,'directory':str(out),'status':'interrupted','error':str(error)})
        record('provider_python_search_interrupted',str(error)[:600],out.name,status='interrupted',artifacts=str(out.relative_to(ROOT)))
        runtime.archive_run(out)
        raise


if __name__=='__main__':main()
