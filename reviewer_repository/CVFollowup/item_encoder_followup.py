"""Validation-only FEATURE ablation, then a fixed semantic item-graph ablation."""
import os
os.environ.setdefault('OMP_NUM_THREADS','2')
os.environ.setdefault('MKL_NUM_THREADS','2')
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
import argparse
import gc
import inspect
import json
from pathlib import Path
import shutil
import subprocess
import sys
import hashlib
import numpy as np
import pandas as pd
import torch
import context_global_aux_v3 as previous
from common import ROOT,DATA,OUT,REPORT,read,write,sha,record

RUN='hm_medium_item_encoder_feature_semgraph_seed42_v1'
DEST=OUT/'item_encoder_followup_v1'
REP=REPORT/'item_encoder_followup_v1'
CONTROL=OUT/'context_global_aux_v3'
ARMS=['control','feature','similarity_graph']
NAMES={'control':'FUSION','feature':'FEATURE','similarity_graph':'FUSION + semantic item graph'}
GRAPH_COLUMNS=previous.base.CODE_COLUMNS
TEXT_COLUMNS=['prod_name','detail_desc']


def freeze():
    refs={}
    for f in range(3):
        for n in ['best.pt','result.json','history.json','val_hybrid_scores.npy','val_global_scores.npy','val_ap.npy','val_predictions.npy']:
            p=CONTROL/f'fold_{f}/control'/n;refs[str(p.relative_to(ROOT))]=sha(p)
        for n in ['seen_mask.npy','annotations.json']:
            p=CONTROL/f'fold_{f}'/n;refs[str(p.relative_to(ROOT))]=sha(p)
        for n in ['db/article.parquet','article_id_map.csv','tasks/user-item-purchase/train.parquet','tasks/user-item-purchase/val.parquet']:
            p=DATA/f'fold_{f}'/n;refs[str(p.relative_to(ROOT))]=sha(p)
    sources={n:sha(ROOT/n) for n in ['CVFollowup/item_encoder_followup.py','CVFollowup/context_global_aux_v3.py',
        'CVFollowup/context_first3.py','CVFollowup/novelty_audit.py','ContextGNN/upstream/contextgnn/nn/rhs_embedding.py',
        'ContextGNN/upstream/contextgnn/nn/models/contextgnn.py']}
    value=dict(run_id=RUN,validation_only=True,no_test_scoring=True,no_api=True,seed=42,pythonhashseed='42',
        order='Three FEATURE fits and report first, then graph construction and three graph fits; verified FUSION controls reused unchanged',
        training='Original full-catalog sparse CE only; NO auxiliary global loss; Adam .001, batch128, fanout64/32, max10/patience3 on hybrid MAP',
        initialization='Construct identical seeded FUSION first; verify full initial-state hash against controls; FEATURE deletes lookup weights, graph wraps unchanged RHS. All common starting weights preserved.',
        graph=dict(candidates=10000,neighbors=20,text_columns=TEXT_COLUMNS,categorical_columns=GRAPH_COLUMNS,
            text='word TFIDF uni/bigrams, min_df2, max_features12000, sublinear_tf, float32, L2',
            attributes='categorical one-hot, L2 per row; all eight corrected codes',
            similarity='cosine of equally weighted text and attribute blocks; exact blockwise top20, no self edge, stable item-ID tie order; positive weights row-normalized',
            propagation='e_final = 0.5*e_FUSION + 0.5*P@e_FUSION, one differentiable propagation step, fixed graph, no new trainable parameters',
            information='Only fixed catalog attributes/descriptions already present in original model inputs; NO transactions/labels used to create edges; local images not found',
            attribution='Custom lightweight adaptation inspired by semantic item graphs (FREEDOM/PinSage), NOT a reproduction of either paper'),
        replay='Original FP32 bound 32*eps*score_scale; all rank changes and AP differences quantified, canonical best-epoch scores retained; no target-based replay selection',
        reference_hashes=refs,sources=sources,
        limitation='One seed on reused checkpoint-selection validation; 5000 paired customer bootstrap, no multiple-comparison correction or independent confirmation')
    p=REP/'protocol.json'
    if p.exists():assert read(p)==value,'Changed protocol needs a new run ID'
    else:write(p,value)
    for name in sources:
        target=REP/'frozen_source'/name;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():assert sha(target)==sha(ROOT/name)
        else:shutil.copyfile(ROOT/name,target)
    for f in range(3):
        target=DEST/f'fold_{f}';target.mkdir(parents=True,exist_ok=True)
        for n in ['annotations.json','seen_mask.npy']:
            p=target/n
            if p.exists():assert sha(p)==sha(CONTROL/f'fold_{f}'/n)
            else:shutil.copyfile(CONTROL/f'fold_{f}'/n,p)
        if not (target/'control/result.json').exists():
            shutil.copytree(CONTROL/f'fold_{f}/control',target/'control')
            write(target/'control/reuse_lineage_item_encoder.json',dict(source=str((CONTROL/f'fold_{f}/control').relative_to(ROOT)),
                checkpoint_sha256=sha(target/'control/best.pt'),note='Verified original-loss FUSION control; not the auxiliary lambda1 variant'))
    return value


