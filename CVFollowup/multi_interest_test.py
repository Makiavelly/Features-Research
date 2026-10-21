"""Frozen three-arm test and all-method MAP/novelty chart, no model selection."""
import os
for name in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[name]='2'
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
os.environ['PATH']='/usr/lib/wsl/lib:'+os.environ.get('PATH','')
import argparse
import gc
from pathlib import Path
import subprocess
import sys
import numpy as np
import pandas as pd
import torch
import context_multi_interest_v2 as experiment
import novelty_audit as audit
from common import ROOT,DATA,OUT,read,write,sha,record

RUN='hm_medium_multi_interest_test_all_methods_seed42_v1'
DEST=OUT/'multi_interest_test_v1'
REP=ROOT/'reports/medium_multi_interest_test_v1'
OLD=ROOT/'reports/medium_h010_h011_feature_novelty_v1'
ARMKEY={'control':'fusion_matched','interest1':'multi_interest1','interest4':'multi_interest4'}
LABELS={'control':'ContextGNN FUSION matched (64/32)','interest1':'ContextGNN attention K=1','interest4':'ContextGNN attention K=4'}


def freeze():
    assert read(experiment.REP/'final_verification.json')['passed']
    refs={}
    for f in range(3):
        for arm in experiment.ARMS:
            for name in ['best.pt','result.json']:
                p=experiment.DEST/f'fold_{f}'/arm/name;refs[str(p.relative_to(ROOT))]=sha(p)
        for name in ['annotations.json','seen_mask.npy']:
            p=audit.DEST/f'fold_{f}'/name;refs[str(p.relative_to(ROOT))]=sha(p)
        for name in ['bundle/test_targets.parquet','article_id_map.csv','customer_id_map.csv','db/article.parquet']:
            p=DATA/f'fold_{f}'/name;refs[str(p.relative_to(ROOT))]=sha(p)
    for p in [OLD/'metrics_all_methods.csv',OLD/'per_user_metrics.parquet',
        audit.REP/'per_user_metrics.parquet',ROOT/'reports/medium_h010_h011_novelty_v1/per_user_metrics.parquet',
        experiment.REP/'final_verification.json',experiment.REP/'final_summary.json']:
        refs[str(p.relative_to(ROOT))]=sha(p)
    for folder in [OLD,ROOT/'reports/medium_all_methods_h011_feature_v1']:
        for p in folder.glob('*.png'):refs[str(p.relative_to(ROOT))]=sha(p)
    sources={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'CVFollowup/context_multi_interest_v2.py',
        ROOT/'CVFollowup/context_first3.py',ROOT/'CVFollowup/novelty_audit.py',ROOT/'CVFollowup/context_global_aux_v3.py']}
    protocol=dict(run_id=RUN,no_training=True,no_reselection=True,no_api=True,
        selection='Nine fixed validation-selected checkpoints: matched FUSION, attentionK1/K4, three folds. Freeze before any test scoring.',
        test='Same5519 observations,4548 original customers,10000 candidates. MAP includes all unavailable future targets.',
        novelty='Unchanged full-source past-history annotations/masks; normal and seen-excluded-before-full-catalog-top12. Full and available recall reported separately.',
        plot='All18 previous methods unchanged, add three matched experiment arms; MAP and two available-new recall panels, shared method order.',
        bootstrap='5000 original-customer clusters seed42; paired K4-K1 and each interest arm vs matched FUSION',
        replay='Canonical first-pass scores retained, second reload inference with FP32 bound and all top12/AP sensitivity quantified; no best replay selection',
        resource_policy='Sequential isolated subprocesses,2CPU nice5; same existing feature caches, no simultaneous fitting',
        limitation='One seed, previously inspected test weeks; internal comparison, not independent confirmation',
        reference_hashes=refs,sources=sources)
    p=REP/'pretest_freeze.json'
    if p.exists():assert read(p)==protocol
    else:write(p,protocol)


