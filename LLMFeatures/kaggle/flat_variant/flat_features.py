"""Fixed past-only base table; Llama only transforms existing numeric columns."""
import ast
import hashlib
import json
from pathlib import Path
import shutil
import signal
import numpy as np
import pandas as pd
from sql_features import compile_sql
from original_data import Data as HistoryData
from program_guard import extract

RAW='def modify_features(X):\n    return X.copy()\n'
SEED='''def modify_features(X):
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(X['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(X['h_article_count_30'].fillna(0))
    return F
'''
RAW_ONLY='def modify_features(X):\n    return X[[c for c in X.columns if c.startswith("raw_")]].copy()\n'
BASE_SPEC={'aggregates':[], 'derived':[]}
for entity,key in [('user','customer_id'),('article','article_id')]:
    for window in [7,30,180]:
        BASE_SPEC['aggregates'].append({'name':f'f_{entity}_count_{window}','keys':[key],
            'sql':f'COUNT(*) FILTER (WHERE days_ago <= {window})'})
    BASE_SPEC['aggregates'] += [
        {'name':f'f_{entity}_recency','keys':[key],'sql':'MIN(days_ago)'},
        {'name':f'f_{entity}_price_mean','keys':[key],'sql':'AVG(price)'}]
for window in [30,180]:
    BASE_SPEC['aggregates'].append({'name':f'f_user_type_count_{window}',
        'keys':['customer_id','product_type_no'],'sql':f'COUNT(*) FILTER (WHERE days_ago <= {window})'})
BASE_SPEC['aggregates'] += [
    {'name':'f_user_article_count','keys':['customer_id','article_id'],'sql':'COUNT(*)'},
    {'name':'f_user_article_recency','keys':['customer_id','article_id'],'sql':'MIN(days_ago)'},
    {'name':'f_user_colour_count','keys':['customer_id','colour_group_code'],'sql':'COUNT(*)'}]


def prepare(source,working):
    source=Path(source);working=Path(working)
    source_manifest=json.loads((source/'manifest.json').read_text())
    identity={'source_manifest_sha256':hashlib.sha256((source/'manifest.json').read_bytes()).hexdigest(),
              'fixed_base_spec':BASE_SPEC,'preparer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'history_data_sha256':hashlib.sha256(Path(__file__).with_name('original_data.py').read_bytes()).hexdigest(),
              'sql_engine_sha256':hashlib.sha256(Path(__file__).with_name('sql_features.py').read_bytes()).hexdigest()}
    key=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()[:12]
    root=working/('hm_flat_table_v1_'+key);root.mkdir(parents=True,exist_ok=True)
    done=root/'flat_manifest.json'
    if done.exists():
        manifest=json.loads(done.read_text())
        assert manifest['identity']==identity
        for name,digest in manifest['file_sha256'].items():
            assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
        return root,manifest
    data=HistoryData(source);function=compile_sql(json.dumps(BASE_SPEC))
    fields=None;files=[]
    for split in ['train','search','confirm','val','test']:
        pairs=pd.read_parquet(source/f'{split}_pairs.parquet')
        frames=[]
        for cutoff,frame in pairs.groupby('timestamp',sort=False):
            X,history=data.inputs(frame,cutoff)
            F=function(X,history).rename(columns=lambda c:'h_'+c[2:])
            flat=pd.concat([X[data.raw_u+data.raw_i],F],axis=1).astype('float32')
            if fields is None:fields=list(flat)
            assert list(flat)==fields
            flat.index=frame.index;frames.append(flat)
            print('Preparing flat table:',split,str(cutoff),'pairs',len(frame),flush=True)
        flat=pd.concat(frames).reindex(pairs.index)
        assert len(flat)==len(pairs) and flat.index.equals(pairs.index)
        tagged=pairs.copy();tagged['_flat_row']=np.arange(len(pairs));tagged['_flat_split']=split
        pd.testing.assert_frame_equal(tagged[pairs.columns],pairs)
        for name,frame in [(f'{split}_pairs.parquet',tagged),(f'{split}_flat.parquet',flat)]:
            temp=root/(name+'.tmp');frame.to_parquet(temp,index=False);temp.replace(root/name);files.append(name)
    for path in source.iterdir():
        if path.name.endswith('_targets.parquet') or path.name.endswith('_reference.npy'):
            shutil.copy2(path,root/path.name);files.append(path.name)
    copied_manifest={**source_manifest,'flat_base_fields':fields,'source_pair_rows_preserved':True}
    (root/'manifest.json').write_text(json.dumps(copied_manifest));files.append('manifest.json')
    manifest={'identity':identity,'base_fields':fields,'category_maps':data.category_maps,
              'raw_u':data.raw_u,'raw_i':data.raw_i,'train_pairs':source_manifest['train_pairs'],
              'base_feature_origin':'15 raw static +15 fixed human-defined past-only aggregates',
              'file_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in files}}
    done.write_text(json.dumps(manifest,indent=2))
    return root,manifest


def normalize(source):
    return extract(source)


def check_program(source):
    normalized=normalize(source)
    tree=ast.parse(normalized)
    blocked={'groupby','rolling','expanding','ewm','pivot','pivot_table','merge','join','sample',
             'fit','fit_transform','transform','rank','quantile','value_counts','corr','cov','describe'}
    reductions={'mean','sum','min','max','median','std','var','count','nunique'}
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute):
            method=node.func.attr
            if method in blocked:raise ValueError('Flat rowwise transformations only; forbidden: '+method)
            if method in reductions and not any(k.arg=='axis' and isinstance(k.value,ast.Constant) and k.value.value==1 for k in node.keywords):
                raise ValueError('No statistics across rows: '+method+'; only axis=1 reductions are allowed')
    return normalized


