"""Record notebook preparation, never an actual H003 LLM result."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record

verification = json.loads((ROOT / 'reports/kaggle_llmfe_validation/h003_small_v1/verification.json').read_text())
assert verification['status'] == 'passed'
context = ROOT / 'CONTEXT.md'
heading = '## H003: новый Kaggle-ноутбук Qwen7B'
text = context.read_text(encoding='utf-8-sig')
if heading not in text:
    start = text.index('\n', text.index('# ')) + 1
    entry = '''
## H003: новый Kaggle-ноутбук Qwen7B

По поручению пользователя подготовлен LLMFeatures/kaggle/hm_small_qwen7b_h003_kaggle_t4.ipynb.
Protocol hm_small_qwen7b_h003_v1. Default ARMS h003a/h003b/h003c = A/AB/ABC;
три независимых поиска20успехов/300обращений/3repair/3популяции каждый.
Одна загрузка Qwen7B NF4 наT4, pinned c03e6d358207e414f1eca0bb1891e29f1db0e242.
A адресная диагностика всех features/EXPLAIN пустойсхемы; B добавляет примеры;
C адресные дубликаты/прекращение неизменённого repair. Автоисправлений нет.
Input прежний hm_small_sql_compare_v1.zip;72813пар,LightGBM150/31/4threads,
search128/confirm88/heldout88,val304/test250/catalog5000. Features/worker/original_prompt
байт-в-байт прежние. Контроль прошлый Kaggle Qwen7B; сравнивать A→B→C.
Все selection доtest; test ранее просмотрен, оценка повторная. Старые ноутбуки не менялись.
CPU smoke с заданными ответами/3раундами пройден отдельно, без LLM-генерации.
Проверка67историческихответов:30отказов диагностированы,37valid/duplicate приняты.
Проверены routing/repair/duplicate/unchanged/resume,full5000,метрики/references/
frozen replay/графики/ZIP. reports/kaggle_llmfe_validation/h003_small_v1/verification.json.
Реальный H003 наGPU ещё не запускался; пользователь запустит вKaggle.

'''
    context.write_text(text[:start] + entry + text[start:], encoding='utf-8')
record('h003_kaggle_notebook_prepared',
       'Подготовлен отдельный Kaggle T4 ноутбук H003 для Qwen2.5-Coder-7B-Instruct: A/AB/ABC, '
       'те же72813пары иSQLинтерфейс; CPU smoke/67историческихответов проверены. '
       'Реальная LLM-генерация H003 не выполнялась; старые эксперименты сохранены.',
       notebook='LLMFeatures/kaggle/hm_small_qwen7b_h003_kaggle_t4.ipynb',
       verification='reports/kaggle_llmfe_validation/h003_small_v1/verification.json',
       protocol='hm_small_qwen7b_h003_v1', actual_llm_experiment_started=False)
