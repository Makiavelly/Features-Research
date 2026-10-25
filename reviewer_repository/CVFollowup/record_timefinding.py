from common import ROOT,record

note='''## Исправление GNN и новые проверки (2026-10-18)

Выявлена ошибка загрузчика: medium validation/test в datetime64[ms] ошибочно
считались ns. Входной cutoff становился около 1597 секунд вместо 1.597e9,
и ContextGNN/ID-GNN не получали историю. Их прежние medium-метрики и выбор
checkpoint невалидны; предыдущие цифры ниже сохранены как история ошибки.
Проверки и исправленные запуски: CVFollowup/GNN_TIMEFIX_PROTOCOL.md,
reports/medium_followup_v1/graph_time_audit.json, graph_time_fix_verification.json.
Отдельные новые веса: CVFollowup/results/v1/fold_*/gnn_timefix_refit/.
API H008/H009 продолжаются с прежних20 к30/40; Recformer — сетка четырёх
LR/warmup настроек на трёх фолдах, выбор только по inner validation.

'''
path=ROOT/'CONTEXT.md'
text=path.read_text(encoding='utf-8')
if note not in text:path.write_text(note+text,encoding='utf-8')
for name in ['report.md','summary_ru.md']:
    path=ROOT/'reports/medium_cv_v2'/name
    text=path.read_text(encoding='utf-8')
    warning='> Исправление 2026-10-18: результаты ContextGNN и ID-GNN в этом историческом отчёте невалидны из-за ошибки единиц timestamp при validation/test. См. ../../CVFollowup/GNN_TIMEFIX_PROTOCOL.md. Остальные цифры этим аудитом не опровергнуты.\n\n'
    if warning not in text:path.write_text(warning+text,encoding='utf-8')
record('gnn_timestamp_root_cause','Confirmed ms/ns cutoff bug: all six medium GNN validation/test splits sampled no transaction context. Historical GNN scores and checkpoint selection invalid; isolated correction and refits scheduled. Original artifacts retained.',
       'hm_medium_gnn_timefix_v1',status='diagnosing',artifacts='reports/medium_followup_v1/graph_time_audit.json')
