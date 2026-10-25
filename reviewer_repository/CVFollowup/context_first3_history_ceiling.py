"""Coverage ceiling from all of each root customer's observable purchases."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from common import ROOT, DATA, write

sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from relbench import load_dataset
from time_units import unix_seconds

def run():
    output={}
    for fold in range(3):
        ds=load_dataset(DATA/f'fold_{fold}')
        task=ds.load_task('user-item-purchase')
        db=ds.get_db()
        tx=db.table_dict['transactions'].df
        n=len(db.table_dict['article'].df)
        histories={}
        for customer,group in tx.groupby('customer_id',sort=False):
            order=np.argsort(unix_seconds(group.t_dat),kind='stable')
            histories[int(customer)]=(unix_seconds(group.t_dat)[order],group.article_id.to_numpy()[order])
        output[str(fold)]={}
        for split in ['train','val']:
            table=task.get_table(split).df
            times=unix_seconds(table.timestamp)
            total=eligible=covered=0
            for i,row in enumerate(table.itertuples(index=False)):
                customer=int(getattr(row,task.src_entity_col))
                truth=set(map(int,getattr(row,task.dst_entity_col)))
                in_catalog={x for x in truth if 0<=x<n}
                history_times,articles=histories.get(customer,(np.array([]),np.array([])))
                stop=np.searchsorted(history_times,times[i],side='right')
                seen=set(map(int,articles[:stop]))
                total+=len(truth)
                eligible+=len(in_catalog)
                covered+=len(in_catalog & seen)
            output[str(fold)][split]=dict(users=len(table),positives=total,in_catalog=eligible,
                covered_by_all_own_history=covered,fraction_in_catalog=covered/max(1,eligible))
    path=ROOT/'reports/medium_followup_v1/context_first3_v1/all_history_coverage.json'
    write(path,output)
    print(path,output,flush=True)

if __name__=='__main__':
    run()