class GraphItemEmbedding(torch.nn.Module):
    def __init__(self,base,adjacency):
        super().__init__();self.base=base
        self.register_buffer('adjacency',adjacency,persistent=False)
        self._cached_rhs_embedding=None

    def forward(self,index=None):
        if not self.training and self._cached_rhs_embedding is not None:
            value=self._cached_rhs_embedding
        else:
            # Outer clear_rhs must also invalidate the original FUSION cache.
            self.base._cached_rhs_embedding=None
            raw=self.base()
            value=.5*raw+.5*torch.sparse.mm(self.adjacency,raw)
            if not self.training:self._cached_rhs_embedding=value
        return value if index is None else value[index]


def graph_smoke():
    class Toy(torch.nn.Module):
        def __init__(self):
            super().__init__();self.weight=torch.nn.Parameter(torch.tensor([[1.,0.],[0.,2.]]));self._cached_rhs_embedding=None
        def forward(self):return self.weight
    identity=torch.eye(2).to_sparse()
    base=Toy();wrapped=GraphItemEmbedding(base,identity)
    assert torch.equal(wrapped(),base())
    edge=torch.tensor([[0.,1.],[1.,0.]]).to_sparse()
    base=Toy();wrapped=GraphItemEmbedding(base,edge)
    value=wrapped();assert torch.equal(value,torch.tensor([[.5,1.],[.5,1.]]))
    value[0].sum().backward();assert (base.weight.grad[1]>0).all()
    wrapped.eval();wrapped();base.weight.data.add_(1);wrapped._cached_rhs_embedding=None
    assert torch.equal(wrapped(),torch.tensor([[1.5,2.],[1.5,2.]]))
    write(REP/'graph_smoke.json',dict(passed=True,checks=['identity adjacency preserves raw embedding','one-step propagation equals hand calculation','neighbor gradients flow','outer cache invalidation updates nested embedding']))


