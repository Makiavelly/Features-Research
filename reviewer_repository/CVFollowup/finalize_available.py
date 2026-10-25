"""Record independently verified results after manual review of all report images."""
from common import ROOT,OUT,REPORT,read,write,sha,record

def main():
    dest=REPORT/'final_comparison';result=read(dest/'comparison.json');extra=read(dest/'available_summary.json')
    assert result['status']=='passed' and result['users']==5519
    frozen=read(REPORT/'recformer_pretest_freeze.json');selected=frozen['selected_label']
    assert frozen['scope']=='available_three_of_four_new_settings'
    for fold in range(3):
        folder=OUT/f'fold_{fold}/recformer_grid'/selected
        assert read(folder/'verification.json')['passed']
        assert sha(folder/'finetuned/best.pt')==frozen['checkpoints'][str(fold)]
        m=read(folder/'finetuned/metrics.json')
        record('available_recformer_verified',f'Selected available-grid Recformer {selected}, fold{fold}: test/replay verified; no new fit.',
            f'hm_medium_recformer_tune_f{fold}_{selected}_seed42_v1',status='evaluated_verified',
            val_metrics=m['val_metrics'],test_metrics=m['test_metrics'],artifacts=str(folder.relative_to(ROOT)))
        for mode in ['h008','h009']:
            for budget in [20,30,40]:
                p=OUT/f'fold_{fold}'/mode/f'budgets/{budget}'
                assert read(p/'verification.json')['passed']
                record('available_api_budget_verified',f'Fold{fold} {mode} budget{budget}: frozen selection test/replay and independent AP verified.',
                    f'hm_medium_followup_f{fold}_{mode}_budget{budget}_seed42_v1',status='evaluated_verified',
                    test_metrics=read(p/'test_metrics.json'),artifacts=str(p.relative_to(ROOT)))
    plots=['comparison.png','fold_comparison.png','ap_histograms.png','api_budget_curves.png','recformer_validation_grid.png']
    write(dest/'visual_review.json',{'passed':True,'reviewed_by':'Codex visually inspected all five PNGs; labels/scales/readability checked',
        'plots':{p:sha(dest/p) for p in plots},'scope':frozen['scope'],
        'recformer_checkpoint_sha256_verified_after_test':True})
    s={r['method']:r for r in result['summary']}
    record('available_results_summary_verified','Available-results summary complete: corrected GNN, API20/30/40 and validation-selected Recformer evaluated; paired bootstrap and five figures visually verified. Missing Kaggle lr3e6_w100 explicitly excluded, original full grid not claimed complete.',
        'hm_medium_followup_available_summary_v1',status='complete_available_summary',
        artifacts=str((dest/'summary_ru.md').relative_to(ROOT)),summary=result['summary'],contrasts=extra['contrasts'])
    record('recformer_available_grid_closed','User requested summary without unavailable Kaggle run. Nine of twelve originally planned new fits complete, selected available setting evaluated. Original full grid remains incomplete; no active wait or new training.',
        'hm_medium_recformer_distributed_v1',status='closed_available_summary',artifacts=str((dest/'summary_ru.md').relative_to(ROOT)))
    record('recformer_available_grid_closed','Available grid selected and evaluated on three folds. Original four-setting grid is incomplete: lr3e6_w100 unavailable. No training remains active; preserve completed fits.',
        'hm_medium_recformer_grid_seed42_v1',status='closed_available_summary',artifacts=str((dest/'summary_ru.md').relative_to(ROOT)))
    record('api_budget_report_complete','All six API streams and18 frozen20/30/40 budget evaluations/replays complete; comparisons, usage and incumbent-selection audit published.',
        'hm_medium_followup_api_budget_v1',status='complete',artifacts=str((dest/'api_budget_curves.png').relative_to(ROOT)))
    note=f'''## Сводка доступных результатов завершена (2026-10-18)

Актуальный отчёт: reports/medium_followup_v1/final_comparison/summary_ru.md,
comparison.json, available_summary.json,5PNG/SVG и CSV парных разниц.
Все5PNG визуально проверены; source checkpoint hashes совпали после оценки.
Три фолда,5519user-times, seed42;5000paired customer bootstrap.
ContextGNN pooled MAP={100*s['contextgnn']['pooled_map']:.4f}%;
IDGNN={100*s['idgnn']['pooled_map']:.4f}%;
Recformer tuned({selected})={100*s['recformer_tuned']['pooled_map']:.4f}%;
Recformer zero={100*s['recformer_zero']['pooled_map']:.4f}%.
H008 budget20/30/40={100*s['h008_20']['pooled_map']:.4f}/{100*s['h008_30']['pooled_map']:.4f}/{100*s['h008_40']['pooled_map']:.4f}%;
H009={100*s['h009_20']['pooled_map']:.4f}/{100*s['h009_30']['pooled_map']:.4f}/{100*s['h009_40']['pooled_map']:.4f}%.
API:240принятыхAST-программ,18выборов/оценок прошли replay/independentAP.
Выявлен shortlist bottleneck: прежний confirmation winner может выпасть
из top3search при расширении бюджета. Наfold0H008call8 при20 имел confirm0.7180%,
при30/40 исключён; выбранcall14confirm0.6966%. Не переотбирали задним числом.
Следующее сохранение incumbent — отдельная гипотеза/новый эксперимент.
Recformer:3из4новыхнастроек+baseline; lr3e6_w100 не запустилась в Kaggle,
исключена по доступности. Девять новыхfit готовы; исходная полная сетка
НЕзавершена. Выбранная настройка зафиксирована только по inner validation,
test/replay проведены без нового обучения. Ожидающие контроллеры остановлены.
Не запускать старый recformer_lane/distributed для этой сводки. Если четвёртая
настройка появится позже, создавать новый протокол/отчёт, не заменять этот.
Одинseed/тринедели/ранее просмотренныеtest: не делать сильных claims о
других временныхрежимах. Численное replay ограничениеGNNfold2 описано.

'''
    path=ROOT/'CONTEXT.md';text=path.read_text(encoding='utf-8')
    if note not in text:path.write_text(note+text,encoding='utf-8')

if __name__=='__main__':main()
