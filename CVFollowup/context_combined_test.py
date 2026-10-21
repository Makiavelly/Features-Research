"""Frozen combined ContextGNN test inference and a replacement comparison plot."""
import argparse
import copy
import gc
import importlib.util
import inspect
import itertools
from pathlib import Path
import shutil
import sys

import context_first3 as base
from common import ROOT, OUT, REPORT, DATA, read, write, sha, record

RUN='hm_medium_context_combined_test_seed42_v1'
MODELS=OUT/'context_combined_v1'
DEST=OUT/'context_combined_test_v1'
REP=REPORT/'context_combined_test_v1'
ORIGINAL=REPORT/'final_comparison'


def freeze():
    REP.mkdir(parents=True,exist_ok=True)
    frozen={}
    for f in range(3):
        folder=MODELS/f'fold_{f}/combined'
        fit=read(folder/'result.json')
        assert sha(folder/'best.pt')==fit['checkpoint_sha256']
        assert fit['fanout']==[64,32] and fit['changed_columns']==base.CODE_COLUMNS
        for name in ['best.pt','result.json']:
            path=folder/name
            frozen[str(path.relative_to(ROOT))]=sha(path)
    previous=read(ORIGINAL/'comparison.json')
    for name,digest in previous['prediction_sha256'].items():
        assert sha(ROOT/name)==digest
        frozen[name]=digest
    for name in ['comparison.json','comparison.png','comparison.svg']:
        path=ORIGINAL/name
        frozen[str(path.relative_to(ROOT))]=sha(path)
    protocol=dict(run_id=RUN,model='combined fanout64/32 and eight categorical codes',
        checkpoint_selection='Existing combined checkpoints selected on validation before this request',
        no_training=True,no_reselection=True,fanout=[64,32],seed=42,
        test_folds=[0,1,2],expected_rows=[1839,1982,1698],bootstrap_replicates=5000,
        bootstrap_unit='original customer across folds',reference_hashes=frozen,
        verification='reload checkpoint, bounded FP32 full/ranked scores and exact per-user AP',
        limitation='Already inspected test weeks; internal exploratory comparison, one seed.',
        source_sha256=sha(Path(__file__)),setup_source_sha256=sha(Path(base.__file__)))
    path=REP/'pretest_freeze.json'
    if path.exists():
        assert read(path)==protocol,'Frozen protocol changed'
    else:
        write(path,protocol)
    shutil.copyfile(Path(__file__),REP/Path(__file__).name)
    return protocol


def setup(fold):
    # Keep setup outputs isolated, reuse the exact categorical materialization.
    base.DEST=DEST
    source=inspect.getsource(base.setup).replace('def setup(', 'def test_setup(',1)
    before="mod.CACHE = work / 'cache'"
    assert source.count(before)==1
    source=source.replace(before,"mod.CACHE = COMBINED_MODELS / f'fold_{fold}/categorical/cache'")
    base.__dict__['COMBINED_MODELS']=MODELS
    exec(compile(source,str(Path(__file__))+':setup','exec'),base.__dict__)
    return base.test_setup(fold,categorical=True)


def evaluate(fold):
    import numpy as np
    import pandas as pd
    import torch
    from torch_geometric.seed import seed_everything
    folder=DEST/f'fold_{fold}/combined'
    folder.mkdir(parents=True,exist_ok=True)
    if (folder/'verification.json').exists():
        assert read(folder/'verification.json')['passed']
        print('REUSE',fold,flush=True)
        return
    env=setup(fold)
    task,mod,device=env['task'],env['module'],env['device']
    model=env['make_model']('contextgnn')
    checkpoint=MODELS/f'fold_{fold}/combined/best.pt'
    digest=sha(checkpoint)
    target=pd.read_parquet(DATA/f'fold_{fold}/bundle/test_targets.parquet')
    assert len(target)==[1839,1982,1698][fold]
    assert np.array_equal(target.customer_id,env['tables']['test'].df[task.src_entity_col])
    targets=[set(map(int,x)) for x in target[task.dst_entity_col]]
    @torch.no_grad()
    def infer():
        model.load_state_dict(torch.load(checkpoint,map_location=device)['model_state_dict'])
        model.eval()
        mod.clear_rhs(model)
        seed_everything(42)
        parts=[]
        for batch in base.loader(env,'test',[64,32]):
            batch=batch.to(device)
            base.check_time(batch,task)
            scores=model(batch,task.src_entity_table,task.dst_entity_table)
            assert torch.isfinite(scores).all()
            parts.append(scores.cpu().numpy())
        scores=np.concatenate(parts)
        pred=np.argsort(-scores,axis=1,kind='stable')[:,:12]
        ap=base.aps(pred,targets)
        official=task.evaluate(pred)['map']
        assert abs(float(ap.mean())-official)<1e-10
        return scores,pred,ap
    print('INFER',fold,flush=True)
    scores,pred,ap=infer()
    np.save(folder/'test_scores.npy',scores)
    np.save(folder/'test_predictions.npy',pred)
    np.save(folder/'test_ap.npy',ap)
    first_max=float(np.abs(scores).max())
    del scores,pred,ap
    gc.collect()
    print('REPLAY',fold,flush=True)
    replay,pred,ap=infer()
    reference=np.load(folder/'test_scores.npy',mmap_mode='r')
    previous=np.load(folder/'test_predictions.npy')
    tolerance=32*np.finfo(np.float32).eps*max(1.,first_max)
    max_diff=0.
    for start in range(0,len(replay),128):
        max_diff=max(max_diff,float(np.abs(reference[start:start+128]-replay[start:start+128]).max()))
    ranked=bool(np.allclose(np.take_along_axis(replay,pred,axis=1),
        np.take_along_axis(reference,previous,axis=1),atol=2*tolerance,rtol=0))
    exact_ap=bool(np.array_equal(ap,np.load(folder/'test_ap.npy')))
    check=dict(passed=bool(max_diff<=tolerance and ranked and exact_ap),
        checkpoint_sha256=digest,max_abs_score_difference=max_diff,fp32_tolerance=tolerance,
        ranked_scores_close=ranked,exact_per_user_ap=exact_ap,
        predictions_identical=bool(np.array_equal(pred,previous)),map=float(ap.mean()),rows=len(ap))
    write(folder/'verification.json',check)
    assert check['passed'],check
    assert sha(checkpoint)==digest
    write(folder/'metrics.json',dict(test_metrics={'map':float(ap.mean())},checkpoint_sha256=digest,rows=len(ap)))
    record('context_combined_test_verified',f'Fold{fold}: frozen combined ContextGNN test inference/reload replay and independent AP passed.',RUN+f'_fold{fold}',status='test_verified',test_metrics={'map':float(ap.mean())},artifacts=str(folder.relative_to(ROOT)))
    del model,env,replay,reference
    gc.collect()
    torch.cuda.empty_cache()