def build_graph():
    from scipy import sparse
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import OneHotEncoder,normalize
    from threadpoolctl import threadpool_limits
    for f in range(3):
        folder=DEST/f'fold_{f}/semantic_graph';folder.mkdir(parents=True,exist_ok=True)
        if (folder/'graph_audit.json').exists():
            a=read(folder/'graph_audit.json');assert sha(folder/'graph.npz')==a['graph_sha256'];continue
        article=pd.read_parquet(DATA/f'fold_{f}/db/article.parquet').sort_values('article_id').reset_index(drop=True)
        assert np.array_equal(article.article_id,np.arange(10000))
        assert all(c in article for c in GRAPH_COLUMNS+TEXT_COLUMNS)
        # Reuse an identical graph only after checking both source ordering and content.
        if f and sha(DATA/f'fold_{f}/db/article.parquet')==sha(DATA/'fold_0/db/article.parquet'):
            source=DEST/'fold_0/semantic_graph'
            shutil.copyfile(source/'graph.npz',folder/'graph.npz')
            audit=read(source/'graph_audit.json');audit.update(fold=f,reused_graph_from=0)
            write(folder/'graph_audit.json',audit);continue
        text=article[TEXT_COLUMNS].fillna('').astype(str).agg(' '.join,axis=1)
        vectorizer=TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=12000,sublinear_tf=True,dtype=np.float32)
        words=vectorizer.fit_transform(text)
        encoder=OneHotEncoder(handle_unknown='ignore',dtype=np.float32)
        attrs=normalize(encoder.fit_transform(article[GRAPH_COLUMNS].fillna(-1).astype(str)),norm='l2',copy=False)
        features=normalize(sparse.hstack([np.sqrt(.5)*words,np.sqrt(.5)*attrs],format='csr',dtype=np.float32),norm='l2',copy=False)
        edges=[];weights=[];rows=[]
        with threadpool_limits(limits=2):
            for start in range(0,10000,256):
                stop=min(start+256,10000)
                similarity=(features[start:stop]@features.T).toarray()
                similarity[np.arange(stop-start),np.arange(start,stop)]=-np.inf
                nearest=np.argsort(-similarity,axis=1,kind='stable')[:,:20]
                values=np.take_along_axis(similarity,nearest,axis=1)
                assert np.isfinite(values).all() and (values>=0).all()
                values/=values.sum(axis=1,keepdims=True)
                edges.append(nearest);weights.append(values);rows.append(np.repeat(np.arange(start,stop),20))
                if start%2048==0:print('GRAPH',f,start,flush=True)
        neighbors=np.concatenate(edges);values=np.concatenate(weights)
        assert not (neighbors==np.arange(10000)[:,None]).any()
        graph=sparse.csr_matrix((values.ravel(),(np.concatenate(rows),neighbors.ravel())),shape=(10000,10000))
        assert np.allclose(np.asarray(graph.sum(axis=1)).ravel(),1,atol=1e-6)
        sparse.save_npz(folder/'graph.npz',graph)
        audit=dict(fold=f,graph_sha256=sha(folder/'graph.npz'),article_sha256=sha(DATA/f'fold_{f}/db/article.parquet'),
            rows=10000,edges=graph.nnz,neighbors=20,no_self_edges=True,row_normalized=True,no_transactions_or_labels=True,
            text_nonempty=int(text.str.strip().ne('').sum()),vocabulary_size=len(vectorizer.vocabulary_),feature_dimensions=features.shape[1],
            categorical_columns=GRAPH_COLUMNS,text_columns=TEXT_COLUMNS,selection='Fixed before any graph model training')
        write(folder/'graph_audit.json',audit)
    record('item_encoder_graph_ready','Fixed top20 cosine item graphs built from catalog attributes and descriptions only; no transaction/target input, self edges excluded, row-normalization checked.',RUN,status='graph_ready',artifacts=str(DEST.relative_to(ROOT)))


def replay_check(saved,replay,targets):
    bound=32*np.finfo(np.float32).eps*max(1.,float(np.abs(saved).max()))
    difference=float(np.abs(saved-replay).max());assert difference<=bound
    a=np.argsort(-saved,axis=1,kind='stable')[:,:12];b=np.argsort(-replay,axis=1,kind='stable')[:,:12]
    changed=np.where(np.any(a!=b,axis=1))[0]
    for i in changed:
        assert saved[i,b[i]].min()>=saved[i,a[i,-1]]-2*bound
        assert np.all(np.diff(saved[i,b[i]])<=2*bound)
    ap_a=previous.base.aps(a,targets);ap_b=previous.base.aps(b,targets)
    return dict(max_score_difference=difference,bound=bound,changed_rows=changed.tolist(),changed_positions=int((a!=b).sum()),
        canonical_map=float(ap_a.mean()),replay_map=float(ap_b.mean()),max_per_user_ap_difference=float(np.abs(ap_a-ap_b).max()))


