"""Validation experiment: residual attention over sampled history, K=1 vs K=4."""
import os
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='2'
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
os.environ['PATH']='/usr/lib/wsl/lib:'+os.environ.get('PATH','')
import argparse
import copy
import gc
import inspect
from pathlib import Path
import random
import shutil
import subprocess
import sys
import types
import numpy as np
import torch
import torch.nn.functional as F
import context_global_aux_v3 as previous
import item_encoder_followup as reporting
from common import ROOT,DATA,OUT,REPORT,read,write,sha,record

RUN='hm_medium_context_multi_interest_k1_k4_seed42_v1'
DEST=OUT/'context_multi_interest_v1'
REP=REPORT/'context_multi_interest_v1'
CONTROL=OUT/'context_global_aux_v3'
ARMS=['control','interest1','interest4']
NAMES={'control':'FUSION original','interest1':'FUSION + attention K=1','interest4':'FUSION + attention K=4'}


class InterestPool(torch.nn.Module):
    def __init__(self,channels,dim,k):
        super().__init__()
        self.k=k
        self.hidden=torch.nn.Linear(channels,channels*4)
        # Always initialize four heads, then keep the active rows. Shared weights
        # including head0 match exactly between K1/K4 without changing sampler RNG.
        heads=torch.nn.Linear(channels*4,4)
        self.project=torch.nn.Linear(channels,dim,bias=False)
        self.heads=torch.nn.Linear(channels*4,k)
        with torch.no_grad():
            self.heads.weight.copy_(heads.weight[:k]);self.heads.bias.copy_(heads.bias[:k])

    def forward(self,items,groups,count):
        # Ragged segment softmax along history, separately for each root/head.
        logits=self.heads(self.hidden(items).tanh())
        index=groups[:,None].expand(-1,self.k)
        maxima=logits.new_full((count,self.k),-torch.inf)
        maxima.scatter_reduce_(0,index,logits,reduce='amax',include_self=True)
        weights=(logits-maxima[groups]).exp()
        sums=logits.new_zeros((count,self.k));sums.scatter_add_(0,index,weights)
        weights=weights/sums[groups].clamp_min(1e-12)
        pooled=items.new_zeros((count,self.k,items.shape[-1]))
        pooled.index_add_(0,groups,weights[:,:,None]*items[:,None,:])
        return self.project(pooled),weights


def components(model,batch,task):
    x=model.forward_gnn(batch,task.src_entity_table)
    count=batch[task.src_entity_table].batch_size
    lhs=x[task.src_entity_table][:count];q0=model.lhs_projector(lhs)
    items=x[task.dst_entity_table]
    groups=batch[task.dst_entity_table].batch;ids=batch[task.dst_entity_table].n_id
    delta,attention=model.interest_pool(items,groups,count)
    queries=q0[:,None,:]+delta
    rhs=model.rhs_embedding()
    per_interest=queries@rhs.t()
    global_scores=per_interest.max(dim=1).values+model.lin_offset_embgnn(q0).flatten()[:,None]
    # Local formula/offsets are the unmodified upstream formula using q0.
    original=model.construct_logits(q0,lhs,items,rhs,groups,ids)
    hybrid=global_scores.clone();hybrid[groups,ids]=original[groups,ids]
    return hybrid,global_scores,queries,attention,groups,per_interest


def forward_pair(model,batch,task):
    value=components(model,batch,task)
    return value[0],value[1]


def forward(self,batch,entity_table,dst_table):
    task=types.SimpleNamespace(src_entity_table=entity_table,dst_entity_table=dst_table)
    return forward_pair(self,batch,task)[0]


def install_model(model,k):
    initial=previous.state_fingerprint(model)
    # Additional parameters never advance the original training/sampling RNG.
    device=model.lhs_projector.weight.device
    with torch.random.fork_rng(devices=[device.index or 0]):
        torch.manual_seed(314159)
        pool=InterestPool(model.channels,model.lhs_projector.out_features,k).to(device)
    model.interest_pool=pool
    model._fusion_initial_fingerprint=initial
    model.forward=types.MethodType(forward,model)
    return model


