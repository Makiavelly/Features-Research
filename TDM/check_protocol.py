"""Behavioral checks and separate CUDA smoke; never reported as full metrics."""
import copy
import json
import time
import numpy as np
import torch
from torch.nn import functional as F
from common import (ROOT,CONFIG,WINDOWS,Dataset,TDM,seed,build_tree,validate_tree,
                    history_at,mapped_history,sample_pairs,evaluate,dump,record,pair_ranges)

def main():
    seed()
    dataset=Dataset()
    assert torch.cuda.is_available()
    device=torch.device('cuda')
    dates=np.array(['2020-01-01','2020-01-02','2020-01-03'],dtype='datetime64[ns]')
    assert np.array_equal(history_at(dates,np.array([0,1,999]),'2020-01-02'),[1,0])
    assert np.array_equal(history_at(dates[:2],np.array([0,1]),'2020-01-02'),[1,0])
    for n in [3,7,17,5000]: validate_tree(build_tree(n,categories=np.arange(n)%3))
    cluster=build_tree(17,embeddings=np.random.default_rng(42).normal(size=(17,24)))
    validate_tree(cluster)
    tree=build_tree(5000,categories=dataset.article.product_type_no.to_numpy())
    before=dataset.history['train'].copy()
    mapped=mapped_history(before,tree)
    assert np.all(mapped[before<0]==0)
    assert np.all(mapped[before==0]==tree['leaves'][0])
    idx=np.arange(8)
    rows,nodes,labels,weights=sample_pairs(dataset.targets['train'],idx,tree,np.random.default_rng(42))
    assert np.isclose(weights.sum(),1.)
    for local in range(8):
        positive_union=np.unique(tree['paths'][dataset.targets['train'][local]])
        assert not np.isin(nodes[(rows==local)&(labels==0)],positive_union).any()
        assert np.array_equal(np.sort(nodes[(rows==local)&(labels==1)]),positive_union)
        assert np.isclose(weights[rows==local].sum(),1/8)
    model=TDM(tree).to(device)
    model.eval()
    h=torch.as_tensor(mapped[:4],device=device)
    q=torch.as_tensor(tree['leaves'][:4],device=device)
    with torch.no_grad():
        together=model(h,q)
        separately=torch.cat([model(h[i:i+1],q[i:i+1]) for i in range(4)])
        assert torch.allclose(together,separately,atol=1e-6,rtol=1e-6)
        # Compare local pooling against the upstream pad/segment_reduce formula.
        seq=model.embedding(h); query=model.embedding(q)
        qs=query[:,None].expand_as(seq)
        attention=model.attention(torch.cat([seq,seq*qs,qs],-1))
        attended=seq*attention*h.ne(0)[:,:,None]
        reduced=torch.segment_reduce(attended.transpose(0,1),reduce='sum',lengths=torch.tensor(WINDOWS,device=device),axis=0).transpose(0,1)
        counts=torch.minimum(h.ne(0).sum(1)[:,None]-torch.tensor(np.cumsum([0]+WINDOWS[:-1]),device=device),torch.tensor(WINDOWS,device=device)).clamp_min(1)
        expected=model.mlp(torch.cat([reduced/counts[:,:,None],query[:,None]],1).reshape(4,-1)).squeeze(-1)
        assert torch.allclose(together,expected,atol=1e-6,rtol=1e-6)
    # Expand beam to the entire tree: retrieval must recover exhaustive leaf top12.
    tiny=copy.copy(dataset)
    tiny.tables=dict(dataset.tables)
    tiny.tables['val']=copy.copy(dataset.tables['val'])
    tiny.tables['val'].df=dataset.tables['val'].df.iloc[:2].copy()
    tiny.history=dict(dataset.history);tiny.history['val']=dataset.history['val'][:2]
    tiny.targets=dict(dataset.targets);tiny.targets['val']=dataset.targets['val'][:2]
    old=CONFIG['beam']; CONFIG['beam']=8192
    _,full=evaluate(model,tree,tiny,'val','full',device)
    _,beam=evaluate(model,tree,tiny,'val','beam',device)
    assert np.array_equal(full['predictions'],beam['predictions'])
    CONFIG['beam']=old
    # Force score ties: both exhaustive and all-branches search use article ID.
    with torch.no_grad():
        for p in model.parameters(): p.zero_()
    CONFIG['beam']=8192
    _,tied=evaluate(model,tree,tiny,'val','beam',device)
    assert np.array_equal(tied['predictions'],np.tile(np.arange(12),(2,1)))
    CONFIG['beam']=old
    seed();model=TDM(tree).to(device);model.train()
    torch.cuda.reset_peak_memory_stats()
    optimizer=torch.optim.Adam(model.parameters(),lr=CONFIG['lr'])
    started=time.perf_counter()
    optimizer.zero_grad(set_to_none=True)
    for off,stop in pair_ranges(len(nodes)):
        logits=model(torch.as_tensor(mapped[rows[off:stop]],device=device),torch.as_tensor(nodes[off:stop],device=device))
        loss=(F.binary_cross_entropy_with_logits(logits,torch.as_tensor(labels[off:stop],device=device),reduction='none')*torch.as_tensor(weights[off:stop],device=device)).sum()
        loss.backward()
    optimizer.step()
    torch.cuda.synchronize()
    result=dict(passed=True,scope='behavioral checks and separate one-update CUDA smoke; no experiment metrics',
                torch=torch.__version__,cuda=torch.cuda.is_available(),
                smoke8user_update_seconds=time.perf_counter()-started,peak_cuda_bytes=torch.cuda.max_memory_allocated(),
                checks=['all10dataSHA','tree_reachability_nonpower2','future_invariance','item0_padding',
                        'multi_positive_negative_exclusion','equal_user_mass','upstream_pooling_parity',
                        'eval_batch_invariance','exhaustive_beam_matches_full','article_id_ties','cuda_backward'])
    dump(ROOT/'reports/tdm_small_v1/smoke/verification.json',result)
    print(json.dumps(result),flush=True)
    record('tdm_smoke','TDM behavioral checks and isolated CUDA smoke passed', 'hm_tdm_small_smoke_v1',status='smoke_complete',checks=result)

if __name__=='__main__': main()
