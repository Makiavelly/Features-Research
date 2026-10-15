"""CPU-only bounded evaluator for LLM-authored pandas feature programs."""
import os
if __name__=='__main__':
    os.environ['CUDA_VISIBLE_DEVICES']=''
    for key in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS']:
        os.environ[key]='1'
import argparse
import ast
import hashlib
import json
from pathlib import Path
import resource
import signal
import time
import numpy as np
import pandas as pd
import xgboost as xgb

RAW = '''def modify_features(X, history):
    return pd.DataFrame(index=X.index)
'''
DISALLOWED_CALLS={'open','eval','exec','compile','getattr','setattr','delattr','globals','locals','vars',
                  'input','breakpoint','help','dir','memoryview','type','super','__import__'}
DISALLOWED_ATTRIBUTES={'eval','query','read_csv','read_parquet','read_pickle','read_json','read_sql',
                        'read_excel','read_html','read_feather','load','loads','save','savetxt','savez',
                        'savez_compressed','fromfile','tofile','loadtxt','genfromtxt','memmap','ctypes',
                        'f2py','testing','lib','io','compat'}


def check_program(source):
    if not isinstance(source,str) or len(source)>20000:
        raise ValueError('Program must be <=20000 characters')
    tree=ast.parse(source)
    functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='modify_features']
    if len(functions)!=1 or [a.arg for a in functions[0].args.args]!=['X','history']:
        raise ValueError('Define exactly def modify_features(X, history)')
    for node in ast.walk(tree):
        if isinstance(node,(ast.Import,ast.ImportFrom,ast.ClassDef,ast.Global,ast.Nonlocal,ast.AsyncFunctionDef,ast.With)):
            raise ValueError('No imports/classes/global state/context managers: pd and np are already supplied')
        if isinstance(node,ast.Name) and (node.id.startswith('_') or node.id in DISALLOWED_CALLS):
            raise ValueError('Forbidden name: '+node.id)
        if isinstance(node,ast.Attribute):
            name=node.attr
            if name.startswith('_') or name.startswith(('read_','to_')) and name not in {'to_numpy','to_frame','to_dict','to_list','to_datetime','to_numeric'} or name in DISALLOWED_ATTRIBUTES:
                raise ValueError('Forbidden attribute: '+name)
        if isinstance(node,ast.FunctionDef) and node.decorator_list:
            raise ValueError('No decorators')
    for node in tree.body:
        if not isinstance(node,(ast.FunctionDef,ast.Expr)) or isinstance(node,ast.Expr) and not isinstance(node.value,ast.Constant):
            raise ValueError('Only function definitions at module level')
    return tree


def compile_program(source):
    tree=check_program(source)
    names=['abs','min','max','sum','len','range','enumerate','zip','list','tuple','dict','set','sorted',
           'float','int','str','bool','round','isinstance','any','all','ValueError','Exception']
    import builtins
    scope={'pd':pd,'np':np,'__builtins__':{n:getattr(builtins,n) for n in names}}
    exec(compile(tree,'<llm-features>','exec'),scope)
    return scope['modify_features']


class Data:
    def __init__(self,root):
        self.root=Path(root)
        self.manifest=json.loads((self.root/'manifest.json').read_text())
        self.items=pd.read_parquet(self.root/'articles.parquet').set_index('article_id')
        # XGBoost allocates categorical histograms up to the maximum code. Compact
        # all static item categories consistently in both X and history.
        self.category_maps={}
        for column in self.items:
            encoded,categories=pd.factorize(self.items[column],sort=True)
            self.category_maps[column]=categories.tolist()
            self.items[column]=encoded.astype('int32')
        self.users=pd.read_parquet(self.root/'customers.parquet').set_index('customer_id')
        self.tx=pd.read_parquet(self.root/'history.parquet')
        self.raw_u=['raw_u_'+c.lower() for c in self.users.columns]
        self.raw_i=['raw_i_'+c for c in self.items.columns]

    def inputs(self,pairs,cutoff):
        pairs=pairs[['customer_id','article_id']].reset_index(drop=True)
        users=self.users.reindex(pairs.customer_id).reset_index(drop=True)
        items=self.items.reindex(pairs.article_id).reset_index(drop=True)
        users.columns=self.raw_u
        items.columns=self.raw_i
        X=pd.concat([pairs,users,items],axis=1)
        cutoff=pd.Timestamp(cutoff)
        history=self.tx[(self.tx.t_dat<=cutoff)&(self.tx.t_dat>cutoff-pd.Timedelta(days=180))].copy()
        assert (history.t_dat<=cutoff).all()
        history['days_ago']=(cutoff-history.t_dat).dt.days.astype('int32')
        history=history.drop(columns='t_dat').merge(self.items.reset_index(),on='article_id',how='left',validate='many_to_one')
        history=history.merge(self.users[['age']].rename(columns={'age':'customer_age'}).reset_index(),on='customer_id',how='left',validate='many_to_one')
        return X,history


