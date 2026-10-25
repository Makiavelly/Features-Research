"""Read-only LightGBM inference: normal ranking replay and unseen-item rerank."""
import argparse
import gc
import importlib.util
import json
import sys
import time
from pathlib import Path

import novelty_audit as audit
from common import ROOT,DATA,OLD,OUT,read,write,sha,record


def run(fold,kind):
    import numpy as np
    import pandas as pd
    import lightgbm as lgb
    runtime=OLD/f'fold_{fold}/runtime/api'
    sys.path.insert(0,str(runtime))
    bundle=DATA/f'fold_{fold}/bundle'
    target=pd.read_parquet(bundle/'test_targets.parquet')
    masks=np.load(audit.DEST/f'fold_{fold}/seen_mask.npy',mmap_mode='r')
    methods=audit.methods(fold)
    jobs=[]
    if kind=='api':
        from features import FeatureEngine,validate_program
        from worker import timed_frame
        for key,item in methods.items():
            if not key.startswith('h00'):continue
            mode,budget=key.rsplit('_',1)
            selection=read(OUT/f'fold_{fold}/{mode}/budgets/{budget}/selected.json')
            source=Path(selection['directory'])
            assert sha(source/'model.txt')==selection['model_sha256']
            assert sha(source/'program.json')==selection['program_sha256']
            fingerprint=selection['model_sha256']+selection['program_sha256']
            jobs.append((key,source,fingerprint))
    else:
        key=kind
        source=OLD/f'fold_{fold}/lightgbm_{kind}'
        jobs=[(key,source,sha(source/'model.txt'))]
    completed={}
    for key,source,fingerprint in jobs:
        folder=audit.output(fold,key)
        if (folder/'verification.json').exists():
            assert read(folder/'verification.json')['passed']
            completed[fingerprint]=folder
            continue
        if fingerprint in completed:
            prior=completed[fingerprint]
            # Reuse only if the saved original ranking is also identical.
            other_key=read(prior/'verification.json')['method']
            assert np.array_equal(np.load(methods[key]['prediction']),np.load(methods[other_key]['prediction']))
            np.save(folder/'new_predictions.npy',np.load(prior/'new_predictions.npy'))
            info=read(prior/'verification.json');info.update(method=key,reused_identical_model=str(prior.relative_to(ROOT)))
            write(folder/'verification.json',info)
            print('REUSE_MODEL',fold,key,flush=True)
            continue
        started=time.perf_counter()
        model=lgb.Booster(model_file=str(source/'model.txt'))
        names=model.feature_name()
        if kind=='api':
            program=validate_program(read(source/'program.json'))
            assert names==read(source/'feature_schema.json')['features']
            engine=FeatureEngine(folder/'scratch',bundle)
            engine.prepare(target.timestamp.iloc[0],target.customer_id.to_numpy(),program)
            engine.names=list(names)
            def matrix(pairs):return timed_frame(engine,pairs)
        elif kind=='raw15':
            from base_features import FeatureEngine as RawEngine
            engine=RawEngine(folder/'scratch',bundle)
            engine.prepare(target.timestamp.iloc[0],target.customer_id.to_numpy(),{'aggregates':[]})
            def matrix(pairs):
                frame=engine.frame(pairs)
                assert list(frame)==names
                return np.nan_to_num(frame.to_numpy(dtype=np.float32),nan=-1,posinf=-1,neginf=-1)
        else:
            sys.path.insert(0,str(ROOT/'baseline'))
            from manual_features import ManualFeatures
            engine=ManualFeatures(DATA/f'fold_{fold}/db',folder/'scratch')
            engine.prepare(target.timestamp.iloc[0],target.customer_id.to_numpy())
            def matrix(pairs):
                pairs=pairs[['customer_id','article_id']].reset_index(drop=True).copy()
                pairs['_row']=np.arange(len(pairs))
                frame=engine.frame(pairs).sort_values('_row',kind='stable').reset_index(drop=True)
                assert np.array_equal(frame['_row'],np.arange(len(pairs)))
                frame=frame.drop(columns=['customer_id','article_id','_row'])
                assert list(frame)==names
                return np.nan_to_num(frame.to_numpy(dtype=np.float32),nan=-1,posinf=-1,neginf=-1)
        expected=np.load(methods[key]['prediction'])
        predictions=[]
        try:
            for start in range(0,len(target),8):
                users=target.customer_id.iloc[start:start+8].to_numpy()
                pairs=pd.DataFrame({'customer_id':np.repeat(users,10000),'article_id':np.tile(np.arange(10000),len(users))})
                values=matrix(pairs)
                scores=model.predict(values,num_threads=2).reshape(len(users),10000)
                assert np.isfinite(scores).all()
                normal=np.argsort(-scores,axis=1,kind='stable')[:,:12]
                assert np.array_equal(normal,expected[start:start+8]),(fold,key,start,'original predictions differ')
                scores[masks[start:start+8]]=-np.inf
                novel=np.argsort(-scores,axis=1,kind='stable')[:,:12]
                assert np.isfinite(np.take_along_axis(scores,novel,axis=1)).all()
                assert not masks[start:start+8][np.arange(len(users))[:,None],novel].any()
                predictions.append(novel)
                if start%128==0:
                    write(folder/'progress.json',dict(method=key,fold=fold,users_done=start+len(users),users=len(target),seconds=time.perf_counter()-started))
                    print('SCORING',fold,key,start+len(users),'/',len(target),flush=True)
        finally:
            engine.close()
        np.save(folder/'new_predictions.npy',np.concatenate(predictions))
        write(folder/'verification.json',dict(passed=True,method=key,normal_top12_identical=True,
            all_full_catalog_original_predictions_replayed=True,model_sha256=sha(source/'model.txt'),
            program_sha256=sha(source/'program.json') if kind=='api' else None,
            full_catalog=10000,scoring_batch=8,no_refitting=True,no_api=True,
            seconds=time.perf_counter()-started,policy='Original features/models; mask all source-history purchased candidates before top12'))
        completed[fingerprint]=folder
        record('novelty_tree_verified',f'Fold{fold} {key}: full-catalog original top12 reproduced exactly; unseen-only reranking saved, no fitting/API.',audit.RUN+f'_f{fold}_{key}',status='verified',artifacts=str(folder.relative_to(ROOT)))
        del model,engine,predictions
        gc.collect()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('fold',type=int);p.add_argument('kind',choices=['raw15','manual','api']);a=p.parse_args();run(a.fold,a.kind)
