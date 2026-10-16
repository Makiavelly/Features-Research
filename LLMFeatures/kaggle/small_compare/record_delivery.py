"""Record a verified notebook delivery, without recording fake LLM metrics."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record


def main():
    manifest = json.loads((HERE / 'delivery_manifest.json').read_text())
    verification = json.loads((ROOT / 'reports/kaggle_llmfe_validation/small_compare_v1/verification.json').read_text())
    assert verification['status'] == 'passed'
    record('kaggle_notebook_ready',
           'Отдельный KaggleT4 notebook Qwen2.5-Coder7B vs Llama3.1-8B на неизменном ContextGNN small-v1 готов. '
           'Прежний SQL/JSON интерфейс Qwen; обе NF4/FP16, одинаковые72813trainпар,128search/88confirm/88heldoutval, '
           'val304/test250 и весь5000каталог.20успешных/300calls/3repairs/3islands на каждую. '
           'Семь сохранённых baseline+Popularity, графики/гистограммы, независимый replay и ZIP. '
           'CPU integration с фиктивными ответами проверен; реального нового LLM результата нет. '
           'Категории компактно закодированы согласованно в raw/history: тестовый model.txt уменьшен174MB→1.3MB. '
           'Проверка ID-сопоставления применяется к обеим моделям; старая обнаруженная ошибка была в Python Llama v5, '
           'а не установленной ошибкой Qwen.',
           'hm_small_qwen_llama_sql_v1', status='notebook_ready',
           artifacts='LLMFeatures/kaggle/small_compare', delivery=manifest,
           verification='reports/kaggle_llmfe_validation/small_compare_v1/verification.json')
    context = ROOT / 'CONTEXT.md'
    text = context.read_text(encoding='utf-8')
    heading = '## Kaggle: одинаковый SQL-поиск Qwen и Llama на small-v1 (2026-10-16)'
    if heading not in text:
        addition = '''
## Kaggle: одинаковый SQL-поиск Qwen и Llama на small-v1 (2026-10-16)

По поручению пользователя создан отдельный Kaggle T4 notebook
LLMFeatures/kaggle/hm_small_qwen_vs_llama_sql_kaggle_t4.ipynb и Input
hm_small_sql_compare_v1.zip (~0.9MB). Прежние notebooks/результаты сохранены.
Протокол hm_small_qwen_llama_sql_v1, статус notebook_ready, реального нового
запуска Qwen/Llama ещё нет. Модели Qwen/Qwen2.5-Coder-7B-Instruct и официальная
Llama3.1-8B-Instruct (с выбором публикации unsloth), последовательно NF4/FP16.
Ранее локальная Qwen была Q4_K_M/Ollama; это явное изменение квантизации.
Интерфейс прежней Qwen: JSON aggregates{name,keys,sql}/derived{name,sql},
host владеет joins/порядком/фильтром t_dat<=cutoff. Ограничений по грамматике
при генерации нет. Согласованная factorize товарных категорий в raw/history
устраняет огромные sparse categorical bitsets (smoke174MB→1.3MB model.txt).
Данные неизменные ContextGNN small-v1:5000users/items/46442tx,
72813исходныхtrainпар/4804user-times/8срезов; SHA ключей/меток совпал manual.
Оценка всех5000товаров, val304 делится128search/88confirm/88heldout seed42;
test250 только после фиксации обоих победителей. Top3+raw наconfirmation.
Каждой LLM20успешных/300calls/3repairs/3islands/1best-in-island; LGB150/31,
4threads/seeds42. Общийval содержит search/confirm, baseline выбирались на
полномval: heldout88 не закрыт для их старого отбора. Разные budgets/одинseed.
Семь сохранённых baseline (включая Recformer)+Popularity пересчитываются
из top12; graphs/search/loss/AP histograms/bootstrap/frozen replay/ZIP.
CPU integration на реальных данных с фиктивными LLM-ответами пройден;
это НЕ оценка Qwen/Llama. ID joins/known pandas answer/time filtering,
перестановка/блоки/repair/duplicate/islands/resume/fullcatalog/references
проверены. Отчёт проверки reports/kaggle_llmfe_validation/small_compare_v1.
README/исходники/manifest в LLMFeatures/kaggle/small_compare.

'''
        text = text.replace('# Контекст для продолжения проекта\n', '# Контекст для продолжения проекта\n' + addition, 1)
        context.write_text(text, encoding='utf-8')


if __name__ == '__main__':
    main()