def matrix(data,pairs,func,expected=None):
    parts=[]
    schema=None
    for cutoff,frame in pairs.groupby('timestamp',sort=False):
        X,history=data.inputs(frame,cutoff)
        # Only safe columns, no labels/targets/timestamps, are passed to the program.
        def expired(*_):
            raise TimeoutError('Feature function exceeded30 seconds for one snapshot')
        signal.signal(signal.SIGALRM,expired)
        signal.alarm(30)
        try:
            out=func(X.copy(deep=True),history.copy(deep=True))
        finally:
            signal.alarm(0)
        if not isinstance(out,pd.DataFrame) or not out.index.equals(X.index):
            raise ValueError('Return a DataFrame with unchanged X.index and one row per pair')
        if len(out.columns)>48 or out.columns.duplicated().any():
            raise ValueError('At most48 unique generated feature columns')
        for col in out.columns:
            if not isinstance(col,str) or not col.startswith('f_') or not pd.api.types.is_numeric_dtype(out[col]):
                raise ValueError('Generated features must be numeric with f_ names; do not return IDs/raw columns')
            if np.array_equal(out[col].to_numpy(),X.customer_id.to_numpy()) or np.array_equal(out[col].to_numpy(),X.article_id.to_numpy()):
                raise ValueError('IDs are join keys, not numeric features')
        raw=X[data.raw_u+data.raw_i]
        full=pd.concat([raw,out],axis=1)
        if schema is None:
            schema=list(full)
        if list(full)!=schema or expected is not None and schema!=expected:
            raise ValueError('Feature schema changed between snapshots or splits')
        values=full.to_numpy(dtype=np.float32)
        values[~np.isfinite(values)]=np.nan
        parts.append(pd.DataFrame(values,index=frame.index,columns=schema))
    values=pd.concat(parts).reindex(pairs.index).to_numpy(dtype=np.float32)
    return values,schema


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
    parser.add_argument('--stage',choices=['search','confirm','val','test','replay_val','replay_test'],required=True)
    parser.add_argument('--threads',type=int,default=4)
    parser.add_argument('--memory-gb',type=float,default=4)
    parser.add_argument('--backend',choices=['xgboost','lightgbm'],default='xgboost')
    args=parser.parse_args()
    limits(args.memory_gb)
    tick=time.perf_counter()
    destination=Path(args.directory)
    source=(destination/'program.py').read_text()
    func=compile_program(source)
    data=Data(args.data)
    model_path=destination/('model.json' if args.backend=='xgboost' else 'model.txt')
    if args.stage=='search' and not model_path.exists():
        pairs=pd.read_parquet(data.root/'train_pairs.parquet')
        values,names=matrix(data,pairs,func)
        if source!=RAW and len(names)==len(data.raw_u+data.raw_i):
            raise ValueError('Program generated no new features')
        categorical=set(data.raw_i+['raw_u_club_member_status','raw_u_fashion_news_frequency'])
        kinds=['c' if n in categorical else 'q' for n in names]
        for i,kind in enumerate(kinds):
            if kind=='c':
                values[values[:,i]<0,i]=np.nan
        history={}
        if args.backend=='xgboost':
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
    if args.backend=='xgboost':
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
