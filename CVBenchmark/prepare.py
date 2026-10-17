"""Create fixed past-selected medium cohort and three non-overlapping test weeks."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import duckdb
import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record
SOURCE=ROOT/'data/rel-hm'
OUT=ROOT/'data/hm-cv-medium-v1'
RUN='hm_medium_temporal_cv_v1'

def sha(p):
    with Path(p).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()

def write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def main():
    if (OUT/'manifest.json').exists():
        print((OUT/'manifest.json').read_text(),flush=True); return
    OUT.mkdir(parents=True,exist_ok=True)
    record('medium_cv_prepare','Preparing larger fixed past-only cohort and temporal CV; no model fitting yet.',RUN,status='preparing',artifacts='CVBenchmark/PROTOCOL.md')
    con=duckdb.connect();con.execute("SET threads=4");con.execute("SET memory_limit='2GB'")
    anchor=pd.Timestamp('2020-06-29'); txpath=str(SOURCE/'db/transactions.parquet')
    old=pd.read_csv(ROOT/'data/rel-hm-small-v1/customer_id_map.csv')
    con.register('old',old)
    eligible=con.execute('''SELECT DISTINCT customer_id FROM read_parquet(?)
        WHERE t_dat > ? AND t_dat <= ? AND customer_id NOT IN(SELECT original_customer_id FROM old)
        ORDER BY customer_id''',[txpath,anchor-pd.Timedelta(days=90),anchor]).fetchnumpy()['customer_id']
    users=np.sort(np.random.default_rng(42).choice(eligible,20000,replace=False))
    umap=pd.DataFrame({'original_customer_id':users,'customer_id':np.arange(len(users),dtype=np.int64)})
    con.register('users',umap)
    imap=con.execute('''SELECT article_id AS original_article_id,count(*) AS historical_count
        FROM read_parquet(?) t JOIN users u ON t.customer_id=u.original_customer_id
        WHERE t_dat > ? AND t_dat <= ? GROUP BY article_id
        ORDER BY historical_count DESC,original_article_id LIMIT 10000''',[txpath,anchor-pd.Timedelta(days=180),anchor]).fetchdf()
    imap=imap.sort_values('original_article_id').reset_index(drop=True)
    assert len(imap)==10000
    imap['article_id']=np.arange(len(imap),dtype=np.int64);con.register('items',imap)
    tx=con.execute('''SELECT t.* EXCLUDE(customer_id,article_id),u.customer_id,i.article_id
        FROM read_parquet(?) t JOIN users u ON t.customer_id=u.original_customer_id
        JOIN items i ON t.article_id=i.original_article_id
        WHERE t_dat >= ? AND t_dat <= ? ORDER BY t_dat,u.customer_id,i.article_id''',
        [txpath,anchor-pd.Timedelta(days=180),pd.Timestamp('2020-09-21')]).fetchdf()
    shared=OUT/'shared';shared.mkdir(exist_ok=True)
    tx.to_parquet(shared/'transactions.parquet',index=False)
    for table,ids,key in [('customer',users,'customer_id'),('article',imap.original_article_id.to_numpy(),'article_id')]:
        frame=pd.read_parquet(SOURCE/f'db/{table}.parquet',filters=[(key,'in',ids.tolist())]).sort_values(key).reset_index(drop=True)
        assert np.array_equal(frame[key],ids)
        frame[key]=np.arange(len(frame),dtype=np.int64)
        frame.to_parquet(shared/f'{table}.parquet',index=False)
    umap.to_csv(OUT/'customer_id_map.csv',index=False);imap.to_csv(OUT/'article_id_map.csv',index=False)
    con.register('tx',tx)
    folds=[]
    for fold,test in enumerate(pd.to_datetime(['2020-08-17','2020-08-31','2020-09-14'])):
        dest=OUT/f'fold_{fold}';db=dest/'db';task=dest/'tasks/user-item-purchase'
        db.mkdir(parents=True,exist_ok=True);task.mkdir(parents=True,exist_ok=True)
        for name in ['customer','article','transactions']:
            shutil.copyfile(shared/f'{name}.parquet',db/f'{name}.parquet')
        for name in ['customer_id_map.csv','article_id_map.csv']:shutil.copyfile(OUT/name,dest/name)
        val=test-pd.Timedelta(days=7)
        train=list(pd.date_range(end=val-pd.Timedelta(days=7),periods=6,freq='7D'))
        assert train[0]>=anchor and train[-1]+pd.Timedelta(days=7)==val
        stats={}
        for split,times in [('train',train),('val',[val]),('test',[test])]:
            frames=[]
            for cutoff in times:
                f=con.execute('''SELECT customer_id,list(DISTINCT article_id ORDER BY article_id) AS article_id
                    FROM tx WHERE t_dat > ? AND t_dat <= ? GROUP BY customer_id ORDER BY customer_id''',
                    [cutoff,cutoff+pd.Timedelta(days=7)]).fetchdf()
                f.insert(0,'timestamp',cutoff);frames.append(f)
            f=pd.concat(frames,ignore_index=True)
            f.to_parquet(task/f'{split}.parquet',index=False)
            raw=con.execute('''SELECT count(DISTINCT customer_id) AS users,count(*) AS transactions FROM read_parquet(?)
                WHERE customer_id IN(SELECT original_customer_id FROM users) AND t_dat > ? AND t_dat <= ?''',
                [txpath,min(times),max(times)+pd.Timedelta(days=7)]).fetchone()
            # Coverage counts DISTINCT weekly labels, rather than transaction repeats.
            total=0;source_rows=0
            for cutoff in times:
                row=con.execute('''SELECT count(*) FROM(SELECT DISTINCT customer_id,article_id FROM read_parquet(?)
                    WHERE customer_id IN(SELECT original_customer_id FROM users) AND t_dat > ? AND t_dat <= ?)''',
                    [txpath,cutoff,cutoff+pd.Timedelta(days=7)]).fetchone()[0]
                source_rows+=con.execute('''SELECT count(DISTINCT customer_id) FROM read_parquet(?)
                    WHERE customer_id IN(SELECT original_customer_id FROM users) AND t_dat > ? AND t_dat <= ?''',
                    [txpath,cutoff,cutoff+pd.Timedelta(days=7)]).fetchone()[0]
                total+=row
            retained=int(f.article_id.map(len).sum())
            stats[split]={'rows':len(f),'positive_items':retained,'source_positive_items':total,
                          'positive_coverage':retained/total,'dropped_empty_user_times':source_rows-len(f),
                          'cutoffs':list(map(str,times))}
        meta=yaml.safe_load((SOURCE/'manifest.yaml').read_text())
        meta.update(name=f'hm-medium-cv-fold{fold}-v1',val_timestamp=str(val.date()),test_timestamp=str(test.date()))
        (dest/'manifest.yaml').write_text(yaml.safe_dump(meta,sort_keys=False))
        shutil.copyfile(SOURCE/'tasks/user-item-purchase/manifest.yaml',task/'manifest.yaml')
        files={str(p.relative_to(dest)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(dest.rglob('*')) if p.is_file()}
        summary={'fold':fold,'seed':42,'users':len(users),'items':len(imap),'transactions':len(tx),
                 'selection_cutoff':str(anchor),'selection_uses_outer_labels':False,'splits':stats,'files':files}
        write(dest/'subset_manifest.json',summary);folds.append(summary)
        print('fold',fold,json.dumps(stats),flush=True)
    summary={'protocol':'hm_medium_temporal_cv_v1','users':len(users),'items':len(imap),
             'transactions':len(tx),'old_cohort_overlap':int(np.isin(users,old.original_customer_id).sum()),
             'selection_cutoff':str(anchor),'folds':folds,'protocol_sha256':sha(ROOT/'CVBenchmark/PROTOCOL.md')}
    assert summary['old_cohort_overlap']==0
    write(OUT/'manifest.json',summary)
    write(ROOT/'reports/medium_cv_v1/dataset_summary.json',summary)
    record('medium_cv_dataset_ready','Larger fixed cohort and three temporal folds saved; originals unchanged.',RUN,status='data_ready',users=len(users),items=len(imap),fold_rows=[{s:f['splits'][s]['rows'] for s in ['train','val','test']} for f in folds],artifacts='reports/medium_cv_v1')

if __name__=='__main__':main()
