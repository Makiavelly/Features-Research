"""Matched validation-only experiment: mixed CE plus pre-overwrite global CE."""
import os
os.environ.setdefault('OMP_NUM_THREADS','2')
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
os.environ.setdefault('MKL_NUM_THREADS','2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
import argparse
import gc
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time
import numpy as np
import pandas as pd
import torch
import context_first3 as base
import novelty_audit as novelty
from common import ROOT,DATA,OUT,REPORT,read,write,sha,record

RUN='hm_medium_context_global_aux_lambda1_seed42_v2'
DEST=OUT/'context_global_aux_v2'
REP=REPORT/'context_global_aux_v2'
REF=OUT/'context_combined_v1'
FANOUT=[64,32]


def resource_audit():
    gpu=subprocess.check_output(['nvidia-smi','--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],text=True).strip()
    mem={x.split(':')[0]:int(x.split()[1]) for x in Path('/proc/meminfo').read_text().splitlines() if ':' in x and len(x.split())>=2 and x.split()[1].isdigit()}
    procs=[]
    for p in Path('/proc').iterdir():
        if not p.name.isdigit() or int(p.name)==os.getpid():continue
        try:
            cmd=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
            if 'python' in cmd and ('Features/' in cmd or 'Features\\' in cmd):
                procs.append(dict(pid=int(p.name),command=cmd))
        except (FileNotFoundError,PermissionError,ProcessLookupError):pass
    return dict(gpu_memory_used_and_utilization=gpu,available_ram_mb=mem['MemAvailable']/1024,other_project_processes=procs)


def wait_for_resources(tag):
    while True:
        torch.cuda.empty_cache()
        snapshot=resource_audit()
        used=int(snapshot['gpu_memory_used_and_utilization'].split(',')[0])
        if used<512 and snapshot['available_ram_mb']>5000:
            write(REP/f'resources_{tag}.json',snapshot)
            return
        print('WAIT_RESOURCES',tag,json.dumps(snapshot),flush=True)
        record('global_aux_resource_wait','Waiting for free GPU and RAM; existing processes are not interrupted.',RUN,status='waiting_resources')
        time.sleep(30)


def freeze():
    REP.mkdir(parents=True,exist_ok=True)
    frozen={}
    for f in range(3):
        for n in ['best.pt','result.json','val_scores.npy','val_ap.npy','val_predictions.npy']:
            p=REF/f'fold_{f}/combined'/n;frozen[str(p.relative_to(ROOT))]=sha(p)
        for n in ['article_id_map.csv','customer_id_map.csv','bundle/val_targets.parquet','tasks/user-item-purchase/val.parquet','tasks/user-item-purchase/train.parquet','subset_manifest.json']:
            p=DATA/f'fold_{f}'/n;frozen[str(p.relative_to(ROOT))]=sha(p)
        p=OUT/f'fold_{f}/runtime/gnn_timefix_refit/gnn.py';frozen[str(p.relative_to(ROOT))]=sha(p)
    sources={n:sha(ROOT/n) for n in ['CVFollowup/context_global_aux_v2.py','CVFollowup/context_first3.py',
        'CVFollowup/novelty_audit.py','ContextGNN/upstream/contextgnn/nn/models/contextgnn.py',
        'ContextGNN/upstream/contextgnn/nn/rhs_embedding.py']}
    protocol=dict(run_id=RUN,arms={'control':0.,'aux':1.},seed=42,folds=[0,1,2],
        objective='Original full-catalog sparse CE(hybrid) + lambda * same CE(global scores before local overwrite); same batch/positives/normalization',
        baseline='Combined fanout64/32 and eight categorical article codes, FUSION',fanout=FANOUT,
        optimizer='Adam lr=.001',batch_size=128,max_epochs=10,patience=3,
        selection='Same 256 validation rows per fold; early stopping on ordinary hybrid full-target MAP; no lambda search',
        diagnostics='hybrid/global-only/new-only top12; novelty groups from source past history; unavailable targets retained, conditional metrics separate',
        no_test_evaluation=True,no_api=True,training_from_scratch=True,
        verification='Native-vs-dual and reload bounded by 32*eps*score_scale, exact top12; matched initial-state and epoch training-graph hashes across arms; historical training reproduction measured, not required',
        reference_hashes=frozen,sources=sources,resource_policy='sequential fits; two CPU threads; nice+5; require GPU memory<512MiB and available RAM>5GB before each fit',
        limitation='Exploratory repeatedly inspected validation, one seed; no independent confirmation')
    p=REP/'protocol.json'
    if p.exists():assert read(p)==protocol,'Changed protocol requires a new run ID'
    else:write(p,protocol)
    for name in sources:
        source=ROOT/name;target=REP/'frozen_source'/name
        target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():assert sha(target)==sha(source)
        else:shutil.copyfile(source,target)
    return protocol


def gradient_test():
    # A local overwrite removes direct supervision of that global logit.
    for weight in [0.,1.]:
        g=torch.tensor([[.3,.2,-.1]],requires_grad=True)
        local=torch.tensor(.4,requires_grad=True)
        mixed=g.clone();mixed[0,0]=local
        main=torch.logsumexp(mixed,1).sum()-mixed[0,0]
        extra=torch.logsumexp(g,1).sum()-g[0,0]
        (main+weight*extra).backward()
        assert torch.isfinite(g.grad).all()
        assert (g.grad[0,0]==0 if weight==0 else g.grad[0,0]<0)
        assert local.grad<0
    write(REP/'gradient_verification.json',dict(passed=True,checks=['overwritten positive global logit has zero direct gradient at lambda0','auxiliary CE restores positive supervision','local gradient preserved']))


def prepare_labels():
    import duckdb
    if (DEST/'labels_ready.json').exists():return
    article=pd.read_parquet(ROOT/'data/rel-hm/db/article.parquet',columns=['article_id','product_code','product_type_no'])
    product=dict(zip(article.article_id.astype(int),article.product_code.astype(int)))
    types=dict(zip(article.article_id.astype(int),article.product_type_no.astype(int)))
    tables={f:pd.read_parquet(DATA/f'fold_{f}/tasks/user-item-purchase/val.parquet') for f in range(3)}
    maps={f:pd.read_csv(DATA/f'fold_{f}/customer_id_map.csv').set_index('customer_id').original_customer_id for f in range(3)}
    wanted=set().union(*(set(map(int,maps[f].loc[t.customer_id])) for f,t in tables.items()))
    con=duckdb.connect();con.execute('SET threads=2');con.execute("SET memory_limit='1GB'")
    con.register('wanted',pd.DataFrame({'customer_id':sorted(wanted)}))
    hist=con.execute('SELECT t.customer_id,t.article_id,t.t_dat FROM read_parquet(?) t JOIN wanted w USING(customer_id) WHERE t.t_dat<=? ORDER BY t.customer_id,t.t_dat,t.article_id',
        [str(ROOT/'data/rel-hm/db/transactions.parquet'),max(t.timestamp.max() for t in tables.values())]).fetchdf()
    con.close()
    history={int(u):g for u,g in hist.groupby('customer_id',sort=False)}
    for f,t in tables.items():
        imap=pd.read_csv(DATA/f'fold_{f}/article_id_map.csv').sort_values('article_id')
        candidate=imap.original_article_id.to_numpy(dtype=np.int64)
        assert np.array_equal(imap.article_id,np.arange(10000)) and len(t)==256
        masks=[];annotations=[]
        for i,row in enumerate(t.itertuples(index=False)):
            u=int(maps[f].loc[row.customer_id]);g=history.get(u)
            past=g[g.t_dat<=row.timestamp] if g is not None else None
            seen=set(map(int,past.article_id)) if past is not None else set()
            ps={product[x] for x in seen};ts={types[x] for x in seen}
            targets=sorted(set(map(int,row.article_id)))
            original=[int(candidate[x]) if x<10000 else x-10000 for x in targets]
            groups=[novelty.classify(x,seen,ps,ts,product,types) for x in original]
            masks.append(np.isin(candidate,list(seen)))
            annotations.append(dict(fold=f,row=i,customer=u,mapped_customer=int(row.customer_id),cutoff=str(row.timestamp),
                targets=targets,groups=groups,available=[x<10000 for x in targets]))
        folder=DEST/f'fold_{f}';folder.mkdir(parents=True,exist_ok=True)
        np.save(folder/'seen_mask.npy',np.array(masks));write(folder/'annotations.json',annotations)
    write(DEST/'labels_ready.json',dict(validation_only=True,observations=768,customers=len(wanted),history_start=str(hist.t_dat.min()),policy='Source transactions <= each validation cutoff; diagnostic labels/masks only; model inputs unchanged'))


def forward_pair(model,batch,task):
    x=model.forward_gnn(batch,task.src_entity_table)
    count=batch[task.src_entity_table].batch_size
    lhs=x[task.src_entity_table][:count];projected=model.lhs_projector(lhs)
    rhs=model.rhs_embedding()
    global_scores=projected@rhs.t()+model.lin_offset_embgnn(projected).flatten()[:,None]
    hybrid=model.construct_logits(projected,lhs,x[task.dst_entity_table],rhs,
        batch[task.dst_entity_table].batch,batch[task.dst_entity_table].n_id)
    return hybrid,global_scores


def state_fingerprint(model):
    h=hashlib.sha256()
    for name,value in sorted(model.state_dict().items()):
        h.update(name.encode());h.update(value.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def fit(fold,arm,weight):
    from torch_geometric.seed import seed_everything
    work=DEST/f'fold_{fold}'/arm;work.mkdir(parents=True,exist_ok=True)
    if (work/'result.json').exists():
        result=read(work/'result.json');assert sha(work/'best.pt')==result['checkpoint_sha256'];return
    assert not (work/'history.json').exists(),'Partial training preserved; investigate before restart'
    wait_for_resources(f'f{fold}_{arm}')
    env=base.setup(fold,categorical=True)
    task,device,mod=env['task'],env['device'],env['module']
    assert device.type=='cuda'
    annotations=read(DEST/f'fold_{fold}/annotations.json')
    assert [a['targets'] for a in annotations]==[sorted(t) for t in base.labels(env,'val')]
    assert [a['mapped_customer'] for a in annotations]==env['tables']['val'].df[task.src_entity_col].tolist()
    model=env['make_model']('contextgnn')
    initial_state=state_fingerprint(model)
    if arm=='aux':
        assert initial_state==read(DEST/f'fold_{fold}/control/result.json')['initial_state_sha256']
    optimizer=torch.optim.Adam(model.parameters(),lr=.001)
    train_loader=base.loader(env,'train',FANOUT,shuffle=True)
    targets=base.labels(env,'val')
    @torch.no_grad()
    def evaluate(check_native=False):
        model.eval();mod.clear_rhs(model);seed_everything(42)
        parts={'hybrid':[],'global':[]}
        for batch in base.loader(env,'val',FANOUT):
            batch=batch.to(device);base.check_time(batch,task)
            hybrid,global_scores=forward_pair(model,batch,task)
            if check_native:
                native=model(batch,task.src_entity_table,task.dst_entity_table)
                bound=32*torch.finfo(hybrid.dtype).eps*max(1.,float(native.abs().max()))
                assert float((hybrid-native).abs().max())<=bound,'Dual forward exceeds FP32 bound'
                assert torch.equal(hybrid.argsort(descending=True,stable=True)[:,:12],native.argsort(descending=True,stable=True)[:,:12])
            for key,score in [('hybrid',hybrid),('global',global_scores)]:
                assert torch.isfinite(score).all();parts[key].append(score.cpu().numpy())
        return {key:np.concatenate(value) for key,value in parts.items()}
    run_id=RUN+f'_f{fold}_{arm}'
    record('global_aux_fit_started',f'Fold{fold} {arm}: lambda={weight}, matched initialization/training, validation only.',run_id,status='training',artifacts=str(work.relative_to(ROOT)))
    best=-1.;stale=0;history=[];started=time.perf_counter();torch.cuda.reset_peak_memory_stats()
    for epoch in range(1,11):
        model.train();mod.clear_rhs(model);losses=[]
        graph_hash=hashlib.sha256()
        for batch in train_loader:
            graph_hash.update(batch[task.src_entity_table].input_id.numpy().tobytes())
            for node_type in sorted(batch.node_types):
                graph_hash.update(node_type.encode());graph_hash.update(batch[node_type].n_id.numpy().tobytes())
            for edge_type in sorted(batch.edge_types):
                graph_hash.update(str(edge_type).encode());graph_hash.update(batch[edge_type].edge_index.numpy().tobytes())
            batch=batch.to(device);base.check_time(batch,task)
            src,dst=env['sparse_labels'][batch[task.src_entity_table].input_id]
            optimizer.zero_grad()
            hybrid,global_scores=forward_pair(model,batch,task)
            mixed_loss=mod.sparse_ce(hybrid,src,dst);global_loss=mod.sparse_ce(global_scores,src,dst)
            loss=mixed_loss+weight*global_loss if weight else mixed_loss
            assert torch.isfinite(loss);loss.backward();optimizer.step()
            losses.append((float(mixed_loss.detach()),float(global_loss.detach()),float(loss.detach())))
        scores=evaluate()
        pred=np.argsort(-scores['hybrid'],axis=1,kind='stable')[:,:12]
        ap=base.aps(pred,targets);metric=float(ap.mean())
        assert abs(metric-task.evaluate(pred,env['tables']['val'])['map'])<1e-10
        global_ap=base.aps(np.argsort(-scores['global'],axis=1,kind='stable')[:,:12],targets)
        if metric>best:
            best=metric;best_epoch=epoch;stale=0
            torch.save(dict(model_state_dict=model.state_dict(),epoch=epoch,lambda_global=weight,arm=arm),work/'best.pt')
            for key,value in scores.items():np.save(work/f'val_{key}_scores.npy',value)
            np.save(work/'val_ap.npy',ap);np.save(work/'val_predictions.npy',pred)
        else:stale+=1
        means=np.mean(losses,axis=0)
        item=dict(epoch=epoch,mixed_loss=float(means[0]),global_loss=float(means[1]),total_loss=float(means[2]),val_map=metric,global_map=float(global_ap.mean()),steps=len(losses),training_graph_sha256=graph_hash.hexdigest())
        if arm=='aux':
            control_history=read(DEST/f'fold_{fold}/control/history.json')
            if epoch<=len(control_history):assert item['training_graph_sha256']==control_history[epoch-1]['training_graph_sha256']
        history.append(item);write(work/'history.json',history)
        print('EPOCH',fold,arm,json.dumps(item),flush=True)
        record('global_aux_epoch',f'Fold{fold} {arm} epoch{epoch}: hybrid MAP {100*metric:.5f}%, global MAP {100*global_ap.mean():.5f}%.',run_id,status='training',epoch=epoch,val_metrics={'map':metric})
        if stale>=3:break
    checkpoint=sha(work/'best.pt')
    model.load_state_dict(torch.load(work/'best.pt',map_location=device)['model_state_dict'])
    replay=evaluate(check_native=True)
    for key,value in replay.items():
        saved=np.load(work/f'val_{key}_scores.npy')
        tolerance=32*np.finfo(np.float32).eps*max(1.,float(np.abs(saved).max()))
        assert np.max(np.abs(saved-value))<=tolerance
        assert np.array_equal(np.argsort(-saved,axis=1,kind='stable')[:,:12],np.argsort(-value,axis=1,kind='stable')[:,:12])
    historical_equal=None
    if arm=='control':
        prior=np.load(REF/f'fold_{fold}/combined/val_scores.npy')
        historical_equal=bool(np.array_equal(np.load(work/'val_ap.npy'),np.load(REF/f'fold_{fold}/combined/val_ap.npy')))
    assert sha(work/'best.pt')==checkpoint
    write(work/'result.json',dict(fold=fold,arm=arm,lambda_global=weight,validation_only=True,val_map=best,
        best_epoch=best_epoch,epochs=len(history),seconds=time.perf_counter()-started,peak_cuda_bytes=torch.cuda.max_memory_allocated(),
        checkpoint_sha256=checkpoint,protocol_sha256=sha(REP/'protocol.json'),
        verification='Native forward and reload within FP32 bound; exact top12; independent AP',
        initial_state_sha256=initial_state,previous_control_ap_equal=historical_equal,
        comparison_control='Fresh lambda0 fit with identical initial state and same epoch training graphs; historical metrics are contextual only'))
    record('global_aux_fit_verified',f'Fold{fold} {arm}: checkpoint and both ranking branches reloaded and verified.',run_id,status='validation_verified',val_metrics={'map':best},artifacts=str(work.relative_to(ROOT)))
    del model,optimizer,env,train_loader,replay,scores
    gc.collect();torch.cuda.empty_cache()


def report():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter
    rows=[];inventory=[]
    for fold in range(3):
        annotations=read(DEST/f'fold_{fold}/annotations.json');masks=np.load(DEST/f'fold_{fold}/seen_mask.npy')
        for a in annotations:
            for group,value in novelty.per_user(np.full(12,-1),a).items():
                inventory.append(dict(fold=fold,row=a['row'],group=group,targets=value['targets'],available=value['available']))
        for arm in ['control','aux']:
            folder=DEST/f'fold_{fold}'/arm
            assert sha(folder/'best.pt')==read(folder/'result.json')['checkpoint_sha256']
            for mode in ['hybrid','global','new_only']:
                scores=np.load(folder/f"val_{'global' if mode=='global' else 'hybrid'}_scores.npy")
                if mode=='new_only':scores[masks]=-np.inf
                pred=np.argsort(-scores,axis=1,kind='stable')[:,:12]
                if mode=='new_only':assert not masks[np.arange(len(pred))[:,None],pred].any()
                np.save(folder/f'val_{mode}_predictions.npy',pred)
                for rec,a in zip(pred,annotations):
                    for group,value in novelty.per_user(rec,a).items():
                        rows.append(dict(fold=fold,row=a['row'],customer=a['customer'],arm=arm,mode=mode,group=group,**value))
    users=pd.DataFrame(rows);users.to_parquet(REP/'per_user_metrics.parquet',index=False)
    summaries=[]
    for (arm,mode,group),g in users.groupby(['arm','mode','group'],sort=False):
        eligible=g[g.targets>0];available=g[g.available>0]
        summaries.append(dict(arm=arm,mode=mode,group=group,observations=len(g),eligible=len(eligible),available_users=len(available),
            targets=int(g.targets.sum()),available_targets=int(g.available.sum()),map=eligible['map'].mean(),
            recall=eligible.recall.mean(),available_recall=available.available_recall.mean(),ap_contribution=g.ap_contribution.mean()))
    table=pd.DataFrame(summaries);table.to_csv(REP/'metrics.csv',index=False)
    users.groupby(['fold','arm','mode','group'])[['map','available_recall']].mean().reset_index().to_csv(REP/'fold_metrics.csv',index=False)
    coverage=pd.DataFrame(inventory).groupby('group')[['targets','available']].sum().reset_index()
    coverage.to_csv(REP/'coverage.csv',index=False)
    contrasts=[]
    for mode,group,metric in [('hybrid','all','map'),('global','all','map'),('hybrid','new','available_recall'),('global','new','available_recall'),('new_only','new','available_recall')]:
        s=users[(users['mode']==mode)&(users['group']==group)]
        a=s[s.arm=='aux'].sort_values(['fold','row']);b=s[s.arm=='control'].sort_values(['fold','row'])
        assert np.array_equal(a[['fold','row']],b[['fold','row']])
        valid=a[metric].notna().to_numpy();assert np.array_equal(valid,b[metric].notna())
        delta=a[metric].to_numpy()[valid]-b[metric].to_numpy()[valid]
        ids=a.customer.to_numpy()[valid];unique,inverse=np.unique(ids,return_inverse=True)
        counts=np.bincount(inverse);sums=np.bincount(inverse,weights=delta);rng=np.random.default_rng(42);boot=[]
        for _ in range(5000):
            ix=rng.integers(0,len(unique),len(unique));boot.append(sums[ix].sum()/counts[ix].sum())
        low,high=np.quantile(boot,[.025,.975])
        contrasts.append(dict(mode=mode,group=group,metric=metric,delta=float(delta.mean()),ci95_low=float(low),ci95_high=float(high),observations=len(delta)))
    pd.DataFrame(contrasts).to_csv(REP/'paired_contrasts.csv',index=False)
    frozen=read(REP/'protocol.json')
    for p,h in frozen['reference_hashes'].items():assert sha(ROOT/p)==h
    for p,h in frozen['sources'].items():assert sha(ROOT/p)==h
    lines=['# Дополнительный global loss в ContextGNN','',
        'Три фолда, seed42, 768 validation-наблюдений. Контроль lambda=0 и эксперимент lambda=1 обучены заново '
        'с одинаковой инициализацией, fanout64/32, восемью категориальными кодами и прежними параметрами. '
        'Сравнение проводится со свежим контролем lambda0; побитовое воспроизведение прежнего обучения '
        'не утверждается. Начальные веса и обучающие графы совпали между парными вариантами. '
        'Эпоха выбрана по обычному hybrid MAP, '
        'коэффициент не подбирался. Test не оценивался.','',
        '| Режим | Метрика | Контроль, % | +global loss, % | Разница, п.п. | 95% интервал, п.п. |',
        '|---|---|---:|---:|---:|---:|']
    chart=[]
    for c in contrasts:
        q=table[(table['mode']==c['mode'])&(table['group']==c['group'])].set_index('arm')
        control=q.loc['control',c['metric']];aux=q.loc['aux',c['metric']]
        label=f"{c['mode']}: {c['metric']} ({c['group']})"
        lines.append(f"| {c['mode']} | {c['metric']} / {c['group']} | {100*control:.4f} | {100*aux:.4f} | {100*c['delta']:+.4f} | [{100*c['ci95_low']:+.4f}; {100*c['ci95_high']:+.4f}] |")
        chart.append((label,control,aux))
    lines+=['','Global — оценки до локальной перезаписи. New-only — исключены все прошлые покупки из исходной истории '
        'до cutoff; затем заново выбран top12. Новые товары определены относительно доступной истории, '
        'а не всей жизни пользователя. Отсутствующие среди кандидатов цели сохранены в полных MAP/recall; '
        'available_recall рассчитан отдельно на одинаковом для обоих вариантов подмножестве наблюдений.', '',
        '| Группа | Всего целей | Доступно |', '|---|---:|---:|',
        *[f'| {r.group} | {r.targets} | {r.available} |' for r in coverage.itertuples()],
        '','Интервалы: 5 000 парных bootstrap по исходным покупателям, без поправки '
        'за множество сравнений. Это повторно использованная validation и один seed; результат не является '
        'независимым подтверждением. Полная диагностика групп и фолдов сохранена в CSV/Parquet.', '',
        '![Сравнение](comparison.png)','']
    (REP/'report_ru.md').write_text('\n'.join(lines),encoding='utf-8')
    y=np.arange(len(chart));fig,ax=plt.subplots(figsize=(12,6))
    ax.barh(y-.18,[100*x[1] for x in chart],height=.34,label='Control: lambda=0')
    ax.barh(y+.18,[100*x[2] for x in chart],height=.34,label='Auxiliary global CE: lambda=1')
    ax.set(yticks=y,yticklabels=[x[0] for x in chart],xlabel='Metric (%)',title='ContextGNN global auxiliary loss — validation only, seed42')
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=100));ax.legend();fig.tight_layout()
    fig.savefig(REP/'comparison.png',dpi=170);fig.savefig(REP/'comparison.svg');plt.close(fig)
    write(REP/'summary.json',dict(status='pending_visual_review',run_id=RUN,validation_only=True,observations=768,
        contrasts=contrasts,metrics=table.replace({np.nan:None}).to_dict('records'),reference_hashes_unchanged=True,
        fits=[read(DEST/f'fold_{f}'/arm/'result.json') for f in range(3) for arm in ['control','aux']]))
    record('global_aux_report_ready','Six matched fits verified: identical paired initial states and training graphs; FP32-bounded native/reload inference and exact top12. Fresh lambda0 controls used; historical bitwise training reproduction not claimed. Global/hybrid/new-only diagnostics and intervals saved; awaiting visual review.',RUN,status='pending_visual_review',artifacts=str(REP.relative_to(ROOT)))
    print('REPORT_READY',str(REP/'report_ru.md'),flush=True)


def main():
    import fcntl
    torch.set_num_threads(2);torch.set_num_interop_threads(2);os.nice(5)
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['run','report'],default='run',nargs='?');args=parser.parse_args()
    DEST.mkdir(parents=True,exist_ok=True);REP.mkdir(parents=True,exist_ok=True)
    if args.stage=='report':report();return
    with (DEST/'execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        freeze();gradient_test()
        record('global_aux_started','Authorized auxiliary global CE experiment: six sequential matched fits (lambda0 control / fixed lambda1), validation only, no API. Existing H011 CPU process left untouched; free GPU/RAM checked before each fit.',RUN,status='preparing',artifacts=str(REP.relative_to(ROOT)))
        prepare_labels()
        base.RUN,base.DEST,base.REP=RUN,DEST,REP
        for fold in range(3):
            for arm,weight in [('control',0.),('aux',1.)]:fit(fold,arm,weight)
        report()


if __name__=='__main__':main()
