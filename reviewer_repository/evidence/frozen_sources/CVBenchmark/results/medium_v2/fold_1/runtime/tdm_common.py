"""Local weekly TDM adaptation. See PROTOCOL_SMALL.md for provenance/deviations."""
import hashlib
import json
import math
from pathlib import Path
import random
import sys
import time

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.nn import functional as F
from sklearn.cluster import KMeans

ROOT = Path('/mnt/c/Users/Мишаня/ml/projs/tbank/Features')
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record
from relbench import load_dataset

DATA = Path('/mnt/c/Users/Мишаня/ml/projs/tbank/Features/data/hm-cv-medium-v2/fold_1')
OUT = Path('/mnt/c/Users/Мишаня/ml/projs/tbank/Features/CVBenchmark/results/medium_v2/fold_1/tdm')
WINDOWS = [1, 1, 1, 2, 2, 2, 5, 6, 10, 20]
CONFIG = dict(seed=42, embedding_dim=24, windows=WINDOWS, hidden=[128,64,24],
              attention_hidden=36, batch=32, pair_chunk=512, max_epochs=20,
              patience=4, minimum_epochs=5, max_training_seconds=1800,
              lr=.001, negatives_per_level=8, beam=64, history_length=50,
              precision='FP32', objective='equal-user equal-level balanced multi-positive BCE',
              tree_selection='best beam64 validation MAP; strict improvement',
              upstream_reference='TorchEasyRec 4458f1c66f6c32dc672b9c805855f3d2e6e6179e',
              implementation='local adaptation; no upstream framework installed')

