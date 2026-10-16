"""Persist notebook delivery; never report CPU-fixture scores as14B results."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record


def main():
    manifest = json.loads((HERE / 'delivery_manifest.json').read_text())
    check = json.loads((ROOT / 'reports/kaggle_llmfe_validation/qwen14_small_v1/verification.json').read_text())
    assert check['status'] == 'passed'
    record('external_run_reported',
           'Пользователь сообщил: исходный hm_small_qwen_vs_llama_sql_kaggle_t4.ipynb сейчас выполняется на Kaggle. '
           'Итоговый ZIP ещё не получен; фактических новых метрик нет. Не повторять Qwen7B/Llama.',
           'hm_small_qwen_llama_sql_v1', status='running_on_kaggle_user_reported')
    record('kaggle_notebook_ready',
           'Создан отдельный hm_small_qwen14b_sql_kaggle_t4.ipynb для параллельного запуска пользователем на KaggleT4. '
           'Только публичная Qwen2.5-Coder-14B-Instruct,NF4/FP16,безHF_TOKEN. Те жеInput,72813trainпар, '
           'search128/confirm88/heldout88,val304/test250/full5000,LightGBM150/31/4threads,20success/300calls/3repairs/3islands. '
           'Все4основныхмодуля побайтово совпали с работающим7B/Llama notebook; исходный notebook/архив не изменены. '
           'По уточнению пользователя импорт результатов другихLLM вKaggle убран: отчёты трёх моделей сравнить позже локально. '
           'Схема/сопоставимость/начальныйprompt/одномодельныйотчёт/графики/ZIP проверены на frozenCPUfixtures; '
           'реального14Bинференса и измеренияVRAM пока нет.',
           'hm_small_qwen14b_sql_v1', status='notebook_ready', artifacts='LLMFeatures/kaggle/qwen14_small',
           delivery=manifest, verification='reports/kaggle_llmfe_validation/qwen14_small_v1/verification.json')
    context = ROOT / 'CONTEXT.md'
    text = context.read_text(encoding='utf-8')
    heading = '## Kaggle: отдельная Qwen14B на прежнем small SQL протоколе (2026-10-16)'
    if heading not in text:
        section = '''
## Kaggle: отдельная Qwen14B на прежнем small SQL протоколе (2026-10-16)

Пользователь сообщил,что Qwen7B/Llama notebook уже работает вKaggle;
результатов ещё нет,не повторять их запуск. Новый отдельный notebook
LLMFeatures/kaggle/hm_small_qwen14b_sql_kaggle_t4.ipynb готов для параллельного
KaggleT4 запуска Qwen/Qwen2.5-Coder-14B-Instruct,NF4/doublequant/FP16,
безодобренияHF/токена. Runprotocol hm_small_qwen14b_sql_v1,пока notebook_ready,
не реальная оценка14B. ПикVRAM не измерен,контекст приOOM не сокращаетсяавто.
Исходный работающий notebook и Input hm_small_sql_compare_v1.zip не менялись.
4sharedмодуля побайтово взяты изнего; добавлен только runtime14 reportadapter.
Те же72813trainпар/4804user-time/8срезов; search128/confirm88/heldout88,
val304/test250/все5000товаров;SQLJSON24/12,raw15,LightGBM150/31/4threads,
seed42,temp.8,tokens6144+2048,20success/300calls/3repairs/3islands.
Метрики/предсказания/графики/гистограммы/программы/models/frozenreplay/ZIP
сохраняются отдельно. По последнему уточнению НЕ импортировать выводы
7B/Llama в14B notebook: пользователь пришлёт отчётытрёхLLM длялокального
сравнения позже. Input только прежний архивмалыхданных.
Проверены nbformat/AST,configs/начальныйprompt/sharedSHA/неизменностьInput
и одномодельныйотчёт с7baseline+Popularity наfrozenCPUfixtures. Это НЕ
метрики14B,новогоLLMинференса/обучения дляпроверки не было. Verification:
reports/kaggle_llmfe_validation/qwen14_small_v1/verification.json.
README/manifest/buildercheck вLLMFeatures/kaggle/qwen14_small.

'''
        context.write_text(text.replace('# Контекст для продолжения проекта\n', '# Контекст для продолжения проекта\n' + section, 1), encoding='utf-8')


if __name__ == '__main__':
    main()
