"""Persist verified Kaggle results, separate from local CPU smoke fixtures."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/hm_small_llms_v1'
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record


def main():
    audit = json.loads((OUT / 'audit.json').read_text())
    report = json.loads((OUT / 'report.json').read_text())
    assert audit['status'] == 'passed' and report['audit_passed']
    rows = {row['model']: row for row in report['comparison']}
    parent = 'hm_small_qwen_llama_sql_v1_2ecc60d61fd4'
    for title, run_id in [('Qwen7B_LightGBM', parent + '_qwen'), ('Llama8B_LightGBM', parent + '_llama'),
                          ('Qwen14B_LightGBM', 'hm_small_qwen14b_sql_v1_f373011050bf')]:
        value, stats = rows[title], audit['models'][title]
        message = (f"{title}: реальный Kaggle запуск проверен;20успешных/{stats['calls']}вызовов,candidate{stats['selected_call']}; "
                   f"val/testMAP={value['val_map_percent']:.6f}/{value['test_map_percent']:.6f}%. "
                   'Совпали72813trainпар/source/model/programSHA/выборпоconfirmation. НезависимыйCPUreplay точно совпал top12/AP/MAP. Безобучения/новойгенерации/выборапоtest.')
        record('kaggle_small_llm_audited', message, run_id, status='complete',
               val_metrics={'map': value['val_map_percent'] / 100}, test_metrics={'map': value['test_map_percent'] / 100},
               artifacts='reports/hm_small_llms_v1', selected_call=stats['selected_call'], llm_calls=stats['calls'], evaluated_distinct=20)
    message = ('Оба ZIP проверены,все60программ. Qwen7Btest1.107143%,Llama8B0.780337%,Qwen14B0.743306%; '
               'Raw0.959630%,manual1.233880%,ContextGNN3.015575%. У14B45calls против67/201,но генерация71.61мин против46.42/262.10мин. '
               'Выбранные14B/Llama historyагрегатытолькоcustomer_id;Qwen7B включаетcategory/customer×department;причинностьне установлена. '
               'Report/таблицы/5PNG/bootstrap10kготовы. Одинseed250test,точечныйпорядокне доказываетустойчивоепревосходство. '
               'ИзначальныйWSLстекотклонилnullableboolLlama;точныеCPUверсииKaggleустановленыизолированновaudit_deps,старыеenvне менялись. '
               '4модели×val/testreplayточносовпали. Никакогообучения/измененияисходныхZIP.')
    record('kaggle_small_llms_comparison', message, 'hm_small_llms_comparison_v1', status='complete',
           artifacts='reports/hm_small_llms_v1', audit='reports/hm_small_llms_v1/audit.json',
           report='reports/hm_small_llms_v1/report.md', bootstrap='reports/hm_small_llms_v1/paired_test_bootstrap.csv')
    for generic, actual in [('hm_small_qwen_llama_sql_v1', parent), ('hm_small_qwen14b_sql_v1', 'hm_small_qwen14b_sql_v1_f373011050bf')]:
        record('external_run_audited', 'Kaggle запуск завершён и проверен; фактические результаты отдельно: ' + actual,
               generic, status='completed_on_kaggle_audited', actual_run_id=actual, artifacts='reports/hm_small_llms_v1')
    context = ROOT / 'CONTEXT.md'
    text = context.read_text(encoding='utf-8')
    heading = '## Проверенные реальные Kaggle результаты трёх LLM на small-v1 (2026-10-16)'
    if heading not in text:
        lines = [heading, '', message, '',
                 'Исходные архивы hm_small_qwen_llama_sql_v1_2ecc60d61fd4_results.zip и hm_small_qwen14b_sql_v1_f373011050bf_results.zip сохранены.',
                 'Конфиги/версии/T4/4sharedsourceSHA совпали. Data:72813train/4804user-time/8cutoffs,search128/confirm88/heldout88,val304/test250/5000catalog.',
                 'Обаrawконтроля идентичны по моделям и прогнозам. Выборtop3+rawпоconfirm проверен;тест не использовался для переотбора.',
                 'CPU audit versions:numpy2.1.3,pandas2.3.3,pyarrow23.0.1,duckdb1.4.1,lightgbm4.6.0. Файлы и первоначальные failurelogs в reports/hm_small_llms_v1.',
                 'ПрежнейPandasIDошибкинет:joinsownedbyhost;проверкиперестановки/блоковпрошли. Raw item features присутствуют у всех.',
                 'Отчёт reports/hm_small_llms_v1/report.md,audit.json,comparison_all_methods.csv,search_efficiency.csv,paired_test_bootstrap.csv;5PNG.',
                 'НовыеKaggleрезультатыне smoke;локальныеfakefixturesотдельно. Не сравнивать малыйкаталог со старымполнымH&M/статьёй.', '']
        for title in ['Qwen7B_LightGBM', 'Llama8B_LightGBM', 'Qwen14B_LightGBM']:
            stats, row = audit['models'][title], rows[title]
            lines.append(f"{title}: val/testMAP={row['val_map_percent']:.8f}%/{row['test_map_percent']:.8f}%,calls{stats['calls']},selected{stats['selected_call']},statuses{stats['statuses']}.")
        section = '\n' + '\n'.join(lines) + '\n\n'
        context.write_text(text.replace('# Контекст для продолжения проекта\n', '# Контекст для продолжения проекта\n' + section, 1), encoding='utf-8')


if __name__ == '__main__':
    main()
