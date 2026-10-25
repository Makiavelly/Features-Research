"""Meaningful metric, temporal, validator, alignment and message regressions."""
import importlib.util
import sys
import tempfile
import numpy as np
import pandas as pd
from common import ROOT,paths,read,write,sha,metrics
from build_runtime import build
from pairs import prepare

def main(fold):
    data,out=paths(fold);runtime=build(fold);bundle=prepare(fold)
    sys.path.insert(0,str(runtime/'api'))
    from python_features import parse,compile_function,construct,program_key,FeatureEngine,RAW
    from worker import preflight
    from base_features import FeatureEngine as RawEngine
    passed=[]
    # Existing real regression source, run against the NEW frozen validator.
    source=(ROOT/'LLMFeatures/check_python_features.py').read_text(encoding='utf-8')
    body=source[source.index('    passed=[]'):source.index("    data=ROOT/'data/kaggle_hm_small_sql_compare_v1'")]
    scope=dict(globals(),parse=parse,compile_function=compile_function,construct=construct,program_key=program_key)
    exec(compile('def regression():\n'+body+'\n    return passed','<trusted-regressions>','exec'),scope)
    passed+=scope['regression']()
    p=parse("def modify_features(X, history):\n    a=hasattr(X,'columns')\n    return pd.DataFrame({'f_x':np.ones(len(X))},index=X.index)\n")
    assert len(construct(compile_function(p),pd.DataFrame({'customer_id':[0]}),pd.DataFrame()))==1
    passed.append('host_hasattr_is_supported')
    try:construct(compile_function(parse('def modify_features(X, history):\n    return pd.DataFrame(index=X.index)')),pd.DataFrame(index=[0]),pd.DataFrame())
    except ValueError:passed.append('empty_feature_set_rejected')
    else:raise AssertionError('Empty set accepted')
    pairs=pd.read_parquet(bundle/'train_pairs.parquet')
    engine=FeatureEngine(out/'cache/validator',bundle)
    p=parse("def modify_features(X, history):\n    a=history.groupby('article_id').size()\n    return pd.DataFrame({'f_count':X['article_id'].map(a).fillna(0),'f_age':X['raw_u_age']},index=X.index)\n")
    try:
        assert preflight(engine,pairs,p)['passed'];passed.append('real_batch_permutation_empty_absent_checks')
        for cutoff in [pairs.timestamp.min(),pairs.timestamp.max()]:
            sample=pairs[pairs.timestamp==cutoff].head(128)
            engine.prepare(cutoff,sample.customer_id.to_numpy(),p)
            assert engine.history.days_ago.min()>=0
            expected=engine.con.sql('SELECT article_id,count(*) AS n FROM history GROUP BY article_id').df().set_index('article_id').n
            np.testing.assert_array_equal(engine.frame(sample).f_count,sample.article_id.reset_index(drop=True).map(expected).fillna(0))
            assert len(engine.feature_names)==2 and all(n.startswith('f_') for n in engine.feature_names)
        passed+=['real_SQL_reference','no_automatic_raw15','no_future_history']
    finally:engine.close()
    # A hit whose other target is unretrievable must yield AP=.5, not1.
    targets=pd.DataFrame({'article_id':[[1,10001],[10002]],'customer_id':[1,2]})
    pred=np.array([[1,*range(2,13)],list(range(12))])
    metric,ap=metrics(pred,targets);np.testing.assert_array_equal(ap,[.5,0]);assert metric['map']==.25
    passed.append('unretrievable_targets_kept_in_AP_denominator')
    selection=read(bundle/'selection.json')
    assert len(set(selection['search'])|set(selection['confirm'])|set(selection['heldout_val']))==sum(map(len,selection.values()))
    tables={s:pd.read_parquet(data/f'tasks/user-item-purchase/{s}.parquet') for s in ['train','val','test']}
    assert tables['train'].timestamp.max()+pd.Timedelta(days=7)<=tables['val'].timestamp.min()
    assert tables['val'].timestamp.max()+pd.Timedelta(days=7)<=tables['test'].timestamp.min()
    assert all((p.customer_id<20000).all() for p in tables.values())
    assert any((a>=10000).any() for a in tables['test'].article_id)
    # Check that hosted RelBench labels are not silently filtered/reordered.
    from relbench import load_dataset
    task=load_dataset(data).load_task('user-item-purchase')
    for split in tables:
        actual=task.get_table(split,mask_input_cols=False).df
        assert len(actual)==len(tables[split])
        assert all(np.array_equal(x,y) for x,y in zip(actual.article_id,tables[split].article_id))
    passed+=['disjoint_inner_users','nonoverlapping_label_windows','relbench_preserves_full_targets']
    # Existing13 mock dialog checks, retargeted without touching old reports.
    source=(ROOT/'LLMFeatures/check_dialog_history.py').read_text(encoding='utf-8')
    source=source.replace("CODE = ROOT/'LLMFeatures/provider_history_runtime_v1'",f'CODE = __import__("pathlib").Path({str(runtime/"api")!r})')
    source=source.replace("OUT = ROOT/'reports/provider_history_v1'",f'OUT = __import__("pathlib").Path({str(out)!r})')
    source=source.replace('from provider_api import ProviderGenerator,ProviderUnavailable','from provider_history import ProviderGenerator,ProviderUnavailable')
    source=source.replace("CODE/'provider_api.py'","CODE/'provider_history.py'")
    scope={'__file__':str(ROOT/'LLMFeatures/check_dialog_history.py'),'__name__':'trusted_dialog_tests'}
    exec(compile(source,'<trusted-dialog-regressions>','exec'),scope);scope['main']()
    passed+=read(out/'dialog_verification.json')['checks']
    write(out/'validator_verification.json',{'status':'passed','checks':passed,'real_api_calls':0,
          'runtime_manifest':read(out/'runtime_manifest.json')})
    print('fold',fold,'checks',len(passed),'PASSED',flush=True)

if __name__=='__main__':main(int(sys.argv[1]))
