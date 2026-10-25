"""Measure accepted-program diversity without changing search or fitting trees."""
import hashlib
import sys
import numpy as np
import pandas as pd
from common import paths,read,write,sha

def main(fold,mode):
    data,out=paths(fold);folder=out/mode;runtime=out/'runtime/api'
    cfg=read(folder/'run_config.json');bundle=data/'bundle'
    sys.path.insert(0,str(runtime))
    from python_features import FeatureEngine,parse,program_key
    pairs=pd.read_parquet(bundle/'train_pairs.parquet')
    assert sha(bundle/'train_pairs.parquet')==cfg['train_pair_sha256']
    trials=[read(p) for p in sorted((folder/cfg['arm']/'candidates').glob('*/trial.json'))]
    valid=[t for t in trials if t['status']=='valid'];assert len(valid)==20
    destination=folder/'numeric_diversity.json'
    if destination.exists():
        previous=read(destination)
        assert previous['train_pairs_sha256']==cfg['train_pair_sha256']
        assert previous['program_keys']==[t['program_key'] for t in valid]
        return
    engine=FeatureEngine(out/f'cache/diversity_{mode}',bundle)
    records=[];groups={}
    try:
        for trial in valid:
            candidate=folder/cfg['arm']/'candidates'/f"candidate_{trial['call']:03d}"
            program=read(candidate/'program.json')
            assert program_key(program)==trial['program_key']
            matrices=[]
            for cutoff,frame in pairs.groupby('timestamp',sort=True):
                engine.prepare(cutoff,frame.customer_id.to_numpy(),program)
                matrices.append(engine.matrix(frame))
            values=np.concatenate(matrices);assert len(values)==len(pairs)
            assert 1<=values.shape[1]<=36 and all(n.startswith('f_') for n in engine.feature_names)
            values[values==0]=0 # normalize negative zero for numeric equality
            columns=[hashlib.sha256(np.ascontiguousarray(values[:,i],dtype='<f4').tobytes()).hexdigest() for i in range(values.shape[1])]
            signature=hashlib.sha256(('|'.join(sorted(columns))).encode()).hexdigest()
            groups.setdefault(signature,[]).append(trial['call'])
            records.append({'call':trial['call'],'columns':values.shape[1],'signature':signature})
            print('numeric audit',fold,mode,trial['call'],len(groups),'distinct so far',flush=True)
    finally:engine.close()
    write(destination,{'status':'passed','accepted':20,'numeric_distinct_sets':len(groups),
          'basis':'all training rows, float32 missing=-1, column-order/name independent, multiplicity preserved',
          'train_pairs_sha256':cfg['train_pair_sha256'],'program_keys':[t['program_key'] for t in valid],
          'records':records,'duplicate_groups':[v for v in groups.values() if len(v)>1],
          'additional_api_requests':0,'additional_tree_fits':0})

if __name__=='__main__':main(int(sys.argv[1]),sys.argv[2])