def freeze():
    sources=['CVFollowup/context_multi_interest.py','CVFollowup/context_global_aux_v3.py',
        'CVFollowup/context_first3.py','CVFollowup/item_encoder_followup.py','CVFollowup/novelty_audit.py',
        'ContextGNN/upstream/contextgnn/nn/models/contextgnn.py','ContextGNN/upstream/contextgnn/nn/rhs_embedding.py']
    refs={}
    for f in range(3):
        for n in ['best.pt','result.json','history.json','val_hybrid_scores.npy','val_global_scores.npy','val_ap.npy','val_predictions.npy']:
            p=CONTROL/f'fold_{f}/control'/n;refs[str(p.relative_to(ROOT))]=sha(p)
        for n in ['seen_mask.npy','annotations.json']:
            p=CONTROL/f'fold_{f}'/n;refs[str(p.relative_to(ROOT))]=sha(p)
        for n in ['db/article.parquet','article_id_map.csv','customer_id_map.csv','tasks/user-item-purchase/train.parquet','tasks/user-item-purchase/val.parquet']:
            p=DATA/f'fold_{f}'/n;refs[str(p.relative_to(ROOT))]=sha(p)
        p=OUT/f'fold_{f}/runtime/gnn_timefix_refit/gnn.py';refs[str(p.relative_to(ROOT))]=sha(p)
    protocol=dict(run_id=RUN,arms=ARMS,validation_only=True,no_test=True,no_api=True,
        source='https://github.com/THUDM/ComiRec/blob/master/src/model.py (Model_ComiRec_SA); https://arxiv.org/abs/2005.09347',
        attribution='Custom ContextGNN adaptation inspired by ComiRec-SA, not a reproduction: no sequence positional table, target readout sampled softmax or diversity reranker',
        history='Only sampled past article nodes already in original two-hop temporal graph, per-root disjoint groups. Temporal GNN features retained. No expanded history or target-conditioned pooling.',
        architecture='A=segment_softmax(W2 tanh(W1 H)); delta_k=Linear(sum A_k H), no projection bias; q_k=q_original+delta_k. Global item score=max_k(q_k dot e_item)+original global offset(q_original). Empty history: delta0.',
        local='Unmodified upstream local scores and offsets, original root q0; global multi-interest scores overwritten at same local positions',
        loss='Original sparse full-catalog hybrid CE only, no auxiliary/diversity loss',
        initialization='Construct seeded original FUSION, verify old full state hash. Extra pool RNG fork seed314159; same shared hidden/project and head0 weights for K1/K4; sampler RNG unaffected.',
        settings=dict(seed=42,pythonhashseed=42,fanout=[64,32],categorical_codes=previous.base.CODE_COLUMNS,
            optimizer='Adam .001',batch_size=128,max_epochs=10,patience=3,selection='Original hybrid MAP on fixed256 validation rows/fold'),
        comparisons='Primary K4 vs matched K1; secondary K4 vs original FUSION. Six new fits and three reused verified controls, no hyperparameter search.',
        diagnostics='Hybrid/global MAP; hybrid/new-only macro recall available new, full unavailable targets retained separately; 5000 paired original-customer bootstrap. K4 win fractions and query/attention similarity for collapse.',
        replay='Canonical best-epoch scores retained, FP32 bound 32*eps*scale; all top12/AP changes measured, no target-based replay selection',
        resources='One fresh subprocess per fit, sequential, 2CPU threads nice5; require GPU<512MiB RAM>5GB; do not interrupt other work',
        reference_hashes=refs,sources={n:sha(ROOT/n) for n in sources},
        limitation='One seed and repeatedly inspected validation; no independent confirmation, multiple comparisons uncorrected')
    p=REP/'protocol.json'
    if p.exists():assert read(p)==protocol,'New configuration needs unique run ID'
    else:write(p,protocol)
    for n in sources:
        p=REP/'frozen_source'/n;p.parent.mkdir(parents=True,exist_ok=True)
        if p.exists():assert sha(p)==sha(ROOT/n)
        else:shutil.copyfile(ROOT/n,p)
    for f in range(3):
        folder=DEST/f'fold_{f}';folder.mkdir(parents=True,exist_ok=True)
        for n in ['seen_mask.npy','annotations.json']:
            p=folder/n
            if p.exists():assert sha(p)==sha(CONTROL/f'fold_{f}'/n)
            else:shutil.copyfile(CONTROL/f'fold_{f}'/n,p)
        if not (folder/'control').exists():shutil.copytree(CONTROL/f'fold_{f}/control',folder/'control')
        write(folder/'control/reuse_lineage.json',dict(source=str((CONTROL/f'fold_{f}/control').relative_to(ROOT)),checkpoint_sha256=sha(folder/'control/best.pt')))


