"""One saved pair sample shared by manual, raw and both GPT feature searches."""
import shutil
import sys
import numpy as np
import pandas as pd
from common import ROOT,paths,read,write,sha

def prepare(fold):
    data,out=paths(fold);bundle=data/'bundle'
    if (bundle/'manifest.json').exists():return bundle
    bundle.mkdir(exist_ok=True)
    for name in ['customer','article','transactions']:
        shutil.copyfile(data/f'db/{name}.parquet',bundle/f'{name}.parquet')
    targets=pd.read_parquet(data/'tasks/user-item-purchase/train.parquet')
    tx=pd.read_parquet(bundle/'transactions.parquet')
    rng=np.random.default_rng(2026);parts=[]
    for cutoff,group in targets.groupby('timestamp',sort=True):
        past=tx[tx.t_dat<=cutoff].sort_values('t_dat',kind='stable').groupby('customer_id',sort=False).tail(128)
        hist={int(u):set(g.article_id) for u,g in past.groupby('customer_id')}
        rows=[]
        for row in group.itertuples():
            pos=set(map(int,row.article_id));pool=np.asarray(sorted(hist.get(int(row.customer_id),set())-pos),dtype=np.int64)
            hard=rng.choice(pool,min(8,len(pool)),replace=False) if len(pool) else []
            neg=set(map(int,hard))
            while len(neg)<len(hard)+8:
                i=int(rng.integers(10000))
                if i not in pos:neg.add(i)
            rows.extend((row.customer_id,i,1,cutoff) for i in sorted(pos))
            rows.extend((row.customer_id,i,0,cutoff) for i in sorted(neg))
        parts.append(pd.DataFrame(rows,columns=['customer_id','article_id','label','timestamp']))
    pairs=pd.concat(parts,ignore_index=True)
    assert not pairs.duplicated(['timestamp','customer_id','article_id']).any()
    assert pairs.groupby(['timestamp','customer_id']).label.sum().gt(0).all()
    pairs.to_parquet(bundle/'train_pairs.parquet',index=False)
    for split in ['val','test']:shutil.copyfile(data/f'tasks/user-item-purchase/{split}_full.parquet',bundle/f'{split}_targets.parquet')
    shutil.copyfile(data/'selection.json',bundle/'selection.json')
    write(bundle/'manifest.json',{'fold':fold,'train_pairs':len(pairs),'train_user_times':len(targets),'catalog':10000,
          'files':{p.name:sha(p) for p in sorted(bundle.iterdir()) if p.is_file() and p.name!='manifest.json'}})
    print('fold',fold,'pairs',len(pairs),flush=True)
    return bundle

if __name__=='__main__':
    for k in range(3):prepare(k)
