"""Finalize diagnostics after human-visible figure inspection; no model changes."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'CVFollowup'))
from common import read,write,sha,record
import novelty_audit as audit


def main():
    rep=audit.REP
    assert read(rep/'visual_review.json')['passed']
    table=pd.read_csv(rep/'metrics.csv')
    checked=0
    for fold in range(3):
        for key in audit.methods(fold):
            assert read(audit.output(fold,key)/'verification.json')['passed']
            checked+=1
    assert checked==45
    expected={x['method']:x['pooled_map'] for x in read(rep.parent/'context_combined_test_v1/comparison.json')['summary']}
    expected['contextgnn_old']=next(x['pooled_map'] for x in read(rep.parent/'final_comparison/comparison.json')['summary'] if x['method']=='contextgnn')
    normal=table[(table['mode']=='normal')&(table['group']=='all')].set_index('method')
    for key,value in expected.items():
        assert abs(normal.loc[key,'map']-value)<1e-14,(key,value)
    frozen=read(rep/'protocol.json')
    for name,digest in frozen['sources'].items():
        assert sha(ROOT/'CVFollowup'/name)==digest
    for name,digest in frozen['reference_hashes'].items():
        assert sha(ROOT/name)==digest
    write(rep/'final_verification.json',dict(passed=True,verified_model_folds=checked,
        original_maps_reproduced=True,reference_hashes_unchanged=True,
        frozen_analysis_sources_unchanged=True,metric_tests=read(rep/'metric_verification.json'),
        visual_review=read(rep/'visual_review.json')))
    summary=read(rep/'summary.json');summary['status']='complete_verified_diagnostics'
    summary['history_start']='2019-09-07'
    write(rep/'summary.json',summary)
    report=(rep/'report_ru.md').read_text(encoding='utf-8')
    for before,after in {
        '5519наблюдений/4548покупателей':'5 519 наблюдений / 4 548 покупателей',
        'дают0':'дают 0', 'поID':'по ID',
        'содержит5000парныхbootstrap':'содержит 5 000 парных bootstrap-оценок',
        'ContextGNN,ID-GNN,Recformer,manual,H008/H009':'ContextGNN, ID-GNN, Recformer, manual, H008/H009',
    }.items():report=report.replace(before,after)
    (rep/'report_ru.md').write_text(report,encoding='utf-8')
    lines=['# Выводы проверки новых товаров','',
        'ContextGNN combined — ранее обученная комбинация fanout [64, 32] и восьми категориальных кодов. '
        'Это та же архитектура ContextGNN, которая показана на последнем сравнительном графике; '
        'в этой диагностике модели не обучались и API не вызывались.','',
        '| Метод | MAP обычного top-12, % | Доля MAP от повторов, % | Recall доступных новых, обычный top-12, % | Recall доступных новых, после исключения покупок, % |',
        '|---|---:|---:|---:|---:|']
    for key in ['contextgnn','contextgnn_old','idgnn','recformer_zero','recformer_tuned','manual','h008_20','h009_40']:
        rows=table[table.method==key]
        def row(mode,group):return rows[(rows['mode']==mode)&(rows['group']==group)].iloc[0]
        total=row('normal','all')['map'];repeat=row('normal','repeat').ap_contribution
        n=row('normal','new').available_macro_recall;masked=row('new_only','new').available_macro_recall
        lines.append(f"| {rows.label.iloc[0]} | {100*total:.4f} | {100*repeat/total:.2f} | {100*n:.4f} | {100*masked:.4f} |")
    lines+=['','Доля MAP от повторов не означает такую же долю повторных покупок. '
        'Recall новых усреднён по наблюдениям с доступной новой целью. '
        'Полные метрики с недоступными целями, численность групп и интервалы приведены в основном отчёте.', '',
        '«Новый» означает отсутствие article_id в доступной исходной истории с 2019-09-07 '
        'до соответствующего cutoff. Это не полная история жизни покупателя. '
        'Доступность означает присутствие в фиксированном каталоге из 10 000 кандидатов, '
        'а не наличие на складе. Отсутствующие в каталоге будущие цели сохранены в полных знаменателях.', '',
        'Эта проверка измеряет попадания в наблюдавшиеся будущие покупки. Она не измеряет '
        'все потенциальные интересы пользователя и не доказывает переносимость на другой датасет. '
        'Внутренний test уже анализировался; результаты являются диагностикой, а не независимым подтверждением.', '',
        'У ID-GNN после маски остаются нулевые скоры: заполнение по ID нельзя трактовать '
        'как обученное персональное ранжирование новых товаров. TDM сохраняет исходный beam64.', '',
        '[Полный отчёт](report_ru.md) · [Вклады в MAP](ap_contributions.png) · [Новые товары](new_item_recall.png)','']
    (rep/'interpretation_ru.md').write_text('\n'.join(lines),encoding='utf-8')
    record('novelty_orchestration_note','The first auxiliary parallel-dispatch launch used an incorrect repository parent path and failed before signaling the dispatcher or running any scoring. Corrected parents[4] to parents[3]; two independent folds then completed and the dispatcher resumed. Frozen model, metric and protocol sources were unchanged.',audit.RUN)
    record('novelty_complete','All 45 frozen-model/fold rankings verified; original MAPs exactly reproduced, unavailable targets retained; tables, paired customer intervals and both figures verified. No training/API in this audit.',audit.RUN,
        status='complete_verified_diagnostics',artifacts=str(rep.relative_to(ROOT)),verified_model_folds=checked)


if __name__=='__main__':main()