def score(fold,arm):
    from torch_geometric.seed import seed_everything
    folder=DEST/f'fold_{fold}'/arm;folder.mkdir(parents=True,exist_ok=True)
    if (folder/'verification.json').exists():assert read(folder/'verification.json')['passed'];return
    experiment.previous.REP,experiment.previous.RUN=REP,RUN
    experiment.previous.wait_for_resources(f'test_f{fold}_{arm}')
    base=experiment.previous.base
    # Read already built categorical feature cache; all test outputs use DEST.
    base.DEST=experiment.DEST
    env=base.setup(fold,categorical=True);task=env['task'];device=env['device']
    model=env['make_model']('contextgnn')
    if arm!='control':model=experiment.install_model(model,1 if arm=='interest1' else 4)
    checkpoint=experiment.DEST/f'fold_{fold}'/arm/'best.pt';digest=sha(checkpoint)
    annotation=read(audit.DEST/f'fold_{fold}/annotations.json')
    target=pd.read_parquet(DATA/f'fold_{fold}/bundle/test_targets.parquet')
    assert len(target)==[1839,1982,1698][fold]
    assert [a['customer_id'] for a in annotation]==target.customer_id.tolist()
    assert target.customer_id.tolist()==env['tables']['test'].df[task.src_entity_col].tolist()
    assert all(set(a['targets'])==set(t) and a['cutoff']==str(time) for a,t,time in zip(annotation,target.article_id,target.timestamp))
    truth=[set(map(int,t)) for t in target.article_id]
    @torch.no_grad()
    def infer():
        model.load_state_dict(torch.load(checkpoint,map_location=device)['model_state_dict'])
        model.eval();env['module'].clear_rhs(model);seed_everything(42)
        parts={'hybrid':[],'global':[]}
        for batch in base.loader(env,'test',[64,32]):
            batch=batch.to(device);base.check_time(batch,task)
            pair=experiment.previous.forward_pair(model,batch,task) if arm=='control' else experiment.forward_pair(model,batch,task)
            for key,value in zip(parts,pair):
                assert torch.isfinite(value).all();parts[key].append(value.cpu().numpy())
        return {key:np.concatenate(values) for key,values in parts.items()}
    print('INFER',fold,arm,flush=True)
    canonical=infer()
    for key,values in canonical.items():np.save(folder/f'test_{key}_scores.npy',values)
    pred=np.argsort(-canonical['hybrid'],axis=1,kind='stable')[:,:12]
    ap=base.aps(pred,truth);assert abs(float(ap.mean())-task.evaluate(pred)['map'])<1e-10
    np.save(folder/'test_predictions.npy',pred);np.save(folder/'test_ap.npy',ap)
    del canonical;gc.collect()
    print('RELOAD',fold,arm,flush=True);replay=infer();checks={}
    for key,value in replay.items():
        saved=np.load(folder/f'test_{key}_scores.npy',mmap_mode='r')
        checks[key]=experiment.reporting.replay_check(saved,value,truth)
    assert sha(checkpoint)==digest
    mask=np.load(audit.DEST/f'fold_{fold}/seen_mask.npy',mmap_mode='r')
    hybrid=np.load(folder/'test_hybrid_scores.npy',mmap_mode='r');global_scores=np.load(folder/'test_global_scores.npy',mmap_mode='r')
    assert np.array_equal(hybrid[~mask],global_scores[~mask])
    novel=[]
    for start in range(0,len(target),64):
        values=np.array(hybrid[start:start+64],copy=True);values[mask[start:start+64]]=-np.inf
        top=np.argsort(-values,axis=1,kind='stable')[:,:12]
        assert np.isfinite(np.take_along_axis(values,top,axis=1)).all()
        assert not mask[start:start+64][np.arange(len(top))[:,None],top].any();novel.append(top)
    np.save(folder/'new_predictions.npy',np.concatenate(novel))
    write(folder/'verification.json',dict(passed=True,fold=fold,arm=arm,rows=len(target),
        checkpoint_sha256=digest,independent_AP=True,canonical_test_map=float(ap.mean()),
        reload=checks,new_only_equals_masked_global=True,canonical_scores_retained=True,no_training=True))
    record('multi_interest_test_fold_verified',f'Fold{fold} {arm}: frozen checkpoint testMAP={100*ap.mean():.4f}%, both branch reloads and full-catalog novelty mask verified.',RUN+f'_f{fold}_{arm}',
        status='test_verified',test_metrics={'map':float(ap.mean())},artifacts=str(folder.relative_to(ROOT)))
    print('VERIFIED',fold,arm,float(ap.mean()),flush=True)


