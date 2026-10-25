"""Record completed corrected GNN comparison after manual visual review."""
from common import ROOT,REPORT,read,write,sha,record

def main():
    directory=REPORT/'gnn_corrected'
    result=read(directory/'comparison.json')
    assert result['status']=='passed'
    assert 'Ограничение replay' in (directory/'report.md').read_text(encoding='utf-8')
    plots=['comparison.png','fold_comparison.png','ap_histograms.png']
    write(directory/'visual_review.json',{'passed':True,'reviewed_by':'Codex: all three PNGs visually inspected; labels/axes readable',
        'plots':{p:sha(directory/p) for p in plots},'numeric_replay_limitation':'See NUMERIC_REPLAY_AMENDMENT.md; no bitwise-deterministic score claim'})
    record('corrected_gnn_report_verified','Corrected three-fold comparison generated and visually checked: ContextGNN pooled MAP1.2791%, IDGNN1.1613%, Recformerzero0.6286%, H00820sets0.4627%. Fold2 numerical replay limitation explicit; API30/40 and Recformer tuning still ongoing.',
        'hm_medium_followup_report_gnn_v1',status='verified_report',artifacts=str(directory.relative_to(ROOT)))
    path=ROOT/'CONTEXT.md';text=path.read_text(encoding='utf-8')
    note='''## Актуально: исправленные GNN завершены, 2026-10-18

Все6 GNN обучены и оценены. Pooled MAP: ContextGNN1.2791%, IDGNN1.1613%.
Новый отчёт и3визуально проверенныхPNG: reports/medium_followup_v1/gnn_corrected/.
Fold2 ContextGNN strict replay остановился: скоры отличаются максимум2.72e-5.
Дополнительный replay: test top12 точные; validation near-tie перестановки,
AP каждого пользователя совпадает. Исходный failure сохранён; применена
явная bounded-FP32/tie-aware проверка, см.CVFollowup/NUMERIC_REPLAY_AMENDMENT.md.
Не заявлять побитовую детерминированность. GPU-controller gnn_lane умер на
первой строгой проверке; НЕперезапускать его одновременно с Recformer!
Recformer продолжен отдельно через recformer_lane.py (PIDфайл актуально проверять).
API H008fold0 достиг39/40, были transport timeouts; retries ограничены.
H009 и остальные фолды продолжаются той же API-очередью послеfold0H008.
Reportwatch живёт отдельно и ожидает концаAPI+Recformer для финального отчёта.

'''
    if note not in text:path.write_text(note+text,encoding='utf-8')

if __name__=='__main__':main()
