"""CPU-only bounded evaluator for LLM-authored pandas feature programs."""
import os
if __name__=='__main__':
    os.environ['CUDA_VISIBLE_DEVICES']=''
    for key in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS']:
        os.environ[key]='1'
import argparse
import ast
import hashlib
import gc
import json
from pathlib import Path
import resource
import signal
import time
import traceback
import numpy as np
import pandas as pd

from flat_features import RAW, SEED, RAW_ONLY, Data, matrix, compile_program, check_program
DISALLOWED_CALLS={'open','eval','exec','compile','getattr','setattr','delattr','globals','locals','vars',
                  'input','breakpoint','help','dir','memoryview','type','super','__import__'}
DISALLOWED_ATTRIBUTES={'eval','query','read_csv','read_parquet','read_pickle','read_json','read_sql',
                        'read_excel','read_html','read_feather','load','loads','save','savetxt','savez',
                        'savez_compressed','fromfile','tofile','loadtxt','genfromtxt','memmap','ctypes',
                        'f2py','testing','lib','io','compat'}






def feature_error(error,func,X,history):
    """Actionable model feedback without a long pandas traceback or any labels."""
    frames=[f for f in traceback.extract_tb(error.__traceback__) if f.filename=='<llm-features>']
    lines=getattr(func,'_feature_source','').splitlines()
    location=''
    if frames:
        number=frames[-1].lineno
        location='\nYour code near line '+str(number)+':\n'+'\n'.join(
            f'{i+1}: {lines[i]}' for i in range(max(0,number-3),min(len(lines),number+2)))
    return (f'{type(error).__name__}: {error}'+location+
            '\nAvailable INPUT X columns: '+str(list(X.columns))+
            '\nAvailable INPUT history columns: '+str(list(history.columns))+
            '\nIntermediate tables may have different columns: inspect your groupby/agg/reset_index/merge. '
            'Overlapping non-key columns get _x/_y suffixes after merge. '
            'History has no raw_u_*/raw_i_* columns. Return only f_* features in unchanged X order.')






def map_at_12(predictions,targets):
    if len(predictions)!=len(targets):
        raise ValueError('User alignment changed')
    hits=np.array([np.isin(p,t) for p,t in zip(predictions,targets)])
    denominator=np.minimum(12,np.array([len(np.unique(t)) for t in targets]))
    if (denominator==0).any():
        raise ValueError('Empty target list')
    ap=((hits.cumsum(axis=1)/np.arange(1,13))*hits).sum(axis=1)/denominator
    return float(ap.mean()),ap


def rank(scores,pairs,targets):
    predictions=[]
    if list(pairs.customer_id.drop_duplicates())!=list(targets.customer_id):
        raise ValueError('Pool/user order changed')
    for _,frame in pairs.assign(score=scores).groupby('customer_id',sort=False):
        if len(frame)<12 or frame.article_id.duplicated().any():
            raise ValueError('Invalid candidate pool')
        predictions.append(frame.sort_values(['score','article_id'],ascending=[False,True]).article_id.head(12).to_numpy())
    return np.stack(predictions)