def install_training(arm,fold):
    previous.RUN,previous.DEST,previous.REP=RUN,DEST,REP
    previous.base.RUN,previous.base.DEST,previous.base.REP=RUN,DEST,REP
    original_setup=previous.base.setup
    def setup(*args,**kwargs):
        env=original_setup(*args,**kwargs);factory=env['make_model']
        def make_model(kind):
            model=factory(kind)
            before=previous.state_fingerprint(model)
            assert before==read(DEST/f'fold_{fold}/control/result.json')['initial_state_sha256']
            if arm=='feature':
                from contextgnn.utils import RHSEmbeddingMode
                assert model.rhs_embedding.lookup_embedding is not None
                model.rhs_embedding.lookup_embedding=None
                model.rhs_embedding.emb_mode=RHSEmbeddingMode.FEATURE
                assert not any('lookup_embedding' in n for n,_ in model.named_parameters())
            else:
                from scipy import sparse
                graph=sparse.load_npz(DEST/f'fold_{fold}/semantic_graph/graph.npz').tocoo()
                idx=torch.from_numpy(np.stack([graph.row,graph.col]).astype(np.int64)).to(env['device'])
                value=torch.from_numpy(graph.data).to(env['device'])
                adjacency=torch.sparse_coo_tensor(idx,value,graph.shape,device=env['device']).coalesce()
                model.rhs_embedding=GraphItemEmbedding(model.rhs_embedding,adjacency)
            model._fusion_initial_fingerprint=before
            return model
        env['make_model']=make_model;return env
    previous.base.setup=setup
    source=inspect.getsource(previous.fit)
    source=source.replace('initial_state=state_fingerprint(model)','initial_state=model._fusion_initial_fingerprint')
    source=source.replace("if arm=='global_ce':","if arm in ('feature','similarity_graph'):")
    source=source.replace("                assert torch.equal(hybrid.argsort(descending=True,stable=True)[:,:12],native.argsort(descending=True,stable=True)[:,:12])",
        "                native_check=replay_check(hybrid.cpu().numpy(),native.cpu().numpy(),[targets[int(i)] for i in batch[task.src_entity_table].input_id.cpu()])\n"
        "                native_checks.append(native_check)")
    source=source.replace('    @torch.no_grad()\n    def evaluate','    native_checks=[]\n    replay_checks={}\n    @torch.no_grad()\n    def evaluate')
    source=source.replace("        assert np.array_equal(np.argsort(-saved,axis=1,kind='stable')[:,:12],np.argsort(-value,axis=1,kind='stable')[:,:12])",
        "        replay_checks[key]=replay_check(saved,value,targets)\n        np.save(work/f'verification_replay_{key}_scores.npy',value)")
    source=source.replace('    historical_equal=None',"    write(work/'replay_verification.json',dict(native=native_checks,reload=replay_checks,canonical_scores_retained=True))\n    historical_equal=None")
    source=source.replace("verification='Native forward and reload within FP32 bound; exact top12; independent AP'",
        "verification='FP32-bounded native/reload scores; rank/AP sensitivity explicitly measured; independent canonical AP'")
    source=source.replace("'global_aux_","'item_encoder_")
    runtime=REP/'executed_refit.py'
    if runtime.exists():assert runtime.read_text(encoding='utf-8')==source
    else:runtime.write_text(source,encoding='utf-8')
    previous.replay_check=replay_check
    exec(compile(source,str(runtime),'exec'),previous.__dict__)


def fit(fold,arm):
    assert os.environ.get('PYTHONHASHSEED')=='42'
    install_training(arm,fold)
    previous.fit(fold,arm,0.)
    work=DEST/f'fold_{fold}'/arm
    result=read(work/'result.json');result.update(item_encoder_arm=arm,no_auxiliary_loss=True,
        executed_refit_sha256=sha(REP/'executed_refit.py'),common_initial_weights_identical_to_control=True,
        graph_sha256=sha(DEST/f'fold_{fold}/semantic_graph/graph.npz') if arm=='similarity_graph' else None,
        description='Remove only learned article-ID lookup; feature encoder and all common initial weights unchanged' if arm=='feature' else 'FUSION plus fixed semantic top20 graph, one residual propagation, alpha=.5')
    write(work/'result.json',result)