def report():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    rows=[]
    for fold in range(3):
        annotation=read(audit.DEST/f'fold_{fold}/annotations.json')
        mask=np.load(audit.DEST/f'fold_{fold}/seen_mask.npy',mmap_mode='r')
        for arm,key in ARMKEY.items():
            folder=DEST/f'fold_{fold}'/arm;assert read(folder/'verification.json')['passed']
            for mode,name in [('normal','test_predictions.npy'),('new_only','new_predictions.npy')]:
                for i,(pred,a) in enumerate(zip(np.load(folder/name),annotation)):
                    for group,value in audit.per_user(pred,a).items():
                        rows.append(dict(fold=fold,row=i,customer=a['original_customer_id'],method=key,label=LABELS[arm],mode=mode,group=group,
                            recommendation_count=12,repeat_recommendations=int(mask[i,pred].sum()),**value))
    users=pd.DataFrame(rows);users.to_parquet(REP/'per_user_metrics.parquet',index=False)
    metrics=users.groupby(['method','label','mode','group'],sort=False).apply(audit.aggregate,include_groups=False).reset_index()
    metrics.to_csv(REP/'metrics_new_methods.csv',index=False)
    old=pd.read_csv(OLD/'metrics_all_methods.csv');combined=pd.concat([old,metrics],ignore_index=True)
    pd.testing.assert_frame_equal(combined.iloc[:len(old)].reset_index(drop=True),old)
    combined.to_csv(REP/'metrics_all_methods.csv',index=False)
    sources=[audit.REP/'per_user_metrics.parquet',ROOT/'reports/medium_h010_h011_novelty_v1/per_user_metrics.parquet',OLD/'per_user_metrics.parquet']
    previous_users=pd.concat([pd.read_parquet(p,filters=[('group','in',['all','new'])]) for p in sources],ignore_index=True)
    all_users=pd.concat([previous_users,users[users['group'].isin(['all','new'])]],ignore_index=True)
    order=combined[(combined['mode']=='normal')&(combined['group']=='all')].sort_values('map',ascending=False)
    keys=order.method.tolist();labels=order.label.tolist();assert len(keys)==len(set(keys))==21
    specs=[('normal','all','map','map','Test MAP@12, все цели'),
        ('normal','new','available_recall','available_macro_recall','Recall новых: обычный top12'),
        ('new_only','new','available_recall','available_macro_recall','Recall новых: без прежних покупок')]
    intervals=[];contrasts=[];values_by_metric=[]
    for mode,group,metric,column,title in specs:
        frame=all_users[(all_users['mode']==mode)&(all_users['group']==group)]
        matrices=[];ids=None
        for key in keys:
            p=frame[frame.method==key].sort_values(['fold','row'])
            index=p[['fold','row','customer']].to_numpy()
            if ids is None:ids=index
            else:np.testing.assert_array_equal(ids,index)
            matrices.append(p[metric].to_numpy())
        matrix=np.stack(matrices,axis=1);valid=np.isfinite(matrix[:,0]);assert np.array_equal(np.isfinite(matrix),np.broadcast_to(valid[:,None],matrix.shape))
        matrix=matrix[valid];identities=ids[:,2][valid]
        _,inverse=np.unique(identities,return_inverse=True);counts=np.bincount(inverse)
        sums=np.zeros((len(counts),len(keys)));np.add.at(sums,inverse,matrix)
        rng=np.random.default_rng(42);boot=[]
        for _ in range(5000):
            ix=rng.integers(0,len(counts),len(counts));boot.append(sums[ix].sum(0)/counts[ix].sum())
        boot=np.array(boot);low,high=np.quantile(boot,[.025,.975],axis=0)
        central=combined[(combined['mode']==mode)&(combined['group']==group)].set_index('method').loc[keys,column].to_numpy()
        np.testing.assert_allclose(central,matrix.mean(0),atol=1e-12,rtol=0)
        assert len(matrix)==(5519 if metric=='map' else 3178)
        values_by_metric.append((central,low,high,title))
        for i,key in enumerate(keys):intervals.append(dict(method=key,mode=mode,group=group,metric=metric,value=float(central[i]),low=float(low[i]),high=float(high[i]),observations=len(matrix)))
        for a,b in [('multi_interest4','multi_interest1'),('multi_interest4','fusion_matched'),('multi_interest1','fusion_matched')]:
            i,j=keys.index(a),keys.index(b);lo,hi=np.quantile(boot[:,i]-boot[:,j],[.025,.975])
            contrasts.append(dict(a=a,b=b,mode=mode,metric=metric,delta=float((matrix[:,i]-matrix[:,j]).mean()),low=float(lo),high=float(hi)))
    pd.DataFrame(intervals).to_csv(REP/'confidence_intervals.csv',index=False)
    pd.DataFrame(contrasts).to_csv(REP/'paired_differences.csv',index=False)
    colors={'contextgnn_feature':'#16a085','multi_interest1':'#e69f00','multi_interest4':'#d64a3a','fusion_matched':'#277da8','h010_20':'#1976d2','h011_20':'#7c3aed'}
    fig,axes=plt.subplots(1,3,figsize=(25,14),sharey=True)
    for ax,(values,low,high,title) in zip(axes,values_by_metric):
        values=values*100;low=low*100;high=high*100
        ax.barh(range(len(keys)),values,color=[colors.get(k,'#9aa7b6') for k in keys],height=.68)
        ax.errorbar(values,range(len(keys)),xerr=[np.maximum(0,values-low),np.maximum(0,high-values)],fmt='none',ecolor='#354254',capsize=2,linewidth=.8)
        limit=max(high)*1.25
        for y,value in enumerate(values):ax.text(limit*.985,y,f'{value:.3f}%',ha='right',va='center',fontsize=8,fontweight='bold' if keys[y] in ARMKEY.values() else 'normal')
        ax.set(yticks=range(len(keys)),yticklabels=labels,xlim=(0,limit),title=title,xlabel='Метрика, %')
        ax.xaxis.grid(True,alpha=.15);ax.set_axisbelow(True);ax.tick_params(axis='y',length=0)
    axes[0].invert_yaxis()
    fig.suptitle('ContextGNN: один и четыре интереса среди всех методов — test',fontsize=20,y=.98)
    fig.text(.02,.035,'3 прежних test-недели, 5519 наблюдений / 4548 покупателей, каталог 10000. MAP сохраняет недоступные будущие цели.\n'
        'Recall: доступные новые для покупателя цели, те же3178 наблюдений. Усы:95% customer bootstrap,5000 повторов. Один seed; test ранее просматривался.',fontsize=11)
    fig.text(.02,.008,'Справа маска всех прежних покупок до top12 полного каталога. TDM сохраняет beam64; новые ID-GNN — нулевые ничьи. H011: бюджет40→300 во время поиска.',fontsize=10)
    fig.subplots_adjust(left=.25,right=.99,bottom=.11,top=.93,wspace=.12)
    fig.savefig(REP/'comparison_all.png',dpi=160);fig.savefig(REP/'comparison_all.svg');plt.close(fig)
    frozen=read(REP/'pretest_freeze.json')
    for name,digest in {**frozen['reference_hashes'],**frozen['sources']}.items():assert sha(ROOT/name)==digest
    write(REP/'comparison.json',dict(status='pending_visual_review',methods=keys,methods_count=21,
        original_18_metrics_unchanged=True,reference_files_unchanged=True,no_training=True,no_reselection=True,
        metrics=metrics.replace({np.nan:None}).to_dict('records'),paired_differences=contrasts))
    lines=['# Multi-interest ContextGNN: общий test-график','',
        'Те же5519наблюдений/4548покупателей/10000кандидатов. Веса девяти моделей зафиксированы до test; обучения и переотбора нет. '
        'Все18 прежних методов сохранены. FUSION matched — контроль именно новой серии; старый fanout64/32 — отдельный исторический запуск.','',
        '| Новый вариант | MAP@12, все цели | Recall новых, все цели | Recall новых, доступные | Recall новых new-only, все | Recall новых new-only, доступные |',
        '|---|---:|---:|---:|---:|---:|']
    for arm,key in ARMKEY.items():
        p=metrics[metrics.method==key].set_index(['mode','group'])
        values=[p.loc[('normal','all'),'map'],p.loc[('normal','new'),'macro_recall'],p.loc[('normal','new'),'available_macro_recall'],p.loc[('new_only','new'),'macro_recall'],p.loc[('new_only','new'),'available_macro_recall']]
        lines.append('|'+LABELS[arm]+'|'+'|'.join(f'{100*v:.4f}%' for v in values)+'|')
    lines+=['','Доступных новых целей6298 из17456; недоступных11158. Полный recall усреднён по5358наблюдениям с новыми целями, '
        'условный по3178 с доступными. 2180наблюдений только с недоступными новыми целями не входят в условный recall; в полном дают0. '
        'Маски полной исходной прошлой истории прежние. Новые списки получены пересортировкой всех10000сохранённых оценок после маски.','',
        'Усы —95% bootstrap по исходным покупателям,5000повторов seed42. Парные разности K4−K1 и каждого варианта−matched FUSION '
        'в paired_differences.csv, без поправки за множество сравнений. Один seed и уже просмотренные test-недели: внутреннее сравнение. '
        'FP32 replay и влияние перестановок на AP измерены; канонические первые оценки сохранены.','',
        '![Все методы](comparison_all.png)','']
    (REP/'summary_ru.md').write_text('\n'.join(lines),encoding='utf-8')
    record('multi_interest_test_plot_ready','Nine frozen checkpoint test/replay jobs verified;21-method joint MAP/new recall chart generated, all18 historical method metrics preserved. Awaiting visual review.',RUN,status='pending_visual_review',artifacts=str(REP.relative_to(ROOT)))
    print(pd.DataFrame(contrasts).to_string(index=False),flush=True)


