"""Record audited provider results without repeating generation or training."""
import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record


def main():
    identifiers = [
        ('v1', 'hm_small_gpt61sol_full_sql_seed42_v1_f33bb22767c0'),
        ('v2', 'hm_small_gpt61sol_full_sql_corrected_eval_v2_ffbd51c51899'),
    ]
    for version, run_id in identifiers:
        report = ROOT / 'reports' / f'gpt61sol_small_{version}'
        assert json.loads((report / 'audit.json').read_text())['status'] == 'passed'
        assert (report / 'report.md').exists()
        rows = list(csv.DictReader((report / 'comparison.csv').open()))
        result = next(row for row in rows if row['model'] == 'GPT61Sol')
        record('provider_feature_experiment_audited',
               'Поиск GPT-6.1 Sol завершён и независимо проверен. '
               '20 оценённых наборов; test MAP@12 0.979030%, raw 0.959630%, '
               'прежний Qwen7B 1.107143%. Преимущество по качеству не подтверждено. '
               + ('Исходный поток: 26 API обращений, 5 дубликатов и один ложный отказ AND.'
                  if version == 'v1' else
                  'Исправленная оценка сохранённого потока: первые 20 валидных за 24 ответа, '
                  '4 дубликата, без отказов; дополнительных API обращений 0. '
                  'Это не независимый LLM запуск. Выбран тот же candidate_004.'),
               run_id, status='complete', artifacts=str(report.relative_to(ROOT)),
               evaluated_distinct=20, api_requests=26 if version == 'v1' else 0,
               source_api_requests=26,
               val_metrics={'map': float(result['val_map_percent']) / 100},
               test_metrics={'map': float(result['test_map_percent']) / 100},
               independent_audit='passed', independent_llm_run=version == 'v1')

    note = '''
## Итог H005: GPT-6.1 Sol / полный SQL (2026-10-17)

Реальный API эксперимент завершён: 26 оплачиваемых запросов, 20 оценённых наборов.
Независимая проверка обоих вариантов оценки прошла, включая frozen inference raw/GPT × val/test.
Test MAP@12: GPT 0.979030%, raw15 0.959630%, прежний Qwen7B 1.107143%,
ручные признаки 1.233880%, ID-GNN 2.653413%, ContextGNN 3.015575%.
Улучшение качества не подтверждено; bootstrap интервалы разниц включают ноль.
Один seed, 250 test пользователей, ранее просмотренный test; прежний Qwen использовал JSON,
а GPT полный SQL, поэтому эффект модели отдельно от интерфейса не установлен.

Обнаружен наш ложный отказ AND в SQLGlot allowlist. Исходный запуск сохранён.
Исправленная оценка первых 20 валидных программ сохранённого потока заняла первые 24 ответа
(4 дубликата, 0 отказов), без дополнительных API вызовов; всего реально вызвано 26.
Выбран тот же candidate_004: 20 новых числовых признаков + 15 исходных полей, LightGBM 150 деревьев.
Исправленный replay не является независимым LLM экспериментом и сохраняет исходную историю промптов.
Отчёт: reports/gpt61sol_small_v2/report.md; графики и гистограммы рядом.
Исходный отчёт: reports/gpt61sol_small_v1/report.md. ZIP обоих запусков в LLMFeatures/results.
Исправлен также отдельный Kaggle full SQL v2 ноутбук Qwen; CPU regression пройден,
реальной Qwen генерации в нём пока нет. Токен не сохраняется в артефактах.

'''
    path = ROOT / 'CONTEXT.md'
    content = path.read_text(encoding='utf-8-sig')
    marker = '## H005: реальный поиск GPT-6.1 Sol через Tooken Club'
    start = content.index(marker)
    end = content.index('\n## H004:', start)
    path.write_text(content[:start] + note.lstrip() + content[end:], encoding='utf-8')
    hypothesis = ROOT / 'HYPOTHESES.md'
    with hypothesis.open('a', encoding='utf-8') as handle:
        handle.write(note)
    record('provider_feature_experiment_summary',
           'H005 завершена: 20 наборов, 26 API запросов, независимый аудит пройден. '
           'Полный SQL исполняется успешно, но преимущество по MAP не подтверждено. '
           'Исправление ложного AND отказа не изменило выбранный набор и итоговые метрики.',
           artifacts='reports/gpt61sol_small_v2', seed=42, test_users=250)


if __name__ == '__main__':
    main()
