"""Track the running/completed Python experiment without altering its frozen code."""
import argparse
import csv
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--complete',action='store_true')
    args=parser.parse_args()
    info=json.loads((ROOT/'reports/provider_python_v1/current_run.json').read_text())
    folder=Path(info['directory'])
    state=json.loads((folder/'gpt61sol_python/search_state.json').read_text())
    calls=len(list((folder/'api_attempts').glob('attempt_*')))
    if not args.complete:
        message=(f"H006 Pythonv2: {state['measured']}/20 полностью оценённых наборов, "
                 f"{calls}/300 фактических API запросов. Бюджет включает исходные9POST v1. "
                 'v1 сохранён; v2 выравнивает столбцы по именам и проверяет пустую историю. '
                 '29 регрессий пройдено, два реальных набора (11+17 признаков) совпали с независимым SQL по8срезам. '
                 'Неограниченный exec был отклонён автоматической проверкой безопасности и не выполнялся; '
                 'проверки модельного кода идут через ограниченный wrapper.')
        record('provider_python_progress',message,info['run_id'],status='searching',
               api_requests=calls,evaluated_distinct=state['measured'],artifacts=str(folder.relative_to(ROOT)))
        path=ROOT/'CONTEXT.md'
        content=path.read_text(encoding='utf-8-sig')
        marker='## H006 — GPT-6.1 Sol: полная Python-функция'
        entry=('\nТекущий поток: '+info['run_id']+'. '+message+'\n\n')
        if 'Текущий поток: hm_small_gpt61sol_python_seed42_v2' not in content:
            content=content.replace(marker+'\n',marker+'\n'+entry,1)
            path.write_text(content,encoding='utf-8')
        return
    out=ROOT/'reports/gpt61sol_python_v1'
    audit=json.loads((out/'audit.json').read_text())
    validator=json.loads((out/'validator_review.json').read_text())
    numeric=json.loads((out/'numeric_reference_verification.json').read_text())
    diversity=json.loads((out/'feature_diversity.json').read_text())
    assert audit['status']==validator['status']==numeric['status']==diversity['status']=='passed'
    assert validator['calls_reviewed']==state['calls']
    assert (out/'report.md').exists() and state['measured']==20
    rows=list(csv.DictReader((out/'comparison.csv').open()))
    result=next(r for r in rows if r['model']=='GPT61Sol')
    test=float(result['test_map_percent']);val=float(result['val_map_percent'])
    summary=(f'H006 завершена и независимо проверена: Python test MAP@12 {test:.6f}%, '
             f'validation {val:.6f}%; SQL 0.979030%, прежний Qwen7B 1.107143%, raw 0.959630%. '
             f'20 оценённых программ, {calls} фактическихAPIPOST в одном потоке; '
             f"отказовкода {audit['stats']['statuses'].get('rejected',0)}, "
             f"дубликатов {audit['stats']['statuses'].get('duplicate',0)}, "
             f"ошибокAPI {audit['stats'].get('api_failures_count',0)}. "
             'v1 сохранён, исправлениеv2 выполнено до итогового выбора/test без повторной генерации первых8ответов. '
             '29 регрессий, дополнительный разбор всех ответов и независимые SQL эталоны пройдены. '
             f"Численно различных train-матриц {diversity['groups']['ordered_float32_sha256']['distinct']} из20; "
             'confirmation-кандидаты численно различаются. Все12признаков победителя выраженыSQL '
             'и дают точно те жеfloat32 значения на всех72813train-парах. '
             'Одинseed/250ранее просмотренныхtest пользователей; это диагностическое сравнение, не воспроизведение статьи.')
    record('provider_python_experiment_audited',summary,info['run_id'],status='complete',
           artifacts=str(out.relative_to(ROOT)),api_requests=calls,evaluated_distinct=20,
           val_metrics={'map':val/100},test_metrics={'map':test/100},
           independent_audit='passed',validator_audit='passed',source_run='hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1')
    entry='\n## Итог H006: Python / GPT-6.1 Sol (2026-10-17)\n\n'+summary+'\n\n'
    entry+='Отчёт: reports/gpt61sol_python_v1/report.md; сравнение, графики, гистограммы и разбор валидатора рядом.\n\n'
    for name in ['CONTEXT.md','HYPOTHESES.md']:
        path=ROOT/name
        content=path.read_text(encoding='utf-8-sig')
        if name=='CONTEXT.md':
            content='\n'.join(line for line in content.split('\n') if not line.startswith('Текущий поток: hm_small_gpt61sol_python_seed42_v2'))
        if '## Итог H006: Python / GPT-6.1 Sol' not in content:
            first=content.index('\n')+1
            path.write_text(content[:first]+entry+content[first:],encoding='utf-8')


if __name__=='__main__':main()