def pool_smoke():
    with torch.random.fork_rng():
        torch.manual_seed(314159);one=InterestPool(4,4,1)
        torch.manual_seed(314159);four=InterestPool(4,4,4)
        assert torch.equal(one.hidden.weight,four.hidden.weight)
        assert torch.equal(one.project.weight,four.project.weight)
        assert torch.equal(one.heads.weight,four.heads.weight[:1])
        items=torch.tensor([[1.,0,0,0],[0,1.,0,0],[0,0,2.,0]],requires_grad=True)
        groups=torch.tensor([0,0,1])
        delta,attention=four(items,groups,3)
        assert torch.isfinite(delta).all() and torch.equal(delta[2],torch.zeros_like(delta[2]))
        assert torch.allclose(attention[:2].sum(0),torch.ones(4))
        assert torch.equal(attention[2],torch.ones(4))
        expected=four.project((attention[:,:,None]*items[:,None,:])[:2].sum(0))
        torch.testing.assert_close(delta[0],expected)
        delta.square().sum().backward()
        assert torch.isfinite(items.grad).all() and items.grad.abs().sum()>0
        assert four.hidden.weight.grad.abs().sum()>0 and four.heads.weight.grad.abs().sum()>0
    write(REP/'pool_smoke.json',dict(passed=True,checks=['Shared K1/K4 init','Segment normalization','No cross-root mixing','Empty-history zero residual','Hand calculation','Attention/history gradients']))


def install_training(fold,arm):
    previous.RUN,previous.DEST,previous.REP=RUN,DEST,REP
    previous.base.RUN,previous.base.DEST,previous.base.REP=RUN,DEST,REP
    old_setup=previous.base.setup
    def setup(*a,**kw):
        env=old_setup(*a,**kw);factory=env['make_model']
        def make_model(kind):
            model=factory(kind)
            assert previous.state_fingerprint(model)==read(DEST/f'fold_{fold}/control/result.json')['initial_state_sha256']
            model=install_model(model,1 if arm=='interest1' else 4)
            write(DEST/f'fold_{fold}'/arm/'initial_pool.json',dict(
                shared_hidden=previous.state_fingerprint(model.interest_pool.hidden),
                shared_project=previous.state_fingerprint(model.interest_pool.project),
                head0_sha256=__import__('hashlib').sha256(model.interest_pool.heads.weight[:1].detach().cpu().numpy().tobytes()+model.interest_pool.heads.bias[:1].detach().cpu().numpy().tobytes()).hexdigest(),
                parameter_count=sum(p.numel() for p in model.parameters())))
            return model
        env['make_model']=make_model;return env
    previous.base.setup=setup
    source=inspect.getsource(previous.fit)
    replacements={
        'initial_state=state_fingerprint(model)':'initial_state=model._fusion_initial_fingerprint',
        "if arm=='global_ce':":"if arm in ('interest1','interest4'):",
        '    @torch.no_grad()\n    def evaluate':'    native_checks=[]\n    replay_checks={}\n    @torch.no_grad()\n    def evaluate',
        '                assert torch.equal(hybrid.argsort(descending=True,stable=True)[:,:12],native.argsort(descending=True,stable=True)[:,:12])':
            '                native_checks.append(replay_check(hybrid.cpu().numpy(),native.cpu().numpy(),[targets[int(i)] for i in batch[task.src_entity_table].input_id.cpu()]))',
        "        assert np.array_equal(np.argsort(-saved,axis=1,kind='stable')[:,:12],np.argsort(-value,axis=1,kind='stable')[:,:12])":
            "        replay_checks[key]=replay_check(saved,value,targets)\n        np.save(work/f'verification_replay_{key}_scores.npy',value)",
        '    historical_equal=None':"    write(work/'replay_verification.json',dict(native=native_checks,reload=replay_checks,canonical_scores_retained=True))\n    historical_equal=None",
        "verification='Native forward and reload within FP32 bound; exact top12; independent AP'":
            "verification='FP32-bounded reload, quantified rank/AP sensitivity, independent canonical AP'",
        "'global_aux_":"'multi_interest_"}
    for old,new in replacements.items():
        assert old in source,old
        source=source.replace(old,new)
    p=REP/'executed_refit.py'
    if p.exists():assert p.read_text(encoding='utf-8')==source
    else:p.write_text(source,encoding='utf-8')
    previous.forward_pair=forward_pair;previous.replay_check=reporting.replay_check
    exec(compile(source,str(p),'exec'),previous.__dict__)