def report(arms,tag):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter
    rows=[]
    for f in range(3):
        ann=read(DEST/f'fold_{f}/annotations.json');mask=np.load(DEST/f'fold_{f}/seen_mask.npy')
        for arm in arms:
            folder=DEST/f'fold_{f}'/arm
            assert sha(folder/'best.pt')==read(folder/'result.json')['checkpoint_sha256']
            for mode in ['hybrid','global','new_only']:
                scores=np.load(folder/f"val_{'global' if mode=='global' else 'hybrid'}_scores.npy")
                if mode=='new_only':scores[mask]=-np.inf
                pred=np.argsort(-scores,axis=1,kind='stable')[:,:12]
                np.save(folder/f'val_{mode}_predictions.npy',pred)
                if mode=='new_only':assert not mask[np.arange(len(pred))[:,None],pred].any()
                for rec,a in zip(pred,ann):
                    for group,value in previous.novelty.per_user(rec,a).items():
                        rows.append(dict(fold=f,row=a['row'],customer=a['customer'],arm=arm,mode=mode,group=group,**value))
    users=pd.DataFrame(rows);users.to_parquet(REP/f'{tag}_per_user.parquet',index=False)
    summary=[]
    for (arm,mode,group),g in users.groupby(['arm','mode','group'],sort=False):
        eligible=g[g.targets>0];available=g[g.available>0]
        summary.append(dict(arm=arm,mode=mode,group=group,map=eligible['map'].mean(),recall=eligible.recall.mean(),
            available_recall=available.available_recall.mean(),observations=len(g),eligible=len(eligible),available_users=len(available),
            targets=int(g.targets.sum()),available_targets=int(g.available.sum()),ap_contribution=g.ap_contribution.mean()))
    table=pd.DataFrame(summary);table.to_csv(REP/f'{tag}_metrics.csv',index=False)
    users.groupby(['fold','arm','mode','group'])[['map','recall','available_recall']].mean().reset_index().to_csv(REP/f'{tag}_fold_metrics.csv',index=False)
    contrasts=[]
    for arm in arms[1:]:
        for mode,group,metric in [('hybrid','all','map'),('global','all','map'),('hybrid','new','available_recall'),('new_only','new','available_recall')]:
            s=users[(users['mode']==mode)&(users['group']==group)]
            a=s[s.arm==arm].sort_values(['fold','row']);b=s[s.arm=='control'].sort_values(['fold','row'])
            assert np.array_equal(a[['fold','row']],b[['fold','row']])
            valid=a[metric].notna().to_numpy();assert np.array_equal(valid,b[metric].notna())
            delta=a[metric].to_numpy()[valid]-b[metric].to_numpy()[valid]
            ids=a.customer.to_numpy()[valid];unique,inverse=np.unique(ids,return_inverse=True)
            counts=np.bincount(inverse);sums=np.bincount(inverse,weights=delta);rng=np.random.default_rng(42);boot=[]
            for _ in range(5000):
                ix=rng.integers(0,len(unique),len(unique));boot.append(sums[ix].sum()/counts[ix].sum())
            lo,hi=np.quantile(boot,[.025,.975]);contrasts.append(dict(arm=arm,mode=mode,group=group,metric=metric,
                delta=float(delta.mean()),low=float(lo),high=float(hi),observations=len(delta)))
    pd.DataFrame(contrasts).to_csv(REP/f'{tag}_contrasts.csv',index=False)
    lines=['# FEATURE / FUSION и семантический граф товаров','',
        'Три фолда, seed42, 768 validation-наблюдений. Исходный CE, без дополнительного global loss. '
        'Прежние проверенные FUSION-контроли переиспользованы. Общие начальные веса и обучающие графы совпадают; '
        'эпоха выбирается по обычному hybrid MAP, max10/patience3. Test не оценивался.','',
        '| Метрика | '+' | '.join(NAMES[a] for a in arms)+' |','|---|'+'---:|'*len(arms)]
    chart=[]
    for mode,group,metric in [('hybrid','all','map'),('global','all','map'),('hybrid','new','available_recall'),('new_only','new','available_recall')]:
        label=f'{mode}: {metric} ({group})';values=[]
        for arm in arms:
            value=float(table[(table.arm==arm)&(table['mode']==mode)&(table['group']==group)][metric].iloc[0]);values.append(value)
        chart.append((label,values));lines.append('| '+label+' | '+' | '.join(f'{100*x:.4f}%' for x in values)+' |')
    lines+=['','## Разности с FUSION и парные интервалы','',
        '| Вариант | Режим / метрика | Разница, п.п. | 95% интервал, п.п. |','|---|---|---:|---:|']
    for c in contrasts:lines.append(f"| {NAMES[c['arm']]} | {c['mode']} / {c['metric']} | {100*c['delta']:+.4f} | [{100*c['low']:+.4f}; {100*c['high']:+.4f}] |")
    lines+=['','Новые товары определены по полной доступной исходной истории до cutoff, '
        'входы модели не расширялись. Недоступные будущие цели сохранены в полных MAP/recall. '
        'Условный recall доступных новых рассчитан на одинаковых 493 наблюдениях. '
        'Всего 2477 целей / 1038 доступных, новых 2373 / 972 доступных.', '',
        'FEATURE удаляет только lookup ID-компоненту RHS. Локальный GNN encoder не меняется. '
        'Семантический граф использует только характеристики и описания фиксированного каталога '
        '(TFIDF + one-hot, cosine top20). Один шаг e=.5*e_FUSION+.5*P@e_FUSION обучается end-to-end, '
        'но сами рёбра зафиксированы. Изображения локально не найдены. Это наша адаптация идеи графа '
        'товаров, а не воспроизведение FREEDOM или PinSage.', '',
        'Исходные оценки лучших эпох сохраняются; FP32-перестановки при replay и их влияние на AP '
        'измеряются в replay_verification.json каждого fit. Лучший replay по целям не выбирается. '
        'Перезапуски/исторические результаты не подменяются.', '',
        'Интервалы: 5000 парных bootstrap по покупателям, без поправки за множество сравнений. '
        'Один seed и уже использованная validation; независимого подтверждения нет.', '',
        f'![Сравнение]({tag}_comparison.png)','']
    (REP/f'{tag}_report_ru.md').write_text('\n'.join(lines),encoding='utf-8')
    fig,ax=plt.subplots(figsize=(13,6));y=np.arange(len(chart));height=.75/len(arms)
    for i,arm in enumerate(arms):ax.barh(y+(i-(len(arms)-1)/2)*height,[100*x[1][i] for x in chart],height=height*.93,label=NAMES[arm])
    ax.set(yticks=y,yticklabels=[x[0] for x in chart],xlabel='Metric (%)',title='Item encoder ablation — validation only, seed42')
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=100));ax.legend();fig.tight_layout()
    fig.savefig(REP/f'{tag}_comparison.png',dpi=170);fig.savefig(REP/f'{tag}_comparison.svg');plt.close(fig)
    frozen=read(REP/'protocol.json')
    for p,h in {**frozen['reference_hashes'],**frozen['sources']}.items():assert sha(ROOT/p)==h
    write(REP/f'{tag}_summary.json',dict(status='pending_visual_review',validation_only=True,arms=arms,
        metrics=table.replace({np.nan:None}).to_dict('records'),contrasts=contrasts,reference_hashes_unchanged=True))
    record('item_encoder_report_ready',f'{tag}: validation tables, paired intervals and plot generated for {arms}; references unchanged. Awaiting visual review.',RUN,status='pending_visual_review',artifacts=str(REP.relative_to(ROOT)))


