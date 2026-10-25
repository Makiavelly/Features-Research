"""Stream full-catalog scoring; never materialize giant manual evaluation caches."""
import argparse
import gc
import sys
import time
import numpy as np
import pandas as pd
import lightgbm as lgb
from common import ROOT,paths,read,write,sha,save_predictions,record
from pairs import prepare
sys.path.insert(0,str(ROOT/'baseline'))
from manual_features import ManualFeatures
sys.path.insert(0,str(ROOT/'LLMFeatures/provider_generated_only_runtime_v1'))
from base_features import FeatureEngine as RawEngine

PARAMS=dict(objective='binary',verbosity=-1,learning_rate=.05,num_leaves=31,
            min_data_in_leaf=100,max_bin=127,feature_fraction=.9,bagging_fraction=.8,
            bagging_freq=1,deterministic=True,force_col_wise=True,seed=42,
            feature_fraction_seed=42,bagging_seed=42,data_random_seed=42,num_threads=4)

def frame(engine,pairs,kind):
    if kind=='raw15':return engine.frame(pairs)
    # SQL joins can change row order; attach an explicit ordinal, then restore it.
    pairs=pairs[['customer_id','article_id']].reset_index(drop=True).copy()
    pairs['_row']=np.arange(len(pairs))
    f=engine.frame(pairs).sort_values('_row',kind='stable').reset_index(drop=True)
    assert np.array_equal(f['_row'],np.arange(len(f)))
    return f.drop(columns=['customer_id','article_id','_row'])

def matrix(engine,pairs,kind):
    f=frame(engine,pairs,kind)
    return np.nan_to_num(f.to_numpy(dtype=np.float32),nan=-1,posinf=-1,neginf=-1),list(f)

def run(fold,kind,stage):
    data,out=paths(fold);bundle=prepare(fold);folder=out/f'lightgbm_{kind}';folder.mkdir(parents=True,exist_ok=True)
    if stage=='train' and (folder/'trained.json').exists():return
    if stage=='evaluate' and (folder/'verification.json').exists():return
    engine=ManualFeatures(data/'db',out/f'cache/manual_{kind}') if kind=='manual' else RawEngine(out/'cache/raw',bundle)
    def prep(cutoff,users):
        if kind=='manual':engine.prepare(cutoff,users)
        else:engine.prepare(cutoff,users,{'aggregates':[]})
    try:
        if stage=='train':
            started=time.perf_counter();pairs=pd.read_parquet(bundle/'train_pairs.parquet');xs=[];ys=[]
            for cutoff,g in pairs.groupby('timestamp',sort=True):
                prep(cutoff,g.customer_id.to_numpy());x,names=matrix(engine,g,kind)
                xs.append(x);ys.append(g.label.to_numpy())
            x=np.concatenate(xs);y=np.concatenate(ys);del xs;gc.collect()
            categorical=engine.categorical_names if kind=='manual' else [n for n in names if n not in ['raw_u_age','raw_u_fn','raw_u_active']]
            ds=lgb.Dataset(x,label=y,feature_name=names,categorical_feature=categorical)
            model=lgb.train(PARAMS,ds,num_boost_round=150);model.save_model(str(folder/'model.txt'))
            write(folder/'trained.json',{'kind':kind,'params':PARAMS,'features':names,'categorical':categorical,'rounds':150,
                  'train_pairs':len(y),'train_pairs_sha256':sha(bundle/'train_pairs.parquet'),'seconds':time.perf_counter()-started})
            record('medium_cv_tree_trained',f'Fold{fold} {kind}: trained on shared saved pairs.',f'hm_medium_cv_v2_fold{fold}_{kind}',status='trained_pending_test')
        else:
            model=lgb.Booster(model_file=str(folder/'model.txt'));schema=read(folder/'trained.json')
            for split in ['val','test']:
                target=pd.read_parquet(bundle/f'{split}_targets.parquet');prep(target.timestamp.iloc[0],target.customer_id.to_numpy())
                predictions=[];started=time.perf_counter()
                for offset in range(0,len(target),8):
                    users=target.customer_id.iloc[offset:offset+8].to_numpy()
                    pairs=pd.DataFrame({'customer_id':np.repeat(users,10000),'article_id':np.tile(np.arange(10000),len(users))})
                    values,names=matrix(engine,pairs,kind);assert names==schema['features']
                    scores=model.predict(values,num_threads=4).reshape(len(users),10000)
                    predictions.extend(np.argsort(-scores,axis=1,kind='stable')[:,:12])
                    if offset==0:
                        again=lgb.Booster(model_file=str(folder/'model.txt')).predict(values,num_threads=4)
                        np.testing.assert_array_equal(again,scores.ravel())
                        perm=np.random.default_rng(42).permutation(len(pairs))
                        pvalues,_=matrix(engine,pairs.iloc[perm].reset_index(drop=True),kind)
                        np.testing.assert_allclose(pvalues[np.argsort(perm)],values)
                metric=save_predictions(folder,split,np.asarray(predictions),target)
                write(folder/f'{split}_timing.json',{'seconds':time.perf_counter()-started})
                print(fold,kind,split,metric,flush=True)
            write(folder/'verification.json',{'passed':True,'reload_prediction_check':True,'row_permutation_check':True})
    finally:engine.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('fold',type=int);p.add_argument('kind',choices=['manual','raw15']);p.add_argument('stage',choices=['train','evaluate'])
    a=p.parse_args();run(a.fold,a.kind,a.stage)
