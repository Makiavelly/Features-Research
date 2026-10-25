"""Document causal same-checkpoint evidence without selecting on test metrics."""
from common import ROOT,OUT,OLD,REPORT,read,write,sha,record

def main():
    current=OUT/'fold_0/gnn_timefix_existing'
    assert read(current/'verification.json')['passed']
    audit=read(current/'sampling_audit.json');assert sum(row['article_nodes'] for row in audit)>0
    rows=[]
    for kind in ['contextgnn','idgnn']:
        old=OLD/'fold_0/gnn'/kind;new=current/kind
        assert sha(old/'best.pt')==sha(new/'best.pt')
        before,after=read(old/'metrics.json'),read(new/'metrics.json')
        rows.append({'model':kind,'checkpoint_sha256':sha(old/'best.pt'),
            'before_val_map':before['val_metrics']['map'],'after_val_map':after['val_metrics']['map'],
            'before_test_map':before['test_metrics']['map'],'after_test_map':after['test_metrics']['map']})
    write(REPORT/'same_weights_timefix_diagnostic.json',{'passed':True,'fold':0,'rows':rows,
        'scope':'Identical old weights, only cutoff unit correction; causal diagnostic. Old validation checkpoint selection was wrong, so these are not final corrected training results.',
        'sampling_context_restored':True,'non_gnn_time_audit_passed':read(REPORT/'other_models_time_audit.json')['passed']})
    record('gnn_same_weights_causal_check','Same old fold0 checkpoint weights, corrected cutoffs: ContextGNN test MAP0.0309% ->1.4616%; IDGNN0% ->1.0529%. Full inference replay passed; diagnostic only, corrected validation refits in progress.',
        'hm_medium_gnn_timefix_existing_f0_v1',status='diagnostic_verified',results=rows,
        artifacts='reports/medium_followup_v1/same_weights_timefix_diagnostic.json')
    path=ROOT/'CONTEXT.md';text=path.read_text(encoding='utf-8')
    note='''### Дополнительная проверка 2026-10-18

Те же веса fold0 после исправления cutoff: ContextGNN test MAP0.0309% →1.4616%,
ID-GNN0% →1.0529%. Полный replay прошёл. Это причинная диагностика,
не итоговые результаты переобучения. См. same_weights_timefix_diagnostic.json.
Проверены actual SQL-фильтры manual/raw/API и функции истории Recformer/TDM:
все6 validation/test прошли, ms/ns-ошибка их не затронула. См. other_models_time_audit.json.
Живые очереди проверять: api_lane.pid, gpu_followup.pid, report_watch.pid
в reports/medium_followup_v1. GPU: исправленные6GNN, затем12Recformer fits.
API: наследованные20 →30 →40 в каждом из6 потоков; outer-оценка после freeze.
Новые отчёты создаются автоматически; PNG требуют визуальной проверки Codex.

'''
    if note not in text:path.write_text(note+text,encoding='utf-8')

if __name__=='__main__':main()
