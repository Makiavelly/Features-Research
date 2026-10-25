"""Audit actual dataset time resolutions against UTC epoch seconds."""
import sys
import pandas as pd
from common import ROOT,REPORT,write
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from relbench import load_dataset
from relbench.modeling.utils import to_unix_time

rows=[]
for name,path in [('small',ROOT/'data/rel-hm-small-v1'),*[(f'fold_{f}',ROOT/f'data/hm-cv-medium-v2/fold_{f}') for f in range(3)]]:
    dataset=load_dataset(path);db=dataset.get_db();task=dataset.load_task('user-item-purchase')
    tx=db.table_dict['transactions'].df
    for split in ['train','val','test']:
        table=task.get_table(split).df
        original=table.timestamp.iloc[0]
        legacy=int(table.timestamp.astype('int64').iloc[0]//1_000_000_000)
        expected=int(pd.Timestamp(original).timestamp())
        times=to_unix_time(tx.t_dat)
        rows.append({'case':name,'split':split,'task_dtype':str(table.timestamp.dtype),
             'transaction_dtype':str(tx.t_dat.dtype),'cutoff':str(original),
             'current_loader_input_seconds':legacy,'expected_input_seconds':expected,
             'graph_transaction_min':int(times.min()),'graph_transaction_max':int(times.max()),
             'visible_transactions_with_current_input':int((times<=legacy).sum()),
             'visible_transactions_with_correct_input':int((times<=expected).sum())})
write(REPORT/'graph_time_audit.json',{'rows':rows,'no_model_fitting':True})
for row in rows:print(row,flush=True)