def dump(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def seed():
    random.seed(42)
    np.random.seed(42)
    torch.manual_seed(42)
    torch.cuda.manual_seed_all(42)
    torch.set_num_threads(4)
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False

def history_at(dates, items, cutoff):
    n = np.searchsorted(dates, np.datetime64(cutoff), side='right')
    return items[max(0,n-50):n][::-1].copy()

class Dataset:
    def __init__(self):
        manifest=json.loads((DATA/'subset_manifest.json').read_text(encoding='utf-8'))
        self.hashes={}
        for name, info in manifest['files'].items():
            self.hashes[name]=sha(DATA/name)
            assert self.hashes[name]==info['sha256'],name
        assert len(self.hashes)>=10
        self.task=load_dataset(DATA).load_task('user-item-purchase')
        self.tables={s:self.task.get_table(s,mask_input_cols=False) for s in ['train','val','test']}
        assert all(len(self.tables[s].df)>0 for s in self.tables)
        self.article=pd.read_parquet(DATA/'db/article.parquet').sort_values('article_id')
        assert np.array_equal(self.article.article_id,np.arange(10000))
        tx=pd.read_parquet(DATA/'db/transactions.parquet')
        tx['source_order']=np.arange(len(tx))
        tx=tx.sort_values(['customer_id','t_dat','source_order'],kind='stable')
        groups={int(u):(g.t_dat.to_numpy(),g.article_id.to_numpy()) for u,g in tx.groupby('customer_id',sort=False)}
        self.history={}
        self.targets={}
        for split,table in self.tables.items():
            hist=np.full((len(table.df),50),-1,dtype=np.int64)
            for i,row in enumerate(table.df.itertuples()):
                if int(row.customer_id) in groups:
                    dates,items=groups[int(row.customer_id)]
                    h=history_at(dates,items,row.timestamp)
                    hist[i,:len(h)]=h
            self.history[split]=hist
            self.targets[split]=[np.unique(x).astype(np.int64) for x in table.df.article_id]
        # Train positives are the only labels accessed by all training/tree builders.
        self.train_seen=np.unique(np.concatenate(self.targets['train']))
        self.fingerprint=sha(DATA/'subset_manifest.json')

def build_tree(n_items, categories=None, embeddings=None):
    depth=math.ceil(math.log2(n_items))
    size=2**(depth+1)
    leaves=np.zeros(n_items,dtype=np.int64)
    rng=np.random.default_rng(42)
    order=np.arange(n_items)
    if categories is not None:
        order=np.concatenate([rng.permutation(np.flatnonzero(categories==c))
                              for c in rng.permutation(np.unique(categories))])
    def divide(items,node):
        if len(items)==1:
            while node<2**depth:
                node*=2
            leaves[items[0]]=node
            return
        half=len(items)//2
        if embeddings is not None and len(items)>2:
            x=embeddings[items].astype(np.float64)
            km=KMeans(2,random_state=42,n_init=10).fit(x)
            dist=km.transform(x)
            items=items[np.lexsort((items,dist[:,0]-dist[:,1]))]
        divide(items[:half],node*2)
        divide(items[half:],node*2+1)
    divide(order,1)
    valid=np.zeros(size,dtype=bool)
    paths=np.empty((n_items,depth),dtype=np.int64)
    for item,node in enumerate(leaves):
        for lev in range(depth-1,-1,-1):
            paths[item,lev]=node
            valid[node]=True
            node//=2
    valid[1]=True
    node_to_item=np.full(size,-1,dtype=np.int64)
    node_to_item[leaves]=np.arange(n_items)
    tree=dict(leaves=leaves,paths=paths,valid=valid,node_to_item=node_to_item)
    validate_tree(tree)
    return tree

def validate_tree(tree):
    leaves,paths,valid=tree['leaves'],tree['paths'],tree['valid']
    assert len(np.unique(leaves))==len(leaves)
    assert np.all(leaves>0) and not valid[0]
    assert np.all(paths[:,1:]//2==paths[:,:-1])
    assert np.array_equal(paths[:,-1],leaves)
    assert np.all(valid[paths]) and np.all(paths[:,0]//2==1)
    assert np.array_equal(tree['node_to_item'][leaves],np.arange(len(leaves)))

def tree_digest(tree):
    h=hashlib.sha256()
    for k in sorted(tree):
        h.update(k.encode()); h.update(tree[k].tobytes())
    return h.hexdigest()

class TDM(nn.Module):
    def __init__(self, tree):
        super().__init__()
        self.embedding=nn.Embedding(len(tree['valid']),24,padding_idx=0)
        nn.init.normal_(self.embedding.weight,0,.01)
        with torch.no_grad(): self.embedding.weight[0].zero_()
        self.attention=nn.Sequential(nn.Linear(72,36),nn.PReLU(),nn.Linear(36,1),nn.PReLU())
        layers=[]
        dim=24*(len(WINDOWS)+1)
        for width in CONFIG['hidden']:
            layers += [nn.Linear(dim,width),nn.BatchNorm1d(width),nn.PReLU()]
            dim=width
        self.mlp=nn.Sequential(*layers,nn.Linear(dim,1))

    def forward(self, history_nodes, query_nodes):
        sequence=self.embedding(history_nodes)
        query=self.embedding(query_nodes)
        queries=query[:,None,:].expand_as(sequence)
        weight=self.attention(torch.cat([sequence,sequence*queries,queries],-1))
        mask=history_nodes.ne(0)
        attended=sequence*weight*mask[:,:,None]
        pools=[]
        start=0
        for count in WINDOWS:
            end=start+count
            pools.append(attended[:,start:end].sum(1)/mask[:,start:end].sum(1).clamp_min(1)[:,None])
            start=end
        return self.mlp(torch.cat([*pools,query],-1)).squeeze(-1)

def mapped_history(history,tree):
    return np.where(history>=0,tree['leaves'][np.maximum(history,0)],0)

def pair_ranges(count):
    start=0
    while start<count:
        end=min(start+CONFIG['pair_chunk'],count)
        if count-end==1: end=count  # BatchNorm needs at least two training pairs.
        yield start,end
        start=end

def sample_pairs(targets,indices,tree,rng):
    rows=[]; nodes=[]; labels=[]; weights=[]
    depth=tree['paths'].shape[1]
    for local,idx in enumerate(indices):
        for level in range(depth):
            positives=np.unique(tree['paths'][targets[int(idx)],level])
            lo,hi=2**(level+1),2**(level+2)
            pool=np.flatnonzero(tree['valid'][lo:hi])+lo
            pool=pool[~np.isin(pool,positives)]
            negative=rng.choice(pool,min(CONFIG['negatives_per_level'],len(pool)),replace=False)
            positive_mass=.5 if len(negative) else 1.
            factor=1/(len(indices)*depth)
            rows.extend([local]*(len(positives)+len(negative)))
            nodes.extend([*positives,*negative])
            labels.extend([1.]*len(positives)+[0.]*len(negative))
            weights.extend([positive_mass*factor/len(positives)]*len(positives))
            if len(negative): weights.extend([.5*factor/len(negative)]*len(negative))
    return np.array(rows),np.array(nodes),np.array(labels,dtype=np.float32),np.array(weights,dtype=np.float32)

def ap_per_user(pred,targets):
    values=[]
    for row,true in zip(pred,targets):
        hit=np.isin(row,true)
        values.append((hit*np.cumsum(hit)/np.arange(1,13)).sum()/min(12,len(true)))
    return np.asarray(values)

@torch.no_grad()
def score_nodes(model,hist,nodes,device):
    result=[]
    for offset in range(0,len(nodes),CONFIG['pair_chunk']):
        q=nodes[offset:offset+CONFIG['pair_chunk']]
        h=np.broadcast_to(hist,(len(q),50)).copy()
        result.append(model(torch.as_tensor(h,device=device),torch.as_tensor(q,device=device)).cpu().numpy())
    return np.concatenate(result) if result else np.empty(0,dtype=np.float32)

@torch.no_grad()
def evaluate(model,tree,dataset,split,mode,device):
    model.eval()
    histories=mapped_history(dataset.history[split],tree)
    predictions=[]; scores_out=[]; trace_nodes=[]; trace_scores=[]; counts=[]
    torch.cuda.synchronize()
    start=time.perf_counter()
    for hist in histories:
        if mode=='full':
            nodes=tree['leaves']
            scores=score_nodes(model,hist,nodes,device)
            pred=np.lexsort((np.arange(len(nodes)),-scores))[:12]
            scores_out.append(scores)
            counts.append(len(nodes))
        else:
            frontier=np.array([1],dtype=np.int64)
            visit=[]; values=[]
            for level in range(tree['paths'].shape[1]):
                nodes=np.sort(np.concatenate([frontier*2,frontier*2+1]))
                nodes=nodes[tree['valid'][nodes]]
                scores=score_nodes(model,hist,nodes,device)
                visit.extend(nodes); values.extend(scores)
                tie=tree['node_to_item'][nodes] if level==tree['paths'].shape[1]-1 else nodes
                order=np.lexsort((tie,-scores))
                frontier=nodes[order[:CONFIG['beam']]]
            pred=tree['node_to_item'][nodes[order[:12]]]
            scores_out.append(scores[order[:12]])
            trace_nodes.append(np.asarray(visit,dtype=np.int64))
            trace_scores.append(np.asarray(values,dtype=np.float32))
            counts.append(len(visit))
        assert len(pred)==12 and len(np.unique(pred))==12 and np.all((pred>=0)&(pred<10000))
        predictions.append(pred)
    torch.cuda.synchronize()
    seconds=time.perf_counter()-start
    pred=np.asarray(predictions)
    ap=ap_per_user(pred,dataset.targets[split])
    metric=dataset.task.evaluate(pred,dataset.tables[split])
    assert abs(metric['map']-ap.mean())<1e-12
    result=dict(map=float(ap.mean()),seconds=seconds,mean_scored_nodes=float(np.mean(counts)),
                min_scored_nodes=int(min(counts)),max_scored_nodes=int(max(counts)),
                unique_recommended_items=int(len(np.unique(pred))),
                unseen_target_fraction=float(np.mean([not x in dataset.train_seen for a in dataset.targets[split] for x in a])))
    arrays=dict(predictions=pred,scores=np.asarray(scores_out),ap_per_user=ap,
                user_ids=dataset.tables[split].df.customer_id.to_numpy(),
                timestamps=dataset.tables[split].df.timestamp.astype('int64').to_numpy())
    if mode=='beam':
        offsets=np.cumsum([0]+[len(x) for x in trace_nodes])
        arrays.update(trace_nodes=np.concatenate(trace_nodes),trace_scores=np.concatenate(trace_scores),trace_offsets=offsets)
    return result,arrays
