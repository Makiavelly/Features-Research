"""Extend the verified H010/H011 novelty comparison with frozen FEATURE scores."""
import os
for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '2'
import argparse
import fcntl
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import novelty_audit as audit
from common import ROOT, DATA, OUT, read, write, sha, record

RUN = 'hm_medium_feature_novelty_plot_seed42_v1'
REP = ROOT / 'reports/medium_h010_h011_feature_novelty_v1'
REFERENCE = ROOT / 'reports/medium_h010_h011_novelty_v1'
SCORES = OUT / 'feature_test_comparison_v1'
KEY = 'contextgnn_feature'
LABEL = 'ContextGNN FEATURE (64/32)'


def freeze():
    paths = [Path(__file__), ROOT/'CVFollowup/novelty_audit.py',
             ROOT/'reports/medium_all_methods_h011_feature_v1/final_verification.json']
    paths += list(p for p in REFERENCE.iterdir() if p.is_file())
    for fold in range(3):
        paths += [audit.DEST/f'fold_{fold}'/name for name in ['annotations.json', 'seen_mask.npy']]
        paths += [SCORES/f'fold_{fold}/feature'/name for name in
                  ['test_scores.npy', 'test_predictions.npy', 'test_ap.npy', 'verification.json']]
        paths += [DATA/f'fold_{fold}/bundle/test_targets.parquet']
    value = dict(run_id=RUN, no_training=True, no_inference=True, no_api=True,
        mode='Post-hoc reuse of canonical FEATURE full-catalog scores; mask full past purchases before top12',
        history='Unchanged original novelty annotations: full source history up to cutoff, including out-of-catalog past purchases',
        availability='Plot conditional macro recall of available new targets on same 3178 observations; full new recall retained separately',
        references_sha256={str(p.relative_to(ROOT)):sha(p) for p in paths})
    if (REP/'protocol.json').exists():
        assert read(REP/'protocol.json') == value
    else:
        write(REP/'protocol.json', value)
    return value