def plot():
    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter
    frozen=read(REP/'pretest_freeze.json')
    for name,digest in frozen['reference_hashes'].items():
        assert sha(ROOT/name)==digest,f'Reference changed: {name}'
    old=read(ORIGINAL/'comparison.json')
    result=copy.deepcopy(old)
    summary=result['summary']
    labels=[s['label'] for s in summary]
    keys=[s['method'] for s in summary]
    context_index=keys.index('contextgnn')
    context_label='ContextGNN: fanout64/32 + categorical'
    labels[context_index]=context_label
    prediction_hashes={}
    spec=importlib.util.spec_from_file_location('original_metrics',ROOT/'CVBenchmark/common.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fold_arrays=[]
    identities=[]
    fold_rows=[]
    for fold in range(3):
        assert read(DEST/f'fold_{fold}/combined/verification.json')['passed']
        target=pd.read_parquet(DATA/f'fold_{fold}/bundle/test_targets.parquet')
        mapping=pd.read_csv(DATA/f'fold_{fold}/customer_id_map.csv').set_index('customer_id').original_customer_id
        ids=target.customer_id.map(mapping)
        assert ids.notna().all()
        identities.extend(ids)
        columns=[]
        for i,key in enumerate(keys):
            if key=='contextgnn':
                path=DEST/f'fold_{fold}/combined/test_predictions.npy'
            else:
                candidates=[ROOT/p for p in old['prediction_sha256'] if f'/fold_{fold}/' in p and p.endswith('/test_predictions.npy')]
                # Original figure's own fold table identifies method directories.
                if key=='idgnn':token='/gnn_timefix_refit/idgnn/'
                elif key=='manual':token='/lightgbm_manual/'
                elif key=='raw15':token='/lightgbm_raw15/'
                elif key=='tdm':token='/tdm/fixed/beam/'
                elif key=='recformer_zero':token='/recformer/zero_shot/'
                elif key=='recformer_baseline':token='/recformer/finetuned/'
                elif key=='recformer_tuned':token='/recformer_grid/'+read(REPORT/'recformer_pretest_freeze.json')['selected_label']+'/finetuned/'
                else:
                    mode,budget=key.rsplit('_',1)
                    token=f'/{mode}/budgets/{budget}/'
                matches=[p for p in candidates if token in str(p)]
                assert len(matches)==1,(key,matches)
                path=matches[0]
            metric,ap=module.metrics(np.load(path),target)
            if key=='contextgnn':
                assert np.array_equal(ap,np.load(DEST/f'fold_{fold}/combined/test_ap.npy'))
            else:
                assert abs(metric['map']-summary[i]['fold_maps'][fold])<1e-12
            columns.append(ap)
            fold_rows.append(dict(fold=fold,method=key,label=labels[i],**metric))
            prediction_hashes[str(path.relative_to(ROOT))]=sha(path)
        fold_arrays.append(np.stack(columns,axis=1))
    ap=np.concatenate(fold_arrays)
    unique,inverse=np.unique(identities,return_inverse=True)
    counts=np.bincount(inverse)
    sums=np.zeros((len(unique),len(keys)))
    np.add.at(sums,inverse,ap)
    rng=np.random.default_rng(42)
    boot=[]
    for _ in range(50):
        ix=rng.integers(len(unique),size=(100,len(unique)))
        boot.append(sums[ix].sum(1)/counts[ix].sum(1)[:,None])
    boot=np.concatenate(boot)
    for i,key in enumerate(keys):
        low,high=np.quantile(boot[:,i],[.025,.975])
        folds=[float(x[:,i].mean()) for x in fold_arrays]
        value=dict(method=key,label=labels[i],pooled_map=float(ap[:,i].mean()),
            equal_fold_map=float(np.mean(folds)),fold_maps=folds,ci95_low=float(low),ci95_high=float(high))
        if key!='contextgnn':
            for field in ['pooled_map','ci95_low','ci95_high']:
                assert abs(value[field]-summary[i][field])<1e-12,(key,field)
        summary[i]=value
    pairs=[]
    for i,j in itertools.combinations(range(len(keys)),2):
        low,high=np.quantile(boot[:,i]-boot[:,j],[.025,.975])
        pairs.append(dict(a=keys[i],b=keys[j],difference=float(ap[:,i].mean()-ap[:,j].mean()),ci95_low=float(low),ci95_high=float(high)))
    result.update(summary=summary,paired_comparisons=pairs,prediction_sha256=prediction_hashes,
        stage='combined_contextgnn',replacement='Only ContextGNN row replaced with frozen combined model test predictions',
        limitations='One seed; three already inspected test weeks; combined model chosen after validation exploration. Internal comparison, not independent confirmation.')
    write(REP/'comparison.json',result)
    pd.DataFrame(summary).to_csv(REP/'summary.csv',index=False)
    pd.DataFrame(fold_rows).to_csv(REP/'fold_metrics.csv',index=False)
    pd.DataFrame(pairs).to_csv(REP/'paired_differences.csv',index=False)
    n=len(keys)
    rank=np.argsort(ap.mean(0))
    means=ap.mean(0)[rank]*100
    ci=np.quantile(boot,[.025,.975],axis=0)[:,rank]*100
    fig,ax=plt.subplots(figsize=(12,max(6,n*.45)))
    ax.barh(range(n),means,color='#4c78a8')
    ax.errorbar(means,range(n),xerr=np.maximum(0,np.stack([means-ci[0],ci[1]-means])),fmt='none',color='black',capsize=3)
    for y,value in enumerate(means):
        ax.text(value,y+.18,f'{value:.3f}%',fontsize=8,va='bottom')
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=100,decimals=1))
    ax.set(yticks=range(n),yticklabels=[labels[i] for i in rank],xlabel='Full-target MAP@12 (%)',title='Three temporal folds; customer-cluster 95% intervals')
    fig.tight_layout()
    fig.savefig(REP/'comparison.png',dpi=170)
    fig.savefig(REP/'comparison.svg')
    plt.close(fig)
    context=summary[context_index]
    write(REP/'replacement_audit.json',dict(original_figure_sha256=frozen['reference_hashes'][str((ORIGINAL/'comparison.png').relative_to(ROOT))],
        only_contextgnn_metrics_changed=True,other_method_values_and_intervals_reproduced=True,
        original_reference_hashes_unchanged=True,new_contextgnn=context))
    (REP/'report_ru.md').write_text('# Сравнение с новым ContextGNN\n\n'
        'В исходном test-графике заменён только ContextGNN: fanout64/32 и восемь категориальных кодов. '
        'Все три checkpoint были выбраны и зафиксированы до новой test-оценки. Нового обучения и отбора нет.\n\n'
        f"Test pooled MAP@12={100*context['pooled_map']:.4f}%, 95% customer-bootstrap интервал "
        f"[{100*context['ci95_low']:.4f}%; {100*context['ci95_high']:.4f}%].\n\n"
        'Те же5519наблюдений,4548покупателей,10000товаров, полные исходные цели и5000bootstrap. '
        'Остальные методы и их интервалы воспроизведены точно. Веса перезагружены; '
        'AP каждого пользователя совпал, полные/ранжированные скоры проверены установленным FP32-допуском. '
        'Недели test уже просматривались, модель выбрана после серии validation-проверок; '
        'это внутреннее сравнение, не независимое подтверждение.\n\n![Сравнение](comparison.png)\n',encoding='utf-8')
    record('context_combined_plot_generated','New test comparison generated: only ContextGNN replaced; all other model metrics/intervals identical. Awaiting visual review.',RUN,status='plot_pending_visual_review',artifacts=str((REP/'comparison.png').relative_to(ROOT)),test_metrics={'map':context['pooled_map']})
    print(context,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('stage',choices=['run','plot'],default='run',nargs='?')
    args=parser.parse_args()
    if args.stage=='run':
        import fcntl
        freeze()
        DEST.mkdir(parents=True,exist_ok=True)
        with (DEST/'execution.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            record('context_combined_test_started','User requested original test plot with latest combined ContextGNN; frozen checkpoint inference only, no training or reselection.',RUN,status='evaluating',artifacts=str(REP.relative_to(ROOT)))
            for fold in range(3):
                evaluate(fold)
        plot()
    else:
        plot()
