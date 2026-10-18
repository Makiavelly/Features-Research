"""Continue the six immutable20-program streams to30/40 accepted programs."""
import argparse
import fcntl
import shutil
import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd
from common import ROOT,OLD,DATA,OUT,REPORT,read,write,sha,freeze_text,record

def prepare(fold,mode):
    parent=OUT/f'fold_{fold}';parent.mkdir(parents=True,exist_ok=True)
    runtime=parent/'runtime/api';runtime.mkdir(parents=True,exist_ok=True)
    for source in (OLD/f'fold_{fold}/runtime/api').glob('*.py'):
        freeze_text(runtime/source.name,source.read_text(encoding='utf-8'))
    folder=parent/mode;original=OLD/f'fold_{fold}'/mode
    provenance=folder/'fork_provenance.json'
    if not provenance.exists():
        assert not folder.exists(),'Partial fork exists; inspect before resuming'
        shutil.copytree(original,folder,ignore=shutil.ignore_patterns('scratch','__pycache__'))
        cfg=read(original/'run_config.json');arm=cfg['arm']
        inherited={str(p.relative_to(original)):sha(p) for p in (original/arm/'candidates').glob('*/trial.json')}
        def remap(value):
            if isinstance(value,list):return [remap(v) for v in value]
            if isinstance(value,dict):
                return {k:(v.replace(str(original),str(folder),1) if k=='directory' and isinstance(v,str) and v.startswith(str(original)) else remap(v)) for k,v in value.items()}
            return value
        for path in [folder/arm/'selected.json',folder/arm/'search_state.json',folder/'trained.json',
                     *(folder/arm/'candidates').glob('*/trial.json')]:
            if path.exists():write(path,remap(read(path)))
        selected=read(folder/arm/'selected.json');assert selected['successful_distinct']==20
        write(folder/'budgets/20/selected.json',selected)
        (folder/arm/'selected.json').rename(folder/'budgets/20/runtime_selected.json')
        if (folder/'trained.json').exists():(folder/'trained.json').rename(folder/'inherited_trained20.json')
        # Historical request/response messages are copied byte-for-byte.
        for path in (original/'api_attempts').rglob('*.json'):
            assert sha(path)==sha(folder/path.relative_to(original))
        write(provenance,{'source':str(original),'source_selected_sha256':sha(original/arm/'selected.json'),
              'source_config_sha256':sha(original/'run_config.json'),'inherited_trial_sha256':inherited,
              'original_actual_POST':len(list((original/'api_attempts').glob('attempt_*'))),
              'data_manifest_sha256':sha(DATA/f'fold_{fold}/bundle/manifest.json'),
              'continuation_not_independent_restart':True,'previously_inspected_test':True})
    return folder,runtime

def config(fold,mode,budget,folder,runtime):
    cfg=read(OLD/f'fold_{fold}'/mode/'run_config.json')
    cfg.update(protocol=f'hm_medium_followup_f{fold}_{mode}_budget{budget}_seed42_v1',
        target_successful_distinct=budget,max_llm_calls=300,test_previously_inspected=True,
        runtime_sha256={p.name:sha(p) for p in runtime.glob('*.py')},
        continuation_from=str(OLD/f'fold_{fold}'/mode),budget_checkpoint=budget)
    path=folder/f'run_config_budget{budget}.json'
    if path.exists():assert read(path)==cfg,'Changed config under existing budget'
    else:write(path,cfg)
    return cfg,path

