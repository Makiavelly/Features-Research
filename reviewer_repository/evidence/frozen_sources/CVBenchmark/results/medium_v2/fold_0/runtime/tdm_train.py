"""Train both TDM variants before any test scoring; separately replay frozen outputs."""
import argparse
import copy
import json
from pathlib import Path
import sys
import time

import numpy as np
import torch
from torch.nn import functional as F
from tdm_common import (ROOT,OUT,CONFIG,Dataset,TDM,seed,dump,sha,record,build_tree,
                    tree_digest,mapped_history,sample_pairs,evaluate,pair_ranges)

PIPELINE='hm_medium_cv_v2_fold0_tdm'

def run_id(variant):
    return f'hm_medium_cv_v2_fold0_tdm_{variant}'

def load(variant,device):
    checkpoint=torch.load(OUT/variant/'best.pt',map_location='cpu',weights_only=False)
    tree=checkpoint['tree']
    assert tree_digest(tree)==checkpoint['tree_sha256']
    seed()
    model=TDM(tree).to(device)
    model.load_state_dict(checkpoint['state'],strict=True)
    return model,tree,checkpoint

def train(variant,tree,dataset,device,prerequisite):
    directory=OUT/variant
    directory.mkdir(parents=True,exist_ok=True)
    assert not (directory/'config.json').exists(),'Existing training directory; do not silently restart'
    seed()
    model=TDM(tree).to(device)
    optim=torch.optim.Adam(model.parameters(),lr=CONFIG['lr'])
    config=dict(CONFIG,variant=variant,run_id=run_id(variant),subset_sha256=dataset.fingerprint,
                data_hashes=dataset.hashes,tree_sha256=tree_digest(tree),prerequisite=prerequisite,
                code_sha256={p.name:sha(p) for p in sorted((ROOT/'TDM').glob('*.py'))},
                torch_version=torch.__version__,gpu=torch.cuda.get_device_name(),
                trainable_parameters=sum(p.numel() for p in model.parameters()))
    dump(directory/'config.json',config)
    np.savez(directory/'tree.npz',**tree)
    record('tdm_training_start','TDM small weekly training; fixed validation selection',run_id(variant),status='training',config=config)
    histories=mapped_history(dataset.history['train'],tree)
    history=[]; best=-1.; stale=0; best_epoch=0
    started=time.perf_counter()
    torch.cuda.reset_peak_memory_stats()
    for epoch in range(1,CONFIG['max_epochs']+1):
        epoch_start=time.perf_counter()
        model.train()
        rng=np.random.default_rng(42+epoch)
        order=rng.permutation(len(histories))
        total_loss=0.
        for off in range(0,len(order),CONFIG['batch']):
            idx=order[off:off+CONFIG['batch']]
            row,nodes,label,weight=sample_pairs(dataset.targets['train'],idx,tree,rng)
            assert np.isclose(weight.sum(),1.)
            optim.zero_grad(set_to_none=True)
            step_loss=0.
            for pos,stop in pair_ranges(len(nodes)):
                h=torch.as_tensor(histories[idx[row[pos:stop]]],device=device)
                q=torch.as_tensor(nodes[pos:stop],device=device)
                y=torch.as_tensor(label[pos:stop],device=device)
                w=torch.as_tensor(weight[pos:stop],device=device)
                logits=model(h,q)
                loss=(F.binary_cross_entropy_with_logits(logits,y,reduction='none')*w).sum()
                assert torch.isfinite(loss)
                loss.backward()
                step_loss+=float(loss.detach())
            torch.nn.utils.clip_grad_norm_(model.parameters(),5.,error_if_nonfinite=True)
            optim.step()
            total_loss+=step_loss*len(idx)
        metric,_=evaluate(model,tree,dataset,'val','beam',device)
        seconds=time.perf_counter()-epoch_start
        row=dict(epoch=epoch,train_loss=total_loss/len(histories),val_metrics=metric,
                 epoch_seconds=seconds,train_rows=len(order))
        history.append(row)
        if metric['map']>best:
            best=metric['map'];best_epoch=epoch;stale=0
            torch.save(dict(state=model.state_dict(),tree=tree,tree_sha256=tree_digest(tree),
                            config=config,epoch=epoch,val_metrics=metric),directory/'best.pt')
        else: stale+=1
        dump(directory/'history.json',history)
        print(json.dumps(dict(variant=variant,**row)),flush=True)
        record('tdm_epoch','TDM complete epoch and beam validation',run_id(variant),status='training',epoch=epoch,
               val_metrics={'map':best},best_epoch=best_epoch,train_loss=row['train_loss'])
        if epoch>=CONFIG['minimum_epochs'] and stale>=CONFIG['patience']:
            stop_reason='patience4';break
        if epoch>=CONFIG['minimum_epochs'] and time.perf_counter()-started+seconds>CONFIG['max_training_seconds']:
            stop_reason='training_time_budget';break
    else: stop_reason='max_epochs'
    summary=dict(best_epoch=best_epoch,epochs=len(history),best_validation_map=best,
                 training_and_validation_seconds=time.perf_counter()-started,
                 peak_cuda_bytes=torch.cuda.max_memory_allocated(),stop_reason=stop_reason,
                 checkpoint_sha256=sha(directory/'best.pt'),tree_sha256=tree_digest(tree))
    dump(directory/'training_summary.json',summary)
    record('tdm_training_complete','TDM training complete; test not evaluated',run_id(variant),
           status='trained_pending_test',epoch=len(history),val_metrics={'map':best},artifacts=str(directory.relative_to(ROOT)),summary=summary)
    del model,optim
    torch.cuda.empty_cache()

