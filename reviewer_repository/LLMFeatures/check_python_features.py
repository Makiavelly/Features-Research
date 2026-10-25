"""Regression checks for false acceptance and false rejection; no API calls."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'LLMFeatures/provider_python_runtime_v2'))
from python_features import parse,compile_function,construct,program_key,FeatureEngine,RAW
from base_features import FeatureEngine as RawEngine
from worker import preflight


def main():
    passed=[]
    def check(name, action):
        action()
        passed.append(name)
    X=pd.DataFrame({'customer_id':[2,1,2,3], 'article_id':[4,5,5,9],
                    'raw_u_age':[31.,24.,31.,np.nan]},index=[8,2,7,4])
    history=pd.DataFrame({'customer_id':[1,2,2], 'article_id':[5,4,5],
                          'price':[1.,2.,4.], 'days_ago':[10,5,40]})
    valid={
        'working_map':"""def modify_features(X, history):
    out=pd.DataFrame(index=X.index)
    counts=history.loc[history['days_ago']<=30].groupby('customer_id').size()
    out['f_count']=X['customer_id'].map(counts).fillna(0)
    return out
""",
        'imports_helper_merge':"""import pandas as pd
import numpy as np
def ratio(a,b):
    return a / b.replace(0,np.nan)
def modify_features(X, history):
    stats=history.groupby('customer_id',as_index=False).agg(n=('price','size'),p=('price','mean'))
    out=X[['customer_id']].merge(stats,on='customer_id',how='left',sort=False)
    out.index=X.index
    return pd.DataFrame({'f_ratio':ratio(out['n'],out['p'])},index=X.index)
""",
        'multiindex_reindex':"""def modify_features(X, history):
    counts=history.groupby(['customer_id','article_id']).size()
    keys=pd.MultiIndex.from_frame(X[['customer_id','article_id']])
    return pd.DataFrame({'f_pair':counts.reindex(keys).fillna(0).to_numpy()},index=X.index)
""",
        'lambda_comprehension_numpy':"""def modify_features(X, history):
    out=pd.DataFrame(index=X.index)
    for days in [7,30,180]:
        agg=history[history['days_ago']<=days].groupby('article_id')['price'].agg(lambda s: np.sqrt(np.mean(s*s)))
        out[f'f_rms_{days}']=X['article_id'].map(agg)
    return out
""",
        'empty_history_stable':"""def modify_features(X, history):
    counts=history.groupby('article_id').size()
    out=pd.DataFrame(index=X.index)
    out['f_count']=X['article_id'].map(counts).fillna(0).astype(float)
    return out
"""}
    valid['literal_constants_private_helper'] = """EPS = 0.000001
def _divide(a,b):
    return a/(b+EPS)
def modify_features(X, history):
    out=pd.DataFrame(index=X.index)
    out['f_price']=_divide(X['raw_u_age'],X['raw_u_age'].fillna(0))
    return out
