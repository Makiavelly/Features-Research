"""Exercise non-GNN time filters on real ms-resolution validation/test cutoffs."""
import ast
import sys
import numpy as np
import pandas as pd
from common import ROOT,DATA,OLD,REPORT,read,write,sha,record
from relbench import load_dataset

sys.path.insert(0,str(ROOT/'baseline'))
from manual_features import ManualFeatures
sys.path.insert(0,str(OLD/'fold_0/runtime/api'))
from base_features import FeatureEngine

def extract(path,name):
    tree=ast.parse(path.read_text(encoding='utf-8'))
    function=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name==name)
    namespace={'np':np}
    exec(compile(ast.Module(body=[function],type_ignores=[]),str(path),'exec'),namespace)
    return namespace[name]

def main():
    rows=[];sources={}
    for fold in range(3):
        data=DATA/f'fold_{fold}';runtime=OLD/f'fold_{fold}/runtime'
        rpath=runtime/'recformer.py';tpath=runtime/'tdm_common.py'
        visible=extract(rpath,'visible_items');history_at=extract(tpath,'history_at')
        sources.update({str(p.relative_to(ROOT)):sha(p) for p in [rpath,tpath,runtime/'api/base_features.py',ROOT/'baseline/manual_features.py']})
        task=load_dataset(data).load_task('user-item-purchase')
        tx=pd.read_parquet(data/'db/transactions.parquet').sort_values('t_dat',kind='stable')
        bundle_tx=pd.read_parquet(data/'bundle/transactions.parquet')
        histories={int(user):(g.t_dat.to_numpy(),g.article_id.to_numpy()) for user,g in tx.groupby('customer_id',sort=False)}
        manual=ManualFeatures(data/'db',REPORT/f'scratch/time_audit_f{fold}/manual')
        raw=FeatureEngine(REPORT/f'scratch/time_audit_f{fold}/raw',data/'bundle')
        try:
            for split in ['val','test']:
                table=task.get_table(split,mask_input_cols=False).df;cutoff=table.timestamp.iloc[0]
                users=table.customer_id.to_numpy();assert pd.Timestamp(cutoff).year==2020
                raw.prepare(cutoff,users,{'aggregates':[]});manual.prepare(cutoff,users)
                count_raw,latest_raw=raw.con.sql('SELECT count(*),max(t_dat) FROM tx WHERE t_dat <= '+"TIMESTAMP '"+pd.Timestamp(cutoff).strftime('%Y-%m-%d %H:%M:%S')+"'").fetchone()
                history_count=raw.con.sql('SELECT count(*) FROM history').fetchone()[0]
                count_manual,latest_manual=manual.con.sql('SELECT count(*),max(t_dat) FROM hist').fetchone()
                expected_raw=int((bundle_tx.t_dat<=cutoff).sum())
                expected_manual=int(((tx.t_dat<=cutoff)&tx.customer_id.isin(users)).sum())
                assert count_raw==history_count==expected_raw and count_raw>0
                assert count_manual==expected_manual and count_manual>0
                assert pd.Timestamp(latest_raw)<=cutoff and pd.Timestamp(latest_manual)<=cutoff
                exercised=0
                for user in users[:100]:
                    if int(user) not in histories:continue
                    dates,items=histories[int(user)];mask=dates<=np.datetime64(cutoff)
                    expected=items[mask][-50:]
                    for unit in ['ns','us','ms','s']:
                        stamp=np.datetime64(cutoff,unit)
                        got,n=visible(dates,items,stamp)
                        np.testing.assert_array_equal(got,expected);assert n==int(mask.sum())
                        np.testing.assert_array_equal(history_at(dates,items,stamp),expected[::-1])
                    exercised+=1
                assert exercised>0
                rows.append({'fold':fold,'split':split,'cutoff':str(cutoff),'loaded_dtype':str(table.timestamp.dtype),
                    'raw_and_API_history_count':int(history_count),'manual_history_count':int(count_manual),
                    'recformer_and_tdm_users_checked':exercised,'datetime_resolutions_checked':['ns','us','ms','s'],'passed':True})
        finally:manual.close();raw.close()
    write(REPORT/'other_models_time_audit.json',{'passed':True,'checks':rows,'source_sha256':sources,
        'scope':'Actual manual/raw/API host SQL filters and Recformer/TDM history functions; not a general proof that all model code is bug-free.'})
    record('non_gnn_time_audit','Manual/raw/API history and Recformer/TDM history filters pass on real cutoffs from all six validation/test splits, including ms-resolution dates.',
        'hm_medium_non_gnn_time_audit_v1',status='verified',artifacts='reports/medium_followup_v1/other_models_time_audit.json')
    print('NON-GNN TIME AUDIT: all six real splits passed',flush=True)

if __name__=='__main__':main()