def training(dataset,device):
    assert not OUT.exists(),'New protocol/run directory required; no overwrite of previous execution'
    OUT.mkdir(parents=True)
    start=time.perf_counter()
    fixed=build_tree(5000,categories=dataset.article.product_type_no.to_numpy())
    fixed_seconds=time.perf_counter()-start
    dump(OUT/'data_checks.json',dict(subset_sha256=dataset.fingerprint,files=dataset.hashes,
         rows={s:len(x) for s,x in dataset.history.items()},train_seen_items=len(dataset.train_seen),
         history_policy='past-only t_dat<=cutoff,source-order ties,recent50 reversed',
         history_sha256={s:__import__('hashlib').sha256(x.tobytes()).hexdigest() for s,x in dataset.history.items()}))
    train('fixed',fixed,dataset,device,dict(initial_tree_seconds=fixed_seconds))
    model,tree,checkpoint=load('fixed',device)
    embeddings=model.embedding.weight.detach().cpu().numpy()[tree['leaves']].copy()
    np.save(OUT/'fixed/cluster_source_embeddings.npy',embeddings)
    source_sha=sha(OUT/'fixed/best.pt')
    del model,checkpoint
    torch.cuda.empty_cache()
    start=time.perf_counter()
    cluster=build_tree(5000,embeddings=embeddings)
    cluster_seconds=time.perf_counter()-start
    prerequisite=dict(source_checkpoint_sha256=source_sha,clustering_seconds=cluster_seconds,
                      method='recursive balanced KMeans2 distance difference; no JTM',
                      initialization='fresh seed42; no weight warm start',
                      fixed_training_seconds=json.loads((OUT/'fixed/training_summary.json').read_text())['training_and_validation_seconds'])
    dump(OUT/'cluster_provenance.json',prerequisite)
    train('cluster',cluster,dataset,device,prerequisite)
    selection={v:dict(checkpoint_sha256=sha(OUT/v/'best.pt'),
                      tree_sha256=json.loads((OUT/v/'config.json').read_text())['tree_sha256'],
                      summary=json.loads((OUT/v/'training_summary.json').read_text())) for v in ['fixed','cluster']}
    dump(OUT/'selection_pretest.json',dict(selections=selection,criterion='validation beam64 MAP only',test_not_evaluated=True))
    record('tdm_pretest_frozen','Both TDM models and trees fixed before test scoring',PIPELINE,status='selected',selection=selection)

def evaluation(dataset,device,verify):
    frozen=json.loads((OUT/'selection_pretest.json').read_text())
    checks={}
    for variant in ['fixed','cluster']:
        assert sha(OUT/variant/'best.pt')==frozen['selections'][variant]['checkpoint_sha256']
        model,tree,checkpoint=load(variant,device)
        current={p.name:sha(p) for p in sorted((ROOT/'TDM').glob('*.py'))}
        assert current==checkpoint['config']['code_sha256'],'Runner changed since training'
        assert dataset.fingerprint==checkpoint['config']['subset_sha256']
        assert dataset.hashes==checkpoint['config']['data_hashes']
        checks[variant]={}
        for mode in ['beam','full']:
            folder=OUT/variant/mode
            folder.mkdir(exist_ok=True)
            results={}
            for split in ['val','test']:
                metric,arrays=evaluate(model,tree,dataset,split,mode,device)
                key=f'{mode}_{split}'
                if verify:
                    comparisons={name:bool(np.array_equal(value,np.load(folder/f'{split}_{name}.npy'))) for name,value in arrays.items()}
                    comparisons['metric_identical']=metric['map']==json.loads((folder/'metrics.json').read_text())[f'{split}_metrics']['map']
                    checks[variant][key]=dict(passed=all(comparisons.values()),checks=comparisons,replay_seconds=metric['seconds'])
                    assert all(comparisons.values()),checks[variant][key]
                else:
                    assert not (folder/f'{split}_predictions.npy').exists(),'Existing scored result; no overwrite'
                    for name,value in arrays.items(): np.save(folder/f'{split}_{name}.npy',value)
                results[f'{split}_metrics']=metric
                print(json.dumps(dict(variant=variant,mode=mode,split=split,verify=verify,**metric)),flush=True)
            if not verify: dump(folder/'metrics.json',results)
        del model,checkpoint
        torch.cuda.empty_cache()
        if not verify:
            beam=json.loads((OUT/variant/'beam/metrics.json').read_text())
            record('tdm_scored','TDM weekly MAP measured; independent replay still required',run_id(variant),status='measured_pending_verification',
                   val_metrics={'map':beam['val_metrics']['map']},test_metrics={'map':beam['test_metrics']['map']})
    if verify:
        dump(OUT/'verification.json',dict(passed=True,checks=checks))
        record('tdm_verified','All eight TDM beam/full val/test replays matched exactly',PIPELINE+'_inference',status='verified',checks=checks)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('stage',choices=['train','evaluate','verify'])
    args=parser.parse_args()
    seed()
    assert torch.cuda.is_available()
    dataset=Dataset()
    device=torch.device('cuda')
    if args.stage=='train': training(dataset,device)
    else: evaluation(dataset,device,args.stage=='verify')

if __name__=='__main__':
    try: main()
    except Exception as e:
        record('tdm_error','TDM pipeline stage failed; artifacts retained',PIPELINE,status='failed',error=repr(e))
        raise
