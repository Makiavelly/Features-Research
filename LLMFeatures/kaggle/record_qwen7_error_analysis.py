"""Persist the user's7B choice and completed analysis, not a new experiment."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/qwen7b_generation_errors_v1'
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record


def main():
    result = json.loads((OUT / 'analysis.json').read_text())
    assert result['calls'] == 67 and result['proposed_examples_bind_checked']
    message = ('Пользователь выбрал Qwen2.5-Coder-7B-Instruct. Разобраны67реальныхответовsmall-v1: '
               '20валидных/30отказов/17дубликатов;JSON67/67,обрезаний0. Первыеошибки9строковыхрезультатов,8OVER,6keys, '
               '4history-в-derived,2SQLsyntax,1ID-в-derived. У18ответов несколько проблемныхfeatures;13/40repair '
               'возвращаютнеизменённуюпрограмму(7отказов,6дубликатов).9/17дубликатов=candidate001. '
               'Сохраненывсеошибкипоfeatures/цепочки/примеры/promptaddendum/repairtemplate;SQLпримерыEXPLAIN-проверены '
               'DuckDB1.4.1насинтетическойсхеме. Нетгенерации/обучения/переоценкиMAP/измененийрабочихноутбуков. '
               'H003A/B/CвHYPOTHESES.md предложены,не запущены. Устойчивое превосходство7Bне доказано;testуже просмотрен.')
    record('qwen7_generation_error_analysis', message, artifacts='reports/qwen7b_generation_errors_v1',
           analysis='reports/qwen7b_generation_errors_v1/analysis.json', chosen_model='Qwen/Qwen2.5-Coder-7B-Instruct',
           proposed_hypothesis='H003', experiment_started=False)
    context = ROOT / 'CONTEXT.md'
    text = context.read_text(encoding='utf-8')
    heading = '## Выбрана Qwen7B: разбор ошибок генерации (2026-10-16)'
    if heading not in text:
        section = '\n' + heading + '\n\n' + message + '\n\n'
        section += ('Источник:small-v1/qwen,не смешиватьсошибкамиLlama/v5. Приоритет:адресныеспискиошибоквсехfeatures; '
                    'затемотдельнопримерыprompt;затемduplicate/unchanged. SQLJSONсохранитьдляпервогосравнения. '
                    'Рабочиеметрики/ноутбукине менялись;H003ещёнепоручензапускать.\n\n')
        context.write_text(text.replace('# Контекст для продолжения проекта\n', '# Контекст для продолжения проекта\n' + section, 1), encoding='utf-8')


if __name__ == '__main__':
    main()