def fit(fold,arm):
    assert os.environ.get('PYTHONHASHSEED')=='42'
    install_training(fold,arm)
    previous.fit(fold,arm,0.)
    p=DEST/f'fold_{fold}'/arm/'result.json';r=read(p)
    r.update(interests=1 if arm=='interest1' else 4,no_auxiliary_loss=True,
        original_fusion_initial_state_matched=True,executed_refit_sha256=sha(REP/'executed_refit.py'))
    write(p,r)


def probe():
    previous.REP,previous.RUN=REP,RUN;previous.wait_for_resources('probe')
    previous.base.DEST=DEST
    env=previous.base.setup(0,categorical=True);task=env['task'];model=env['make_model']('contextgnn')
    original=type(model).forward
    model=install_model(model,4);model.eval();env['module'].clear_rhs(model)
    from torch_geometric.seed import seed_everything
    seed_everything(42)
    batch=next(iter(previous.base.loader(env,'val',[64,32]))).to(env['device'])
    previous.base.check_time(batch,task)
    with torch.no_grad():
        hybrid,global_scores,q,attention,groups,per=components(model,batch,task)
        native=original(model,batch,task.src_entity_table,task.dst_entity_table)
        ids=batch[task.dst_entity_table].n_id
        torch.testing.assert_close(hybrid[groups,ids],native[groups,ids],rtol=0,atol=0)
        torch.testing.assert_close(global_scores,per.max(1).values+model.lin_offset_embgnn(model.lhs_projector(model.forward_gnn(batch,task.src_entity_table)[task.src_entity_table][:len(q)])).flatten()[:,None])
        # Zero residual must recover original native scores for every candidate.
        model.interest_pool.project.weight.zero_()
        zero=model(batch,task.src_entity_table,task.dst_entity_table)
        torch.testing.assert_close(zero,native,rtol=1e-5,atol=1e-5)
    model.train();env['module'].clear_rhs(model)
    output=model(batch,task.src_entity_table,task.dst_entity_table)
    output.square().mean().backward()
    assert model.interest_pool.project.weight.grad.abs().sum()>0
    write(REP/'model_probe.json',dict(passed=True,smoke_only=True,validation_batch=len(q),
        local_scores_exactly_unchanged=True,zero_residual_recovers_original=True,max_over_interest_verified=True,
        finite_full_catalog_forward=True,projection_gradient=True,no_fit=True))
    print('PROBE_PASSED',flush=True)