def run(fold,mode,stage):
    locks=OUT/'locks';locks.mkdir(parents=True,exist_ok=True)
    with (locks/f'api_f{fold}_{mode}.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        folder,runtime=prepare(fold,mode)
        sys.path.insert(0,str(runtime))
        import runtime as api
        from provider_best import ProviderGenerator as BestGenerator
        from provider_history import ProviderGenerator as HistoryGenerator
        bundle=DATA/f'fold_{fold}/bundle'
        if stage=='train':
            assert read(REPORT/'api_validator_verification.json')['passed']
            for budget in [30,40]:
                checkpoint=folder/f'budgets/{budget}'
                if (checkpoint/'selected.json').exists():
                    assert read(checkpoint/'selected.json')['successful_distinct']==budget
                    continue
                cfg,cfgpath=config(fold,mode,budget,folder,runtime)
                selectedpath=folder/cfg['arm']/'selected.json'
                if selectedpath.exists():
                    prior=read(selectedpath)
                    if prior['successful_distinct']<budget:
                        assert (folder/f"budgets/{prior['successful_distinct']}/selected.json").exists()
                        selectedpath.replace(folder/f"budgets/{prior['successful_distinct']}/runtime_selected.json")
                generator=(HistoryGenerator if mode=='h009' else BestGenerator)(cfg,folder,ROOT/'.env')
                original_progress=api.progress
                def progress(directory,trials,settings):
                    valid=original_progress(directory,trials,settings)
                    record('followup_api_progress',f'Fold{fold} {mode} budget{budget}: {len(valid)} accepted/{len(trials)} responses.',
                           cfg['protocol'],status='searching',accepted=len(valid),responses=len(trials))
                    return valid
                api.progress=progress
                started=time.perf_counter()
                try:selected=api.search(bundle,folder/cfg['arm'],generator,cfgpath)
                finally:api.progress=original_progress
                assert selected['budget_complete'] and selected['successful_distinct']==budget
                write(checkpoint/'selected.json',selected)
                write(checkpoint/'selection_manifest.json',{'config_sha256':sha(cfgpath),'selection_sha256':sha(checkpoint/'selected.json'),
                      'seconds_this_resume_segment':time.perf_counter()-started,
                      'actual_POST':len(list((folder/'api_attempts').glob('attempt_*'))),
                      'train_pairs_sha256':cfg['train_pair_sha256']})
                record('followup_api_budget_selected',f'Fold{fold} {mode}: selection at{budget} accepted frozen; no outer scoring yet.',
                       cfg['protocol'],status='selected_pending_test',artifacts=str(checkpoint.relative_to(ROOT)))
        else:
            assert (REPORT/'api_pretest_freeze.json').exists()
            for budget in [20,30,40]:
                destination=folder/f'budgets/{budget}'
                if (destination/'verification.json').exists():continue
                cfg,cfgpath=config(fold,mode,budget,folder,runtime)
                selected=read(destination/'selected.json');winner=Path(selected['directory'])
                assert sha(winner/'program.json')==selected['program_sha256']
                assert sha(winner/'model.txt')==selected['model_sha256']
                metric=api.evaluate(bundle,winner,'test',cfgpath)
                replay=api.evaluate(bundle,winner,'replay_test',cfgpath);assert replay['passed']
                pred=np.load(winner/'test_predictions.npy');target=pd.read_parquet(bundle/'test_targets.parquet')
                assert pred.shape==(len(target),12)
                hits=np.array([np.isin(p,np.unique(t)) for p,t in zip(pred,target.article_id)])
                ap=(hits*np.cumsum(hits,1)/np.arange(1,13)).sum(1)/np.minimum(12,[len(np.unique(t)) for t in target.article_id])
                assert abs(ap.mean()-metric['map'])<1e-12
                np.save(destination/'test_predictions.npy',pred);np.save(destination/'test_ap.npy',ap)
                write(destination/'test_metrics.json',metric)
                write(destination/'verification.json',{'passed':True,'full_replay':True,'independent_AP':True,
                      'reused_frozen_prediction_cache':(winner/'test_metrics.json').exists()})

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('fold',type=int)
    parser.add_argument('mode',choices=['h008','h009']);parser.add_argument('stage',choices=['train','evaluate'])
    args=parser.parse_args();run(args.fold,args.mode,args.stage)