def limits(memory_gb):
    size=int(memory_gb*1024**3)
    resource.setrlimit(resource.RLIMIT_AS,(size,size))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',required=True)
    parser.add_argument('--directory',required=True)
    parser.add_argument('--stage',choices=['preflight','search','confirm','val','test','replay_val','replay_test'],required=True)
    parser.add_argument('--threads',type=int,default=4)
    parser.add_argument('--memory-gb',type=float,default=4)
    parser.add_argument('--backend',choices=['xgboost','lightgbm'],default='lightgbm')
    args=parser.parse_args()
    limits(args.memory_gb)
    tick=time.perf_counter()
    destination=Path(args.directory)
    source=(destination/'program.py').read_text()
    func=compile_program(source)
    data=Data(args.data)
    if args.stage=='preflight':
        train=pd.read_parquet(data.root/'train_pairs.parquet')
        names=None
        checked=[]
        for timestamp in [train.timestamp.min(),train.timestamp.max()]:
            sample=train[train.timestamp==timestamp].head(256).copy().reset_index(drop=True)
            values,names=matrix(data,sample,func,expected=names)
            middle=len(sample)//2
            halves=np.concatenate([matrix(data,sample.iloc[:middle],func,expected=names)[0],matrix(data,sample.iloc[middle:],func,expected=names)[0]])
            if not np.array_equal(values,halves,equal_nan=True):raise ValueError('Features depend on batch size or other rows; use rowwise transformations only')
            checked.append({'kind':'train','cutoff':str(timestamp),'pairs':len(sample)})
        sample=pd.read_parquet(data.root/'search_pairs.parquet').head(256).reset_index(drop=True)
        values,names=matrix(data,sample,func,expected=names)
        middle=len(sample)//2
        halves=np.concatenate([matrix(data,sample.iloc[:middle],func,expected=names)[0],matrix(data,sample.iloc[middle:],func,expected=names)[0]])
        if not np.array_equal(values,halves,equal_nan=True):raise ValueError('Features depend on batch size or other rows; use rowwise transformations only')
        checked.append({'kind':'search_validation','pairs':len(sample)})
        if not getattr(func,'_feature_changed',False):
            raise ValueError('Program generated no new features')
        result={'stage':'preflight','passed':True,'smoke':True,'backend':args.backend,
                'program_sha256':hashlib.sha256(source.encode()).hexdigest(),
                'checked':checked,'features':names,'seconds':time.perf_counter()-tick,
                'counted_as_successful_set':False}
        (destination/'preflight_metrics.json').write_text(json.dumps(result,indent=2))
        print(json.dumps(result))
        return
    model_path=destination/('model.json' if args.backend=='xgboost' else 'model.txt')
    if args.stage=='search' and not model_path.exists():
        pairs=pd.read_parquet(data.root/'train_pairs.parquet')
        values,names=matrix(data,pairs,func)
        if source!=RAW and not getattr(func,'_feature_changed',False):
            raise ValueError('Program generated no new features')
        categorical=set(data.raw_i+['raw_u_club_member_status','raw_u_fashion_news_frequency'])
        kinds=['c' if n in categorical else 'q' for n in names]
        for i,kind in enumerate(kinds):
            if kind=='c':
                values[values[:,i]<0,i]=np.nan
        history={}
        if args.backend=='xgboost':
            import xgboost as xgb
            dataset=xgb.QuantileDMatrix(values,label=pairs.label.values,feature_names=names,feature_types=kinds,
                                       enable_categorical=True,nthread=args.threads,max_bin=127)
            params={'objective':'binary:logistic','eval_metric':'logloss','tree_method':'hist','device':'cpu',
                'max_depth':6,'eta':.05,'subsample':.8,'colsample_bytree':.9,'max_bin':127,
                'seed':42,'nthread':args.threads,'max_cached_hist_node':64}
            model=xgb.train(params,dataset,num_boost_round=150,evals=[(dataset,'train')],evals_result=history,verbose_eval=False)
            model.save_model(model_path)
        else:
            import lightgbm as lgb
            params={'objective':'binary','metric':'binary_logloss','verbosity':-1,'num_threads':args.threads,
                    'learning_rate':.05,'num_leaves':31,'min_data_in_leaf':100,'max_bin':127,
                    'feature_fraction':.9,'bagging_fraction':.8,'bagging_freq':1,'deterministic':True,
                    'force_col_wise':True,'seed':42,'feature_fraction_seed':42,'bagging_seed':42,'data_random_seed':42}
            dataset=lgb.Dataset(values,label=pairs.label.values,feature_name=names,categorical_feature=[n for n in names if n in categorical])
            model=lgb.train(params,dataset,num_boost_round=150,valid_sets=[dataset],valid_names=['train'],callbacks=[lgb.record_evaluation(history)])
            history={'train':{'logloss':history['train']['binary_logloss']}}
            model.save_model(str(model_path))
        (destination/'schema.json').write_text(json.dumps({'features':names,'types':kinds,'params':params,'train_pairs':len(pairs),
                                                          'item_category_maps':data.category_maps}))
        (destination/'learning_curve.json').write_text(json.dumps(history))
        del pairs,values,dataset,model
        gc.collect()
    if args.backend=='xgboost':
        import xgboost as xgb
        model=xgb.Booster()
        model.load_model(model_path)
        model.set_param({'nthread':args.threads,'device':'cpu'})
    else:
        import lightgbm as lgb
        model=lgb.Booster(model_file=str(model_path))
    schema=json.loads((destination/'schema.json').read_text())
    split=args.stage.replace('replay_','')
    pairs=pd.read_parquet(data.root/f'{split}_pairs.parquet')
    targets=pd.read_parquet(data.root/f'{split}_targets.parquet')
    values,names=matrix(data,pairs,func,expected=schema['features'])
    for i,kind in enumerate(schema['types']):
        if kind=='c':
            values[values[:,i]<0,i]=np.nan
    if args.backend=='xgboost':
        scores=model.predict(xgb.DMatrix(values,feature_names=names,feature_types=schema['types'],enable_categorical=True,nthread=args.threads))
    else:
        scores=model.predict(values,num_threads=args.threads)
    predictions=rank(scores,pairs,targets)
    score,ap=map_at_12(predictions,targets.article_id)
    if args.stage.startswith('replay_'):
        assert np.array_equal(predictions,np.load(destination/f'{split}_predictions.npy'))
        assert np.array_equal(ap,np.load(destination/f'{split}_user_ap.npy'))
    else:
        np.save(destination/f'{split}_predictions.npy',predictions)
        np.save(destination/f'{split}_user_ap.npy',ap)
    metrics={'map':score,'users':len(targets),'pairs':len(pairs),'seconds':time.perf_counter()-tick,
             'program_sha256':hashlib.sha256(source.encode()).hexdigest(),
             'model_sha256':hashlib.sha256(model_path.read_bytes()).hexdigest(),'backend':args.backend,
             'stage':args.stage,'threads':args.threads,'passed':True,'features':names}
    (destination/f'{args.stage}_metrics.json').write_text(json.dumps(metrics,indent=2))
    print(json.dumps(metrics))


if __name__=='__main__':
    main()