def report():
    reporting.RUN,reporting.DEST,reporting.REP=RUN,DEST,REP
    reporting.ARMS,reporting.NAMES=ARMS,NAMES
    # Common metric implementation is reused; custom text below replaces its
    # item-encoder-specific narrative. Numbers/paired intervals stay untouched.
    reporting.report(ARMS,'final')
    import pandas as pd
    users=pd.read_parquet(REP/'final_per_user.parquet')
    contrasts=pd.read_csv(REP/'final_contrasts.csv').assign(reference='control')
    extra=[]
    for mode,group,metric in [('hybrid','all','map'),('global','all','map'),('hybrid','new','available_recall'),('new_only','new','available_recall')]:
        p=users[(users['mode']==mode)&(users['group']==group)]
        a=p[p.arm=='interest4'].sort_values(['fold','row']);b=p[p.arm=='interest1'].sort_values(['fold','row'])
        assert np.array_equal(a[['fold','row','customer']],b[['fold','row','customer']])
        valid=a[metric].notna().to_numpy();assert np.array_equal(valid,b[metric].notna())
        delta=a[metric].to_numpy()[valid]-b[metric].to_numpy()[valid]
        _,inv=np.unique(a.customer.to_numpy()[valid],return_inverse=True)
        counts=np.bincount(inv);sums=np.bincount(inv,weights=delta);rng=np.random.default_rng(42);boots=[]
        for _ in range(5000):
            ix=rng.integers(0,len(counts),len(counts));boots.append(sums[ix].sum()/counts[ix].sum())
        low,high=np.quantile(boots,[.025,.975])
        extra.append(dict(arm='interest4',reference='interest1',mode=mode,group=group,metric=metric,
            delta=float(delta.mean()),low=float(low),high=float(high),observations=len(delta)))
    contrasts=pd.concat([contrasts,pd.DataFrame(extra)],ignore_index=True)
    contrasts.to_csv(REP/'final_contrasts.csv',index=False)
    table=pd.read_csv(REP/'final_metrics.csv')
    lines=['# ContextGNN: один и четыре интереса','',
        'Три прежних validation-среза,768 наблюдений/753 покупателя. Шесть новых fit, три исходных FUSION-контроля сохранены. '
        'Общие начальные веса и обучающие sampled-графы сверяются. Один seed42, Adam .001, batch128, fanout64/32, '
        'восемь categorical-кодов, max10/patience3 по hybrid MAP. Исходный CE без дополнительного global loss. Test не оценивался.','',
        'Из прошлых товаров текущего sampled-графа attention получает K взвешенных векторов; они проецируются и добавляются '
        'к исходному вектору пользователя. Для товара используется максимальный dot product по K интересам. '
        'Локальная формула и offsets исходного root-вектора сохранены. История модели не расширена; будущих покупок во входах нет.','',
        'Адаптация идеи ComiRec-SA, а не воспроизведение статьи: нет отдельной последовательности с positional embedding, '
        'target-conditioned sampled-softmax readout и reranker разнообразия. [Оригинальный код](https://github.com/THUDM/ComiRec/blob/master/src/model.py), '
        '[статья](https://arxiv.org/abs/2005.09347).','',
        '| Метрика | FUSION | attention K=1 | attention K=4 |','|---|---:|---:|---:|']
    for mode,group,metric in [('hybrid','all','map'),('global','all','map'),('hybrid','new','available_recall'),('new_only','new','available_recall')]:
        values=[float(table[(table.arm==a)&(table['mode']==mode)&(table['group']==group)][metric].iloc[0]) for a in ARMS]
        lines.append(f'|{mode}: {metric}|'+ '|'.join(f'{100*v:.4f}%' for v in values)+'|')
    lines+=['','| Сравнение | Метрика | Разница, п.п. | 95% интервал, п.п. |','|---|---|---:|---:|']
    for c in contrasts.itertuples():
        lines.append(f'|{c.arm} − {c.reference}|{c.mode}/{c.metric}|{100*c.delta:+.4f}|[{100*c.low:+.4f}; {100*c.high:+.4f}]|')
    lines+=['','Основное сравнение K4−K1 отделяет несколько интересов от нового pooling; K4−FUSION вторичное. '
        '5000 paired bootstrap по исходным покупателям, без поправки за несколько сравнений. Один seed и повторно используемая validation: '
        'это диагностический эксперимент, не независимое подтверждение.','',
        'Все будущие цели, включая недоступные, сохранены в MAP/полном recall (CSV). Условный recall новых — на одинаковых493наблюдениях; '
        'всего целей2477/доступно1038, новых2373/доступно972. New-only: маска всей прошлой истории перед top12 полного каталога.','',
        'Проверки начальных весов, обучающих графов, FP32 replay и чувствительности top12/AP сохраняются; канонические оценки не подменяются. '
        'Распределение выбранных голов и сходство векторов — head_diagnostics.json каждого fit.','',
        '![Сравнение](final_comparison.png)','']
    (REP/'final_report_ru.md').write_text('\n'.join(lines),encoding='utf-8')
    # Replace inherited plot title with an experiment-specific chart.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    chart=[('hybrid','all','map'),('global','all','map'),('hybrid','new','available_recall'),('new_only','new','available_recall')]
    fig,ax=plt.subplots(figsize=(13,6));y=np.arange(4);height=.23
    for i,a in enumerate(ARMS):
        values=[100*float(table[(table.arm==a)&(table['mode']==m)&(table['group']==g)][metric].iloc[0]) for m,g,metric in chart]
        ax.barh(y+(i-1)*height,values,height=.21,label=NAMES[a])
    ax.set(yticks=y,yticklabels=[f'{m}: {metric}' for m,g,metric in chart],xlabel='Метрика, %',title='ContextGNN: attention K=1 / K=4 — validation, seed42')
    ax.legend();fig.tight_layout();fig.savefig(REP/'final_comparison.png',dpi=170);fig.savefig(REP/'final_comparison.svg');plt.close(fig)
    summary=read(REP/'final_summary.json');summary.update(contrasts=contrasts.to_dict('records'),primary_comparison='interest4-interest1')
    write(REP/'final_summary.json',summary)