def compile_program(source):
    normalized=check_program(source)
    import builtins
    names=['abs','min','max','sum','len','range','enumerate','zip','list','tuple','dict','set',
           'float','int','str','bool','round','isinstance','any','all','ValueError','Exception']
    scope={'pd':pd,'np':np,'__builtins__':{n:getattr(builtins,n) for n in names}}
    exec(compile(normalized,'<flat-features>','exec'),scope)
    function=scope['modify_features'];function._feature_source=source
    return function


class Data:
    def __init__(self,root):
        self.root=Path(root)
        self.manifest=json.loads((self.root/'manifest.json').read_text())
        self.flat_manifest=json.loads((self.root/'flat_manifest.json').read_text())
        self.fields=self.flat_manifest['base_fields'];self.category_maps=self.flat_manifest['category_maps']
        # Keep all base fields in the baseline; only raw_i categories are categorical in LightGBM.
        self.raw_u=self.flat_manifest['raw_u']+[c for c in self.fields if c.startswith('h_')]
        self.raw_i=self.flat_manifest['raw_i'];self.cache={}

    def inputs(self,pairs):
        split=pairs['_flat_split'].iloc[0]
        assert pairs['_flat_split'].eq(split).all()
        if split not in self.cache:self.cache[split]=pd.read_parquet(self.root/f'{split}_flat.parquet')
        return self.cache[split].iloc[pairs['_flat_row'].to_numpy()].reset_index(drop=True).copy()


def matrix(data,pairs,func,expected=None):
    result=[];fields=None
    raw_only=func._feature_source==RAW_ONLY
    for offset in range(0,len(pairs),65536):
        selected=pairs.iloc[offset:offset+65536]
        X=data.inputs(selected)
        def expired(*_):raise TimeoutError('Flat feature function exceeded30s')
        signal.signal(signal.SIGALRM,expired);signal.alarm(30)
        try:out=func(X.copy(deep=True))
        finally:signal.alarm(0)
        if not isinstance(out,pd.DataFrame) or not out.index.equals(X.index) or out.columns.duplicated().any():
            raise ValueError('Return DataFrame preserving X rows/index and unique columns')
        if not 1<=len(out.columns)<=len(data.fields)+48:raise ValueError('Require1-78 numeric feature columns')
        if any(not isinstance(c,str) for c in out):raise ValueError('Column names must be strings')
        changed=list(out)!=list(X) or any(not np.array_equal(out[c].to_numpy(),X[c].to_numpy(),equal_nan=True) for c in out if c in X)
        func._feature_changed=getattr(func,'_feature_changed',False) or changed
        if any(not pd.api.types.is_numeric_dtype(out[c]) for c in out):raise ValueError('All columns must be numeric')
        if fields is None:fields=list(out)
        if list(out)!=fields or expected is not None and fields!=expected:raise ValueError('Feature schema changed')
        values=out.to_numpy(dtype='float32');values[~np.isfinite(values)]=np.nan
        result.append(values)
    return np.concatenate(result),fields
