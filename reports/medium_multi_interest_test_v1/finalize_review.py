"""Finalize test artifacts after visual inspection; add matched global-branch audit."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'CVFollowup'))
from common import read,write,sha,record
import novelty_audit as audit
REP=Path(__file__).resolve().parent
DEST=ROOT/'CVFollowup/results/v1/multi_interest_test_v1'
protocol=read(REP/'pretest_freeze.json')
for name,digest in {**protocol['reference_hashes'],**protocol['sources']}.items():assert sha(ROOT/name)==digest,name
summary=read(REP/'comparison.json');assert summary['methods_count']==21
metrics=pd.read_csv(REP/'metrics_new_methods.csv')
combined=pd.read_csv(REP/'metrics_all_methods.csv')
old=pd.read_csv(ROOT/'reports/medium_h010_h011_feature_novelty_v1/metrics_all_methods.csv')
pd.testing.assert_frame_equal(combined.iloc[:len(old)].reset_index(drop=True),old,rtol=1e-13,atol=1e-15)
for p in [REP/'comparison_all.png',REP/'comparison_all.svg']:assert p.stat().st_size>10000
changed=0;max_ap=0.;checks=[];global_rows=[]
for fold in range(3):
    annotation=read(audit.DEST/f'fold_{fold}/annotations.json')
    targets=[set(a['targets']) for a in annotation]
    for arm,key in [('control','fusion_matched'),('interest1','multi_interest1'),('interest4','multi_interest4')]:
        folder=DEST/f'fold_{fold}'/arm;check=read(folder/'verification.json');assert check['passed']
        assert sha(ROOT/f'CVFollowup/results/v1/context_multi_interest_v2/fold_{fold}/{arm}/best.pt')==check['checkpoint_sha256']
        checks.append(check)
        for value in check['reload'].values():
            assert value['max_score_difference']<=value['bound']
            changed+=len(value['changed_rows']);max_ap=max(max_ap,value['max_per_user_ap_difference'])
        matrix=np.load(folder/'test_global_scores.npy',mmap_mode='r')
        predictions=np.argsort(-matrix,axis=1,kind='stable')[:,:12]
        ap=[]
        for i,(pred,truth,a) in enumerate(zip(predictions,targets,annotation)):
            hits=np.array([int(p) in truth for p in pred],dtype=float)
            value=float((hits*np.cumsum(hits)/np.arange(1,13)).sum()/min(12,len(truth)))
            ap.append(value);global_rows.append(dict(fold=fold,row=i,customer=a['original_customer_id'],method=key,map=value))
        assert abs(np.mean(ap)-check['reload']['global']['canonical_map'])<1e-12
global_users=pd.DataFrame(global_rows);global_users.to_parquet(REP/'global_per_user.parquet',index=False)
keys=['fusion_matched','multi_interest1','multi_interest4'];columns=[];identity=None
for key in keys:
    frame=global_users[global_users.method==key].sort_values(['fold','row'])
    if identity is None:identity=frame[['fold','row','customer']].to_numpy()
    else:np.testing.assert_array_equal(identity,frame[['fold','row','customer']].to_numpy())
    columns.append(frame['map'].to_numpy())
matrix=np.stack(columns,axis=1)
assert matrix.shape==(5519,3)
_,inv=np.unique(identity[:,2],return_inverse=True);counts=np.bincount(inv)
sums=np.zeros((len(counts),3));np.add.at(sums,inv,matrix)
rng=np.random.default_rng(42);boot=[]
for _ in range(5000):
    sample=rng.integers(0,len(counts),len(counts));boot.append(sums[sample].sum(0)/counts[sample].sum())
boot=np.array(boot);lo,hi=np.quantile(boot,[.025,.975],axis=0)
global_metrics=[dict(method=key,map=float(matrix[:,i].mean()),low=float(lo[i]),high=float(hi[i])) for i,key in enumerate(keys)]
pd.DataFrame(global_metrics).to_csv(REP/'global_branch_metrics.csv',index=False)
global_differences=[]
for i,j in [(2,1),(2,0),(1,0)]:
    low,high=np.quantile(boot[:,i]-boot[:,j],[.025,.975])
    global_differences.append(dict(a=keys[i],b=keys[j],delta=float((matrix[:,i]-matrix[:,j]).mean()),low=float(low),high=float(high)))
pd.DataFrame(global_differences).to_csv(REP/'global_branch_paired_differences.csv',index=False)
status='complete_test_with_replay_qualification' if changed else 'complete_verified_test'
summary.update(status=status,replay_changed_rows=changed,max_per_user_ap_replay_sensitivity=max_ap,
    global_branch_metrics=global_metrics,global_branch_paired_differences=global_differences,visual_review_passed=True)
write(REP/'comparison.json',summary)
write(REP/'visual_review.json',dict(passed=True,image='comparison_all.png',methods=21,
    checks=['Three panels aligned','All21 labels readable','MAP and conditional-new recall explicitly distinguished',
        'All confidence intervals and numeric labels fit','Historical methods retained','Footnotes readable']))
write(REP/'final_verification.json',dict(status=status,passed=True,checkpoints_verified=9,
    original18_methods_and_files_unchanged=True,reference_hashes_unchanged=True,
    no_training=True,no_reselection=True,no_api=True,independent_AP_verified=True,
    seen_items_masked_before_full_catalog_top12=True,new_only_equals_masked_global=True,
    canonical_first_scores_retained=True,replay_changed_rows=changed,max_per_user_ap_replay_sensitivity=max_ap,
    total_observations=5519,customers=4548,available_new_observations=3178,
    bootstrap_replicates=5000,visual_review_passed=True,fold_checks=checks))
lines=['','## Глобальная ветка отдельно','',
    '| Вариант | Global-only test MAP@12 | 95% интервал |','|---|---:|---:|']
for r in global_metrics:lines.append(f"|{r['method']}|{100*r['map']:.4f}%|[{100*r['low']:.4f}%; {100*r['high']:.4f}%]|")
lines+=['',f'Все9checkpoint и исходные18методов проверены; график открыт и проверен визуально. '
    f'Reload: {changed} строк top12 с перестановками, максимальное изменение пользовательского AP={max_ap:.10g}; '
    'первые канонические оценки не подменялись. Подробности в final_verification.json.','']
with (REP/'summary_ru.md').open('a',encoding='utf-8') as stream:stream.write('\n'.join(lines))
messages=[]
for key in keys:
    p=metrics[metrics.method==key].set_index(['mode','group'])
    messages.append(f"{key}: MAP {100*p.loc[('normal','all'),'map']:.4f}%, new available recall {100*p.loc[('normal','new'),'available_macro_recall']:.4f}%/{100*p.loc[('new_only','new'),'available_macro_recall']:.4f}%")
message='; '.join(messages)
with (ROOT/'CONTEXT.md').open('a',encoding='utf-8') as stream:
    stream.write(f'\n\n## Multi-interest: test-график21метода завершён (2026-10-19)\n\n'
        f'Run `{protocol["run_id"]}`: {status}. {message}. '
        'Девять зафиксированных validation-checkpoint, без обучения/переотбора. '
        'Те же5519наблюдений/4548покупателей; условный recall новых на3178. '
        'MAP/полный recall сохраняют недоступные цели, 11158из17456новых вне каталога. '
        f'Replay: {changed} строк с перестановками top12, max AP sensitivity={max_ap:.10g}. '
        'График `reports/medium_multi_interest_test_v1/comparison_all.png` проверен визуально: '
        'MAP и recall новых normal/new-only, все18исторических методов сохранены плюс matched FUSION/K1/K4. '
        '95%customer bootstrap5000; парные разности в paired_differences.csv. '
        'Global-only MAP и парные разности дополнительно в global_branch_metrics.csv/global_branch_paired_differences.csv. '
        'Один seed и ранее просмотренный test: внутреннее сравнение, не независимое подтверждение.\n')
record('multi_interest_test_complete',message+f';9checkpoints verified,21-method chart visually reviewed,18historical metrics/files unchanged. Reload changed {changed} top12 rows; max AP sensitivity {max_ap:.10g}. No fitting/reselection/API.',
    protocol['run_id'],status=status,artifacts=str(REP.relative_to(ROOT)),checkpoints_verified=9,
    replay_changed_rows=changed,max_per_user_ap_replay_sensitivity=max_ap)
print(status,message)