"""
    for name,code in valid.items():
        def action(code=code):
            fun=compile_function(parse(code))
            out=construct(fun,X,history)
            construct(fun,X,history.iloc[:0],expected=list(out))
            perm=[2,0,3,1]
            p=construct(fun,X.iloc[perm],history)
            np.testing.assert_allclose(p.to_numpy()[np.argsort(perm)],out.to_numpy(),equal_nan=True)
            chunks=pd.concat([construct(fun,X.iloc[:2],history),construct(fun,X.iloc[2:],history)])
            np.testing.assert_allclose(chunks,out,equal_nan=True)
        check(name,action)
    # Independently calculated numeric targets, including absent users/items.
    out=construct(compile_function(parse(valid['working_map'])),X,history)
    np.testing.assert_array_equal(out.f_count,[1,1,1,0]);passed.append('independent_count_reference')
    pair=construct(compile_function(parse(valid['multiindex_reindex'])),X,history)
    np.testing.assert_array_equal(pair.f_pair,[1,1,1,0]);passed.append('independent_pair_reference')
    for name,code in {
        'syntax':'def modify_features(X, history)\n return X',
        'forbidden_import':'import os\ndef modify_features(X, history):\n return X',
        'file_read':"def modify_features(X, history):\n return pd.read_csv('x')",
        'file_write':"def modify_features(X, history):\n return X.to_pickle('x')",
        'private_attribute':"def modify_features(X, history):\n return X.__class__",
        'dynamic_eval':"def modify_features(X, history):\n return eval('1')",
        'randomness':"def modify_features(X, history):\n return np.random.rand(2)",
    }.items():
        try:parse(code)
        except ValueError:passed.append('reject_'+name)
        else:raise AssertionError('False acceptance: '+name)
    for name,body in {
        'wrong_type':'return [1,2,3,4]',
        'wrong_rows':"return pd.DataFrame({'f_x':[1]})",
        'wrong_index':"return pd.DataFrame({'f_x':[1]*len(X)})",
        'ID_output':"return pd.DataFrame({'customer_id':X['customer_id']},index=X.index)",
        'nonnumeric':"return pd.DataFrame({'f_x':['a']*len(X)},index=X.index)",
        'unknown_column':"return pd.DataFrame({'f_x':X['gender']},index=X.index)",
        'duplicate_columns':"return pd.DataFrame(np.zeros((len(X),2)),index=X.index,columns=['f_x','f_x'])",
    }.items():
        try:construct(compile_function(parse('def modify_features(X, history):\n    '+body)),X,history)
        except (ValueError,KeyError):passed.append('reject_'+name)
        else:raise AssertionError('False acceptance: '+name)
    code=valid['working_map']
    assert program_key(parse(code))==program_key(parse('# comment\n'+code))
    assert program_key(parse(code))!=program_key(parse(code.replace('<=30','<=7')))
    passed.append('conservative_AST_dedup')
    output=construct(compile_function(parse("def modify_features(X, history):\n    return pd.DataFrame({'f_b': X['raw_u_age'], 'f_a': X['raw_u_age']+1},index=X.index)")),X,history,expected=['f_a','f_b'])
    assert list(output)==['f_a','f_b']
    np.testing.assert_allclose(output.f_a,X.raw_u_age+1,equal_nan=True)
    passed.append('column_name_alignment_without_row_reordering')
    data=ROOT/'data/kaggle_hm_small_sql_compare_v1'
    pairs=pd.read_parquet(data/'train_pairs.parquet')
    scratch=ROOT/'reports/provider_python_v1/validator_scratch'
    engine=FeatureEngine(scratch/'python',data)
    raw=RawEngine(scratch/'raw',data)
    try:
        # Raw predictions can only match if encodings/missing handling match exactly.
        for cutoff in [pairs.timestamp.min(),pairs.timestamp.max()]:
            frame=pairs[pairs.timestamp==cutoff].head(256)
            raw.prepare(cutoff,frame.customer_id.values,{'aggregates':[]})
            engine.prepare(cutoff,frame.customer_id.values,{'code':RAW})
            np.testing.assert_array_equal(engine.matrix(frame),raw.matrix(frame))
            assert engine.history.days_ago.min()>=0
            expected=int(raw.con.sql(f"SELECT count(*) FROM tx WHERE t_dat <= TIMESTAMP '{pd.Timestamp(cutoff)}'").fetchone()[0])
            assert len(engine.history)==expected
            # Check all-history count maps and category ID alignment against host SQL.
            program=parse(valid['working_map'])
            engine.prepare(cutoff,frame.customer_id.values,program)
            values=engine.frame(frame).f_count.to_numpy()
            lookup=raw.con.sql('SELECT customer_id,count(*) AS n FROM history WHERE days_ago<=30 GROUP BY customer_id').df().set_index('customer_id').n
            np.testing.assert_array_equal(values,frame.customer_id.map(lookup).fillna(0))
        passed.extend(['real_raw_byte_equivalence','past_only_history_rows','real_pandas_vs_SQL_reference'])
        preflight(engine,pairs,parse(valid['multiindex_reindex']))
        passed.append('real_permutation_and_batch_preflight')
        bad="""def modify_features(X, history):
    return pd.DataFrame({'f_bad': X['raw_u_age']-X['raw_u_age'].mean()},index=X.index)
"""
        try:preflight(engine,pairs,parse(bad))
        except AssertionError:passed.append('reject_candidate_batch_statistics')
        else:raise AssertionError('Batch-dependent features falsely accepted')
    finally:engine.close();raw.close()
    result={'status':'passed','checks':passed,'checks_count':len(passed),
            'module_sha256':hashlib.sha256((ROOT/'LLMFeatures/provider_python_runtime_v2/python_features.py').read_bytes()).hexdigest(),
            'api_calls':0,'note':'Regression evidence, not a proof that all future correct Python will be accepted. Inspect each real rejection.'}
    out=ROOT/'reports/provider_python_v1/validator_verification.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
