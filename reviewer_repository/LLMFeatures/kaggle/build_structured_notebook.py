"""Independent notebook: structured feature descriptions compiled by the host."""
import ast
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
VARIANT=HERE/'structured_variant'
BASE=HERE/'sql_variant'
notebook=json.loads((HERE/'llmfe_llama31_hm_sql_kaggle_t4.ipynb').read_text(encoding='utf-8'))
worker=(BASE/'worker.py').read_text(encoding='utf-8')
worker=worker.replace('from sql_features import compile_sql, validate_program',
                      'from structured_features import compile_structured, validate_program')
worker=worker.replace('return compile_sql(source)','return compile_structured(source)')
runtime=(BASE/'runtime.py').read_text(encoding='utf-8')
runtime=runtime.replace('from sql_features import validate_program','from structured_features import validate_program, to_sql')
replacement_source=(VARIANT/'prompts.py').read_text(encoding='utf-8')
definitions=ast.parse(replacement_source).body
for node in reversed(ast.parse(runtime).body):
    replacement=next((d for d in definitions if isinstance(d,ast.FunctionDef) and d.name==getattr(node,'name',None)),None)
    if replacement:
        lines=runtime.splitlines(keepends=True)
        lines[node.lineno-1:node.end_lineno]=replacement_source.splitlines(keepends=True)[replacement.lineno-1:replacement.end_lineno]
        runtime=''.join(lines)
runtime=runtime.replace("(directory/'program.json').write_text(code)",
    "(directory/'program.json').write_text(code)\n                write_json(directory/'compiled_sql.json',to_sql(json.loads(code)))")
runtime=runtime.replace('SQL specification validated','Structured specification validated').replace('Duplicate canonical SQL specification','Duplicate canonical structured specification')
assets={'worker.py':worker,'runtime.py':runtime,'sql_features.py':(BASE/'sql_features.py').read_text(encoding='utf-8'),
        'structured_features.py':(VARIANT/'structured_features.py').read_text(encoding='utf-8')}
for name,source in assets.items():
    ast.parse(source)
    (VARIANT/name).write_text(source,encoding='utf-8')
for cell in notebook['cells']:
    text=''.join(cell['source'])
    if cell['cell_type']=='code' and 'MODULES = ' in text:
        start=text.index('MODULES = ');end=text.index('CODE = ',start)
        text=text[:start]+'MODULES = '+repr(assets)+'\n'+text[end:]
    text=text.replace('hm_llmfe_llama31_8b_lightgbm_sql_fulltrain_v1','hm_llmfe_llama31_8b_lightgbm_structured_fulltrain_v1')
    text=text.replace("'feature_interface':'qwen_sql_aggregates_and_derived'","'feature_interface':'structured_aggregates_and_expression_trees'")
    text=text.replace("WORK / 'llmfe_sql_runtime'","WORK / 'llmfe_structured_runtime'")
    text=text.replace('Return only the requested JSON with restricted SQL aggregates. Do not write Python.',
                      'Return only JSON feature descriptions using the specified operations. Never write SQL or Python.')
    if cell['cell_type']=='markdown':
        text=text.replace('Llama → SQL-агрегаты → LightGBM','Llama → структурированные признаки → LightGBM')
        text=text.replace('Llama создаёт JSON с ограниченными SQL-агрегатами; host строит признаки',
                          'Llama выбирает операции, поля, окна и группировки в JSON; host компилирует их в SQL и строит признаки')
        text=text.replace('JSON как у Qwen: до24 SQL-агрегатов и до12 производных формул; соединения выполняет host',
                          'JSON: до24 агрегатов и до12 деревьев формул; Llama не пишет SQL/Python')
        text=text.replace('отдельный протокол SQL v1','отдельный протокол Structured v1')
        text=text.replace('SQL ограничен списком столбцов/функций и числовыми выражениями;',
                          'Все выражения компилирует host из проверенного дерева операций;')
        text=text.replace('полные программы, ответы и причины отказов','описания признаков, ответы и причины отказов; `compiled_sql.json` — SQL, созданный host')
    if cell['cell_type']=='code':ast.parse(text)
    cell['source']=text.splitlines(keepends=True)
    cell['id']=hashlib.sha256(text.encode()).hexdigest()[:12]
notebook['cells'][0]['source'].append('\nЭто новый ограниченный язык признаков, а не свободный SQL-интерфейс Qwen. '
    'Генерация Llama остаётся обычным sampling; маска токенов/grammar decoding не используется. '
    'Структура проверяется после генерации, ошибки отправляются на исправление.\n')
output=HERE/'llmfe_llama31_hm_structured_kaggle_t4.ipynb'
output.write_text(json.dumps(notebook,ensure_ascii=False,indent=1),encoding='utf-8')
manifest={'notebook':output.name,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
          'modules':{name:hashlib.sha256(source.encode()).hexdigest() for name,source in assets.items()},
          'protocol':'hm_llmfe_llama31_8b_lightgbm_structured_fulltrain_v1',
          'dataset':'hm_llmfe_kaggle_fulltrain_v2.zip','gpu_or_llama_executed':False}
(VARIANT/'delivery_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built',output.name,':',len(notebook['cells']),'cells; code parsed')
