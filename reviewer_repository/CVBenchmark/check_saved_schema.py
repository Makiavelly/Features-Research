"""Synthetic reversed-column model boundary and unchanged real confirmation replay."""
from pathlib import Path
import tempfile
import sys
import numpy as np
import pandas as pd
import lightgbm as lgb
from common import ROOT,OUT,REPORT,read,write,sha

def main():
    api=OUT/'fold_0/runtime/api';sys.path.insert(0,str(api))
    import worker,runtime
    from python_features import construct,compile_function,parse
    code="def modify_features(X, history):\n    return pd.DataFrame({'f_b':np.zeros(len(X)), 'f_a':X['article_id']},index=X.index)\n"
    with tempfile.TemporaryDirectory(prefix='saved_schema_') as temporary:
        root=Path(temporary);directory=root/'model';directory.mkdir()
        x=np.column_stack([np.arange(10000),np.zeros(10000)]).astype('float32');y=(x[:,0]>5000).astype(int)
        model=lgb.train({'objective':'binary','verbosity':-1,'num_threads':2,'num_leaves':3,'min_data_in_leaf':5},
                        lgb.Dataset(x,label=y,feature_name=['f_a','f_b']),num_boost_round=5)
        model.save_model(str(directory/'model.txt'));write(directory/'feature_schema.json',{'features':['f_a','f_b']})
        target=pd.DataFrame({'customer_id':[0],'article_id':[np.array([9999])],'timestamp':[pd.Timestamp('2020-06-29')]})
        target.to_parquet(root/'val_targets.parquet',index=False)
        class FreshEngine:
            items=pd.DataFrame({'article_id':np.arange(10000)})
            def prepare(self,*args):self.names=None
            def matrix(self,pairs):
                result=construct(compile_function(parse(code)),pairs,pd.DataFrame(),expected=self.names)
                return result.to_numpy(dtype='float32')
        worker.predict(FreshEngine(),root,directory,'val',{'code':code},{'scoring_user_batch':8,'cpu_threads':2})
        got=np.load(directory/'val_predictions.npy')[0]
        expected=np.lexsort((np.arange(10000),-model.predict(x)))[:12]
        wrong=np.lexsort((np.arange(10000),-model.predict(x[:,::-1])))[:12]
        np.testing.assert_array_equal(got,expected);assert not np.array_equal(expected,wrong)
    inventory=read(REPORT/'confirmation_boundary_fix_inventory.json');checks=[]
    cfg=OUT/'fold_0/h008/run_config.json';data=ROOT/'data/hm-cv-medium-v2/fold_0/bundle'
    for relative in inventory['cached_confirmation_files_before_fix']:
        folder=(ROOT/relative).parent
        replay=runtime.evaluate(data,folder,'replay_confirm',cfg)
        assert replay['passed']
        checks.append({'directory':relative,'predictions_identical':True,'map':replay['map']})
    write(REPORT/'saved_schema_verification.json',{'status':'passed','synthetic_reversed_columns':True,
          'synthetic_tree_fits':1,'new_API_requests':0,'new_candidate_tree_fits':0,
          'existing_confirmation_replays':checks,'worker_sha256':sha(api/'worker.py')})
    print('Saved model schema boundary and',len(checks),'real confirmation replays passed',flush=True)

if __name__=='__main__':main()