def main():
    import fcntl
    torch.set_num_threads(2);torch.set_num_interop_threads(2)
    os.nice(max(0,5-os.getpriority(os.PRIO_PROCESS,0)))
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['run','fit','graph','report'],default='run',nargs='?')
    p.add_argument('--fold',type=int);p.add_argument('--arm',choices=ARMS[1:]);args=p.parse_args()
    DEST.mkdir(parents=True,exist_ok=True);REP.mkdir(parents=True,exist_ok=True)
    if args.stage=='fit':fit(args.fold,args.arm);return
    if args.stage=='graph':build_graph();return
    if args.stage=='report':report(ARMS,'final');return
    with (DEST/'execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        freeze();graph_smoke()
        record('item_encoder_started','Authorized FEATURE/FUSION comparison followed by semantic item graph experiment. Reuse three verified original-loss FUSION controls; six new sequential fit subprocesses, two CPU threads, no API/test. Existing H010/H011 CPU diagnostics left untouched.',RUN,status='training',artifacts=str(REP.relative_to(ROOT)))
        for arm in ARMS[1:]:
            if arm=='similarity_graph':
                with (REP/'graph_build.log').open('a') as stream:
                    subprocess.run([sys.executable,'-u',str(Path(__file__)),'graph'],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True)
            for f in range(3):
                if (DEST/f'fold_{f}'/arm/'result.json').exists():continue
                print('FIT_START',f,arm,flush=True)
                with (REP/f'fold_{f}_{arm}.log').open('a') as stream:
                    subprocess.run([sys.executable,'-u',str(Path(__file__)),'fit','--fold',str(f),'--arm',arm],cwd=ROOT,
                        stdout=stream,stderr=subprocess.STDOUT,check=True,env={**os.environ,'PYTHONHASHSEED':'42'})
                print('FIT_DONE',f,arm,flush=True)
            report(['control','feature'] if arm=='feature' else ARMS,'feature' if arm=='feature' else 'final')


if __name__=='__main__':main()
