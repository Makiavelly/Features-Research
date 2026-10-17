"""Separate pure-SQL Kaggle notebook; old notebooks/modules stay immutable."""
import ast
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
VARIANT=HERE/'full_sql_small'
OUTPUT=HERE/'hm_small_qwen7b_full_sql_kaggle_t4.ipynb'
PARENT=HERE/'hm_small_qwen7b_h003_kaggle_t4.ipynb'


def literal(source,name):
    return next(ast.literal_eval(n.value) for n in ast.parse(source).body if isinstance(n,ast.Assign)
                and isinstance(n.targets[0],ast.Name) and n.targets[0].id==name)


def swap(source,old,new):
    assert old in source,old
    return source.replace(old,new)


def build():
    notebook=json.loads(PARENT.read_text(encoding='utf-8'))
    cells=copy.deepcopy(notebook['cells'])
    modulecell=next(c for c in cells if 'MODULES = ' in ''.join(c['source']))
    parent=literal(''.join(modulecell['source']),'MODULES')
    modules={'base_features.py':parent['features.py'], 'worker.py':parent['worker.py'],
             'features.py':'"""Full SELECT interface; frozen host raw encoding and joins in base_features."""\nfrom full_sql import FeatureEngine, validate_program\n',
             'full_sql.py':(VARIANT/'full_sql.py').read_text(encoding='utf-8'),
             'prompting.py':(VARIANT/'prompting.py').read_text(encoding='utf-8')}
    runtime=parent['runtime.py']
    runtime=swap(runtime,'from original_prompt import INSTRUCTION, program_key\nfrom diagnostics import decode, diagnose, DiagnosticError, signature',
                 'from full_sql import parse, render, program_key, signature, SQLProgramError as DiagnosticError\nfrom prompting import make_prompt')
    for name in ['parse','make_prompt']:
        node=next(n for n in ast.parse(runtime).body if isinstance(n,ast.FunctionDef) and n.name==name)
        runtime=swap(runtime,ast.get_source_segment(runtime,node),'')
    start=runtime.index('\nPROMPT_ADDENDUM = ')
    runtime=runtime[:start]+'\n'
    runtime=runtime.replace("{'aggregates': [], 'derived': []}","{'queries': []}")
    runtime=runtime.replace("config.get('arm') == 'h003c'","config.get('arm') == 'qwen_full_sql'")
    runtime=swap(runtime,"json.dumps(matched['program'], separators=(',', ':'))[:1800]",
                 "'Your Previous SQL response already contains the complete matching program.'")
    runtime=runtime.replace('. Matching formulas: ','. ')
    runtime=swap(runtime,"                write(directory / 'program.json', program)","                write(directory / 'program.json', program)\n                (directory / 'program.sql').write_text(render(program), encoding='utf-8')")
    runtime=runtime.replace('diagnostic_features','diagnostic_queries')
    runtime=runtime.replace('Return one complete JSON feature program following the user interface.',
                            'Return only a complete DuckDB SQL script of SELECT/WITH queries following the user interface.')
    runtime=runtime.replace('Qwen7B H003','Qwen7B full SQL').replace('H003 arms','full SQL arm').replace('H003 feature selections','full SQL selections')
    runtime=runtime.replace('fake H003 responses','scripted SQL responses')
    runtime=runtime.replace('All H003 arms must be selected before test','The full SQL program must be selected before test')
    runtime=runtime.replace('All full SQL arm use the original local-Qwen SQL JSON interface and NF4/FP16 loading.',
                            'Qwen7B returns complete SELECT scripts; NF4/FP16 loading matches the control.')
    runtime=runtime.replace('All full SQL arm use','Full SQL uses')
    runtime=runtime.replace('the original local-Qwen SQL JSON interface','complete SELECT scripts with host-owned final joins')
    runtime=runtime.replace("stream.write('\\n\\nH003 arms: A=diagnostics; B=A+prompt examples; C=B+duplicate/unchanged policy.\\n'\n                     'Compare each adjacent variant, and A to the previous archived Qwen7B control.\\n'",
                            "stream.write('\\n\\nFull SQL: ordinary SELECT/WITH statements, not the aggregates/derived JSON DSL.\\n'\n                     'Compare locally to archived Qwen7B and H003; different SQL interface and dedup semantics.\\n'")
    runtime=runtime.replace('full SQL arm: A=diagnostics; B=A+prompt examples; C=B+duplicate/unchanged policy.',
                            'Full SQL: ordinary SELECT/WITH scripts with host-owned candidate joins.')
    runtime=runtime.replace('Compare each adjacent variant, and A to the previous archived Qwen7B control.',
                            'Compare locally to archived Qwen7B and H003; SQL interface/dedup semantics differ.')
    modules['runtime.py']=runtime
    hashes={n:hashlib.sha256(s.encode()).hexdigest() for n,s in modules.items()}
    for name,source in modules.items():
        ast.parse(source)
        (VARIANT/name).write_text(source,encoding='utf-8')
    for i,cell in enumerate(cells):
        source=''.join(cell['source'])
        if i==0:
            source='''# Qwen2.5-Coder-7B-Instruct: полные SQL-запросы на H&M small-v1

Новый эксперимент: Qwen возвращает **обычный SQL**, не JSON aggregates/derived.
Она пишет один или несколько полных SELECT/WITH-запросов: группировки, CTE,
формулы, aliases и при необходимости окна. Наш код проверяет ключи/числовые
признаки, отсутствие дубликатов ключей и присоединяет результаты к кандидатам.
Модель видит только физически отфильтрованную прошлую history; будущих транзакций,
целей и произвольных таблиц в её SQL-соединении нет. Изменение интерфейса —
осознанная адаптация, не точное повторение старого DSL или статьи.

1. Импортируйте этот `.ipynb` в свежую Kaggle-сессию.
2. Включите **Internet** и **GPU T4**. Qwen публична, HF_TOKEN не нужен.
3. Добавьте прежний **hm_small_sql_compare_v1.zip** через Dataset/Input.
4. **Save Version → Run All**. Старые отчёты не нужны как Input.
5. Скачайте `hm_small_qwen7b_full_sql_v1_<hash>_results.zip` из Output.

Один поиск:20 различных успешно оценённых наборов, до300 обращений,
до3 исправлений,3 популяции. Полные SQL-наборы сравниваются целиком.
Сохраняются все ответы и `program.sql`, ошибки, популяции/repair/parent,
дубликаты, модели, прогнозы, метрики, графики поиска/logloss/сравнения и AP-гистограммы.
ZIP обновляется после каждого вызова. Cancel Kaggle не гарантирует публикацию Output.
'''
        elif cell['cell_type']=='markdown':
            source='''## Условия сравнения

Те же72813 train-пар/4804 user-time/8cutoff,raw15,каталог5000 и val304/test250.
LightGBM150rounds/31leaves/4CPUthreads;NF4/doublequant/FP16 наT4,temperature0.8,
input6144/output2048,seed42+call−1. Та же закреплённая revision Qwen7B.
Search128 → top3+raw → confirmation88;heldout88 отдельно. Выбор фиксируется доtest.
Test уже просматривался: повторная диагностическая оценка, не новый закрытый test.
Старые Qwen7B/H003 результаты сравним локально после получения ZIP.

Новый интерфейс:до6 независимых SELECT-запросов,до36 числовых f_* выходов всего.
Нет разделения на24 aggregates/12 derived: отношения/формулы вычисляет SQL.
Поддержаны CTE,aliases,внутренние joins и числовые окна при уникальности конечных ключей.
Дедупликация консервативная по SQL AST: пробелы/регистр/комментарии и переименование f_*
нормализуются; общая алгебраическая эквивалентность/переименование CTE не распознаются.
Поэтому эксперимент меняет также пространство программ и критерий дубликата.

SQL-парсер:[SQLGlot](https://sqlglot.com/),закреплена
[версия27.20.0](https://pypi.org/project/sqlglot/27.20.0/).
LightGBM,код обучения/оценки,raw-кодирование и конечные joins сохранены прежними.
'''
        elif "'transformers==4.57.1'" in source:
            source=source.replace("'lightgbm==4.6.0'","'sqlglot==27.20.0', 'lightgbm==4.6.0'")
        elif 'ARMS = ' in source:
            start,end=source.index('ARMS = '),source.index('MODELS = ')
            source=source[:start]+"ARMS = ['qwen_full_sql']\n"+source[end:]
            source=source.replace("'hm_small_qwen7b_h003_v1'","'hm_small_qwen7b_full_sql_v1'")
            source=source.replace("'hypothesis': 'H003 cumulative A/AB/ABC'","'hypothesis': 'H004 full SELECT scripts', 'max_sql_queries': 6, 'max_sql_features': 36")
            source=source.replace("'original_local_qwen_SQL_aggregates_and_derived'","'complete_SQL_SELECT_queries_with_host_joins'")
            source=source.replace('/tmp/hm_small_qwen7b_h003_cache','/tmp/hm_small_qwen7b_full_sql_cache')
        elif 'MODULES = ' in source:
            start,end=source.index('MODULES = '),source.index('EXPECTED_MANIFEST = ')
            source=source[:start]+'MODULES = '+repr(modules)+'\nMODULE_SHA = '+repr(hashes)+'\n'+source[end:]
            source=source.replace("WORK / 'hm_small_h003_runtime'","WORK / 'hm_small_full_sql_runtime'")
        elif 'CONFIG.update(models=' in source:
            source=source.replace("'pyarrow']","'pyarrow', 'sqlglot']")
            source=source.replace("{'aggregates': [], 'derived': []}","{'queries': []}")
        elif "raw / 'program.json'" in source:
            source=source.replace("{'aggregates': [], 'derived': []}","{'queries': []}")
            source=source.replace("experiment.write(raw / 'program.json', {'queries': []})","experiment.write(raw / 'program.json', {'queries': []})\n(raw / 'program.sql').write_text('-- Raw15 control', encoding='utf-8')")
        if cell['cell_type']=='code':
            ast.parse(source)
            cell.update(outputs=[],execution_count=None)
        cell['source']=source.splitlines(keepends=True)
        cell['id']=hashlib.sha256(source.encode()).hexdigest()[:12]
    notebook['cells']=cells
    OUTPUT.write_text(json.dumps(notebook,ensure_ascii=False,indent=1),encoding='utf-8')
    manifest=json.loads((HERE/'h003_small/delivery_manifest.json').read_text())
    manifest.update(protocol='hm_small_qwen7b_full_sql_v1',notebook=OUTPUT.name,
                    notebook_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),modules=hashes,
                    default_arms=['qwen_full_sql'],parent_notebook_sha256=hashlib.sha256(PARENT.read_bytes()).hexdigest(),
                    unchanged_worker=True,unchanged_modules=['worker.py'],
                    feature_host_base_matches=hashlib.sha256(parent['features.py'].encode()).hexdigest(),
                    llm_inference_executed_locally=False)
    (VARIANT/'delivery_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('Created',OUTPUT,len(cells),'cells')


if __name__=='__main__':build()
