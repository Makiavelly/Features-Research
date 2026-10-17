"""Independent H008/H009 search for one fold; outer scores only after barrier."""
import argparse
import fcntl
import importlib
import importlib.metadata
import shutil
import sys
import time
import numpy as np
import pandas as pd
from common import ROOT,paths,read,write,sha,save_predictions,record
from pairs import prepare
from build_runtime import build

def config_for(fold,mode,bundle,runtime):
    data,out=paths(fold);selection=read(bundle/'selection.json');meta=read(bundle/'manifest.json')
    config=read(ROOT/'LLMFeatures/results/hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde/run_config.json')
    config.update(protocol=f'hm_medium_cv_v2_fold{fold}_{mode}',train_pairs=meta['train_pairs'],train_user_times=meta['train_user_times'],
                  search_users=len(selection['search']),confirmation_users=len(selection['confirm']),heldout_val_users=len(selection['heldout_val']),
                  validation_users=len(pd.read_parquet(bundle/'val_targets.parquet')),test_users=len(pd.read_parquet(bundle/'test_targets.parquet')),
                  evaluation_catalog=10000,scoring_user_batch=8,bundle_manifest_sha256=sha(bundle/'manifest.json'),
                  train_pair_sha256=sha(bundle/'train_pairs.parquet'),max_input_tokens=None,
                  memory_protocol='full own-island history' if mode=='h009' else 'best own-island program plus current repair',
                  runtime_sha256={p.name:sha(p) for p in (runtime/'api').glob('*.py')},
                  test_previously_inspected=False,evaluation_timeout_seconds=3600,host_hasattr_fixed=True)
    config['versions']={n:importlib.metadata.version(n) for n in ['numpy','pandas','pyarrow','duckdb','lightgbm']}
    from base_features import FeatureEngine
    engine=FeatureEngine(out/f'cache/examples_{mode}',bundle)
    try:
        pairs=pd.read_parquet(bundle/'train_pairs.parquet').head(3)
        engine.prepare(pairs.timestamp.iloc[0],pairs.customer_id.values,{'aggregates':[]})
        config['training_examples']=engine.frame(pairs).to_json(orient='records')
    finally:engine.close()
    return config

def run(fold,mode,stage):
    data,out=paths(fold);bundle=prepare(fold);runtime=build(fold)
    sys.path.insert(0,str(runtime/'api'))
    import runtime as api_runtime
    from python_features import RAW
    from provider_history import ProviderGenerator as HistoryGenerator
    from provider_best import ProviderGenerator as BestGenerator
    folder=out/mode;folder.mkdir(exist_ok=True);configpath=folder/'run_config.json'
    if not configpath.exists():write(configpath,config_for(fold,mode,bundle,runtime))
    cfg=read(configpath)
    assert cfg['runtime_sha256']=={p.name:sha(p) for p in (runtime/'api').glob('*.py')}
    assert read(out/'validator_verification.json')['status']=='passed'
    runid=cfg['protocol']
    if stage=='train':
        if (folder/cfg['arm']/'selected.json').exists():return
        control=folder/'raw_control';control.mkdir(exist_ok=True)
        write(control/'program.json',{'code':RAW});(control/'program.py').write_text(RAW)
        api_runtime.evaluate(bundle,control,'search',configpath)
        generator=(HistoryGenerator if mode=='h009' else BestGenerator)(cfg,folder,ROOT/'.env')
        original=api_runtime.progress
        def progress(directory,trials,config):
            valid=original(directory,trials,config)
            record('medium_cv_api_progress',f'Fold{fold} {mode}: {len(valid)}/20 accepted, {len(trials)} responses.',runid,
                   status='searching',measured=len(valid),responses=len(trials))
            return valid
        api_runtime.progress=progress
        started=time.perf_counter()
        selected=api_runtime.search(bundle,folder/cfg['arm'],generator,configpath)
        assert selected['budget_complete'],'Search budget exhausted without20 accepted sets'
        write(folder/'trained.json',{'selection':selected,'seconds':time.perf_counter()-started})
        record('medium_cv_api_selected',f'Fold{fold} {mode}:20 accepted, selection frozen before outer test.',runid,status='trained_pending_test')
    else:
        selected=read(folder/cfg['arm']/'selected.json');winner=__import__('pathlib').Path(selected['directory'])
        assert selected['program_sha256']==sha(winner/'program.json') and selected['model_sha256']==sha(winner/'model.txt')
        for split in ['val','test']:
            api_runtime.evaluate(bundle,winner,split,configpath)
            result=api_runtime.evaluate(bundle,winner,'replay_'+split,configpath)
            assert result['passed']
            pred=np.load(winner/f'{split}_predictions.npy')
            target=pd.read_parquet(bundle/f'{split}_targets.parquet')
            save_predictions(folder,split,pred,target)
        shutil.copyfile(winner/'program.py',folder/'selected_program.py')
        write(folder/'verification.json',{'passed':True,'frozen_model_full_replay':True})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('fold',type=int);p.add_argument('mode',choices=['h008','h009']);p.add_argument('stage',choices=['train','evaluate'])
    a=p.parse_args()
    # Recovery and an explicit resume may arrive together. Serialize the whole
    # arm, including generation: replay existing responses before any new POST.
    _,out=paths(a.fold)
    folder=out/a.mode;folder.mkdir(parents=True,exist_ok=True)
    with (folder/'.execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        run(a.fold,a.mode,a.stage)
