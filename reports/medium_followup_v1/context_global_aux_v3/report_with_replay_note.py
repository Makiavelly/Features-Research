from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'CVFollowup'))
import context_global_aux_v3 as run
from common import read,write,record

run.report()
d=read(run.REP/'last_fit_replay_diagnostics.json')
note=['','## Уточнение проверки перезагрузки','',
    'Пять fit прошли проверку точного top-12. У последнего fit (fold2, lambda1) '
    'проверка точного top-12 остановилась при оценках внутри исходного допуска FP32. '
    'Выполнен отдельный повторный инференс без обучения. Исходные checkpoint и '
    'оценки выбранной эпохи сохранены; основные таблицы рассчитаны по этим исходным оценкам. '
    'Ни один повтор не выбирался по лучшим метрикам.', '',
    '| Ветка | Максимальная разница оценок | Допуск | Строк с изменением top12 | MAP исходный, % | MAP replay, % |',
    '|---|---:|---:|---:|---:|---:|']
for key,v in d['branches'].items():
    note.append(f"| {key} | {v['max_score_difference']:.8g} | {v['bound']:.8g} | {len(v['changed_rows'])} | {100*v['canonical_map']:.6f} | {100*v['replay_map']:.6f} |")
note+=['',f"Все проверенные пользовательские MAP/recall совпали: {d['all_compared_metrics_identical']}. "
    'Подробности по группам, режимам и изменениям ранжирования — last_fit_replay_diagnostics.json. '
    'Требование точного top-12 для всех шести fit не выполнено; результат завершён с этой явной оговоркой.','']
with (run.REP/'report_ru.md').open('a',encoding='utf-8') as f:f.write('\n'.join(note))
write(run.REP/'verification_addendum.json',dict(reason='Observed FP32 near-tie replay variation after training, no model/data/selection change',
    canonical_scores_retained=True,no_refitting=True,exact_top12_all_fits=False,diagnostics=d))
record('global_aux_report_replay_qualification','Correction to automatic report-ready message: exact top12 replay passed for five fits, not all six. Last fit has FP32-bounded near-tie changes; their metric sensitivity is reported explicitly, canonical scores and checkpoint retained. No refitting or post-hoc checkpoint selection.',run.RUN,status='pending_visual_review',artifacts=str(run.REP.relative_to(ROOT)))