@torch.no_grad()
def diagnose(fold,arm):
    previous.REP,previous.RUN=REP,RUN;previous.wait_for_resources(f'diagnostics_f{fold}_{arm}')
    previous.base.DEST=DEST;env=previous.base.setup(fold,categorical=True)
    k=1 if arm=='interest1' else 4
    model=install_model(env['make_model']('contextgnn'),k)
    folder=DEST/f'fold_{fold}'/arm
    model.load_state_dict(torch.load(folder/'best.pt',map_location=env['device'])['model_state_dict'])
    model.eval();env['module'].clear_rhs(model)
    from torch_geometric.seed import seed_everything
    seed_everything(42);wins=np.zeros(k,dtype=np.int64);cosines=[];rows=[]
    for batch in previous.base.loader(env,'val',[64,32]):
        batch=batch.to(env['device']);previous.base.check_time(batch,env['task'])
        hybrid,global_scores,q,att,groups,per=components(model,batch,env['task'])
        selected=per.argmax(1).cpu().numpy();wins+=np.bincount(selected.ravel(),minlength=k)
        if k>1:
            normalized=F.normalize(q,dim=-1);c=normalized@normalized.transpose(1,2)
            cosines.extend(c[:,torch.triu_indices(k,k,offset=1)[0],torch.triu_indices(k,k,offset=1)[1]].mean(1).cpu().tolist())
        for i in range(len(q)):
            a=att[groups==i]
            if len(a):
                overlaps=F.normalize(a,dim=0).t()@F.normalize(a,dim=0)
                mean_overlap=float(overlaps[torch.triu_indices(k,k,offset=1)[0],torch.triu_indices(k,k,offset=1)[1]].mean()) if k>1 else None
                rows.append(dict(history_items=len(a),attention_pair_cosine=mean_overlap,
                    mean_attention_entropy=float(-(a*a.clamp_min(1e-12).log()).sum(0).mean())))
    write(folder/'head_diagnostics.json',dict(k=k,global_catalog_winner_counts=wins.tolist(),
        global_catalog_winner_fractions=(wins/wins.sum()).tolist(),mean_query_pair_cosine=float(np.mean(cosines)) if cosines else None,
        history_rows=rows,mean_attention_pair_cosine=float(np.mean([r['attention_pair_cosine'] for r in rows])) if k>1 else None,
        checkpoint_sha256=sha(folder/'best.pt'),note='Descriptive collapse indicators only; no retraining or model selection'))
    print('DIAGNOSTICS',fold,arm,flush=True)


def main():
    torch.set_num_threads(2);torch.set_num_interop_threads(2);os.nice(max(0,5-os.getpriority(os.PRIO_PROCESS,0)))
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['run','probe','fit','diagnose','report']);parser.add_argument('--fold',type=int);parser.add_argument('--arm',choices=ARMS[1:]);args=parser.parse_args()
    REP.mkdir(parents=True,exist_ok=True);DEST.mkdir(parents=True,exist_ok=True)
    if args.stage=='fit':fit(args.fold,args.arm);return
    if args.stage=='probe':probe();return
    if args.stage=='diagnose':diagnose(args.fold,args.arm);return
    if args.stage=='report':report();return
    with (DEST/'execution.lock').open('a') as lock:
        import fcntl
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        freeze();pool_smoke()
        def child(stage,fold=None,arm=None):
            command=[sys.executable,'-u',str(Path(__file__)),stage]
            if fold is not None:command+=['--fold',str(fold),'--arm',arm]
            log=REP/(f'fold_{fold}_{arm}_{stage}.log' if fold is not None else f'{stage}.log')
            with log.open('a') as stream:
                subprocess.run(command,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True,env={**os.environ,'PYTHONHASHSEED':'42'})
        child('probe')
        record('multi_interest_started','Authorized multi-interest experiment: original FUSION plus matched attention K1/K4 on three fixed validation folds. Six new sequential fits, same original loss/history. GPU0MiB, RAM10.8GB, no competing training; 2CPU nice5. Smoke/probe separate from experiment.',RUN,
            status='training',artifacts=str(REP.relative_to(ROOT)))
        for arm in ARMS[1:]:
            for fold in range(3):
                print('FIT_START',fold,arm,flush=True);child('fit',fold,arm);print('FIT_DONE',fold,arm,flush=True)
                child('diagnose',fold,arm)
        report()


if __name__=='__main__':main()