def main():
    torch.set_num_threads(2);torch.set_num_interop_threads(2);os.nice(max(0,5-os.getpriority(os.PRIO_PROCESS,0)))
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['run','score','report']);p.add_argument('--fold',type=int);p.add_argument('--arm',choices=experiment.ARMS);a=p.parse_args()
    REP.mkdir(parents=True,exist_ok=True);DEST.mkdir(parents=True,exist_ok=True)
    if a.stage=='score':score(a.fold,a.arm);return
    if a.stage=='report':report();return
    import fcntl
    with (DEST/'execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);freeze()
        record('multi_interest_test_started','User additionally requested joint test MAP/new-recall chart. Freeze all nine validation-selected checkpoints before test; sequential paired branch scoring/reload, no fitting/reselection/API. All18 historical methods retained.',RUN,status='scoring',artifacts=str(REP.relative_to(ROOT)))
        for f in range(3):
            for arm in experiment.ARMS:
                print('TEST_START',f,arm,flush=True)
                with (REP/f'fold_{f}_{arm}.log').open('a') as log:
                    subprocess.run([sys.executable,'-u',str(Path(__file__)),'score','--fold',str(f),'--arm',arm],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,env={**os.environ,'PYTHONHASHSEED':'42'})
        report()


if __name__=='__main__':main()
