"""Build an independent SQL notebook without modifying the existing pandas notebook."""
import ast
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
VARIANT=HERE/'sql_variant'
notebook=json.loads((HERE/'llmfe_llama31_hm_kaggle_t4.ipynb').read_text(encoding='utf-8'))
worker=(HERE/'worker.py').read_text(encoding='utf-8')
worker=worker.replace("RAW = '''def modify_features(X, history):\n    return pd.DataFrame(index=X.index)\n'''", "RAW = '{\"aggregates\": []}'")
start=worker.index('def check_program('); end=worker.index('def feature_error(',start)
worker=worker[:start]+'''from sql_features import compile_sql, validate_program

def check_program(source):
    return validate_program(json.loads(source),allow_empty=True)

def compile_program(source):
    return compile_sql(source)


'''+worker[end:]
runtime=(HERE/'runtime.py').read_text(encoding='utf-8')
runtime=runtime.replace('from worker import RAW, check_program, Data, map_at_12',
                      'from worker import RAW, check_program, Data, map_at_12\nfrom sql_features import validate_program')
# Replace only interface-dependent functions; preserve search budgets, evaluation and final replay.
functions=ast.parse((VARIANT/'sql_prompts.py').read_text(encoding='utf-8'))
prompt_source=(VARIANT/'sql_prompts.py').read_text(encoding='utf-8').splitlines(keepends=True)
for definition in reversed(ast.parse(runtime).body):
    replacement=next((f for f in functions.body if isinstance(f,ast.FunctionDef) and f.name==getattr(definition,'name',None)),None)
    if replacement is not None:
        lines=runtime.splitlines(keepends=True)
        lines[definition.lineno-1:definition.end_lineno]=prompt_source[replacement.lineno-1:replacement.end_lineno]
        runtime=''.join(lines)
runtime=runtime.replace("(directory/'program.py').write_text(code)","(directory/'program.py').write_text(code)\n                (directory/'program.json').write_text(code)")
runtime=runtime.replace('Duplicate Python AST','Duplicate canonical SQL specification').replace('Python validation passed','SQL specification validated')
runtime=runtime.replace("print(trial.get('error','No error text saved'),flush=True)","print(trial.get('error','No error text saved'),flush=True)\n        else:\n            print(f\"ACCEPTED call{index+1}: search MAP@12={100*trial['score']:.6f}%\",flush=True)")
assets={'worker.py':worker,'runtime.py':runtime,'sql_features.py':(VARIANT/'sql_features.py').read_text(encoding='utf-8')}
for name,source in assets.items():
    ast.parse(source)
    (VARIANT/name).write_text(source,encoding='utf-8')
for cell in notebook['cells']:
    text=''.join(cell['source'])
    if cell['cell_type']=='code' and 'MODULES = ' in text:
        start=text.index('MODULES = '); end=text.index("CODE = ",start)
        text=text[:start]+'MODULES = '+repr(assets)+'\n'+text[end:]
    text=text.replace('hm_llmfe_llama31_8b_lightgbm_preflight_fulltrain_v5','hm_llmfe_llama31_8b_lightgbm_sql_fulltrain_v1')
    text=text.replace("'program_interface_version':5", "'program_interface_version':1, 'feature_interface':'qwen_sql_aggregates_and_derived'")
    text=text.replace("'sentencepiece==0.2.1'", "'sentencepiece==0.2.1', 'duckdb==1.4.1'")
    text=text.replace("'lightgbm','pandas','numpy','pyarrow'", "'lightgbm','pandas','numpy','pyarrow','duckdb'")
    text=text.replace("WORK / 'llmfe_runtime'", "WORK / 'llmfe_sql_runtime'")
    text=text.replace('Follow the Python interface exactly.','Return only the requested JSON with restricted SQL aggregates. Do not write Python.')
    if cell['cell_type']=='markdown':
        text=text.replace('Llama создаёт Python-программы признаков','Llama создаёт JSON с ограниченными SQL-агрегатами; host строит признаки')
        text=text.replace('Короткая Python/pandas-функция,2–6 новых признаков','JSON как у Qwen: до24 SQL-агрегатов и до12 производных формул; соединения выполняет host')
        text=text.replace('Это новый протокол v5','Это отдельный протокол SQL v1')
        text=text.replace('`candidates/candidate_*/program.py`','`candidates/candidate_*/program.json` (дубликат в `program.py` для совместимости хранения)')
        text=text.replace('Проверки AST и отдельный CPU-процесс ограничивают интерфейс, время и память, но не являются\nполноценной изоляцией произвольного враждебного Python-кода. Generated code не получает токен,',
                          'LLM не пишет исполняемый Python. SQL ограничен списком столбцов/функций и числовыми выражениями;\nDuckDB не имеет внешнего доступа. Запросы выполняются в отдельном ограниченном CPU-процессе. LLM не получает токен,')
    if cell['cell_type']=='code':
        ast.parse(text)
    cell['source']=text.splitlines(keepends=True)
    cell['id']=hashlib.sha256(text.encode()).hexdigest()[:12]
notebook['cells'][0]['source'].insert(0,'# Отдельный эксперимент: Llama → SQL-агрегаты → LightGBM\n\n')
output=HERE/'llmfe_llama31_hm_sql_kaggle_t4.ipynb'
output.write_text(json.dumps(notebook,ensure_ascii=False,indent=1),encoding='utf-8')
print('Created',output.name,'with',len(notebook['cells']),'cells')
manifest={'protocol':'hm_llmfe_llama31_8b_lightgbm_sql_fulltrain_v1',
          'notebook':output.name,'notebook_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
          'modules':{name:hashlib.sha256(source.encode()).hexdigest() for name,source in assets.items()},
          'dataset':'hm_llmfe_kaggle_fulltrain_v2.zip',
          'dataset_sha256':hashlib.sha256((HERE/'hm_llmfe_kaggle_fulltrain_v2.zip').read_bytes()).hexdigest(),
          'gpu_or_llama_executed_locally':False}
(VARIANT/'delivery_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