def run():
    REP.mkdir(parents=True, exist_ok=True)
    with (REP/'.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX|fcntl.LOCK_NB)
        protocol = freeze()
        record('feature_novelty_started', 'Reuse verified FEATURE test full-catalog scores and original novelty masks. Add FEATURE to original17-method two-panel recall chart; no inference/fitting/API.', RUN,
               status='diagnosing', artifacts=str(REP.relative_to(ROOT)))
        rows=[]
        for fold in range(3):
            folder = SCORES/f'fold_{fold}/feature'
            assert read(folder/'verification.json')['passed_scores']
            scores = np.load(folder/'test_scores.npy', mmap_mode='r')
            expected = np.load(folder/'test_predictions.npy')
            annotations = read(audit.DEST/f'fold_{fold}/annotations.json')
            mask = np.load(audit.DEST/f'fold_{fold}/seen_mask.npy', mmap_mode='r')
            target = pd.read_parquet(DATA/f'fold_{fold}/bundle/test_targets.parquet')
            assert scores.shape == mask.shape == (len(target),10000)
            assert [a['customer_id'] for a in annotations] == target.customer_id.tolist()
            assert all(a['cutoff']==str(t) and set(a['targets'])==set(truth)
                       for a,t,truth in zip(annotations,target.timestamp,target.article_id))
            novel=[]
            for start in range(0,len(target),64):
                values = np.array(scores[start:start+64], copy=True)
                assert np.isfinite(values).all()
                normal = np.argsort(-values, axis=1, kind='stable')[:,:12]
                np.testing.assert_array_equal(normal, expected[start:start+64])
                values[mask[start:start+64]] = -np.inf
                pred = np.argsort(-values, axis=1, kind='stable')[:,:12]
                assert np.isfinite(np.take_along_axis(values,pred,axis=1)).all()
                assert not mask[start:start+64][np.arange(len(pred))[:,None],pred].any()
                novel.append(pred)
            novel=np.concatenate(novel)
            np.save(REP/f'feature_new_predictions_fold{fold}.npy',novel)
            for mode, predictions in [('normal',expected), ('new_only',novel)]:
                all_ap=[]
                for i,(pred,a) in enumerate(zip(predictions,annotations)):
                    assert len(set(pred.tolist()))==12
                    result=audit.per_user(pred,a)
                    all_ap.append(result['all']['map'])
                    for group, metrics in result.items():
                        rows.append(dict(fold=fold,row=i,customer=a['original_customer_id'],method=KEY,
                            label=LABEL,mode=mode,group=group,recommendation_count=12,
                            repeat_recommendations=int(mask[i,pred].sum()),**metrics))
                if mode=='normal':
                    np.testing.assert_allclose(all_ap,np.load(folder/'test_ap.npy'),atol=1e-12,rtol=0)
            print('FOLD_VERIFIED',fold,flush=True)
        users=pd.DataFrame(rows)
        users.to_parquet(REP/'per_user_metrics.parquet',index=False)
        metrics=users.groupby(['method','label','mode','group'],sort=False).apply(audit.aggregate,include_groups=False).reset_index()
        metrics.to_csv(REP/'metrics_feature.csv',index=False)
        users.groupby(['fold','method','label','mode','group'],sort=False).apply(audit.aggregate,include_groups=False).reset_index().to_csv(REP/'fold_metrics.csv',index=False)
        old=pd.read_csv(REFERENCE/'metrics_all_methods.csv')
        combined=pd.concat([old,metrics],ignore_index=True)
        pd.testing.assert_frame_equal(combined.iloc[:len(old)].reset_index(drop=True),old)
        combined.to_csv(REP/'metrics_all_methods.csv',index=False)
        part=metrics[metrics['group']=='new']
        assert set(part.available_users)=={3178} and set(part.targets)=={17456} and set(part.available_targets)=={6298}
        assert set(part.eligible_users)=={5358}
        assert users[(users['mode']=='new_only')&(users['group']=='all')].repeat_recommendations.sum()==0
        normal=combined[(combined['mode']=='normal')&(combined['group']=='all')].sort_values('map',ascending=False)
        keys,labels=normal.method.tolist(),normal.label.tolist()
        assert len(keys)==len(set(keys))==18
        fig,axes=plt.subplots(1,2,figsize=(19,12.5),sharey=True)
        maximum=0
        colors={'h010_20':'#1976d2','h011_20':'#7c3aed','h009_20':'#ea8c24',KEY:'#16a085'}
        for ax,mode,title in zip(axes,['normal','new_only'],['Обычные рекомендации','Ранее купленные товары исключены до top12']):
            selected=combined[(combined['mode']==mode)&(combined['group']=='new')].set_index('method').loc[keys]
            assert (selected.available_users==3178).all()
            values=selected.available_macro_recall.to_numpy()*100
            maximum=max(maximum,values.max())
            ax.barh(range(len(keys)),values,color=[colors.get(k,'#9aa7b6') for k in keys])
            ax.set(yticks=range(len(keys)),yticklabels=labels,title=title,
                xlabel='Macro Recall@12 доступных новых для покупателя товаров, %')
            for y,value in enumerate(values):
                ax.text(value+.025,y,f'{value:.3f}%',va='center',fontsize=8,
                    fontweight='bold' if keys[y]==KEY else 'normal')
            ax.xaxis.grid(True,alpha=.15);ax.set_axisbelow(True)
        axes[0].invert_yaxis()
        for ax in axes:ax.set_xlim(0,maximum*1.16)
        fig.suptitle('Recall новых для покупателя товаров: FEATURE среди остальных методов',fontsize=17,y=.98)
        fig.text(.02,.025,'Те же test-недели и 3178 наблюдений с доступными новыми целями. «Новый» = ранее не покупался этим покупателем.\n'
            'Справа: маска прежних покупок до top12 по полному каталогу; TDM сохраняет beam64; новые ID-GNN — нулевые ничьи. Обучения/API нет.',fontsize=10)
        fig.subplots_adjust(left=.29,right=.98,bottom=.10,top=.93,wspace=.12)
        fig.savefig(REP/'new_item_recall.png',dpi=160);fig.savefig(REP/'new_item_recall.svg');plt.close(fig)
        for name,digest in protocol['references_sha256'].items():assert sha(ROOT/name)==digest,name
        verification=dict(passed=True,status='pending_visual_review',methods_on_plot=18,
            original_17_methods_unchanged=True,reference_files_unchanged=True,
            canonical_full_scores_top12_identical=True,independent_original_AP=True,
            seen_mask_applied_before_top12=True,new_only_has_no_seen_candidates=True,
            total_observations=5519,new_target_observations=5358,available_new_observations=3178,
            new_targets=17456,available_new_targets=6298,unavailable_new_targets=11158,
            no_training=True,no_inference=True,no_api=True)
        write(REP/'verification.json',verification)
        lines=['# Recall новых товаров: FEATURE среди остальных методов','','Сохранены все 17 методов исходного графика; FEATURE добавлен зелёным. Исходный график не изменён.','',
            '| Режим FEATURE | Recall всех новых целей | Recall доступных новых целей |', '|---|---:|---:|']
        for row in part.itertuples():
            lines.append(f'|{row.mode}|{100*row.macro_recall:.4f}%|{100*row.available_macro_recall:.4f}%|')
        lines += ['', 'Слева обычные рекомендации, справа исключены все ранее купленные товары до выбора top12 из 10000 кандидатов. '
            'Пересортированы сохранённые полные оценки FEATURE; повторного инференса, обучения и выбора checkpoint не было.', '',
            'Новый товар ранее не покупался этим пользователем по полной исходной истории до cutoff включительно. '
            'Все 17456 новых целей сохранены в полной метрике; 6298 доступны и 11158 вне каталога. '
            'Полный macro recall усреднён по 5358 наблюдениям с новыми целями. На графике условный macro recall по доступным новым целям '
            'на тех же 3178 наблюдениях для всех методов; остальные 2180 с исключительно недоступными новыми целями в условной метрике не участвуют.', '',
            'Один seed, уже просмотренные test-недели; диагностика фиксированных моделей. FEATURE 64/32 + восемь категориальных кодов; '
            'это не чистая FEATURE/FUSION абляция относительно старого corrected. TDM beam64 и нулевые ничьи ID-GNN сохранены.', '',
            '![Сравнение](new_item_recall.png)','']
        (REP/'summary_ru.md').write_text('\n'.join(lines),encoding='utf-8')
        record('feature_novelty_plot_ready','FEATURE canonical saved-score novelty diagnostics verified;18-method comparison generated. Original17 methods and files preserved; full unavailable targets retained separately. Visual review pending.',RUN,
            status='pending_visual_review',artifacts=str(REP.relative_to(ROOT)))
        print(part[['mode','macro_recall','available_macro_recall']].to_string(index=False),flush=True)


def review():
    verification=read(REP/'verification.json');assert verification['passed']
    for name,digest in read(REP/'protocol.json')['references_sha256'].items():assert sha(ROOT/name)==digest
    verification.update(status='complete_verified_plot',visual_review_passed=True)
    write(REP/'verification.json',verification)
    metrics=pd.read_csv(REP/'metrics_feature.csv')
    part=metrics[metrics['group']=='new'].set_index('mode')
    text='; '.join(f"{mode}: available recall {100*part.loc[mode,'available_macro_recall']:.4f}%, full recall {100*part.loc[mode,'macro_recall']:.4f}%" for mode in ['normal','new_only'])
    with (ROOT/'CONTEXT.md').open('a',encoding='utf-8') as stream:
        stream.write(f'\n\n## FEATURE: novelty test-график (2026-10-19)\n\nRun `{RUN}`: {text}. '
            'Постфактум из уже проверенных полных test scores, без нового инференса/обучения/API. '
            'Прежние novelty-аннотации/полная история; маска всех прошлых покупок до top12 полного каталога. '
            '5358 наблюдений с новыми целями, 3178 с доступными, новых целей17456/доступно6298/недоступно11158. '
            'График `reports/medium_h010_h011_feature_novelty_v1/new_item_recall.png`:18 методов, '
            'все17 исходных методов и файлы сохранены, полные метрики включая недоступные цели в metrics_feature.csv. '
            'Top12 сохранённых полных оценок и исходный AP перепроверены, отсутствие прежних покупок справа проверено. '
            'График проверен визуально. Один seed и ранее просмотренный test, не независимое подтверждение.\n')
    record('feature_novelty_plot_complete',text+';18-method two-panel chart visually verified. Original17 methods/files unchanged, masks before full-catalog top12, unavailable targets retained in full metrics. No inference/fitting/API.',RUN,
        status='complete_verified_plot',artifacts=str(REP.relative_to(ROOT)))
    print(text)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['run','review']);args=parser.parse_args()
    if args.action=='run':run()
    else:review()
