"""Read-only comparison of verified follow-ups; never mutate old results."""
import argparse
import importlib.util
import itertools
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from common import ROOT,DATA,OLD,OUT,REPORT,read,write,sha,record

spec=importlib.util.spec_from_file_location('original_cv_metrics',ROOT/'CVBenchmark/common.py')
metric_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(metric_module)

def main(stage):
    destination=REPORT/('gnn_corrected' if stage=='gnn' else 'final_comparison')
    destination.mkdir(parents=True,exist_ok=True)
    assert read(REPORT/'gnn_lane_status.json')['stage']=='verified'
    frozen=read(REPORT/'gnn_timefix_pretest_freeze.json')
    for name,digest in frozen['checkpoints'].items():assert sha(ROOT/name)==digest
    methods={
        'manual':('LightGBM manual',lambda f:OLD/f'fold_{f}/lightgbm_manual'),
        'raw15':('LightGBM raw15',lambda f:OLD/f'fold_{f}/lightgbm_raw15'),
        'idgnn':('ID-GNN corrected',lambda f:OUT/f'fold_{f}/gnn_timefix_refit/idgnn'),
        'contextgnn':('ContextGNN corrected',lambda f:OUT/f'fold_{f}/gnn_timefix_refit/contextgnn'),
        'recformer_zero':('Recformer zero-shot',lambda f:OLD/f'fold_{f}/recformer/zero_shot'),
        'recformer_baseline':('Recformer LR/warmup baseline',lambda f:OLD/f'fold_{f}/recformer/finetuned'),
        'tdm':('TDM fixed beam64',lambda f:OLD/f'fold_{f}/tdm/fixed/beam')}
    if stage=='all':
        assert read(REPORT/'api_lane_status.json')['status']=='evaluated'
        assert read(REPORT/'recformer_lane_status.json')['status']=='evaluated'
        rf=read(REPORT/'recformer_pretest_freeze.json');selected=rf['selected_label']
        for f in range(3):
            folder=OLD/f'fold_{f}/recformer' if selected=='baseline' else OUT/f'fold_{f}/recformer_grid'/selected
            assert sha(folder/'finetuned/best.pt')==rf['checkpoints'][str(f)]
            assert read(folder/'verification.json')['passed']
        if selected!='baseline':
            methods['recformer_tuned']=(f'Recformer tuned: {selected}',lambda f:OUT/f'fold_{f}/recformer_grid'/selected/'finetuned')
        for mode in ['h008','h009']:
            for budget in [20,30,40]:
                methods[f'{mode}_{budget}']=(f'API {mode.upper()} / {budget} sets',lambda f,m=mode,b=budget:OUT/f'fold_{f}'/m/f'budgets/{b}')
    else:
        for mode in ['h008','h009']:
            methods[f'{mode}_20']=(f'API {mode.upper()} / 20 sets',lambda f,m=mode:OLD/f'fold_{f}'/m)
    arrays=[];identities=[];rows=[];pred_hashes={}
    for f in range(3):
        assert read(OUT/f'fold_{f}/gnn_timefix_refit/verification.json')['passed']
        target=pd.read_parquet(DATA/f'fold_{f}/bundle/test_targets.parquet')
        mapping=pd.read_csv(DATA/f'fold_{f}/customer_id_map.csv').set_index('customer_id').original_customer_id
        ids=target.customer_id.map(mapping);assert ids.notna().all();identities.extend(ids)
        columns=[]
        for key,(label,path) in methods.items():
            folder=path(f)
            if stage=='all' and key.startswith('h00'):assert read(folder/'verification.json')['passed']
            prediction=folder/'test_predictions.npy'
            metrics,ap=metric_module.metrics(np.load(prediction),target)
            rows.append({'fold':f,'method':key,'label':label,**metrics});columns.append(ap)
            pred_hashes[str(prediction.relative_to(ROOT))]=sha(prediction)
        arrays.append(np.stack(columns,axis=1))
    ap=np.concatenate(arrays);n=ap.shape[1];keys=list(methods);labels=[v[0] for v in methods.values()]
    unique,inverse=np.unique(identities,return_inverse=True)
    counts=np.bincount(inverse);sums=np.zeros((len(unique),n));np.add.at(sums,inverse,ap)
    rng=np.random.default_rng(42);boot=[]
    for _ in range(50):
        sampled=rng.integers(len(unique),size=(100,len(unique)))
        boot.append(sums[sampled].sum(1)/counts[sampled].sum(1)[:,None])
    boot=np.concatenate(boot);table=pd.DataFrame(rows);summary=[];pairs=[]
    for i,key in enumerate(keys):
        lo,hi=np.quantile(boot[:,i],[.025,.975]);folds=table[table.method==key].sort_values('fold')['map'].tolist()
        summary.append({'method':key,'label':labels[i],'pooled_map':float(ap[:,i].mean()),
            'equal_fold_map':float(np.mean(folds)),'fold_maps':folds,'ci95_low':float(lo),'ci95_high':float(hi)})
    for i,j in itertools.combinations(range(n),2):
        lo,hi=np.quantile(boot[:,i]-boot[:,j],[.025,.975])
        pairs.append({'a':keys[i],'b':keys[j],'difference':float(ap[:,i].mean()-ap[:,j].mean()),'ci95_low':float(lo),'ci95_high':float(hi)})
    table.to_csv(destination/'fold_metrics.csv',index=False)
    pd.DataFrame(summary).to_csv(destination/'summary.csv',index=False)
    pd.DataFrame(pairs).to_csv(destination/'paired_differences.csv',index=False)
    write(destination/'comparison.json',{'status':'passed','stage':stage,'summary':summary,'paired_comparisons':pairs,
        'users':len(ap),'unique_customers':len(unique),'bootstrap_replicates':5000,
        'bootstrap_unit':'original customer jointly across all three folds','prediction_sha256':pred_hashes,
        'limitations':'One seed, three previously inspected weeks; internal comparison. Intervals do not cover new time regimes or seed variance.'})
    rank=np.argsort(ap.mean(0));means=ap.mean(0)[rank]*100
    ci=np.quantile(boot,[.025,.975],axis=0)[:,rank]*100
    fig,ax=plt.subplots(figsize=(12,max(6,n*.45)))
    ax.barh(range(n),means,color='#4c78a8')
    ax.errorbar(means,range(n),xerr=np.maximum(0,np.stack([means-ci[0],ci[1]-means])),fmt='none',color='black',capsize=3)
    for y,value in enumerate(means):ax.text(value,y+.18,f'{value:.3f}%',fontsize=8,va='bottom')
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=100,decimals=1))
    ax.set(yticks=range(n),yticklabels=[labels[i] for i in rank],xlabel='Full-target MAP@12 (%)',title='Three temporal folds; customer-cluster 95% intervals')
    fig.tight_layout();fig.savefig(destination/'comparison.png',dpi=170);fig.savefig(destination/'comparison.svg');plt.close(fig)
    fig,ax=plt.subplots(figsize=(12,7))
    for s in summary:ax.plot(range(3),np.array(s['fold_maps'])*100,marker='o',label=s['label'])
    ax.set(xticks=range(3),xticklabels=['Aug17','Aug31','Sep14'],ylabel='Full-target MAP@12 (%)')
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100,decimals=1))
    ax.legend(fontsize=8,ncol=2);fig.tight_layout();fig.savefig(destination/'fold_comparison.png',dpi=160);plt.close(fig)
    cols=3;fig,axes=plt.subplots((n+cols-1)//cols,cols,figsize=(12,3*((n+cols-1)//cols)),squeeze=False)
    for i,ax in enumerate(axes.flat):
        if i>=n:ax.set_visible(False);continue
        ax.hist(ap[:,i],bins=np.linspace(0,1,21));ax.set_yscale('log');ax.set(title=labels[i],xlabel='Per-user AP@12',ylabel='Count (log)')
    fig.tight_layout();fig.savefig(destination/'ap_histograms.png',dpi=150);plt.close(fig)
    lines=['# Сравнение после исправления GNN','',
       'Те же три временных фолда, пользователи и полные исходные цели. Старые ошибочные GNN-метрики исключены.',
       'Столбец графика — MAP@12 по всем user-times; интервалы: 5000 парных bootstrap по исходным покупателям.',
       'Выбор checkpoint/настроек использует inner validation. Outer-недели ранее просматривались; это внутреннее сравнение.',
       '', '| Метод | Fold0, % | Fold1, % | Fold2, % | Среднее фолдов, % | Pooled MAP, % |','|---|---:|---:|---:|---:|---:|']
    for s in sorted(summary,key=lambda x:-x['pooled_map']):
        values=[*s['fold_maps'],s['equal_fold_map'],s['pooled_map']]
        lines.append('|'+s['label']+'|'+ '|'.join(f'{v*100:.4f}' for v in values)+'|')
    lines+=['','![Сравнение](comparison.png)','![По фолдам](fold_comparison.png)','![Гистограммы](ap_histograms.png)',
        '', 'Интервалы разностей всех пар — paired_differences.csv. Пересечение нуля не подтверждает превосходство.',
        'Ограничение replay ContextGNN fold2: исходная проверка полных скоров не прошла; max |delta|=2.72e-5. Дополнительный replay сохранил test top12 точно; validation имел перестановки почти равных скоров при точном AP каждого пользователя. Применена явно документированная bounded-FP32/tie-aware проверка; исходный failure сохранён. См. ../../../CVFollowup/NUMERIC_REPLAY_AMENDMENT.md.',
        'Один seed и три недели не позволяют оценить устойчивость к другим обучениям и временным режимам.']
    if stage=='all' and rf.get('excluded_unavailable'):
        lines+=['','Сетка Recformer неполная: доступны3 из4 новых настроек плюс прежний baseline. LR=3e-6/warmup100 не запустилась в Kaggle и исключена по доступности, не по качеству. Выбор сделан по среднему inner validation только среди готовых настроек. Протокол сводки: hm_medium_followup_available_summary_v1.']
    (destination/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    record('followup_comparison_generated',f'Generated {stage} comparison from verified saved predictions, independent AP and paired customer bootstrap.',
        f'hm_medium_followup_report_{stage}_v1',status='report_generated_pending_visual_review',artifacts=str(destination.relative_to(ROOT)))
    print(pd.DataFrame(summary)[['label','pooled_map']].to_string(index=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['gnn','all']);main(p.parse_args().stage)
