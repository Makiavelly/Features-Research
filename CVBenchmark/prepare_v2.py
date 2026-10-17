"""Preserve all future targets/users when evaluating the restricted catalog."""
from pathlib import Path
import json
import shutil
import sys
import duckdb
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'RelBenchGNN'))
from tracking import record
from prepare import ROOT,sha,write

OUT=ROOT/'data/hm-cv-medium-v2'
REPORT=ROOT/'reports/medium_cv_v2'

def main():
    if (OUT/'manifest.json').exists():return
    previous=ROOT/'data/hm-cv-medium-v1'
    base=json.loads((previous/'manifest.json').read_text())
    users=pd.read_csv(previous/'customer_id_map.csv')
    items=pd.read_csv(previous/'article_id_map.csv')
    lookup=dict(zip(items.original_article_id,items.article_id))
    con=duckdb.connect();con.execute('SET threads=4');con.register('users',users)
    folds=[]
    for k in range(3):
        dest=OUT/f'fold_{k}'
        if dest.exists():raise RuntimeError('Partial preparation exists; inspect before resuming')
        shutil.copytree(previous/f'fold_{k}',dest)
        meta=json.loads((dest/'subset_manifest.json').read_text())
        task=dest/'tasks/user-item-purchase'
        for split in ['val','test']:
            cutoff=pd.Timestamp(meta['splits'][split]['cutoffs'][0])
            f=con.execute('''SELECT u.customer_id,list(DISTINCT t.article_id ORDER BY t.article_id) AS article_id
                FROM read_parquet(?) t JOIN users u ON t.customer_id=u.original_customer_id
                WHERE t_dat > ? AND t_dat <= ? GROUP BY u.customer_id ORDER BY u.customer_id''',
                [str(ROOT/'data/rel-hm/db/transactions.parquet'),cutoff,cutoff+pd.Timedelta(days=7)]).fetchdf()
            # Unretrievable targets get stable IDs above the candidate catalog;
            # they cannot collide with predictions and remain in AP denominators.
            f['article_id']=f.article_id.map(lambda a:np.asarray(sorted(lookup.get(int(i),10000+int(i)) for i in a),dtype=np.int64))
            f.insert(0,'timestamp',cutoff)
            f.to_parquet(task/f'{split}_full.parquet',index=False)
            rng=np.random.default_rng(42)
            order=rng.permutation(len(f));n=min(256,int(.6*len(f)));m=int(.2*len(f))
            if split=='val':
                selection={'search':sorted(order[:n].tolist()),'confirm':sorted(order[int(.6*len(f)):int(.6*len(f))+m].tolist()),
                           'heldout_val':sorted(order[int(.6*len(f))+m:].tolist())}
                assert not(set(selection['search'])&set(selection['confirm']))
                f.iloc[selection['search']].reset_index(drop=True).to_parquet(task/'val.parquet',index=False)
                write(dest/'selection.json',selection)
            else:f.to_parquet(task/'test.parquet',index=False)
            meta['splits'][split]['all_source_user_times']=len(f)
            meta['splits'][split]['all_source_positive_items']=int(f.article_id.map(len).sum())
            meta['splits'][split]['zero_retrievable_targets']=int(f.article_id.map(lambda a:np.sum(a<10000)==0).sum())
        meta['protocol']='hm_medium_temporal_cv_v2'
        meta['evaluation']='all source users and original weekly positives; unretained positives remain in denominators'
        meta['files']={str(p.relative_to(dest)):{'sha256':sha(p),'bytes':p.stat().st_size}
                       for p in sorted(dest.rglob('*')) if p.is_file() and p.name!='subset_manifest.json'}
        write(dest/'subset_manifest.json',meta);folds.append(meta)
    base.update(protocol='hm_medium_temporal_cv_v2',folds=folds,primary_metric='unconditional full-target MAP@12',
                selection_metric='same full-target MAP on disjoint inner users',
                protocol_sha256=sha(ROOT/'CVBenchmark/PROTOCOL.md'))
    write(OUT/'manifest.json',base);write(REPORT/'dataset_summary.json',base)
    record('medium_cv_v2_data','Retained all outer users and all original positive labels in metric denominators; no future targets used for catalog selection.',
           'hm_medium_temporal_cv_v2',status='data_ready',test_user_times=[f['splits']['test']['all_source_user_times'] for f in folds],artifacts='reports/medium_cv_v2')
    print('Prepared v2:',[f['splits']['test']['all_source_user_times'] for f in folds],flush=True)

if __name__=='__main__':main()
