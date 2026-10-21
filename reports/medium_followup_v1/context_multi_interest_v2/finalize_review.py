"""Finalize only after opening and visually checking final_comparison.png."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'CVFollowup'))
from common import read,write,sha,record
REP=Path(__file__).resolve().parent
DEST=ROOT/'CVFollowup/results/v1/context_multi_interest_v2'
protocol=read(REP/'protocol.json')
for name,digest in {**protocol['reference_hashes'],**protocol['sources']}.items():
    assert sha(ROOT/name)==digest,name
assert read(REP/'pool_smoke.json')['passed'] and read(REP/'model_probe.json')['passed']
changed=0;max_ap=0.;details=[]
for f in range(3):
    control=DEST/f'fold_{f}/control'
    original=ROOT/f'CVFollowup/results/v1/context_global_aux_v3/fold_{f}/control'
    assert sha(control/'best.pt')==sha(original/'best.pt')
    history=read(control/'history.json')
    one=read(DEST/f'fold_{f}/interest1/initial_pool.json')
    four=read(DEST/f'fold_{f}/interest4/initial_pool.json')
    for field in ['shared_hidden','shared_project','head0_sha256']:
        assert one[field]==four[field],(f,field)
    masks=np.load(DEST/f'fold_{f}/seen_mask.npy')
    ann=read(DEST/f'fold_{f}/annotations.json')
    for arm in ['interest1','interest4']:
        p=DEST/f'fold_{f}'/arm;result=read(p/'result.json')
        assert result['interests']==(1 if arm=='interest1' else 4)
        assert result['no_auxiliary_loss'] and result['lambda_global']==0
        assert sha(p/'best.pt')==result['checkpoint_sha256']
        assert result['initial_state_sha256']==read(control/'result.json')['initial_state_sha256']
        own=read(p/'history.json')
        for x,y in zip(own,history):assert x['training_graph_sha256']==y['training_graph_sha256']
        other=read(DEST/f'fold_{f}/interest1/history.json')
        for x,y in zip(own,other):assert x['training_graph_sha256']==y['training_graph_sha256']
        replay=read(p/'replay_verification.json')
        checks=[*replay['native'],*replay['reload'].values()]
        for c in checks:
            assert c['max_score_difference']<=c['bound']
            changed+=len(c['changed_rows']);max_ap=max(max_ap,c['max_per_user_ap_difference'])
        hybrid=np.load(p/'val_hybrid_scores.npy');global_scores=np.load(p/'val_global_scores.npy')
        predictions=np.argsort(-hybrid,axis=1,kind='stable')[:,:12]
        np.testing.assert_array_equal(predictions,np.load(p/'val_predictions.npy'))
        # All local replacements should disappear when source-history items are masked.
        np.testing.assert_array_equal(hybrid[~masks],global_scores[~masks])
        hits=np.array([[int(item) in a['targets'] for item in pred] for pred,a in zip(predictions,ann)])
        ap=(hits*np.cumsum(hits,axis=1)/np.arange(1,13)).sum(1)/np.array([min(12,len(a['targets'])) for a in ann])
        np.testing.assert_allclose(ap,np.load(p/'val_ap.npy'),atol=1e-12,rtol=0)
        diagnostic=read(p/'head_diagnostics.json')
        assert diagnostic['checkpoint_sha256']==result['checkpoint_sha256']
        assert abs(sum(diagnostic['global_catalog_winner_fractions'])-1)<1e-12
        details.append(dict(fold=f,arm=arm,best_epoch=result['best_epoch'],epochs=result['epochs'],
            head_winner_fractions=diagnostic['global_catalog_winner_fractions'],
            mean_query_pair_cosine=diagnostic['mean_query_pair_cosine'],
            mean_attention_pair_cosine=diagnostic['mean_attention_pair_cosine']))
table=pd.read_csv(REP/'final_metrics.csv')
contrasts=pd.read_csv(REP/'final_contrasts.csv')
assert len(contrasts)==12
status='complete_validation_with_replay_qualification' if changed else 'complete_verified_validation'
summary=read(REP/'final_summary.json')
summary.update(status=status,replay_changed_rows_in_checks=changed,max_per_user_ap_replay_sensitivity=max_ap,
    no_test=True,new_fits=6,reused_controls=3,head_diagnostics=details)
write(REP/'final_summary.json',summary)
write(REP/'visual_review.json',dict(passed=True,image='final_comparison.png',
    checks=['Four metric groups readable','Three methods correctly labeled','Axes/title/legend fit']))
write(REP/'final_verification.json',dict(status=status,passed=True,
    new_fits=6,reused_controls=3,shared_initial_weights_and_head0_matched=True,
    common_epoch_training_graphs_matched=True,local_formula_probe_passed=True,
    new_only_equals_masked_global=True,independent_AP_verified=True,
    references_and_sources_unchanged=True,replay_changed_rows_in_checks=changed,
    max_per_user_ap_replay_sensitivity=max_ap,head_diagnostics=details,
    no_test=True,no_api=True,visual_review_passed=True))
lines=['','## Проверки и использование голов','',
    f'Все шесть fit и три прежних контроля проверены. Native/reload: {changed} строк с изменением top12 '
    f'(сумма проверок), максимальная чувствительность AP={max_ap:.10g}. Канонические оценки сохранены. '
    'После маски всей истории hybrid совпадает с global: локальные замены относятся к прошлым товарам.','',
    '| Фолд K=4 | Доли побед голов по всему каталогу | Средний cosine запросов | Средний cosine attention |',
    '|---|---|---:|---:|']
for d in details:
    if d['arm']=='interest4':
        shares=' / '.join(f'{100*x:.1f}%' for x in d['head_winner_fractions'])
        lines.append(f"|{d['fold']}|{shares}|{d['mean_query_pair_cosine']:.4f}|{d['mean_attention_pair_cosine']:.4f}|")
lines+=['','Это описательные признаки сходства/использования голов; распределение побед само по себе не доказывает наличие четырёх разных семантических интересов.','']
lines+=['## Группы новизны после исключения прошлых покупок','',
    '| Новые товары | Наблюдений с доступной целью | FUSION | attention K=1 | attention K=4 |',
    '|---|---:|---:|---:|---:|']
for group in ['new_variant','new_product_known_type','new_type']:
    part=table[(table['mode']=='new_only')&(table['group']==group)].set_index('arm')
    values=[f"{100*part.loc[arm,'available_recall']:.4f}%" for arm in ['control','interest1','interest4']]
    lines.append('|'+group+'|'+str(int(part.loc['control','available_users']))+'|'+'|'.join(values)+'|')
lines+=['','Подгруппы описательные, малые и без отдельных интервалов значимости; те же доступные цели/наблюдения во всех вариантах.','']
with (REP/'final_report_ru.md').open('a',encoding='utf-8') as stream:stream.write('\n'.join(lines))
measurements=[]
for mode,group,metric in [('hybrid','all','map'),('global','all','map'),('hybrid','new','available_recall'),('new_only','new','available_recall')]:
    values=[float(table[(table.arm==arm)&(table['mode']==mode)&(table['group']==group)][metric].iloc[0]) for arm in ['control','interest1','interest4']]
    measurements.append(f'{mode}/{metric}: '+ ' / '.join(f'{100*v:.4f}%' for v in values))
message='FUSION / attentionK1 / attentionK4: '+'; '.join(measurements)
with (ROOT/'CONTEXT.md').open('a',encoding='utf-8') as stream:
    stream.write(f'\n\n## ContextGNN multi-interest: validation завершена (2026-10-19)\n\n'
        f'Run `{protocol["run_id"]}`: {status}. Шесть новых fit/три reused контроля. {message}. '
        f'Общие начальные веса/shared pool/head0 и обучающие графы совпали. Smoke/probe, независимый AP, '
        f'FP32 replay и SHA проверены; {changed} строк top12 изменилось в проверках, max AP sensitivity={max_ap:.10g}. '
        'Primary K4-K1 и secondary K4-FUSION,5000 paired customer-bootstrap,12 контрастов без multiple-testing поправки: '
        '`reports/medium_followup_v1/context_multi_interest_v2/final_contrasts.csv`. '
        'Отчёт `final_report_ru.md`, график `final_comparison.png` проверен визуально. '
        'Отдельные head_diagnostics.json измеряют использование/сходство голов. '
        'Локальные scores неизменны по формуле; после source-history mask hybrid=global. '
        'Будущие недоступные цели сохранены; условная новизна на493 наблюдениях. '
        'Адаптация ComiRec-SA к sampled temporal graph, не reproduction. Один seed, просмотренная validation, test/API не использовались.\n')
record('multi_interest_complete',message+f'; six new fits verified, three controls unchanged. Matched common initialization and training graphs, independent AP, replay ranks/AP measured ({changed} changed checks, max AP {max_ap:.10g}), graph visually reviewed. No test/API.',
    protocol['run_id'],status=status,artifacts=str(REP.relative_to(ROOT)),new_fits=6,reused_controls=3,
    replay_changed_rows_in_checks=changed,max_per_user_ap_replay_sensitivity=max_ap)
print(status,message)
