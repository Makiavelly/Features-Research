"""Validation-only diagnostics and isolated categorical-feature ablation.

Never writes original runtime, checkpoints, graph caches or predictions.
"""
import argparse
import gc
import importlib.util
import inspect
import json
import os
from pathlib import Path
import sys
import time

os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')
from common import ROOT, OLD, OUT, REPORT, read, write, sha, record

RUN = 'hm_medium_context_first3_seed42_v1'
DEST = OUT / 'context_first3_v1'
REP = REPORT / 'context_first3_v1'
CODE_COLUMNS = ['colour_group_code', 'department_no', 'graphical_appearance_no',
                'perceived_colour_master_id', 'perceived_colour_value_id',
                'product_type_no', 'section_no', 'product_code']


def setup(fold, categorical=False):
    import torch
    runtime = OUT / f'fold_{fold}/runtime/gnn_timefix_refit'
    source = runtime / 'gnn.py'
    sys.path.insert(0, str(runtime))
    # Each fold's cv_graph has the same implementation; load the frozen runtime.
    sys.modules.pop('cv_graph', None)
    spec = importlib.util.spec_from_file_location(f'first3_fold{fold}', source)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    work = DEST / f'fold_{fold}' / ('categorical' if categorical else 'diagnostic')
    work.mkdir(parents=True, exist_ok=True)
    mod.OUT = work
    mod.record = lambda *a, **kw: None
    prefix = inspect.getsource(mod.main).split('    sampling_audit=[]')[0]
    # Use the runtime setup and model factory verbatim, bypassing all training,
    # evaluation and writes to original result folders.
    prefix = prefix.replace('def main():', 'def prepare():', 1)
    if categorical:
        prefix = prefix.replace('    data, stats = make_pkey_fkey_graph',
            "    from torch_frame import stype\n"
            f"    for column in {CODE_COLUMNS!r}:\n"
            "        schema['article'][column] = stype.categorical\n"
            "    data, stats = make_pkey_fkey_graph")
        mod.CACHE = work / 'cache'
    prefix += '    return locals()\n'
    sys.argv = ['context_first3']
    exec(compile(prefix, str(source) + ':isolated_setup', 'exec'), mod.__dict__)
    env = mod.prepare()
    env['module'] = mod
    env['source'] = source
    env['original'] = OUT / f'fold_{fold}/gnn_timefix_refit/contextgnn'
    env['work'] = work
    return env


def labels(env, split):
    task = env['task']
    df = env['tables'][split].df
    return [set(map(int, v)) for v in df[task.dst_entity_col]]


def aps(pred, targets):
    import numpy as np
    result = []
    for rec, target in zip(pred, targets):
        hits = np.array([int(x) in target for x in rec], dtype=float)
        result.append(float((hits * np.cumsum(hits) / np.arange(1, 13)).sum()
                            / min(12, len(target))) if target else 0.)
    return np.array(result)


def loader(env, split, fanout, shuffle=False):
    import torch
    from torch_geometric.loader import NeighborLoader
    mod, task = env['module'], env['task']
    table = env['tables'][split]
    return NeighborLoader(env['data'], num_neighbors=fanout, time_attr='time',
        input_nodes=(task.src_entity_table, torch.from_numpy(table.df[task.src_entity_col].to_numpy())),
        input_time=torch.from_numpy(mod.unix_seconds(table.df.timestamp)),
        subgraph_type='bidirectional', batch_size=128, temporal_strategy='last',
        shuffle=shuffle, num_workers=0)


def check_time(batch, task):
    seed = batch[task.src_entity_table].seed_time
    assert int(seed.min()) > 1_000_000_000
    for kind, times in batch.time_dict.items():
        assert not (times > seed[batch[kind].batch]).any(), 'Future transaction'


def coverage(env, split, fanout):
    import numpy as np
    from torch_geometric.seed import seed_everything
    seed_everything(42)
    target = labels(env, split)
    task, n = env['task'], env['catalog_size']
    rows = []
    for batch in loader(env, split, fanout):
        check_time(batch, task)
        idx = batch[task.src_entity_table].input_id.numpy()
        groups = batch[task.dst_entity_table].batch.numpy()
        ids = batch[task.dst_entity_table].n_id.numpy()
        for j, i in enumerate(idx):
            local = set(map(int, ids[groups == j]))
            truth = target[int(i)]
            eligible = {x for x in truth if 0 <= x < n}
            rows.append(dict(input_id=int(i), local=len(local), positives=len(truth),
                             in_catalog=len(eligible), covered=len(eligible & local)))
    assert sorted(x['input_id'] for x in rows) == list(range(len(target)))
    totals = {key:sum(x[key] for x in rows) for key in ['positives','in_catalog','covered']}
    return dict(users=len(rows), **totals,
        covered_fraction_in_catalog=totals['covered']/max(1,totals['in_catalog']),
        covered_fraction_all=totals['covered']/max(1,totals['positives']),
        mean_local=float(np.mean([x['local'] for x in rows])), rows=rows)


def branch_eval(env, model, fanout):
    import numpy as np
    import torch
    from torch_geometric.seed import seed_everything
    task, device = env['task'], env['device']
    targets = labels(env, 'val')
    model.eval()
    env['module'].clear_rhs(model)
    seed_everything(42)
    predictions = {name:[] for name in ['original','global','blend25','blend50','blend75']}
    local_count = 0
    rows = []
    raw_scores = []
    with torch.no_grad():
        for batch in loader(env, 'val', fanout):
            batch = batch.to(device)
            check_time(batch, task)
            x = model.forward_gnn(batch, task.src_entity_table)
            count = batch[task.src_entity_table].batch_size
            lhs = x[task.src_entity_table][:count]
            projected = model.lhs_projector(lhs)
            rhs_gnn = x[task.dst_entity_table]
            groups = batch[task.dst_entity_table].batch
            ids = batch[task.dst_entity_table].n_id
            rhs = model.rhs_embedding()
            global_scores = projected @ rhs.t() + model.lin_offset_embgnn(projected).flatten()[:,None]
            local = model.head(rhs_gnn).flatten() + (lhs[groups]*rhs_gnn).sum(-1)
            local += model.lin_offset_idgnn(projected).flatten()[groups]
            original = model.construct_logits(projected,lhs,rhs_gnn,rhs,groups,ids)
            reconstructed = global_scores.clone()
            reconstructed[groups,ids] = local
            torch.testing.assert_close(original,reconstructed,rtol=0,atol=0)
            mask = torch.zeros_like(original,dtype=torch.bool)
            mask[groups,ids] = True
            variants = {'original':original,'global':global_scores}
            for name,alpha in [('blend25',.25),('blend50',.5),('blend75',.75)]:
                score = global_scores.clone()
                score[groups,ids] = (1-alpha)*global_scores[groups,ids] + alpha*local
                variants[name] = score
            batch_pred = {}
            for name,score in variants.items():
                assert torch.isfinite(score).all()
                top = torch.argsort(score,dim=1,descending=True,stable=True)[:,:12]
                batch_pred[name] = top.cpu().numpy()
                predictions[name].append(batch_pred[name])
                if name == 'original':
                    local_count += int(mask.gather(1,top).sum())
            raw_scores.append(original.cpu().numpy())
            for j,i in enumerate(batch[task.src_entity_table].input_id.cpu().numpy()):
                truth = targets[int(i)]
                g = set(map(int,batch_pred['global'][j])) & truth
                o = set(map(int,batch_pred['original'][j])) & truth
                rows.append(dict(input_id=int(i),global_hits=len(g),original_hits=len(o),
                    lost_global_hits=len(g-o),gained_hits=len(o-g)))
    all_pred = {name:np.concatenate(value) for name,value in predictions.items()}
    ap = {name:aps(value,targets) for name,value in all_pred.items()}
    for name,pred in all_pred.items():
        official = task.evaluate(pred,env['tables']['val'])['map']
        assert abs(official-float(ap[name].mean())) < 1e-10
    return dict(map={name:float(value.mean()) for name,value in ap.items()},
        local_top12_fraction=local_count/(12*len(targets)),
        lost_global_hits=sum(x['lost_global_hits'] for x in rows),
        gained_hits=sum(x['gained_hits'] for x in rows),
        users_hurt=int((ap['original']<ap['global']).sum()),
        users_helped=int((ap['original']>ap['global']).sum()),
        rows=rows), all_pred, ap, np.concatenate(raw_scores)


def diagnose(fold):
    import numpy as np
    import torch
    env = setup(fold)
    original = env['original']
    checkpoint_hash = sha(original/'best.pt')
    np.save(env['work']/'val_customer_ids.npy',env['tables']['val'].df[env['task'].src_entity_col].to_numpy())
    model = env['make_model']('contextgnn')
    model.load_state_dict(torch.load(original/'best.pt',map_location=env['device'])['model_state_dict'])
    schema = {t:{str(kind):columns for kind,columns in env['data'][t].tf.col_names_dict.items()}
              for t in env['data'].node_types}
    result = dict(fold=fold,checkpoint_sha256=checkpoint_hash,materialized_schema=schema,
        source_sha256=sha(env['source']), validation_only=True, no_refitting=True, fanouts={})
    for fanout in [[32,16],[64,32]]:
        key = '_'.join(map(str,fanout))
        print('COVERAGE',fold,key,flush=True)
        item = {'coverage':{split:coverage(env,split,fanout) for split in ['train','val']}}
        branches,pred,ap,scores = branch_eval(env,model,fanout)
        item['branches'] = branches
        for name,value in ap.items():
            np.save(env['work']/f'{key}_{name}_ap.npy',value)
            np.save(env['work']/f'{key}_{name}_predictions.npy',pred[name])
        if fanout == [32,16]:
            saved = np.load(original/'val_predictions.npy')
            reference = np.load(original/'val_scores.npy',mmap_mode='r')
            max_diff = float(np.abs(reference-scores).max())
            same_ap = np.array_equal(aps(saved,labels(env,'val')),ap['original'])
            # Existing documented FP32 replay limit; no relaxation based on MAP.
            tolerance = 32*np.finfo(np.float32).eps*max(1.,float(np.abs(reference).max()))
            bounded = bool(np.isfinite(scores).all() and max_diff <= tolerance)
            ranked_close = bool(np.allclose(np.take_along_axis(scores,pred['original'],axis=1),
                np.take_along_axis(reference,saved,axis=1),atol=2*tolerance,rtol=0))
            assert bounded and ranked_close and same_ap, f'Replay failed fold{fold}: {max_diff}, AP={same_ap}'
            result['replay'] = dict(max_abs_score_difference=max_diff,
                predictions_identical=bool(np.array_equal(saved,pred['original'])),
                all_user_ap_identical=same_ap,scores_within_documented_fp32_bound=bounded)
        result['fanouts'][key] = item
        write(env['work']/'diagnostics.json',result)
        print('RESULT',fold,key,json.dumps(branches['map']),flush=True)
    assert sha(original/'best.pt') == checkpoint_hash
    record('context_first3_diagnostic',f'Fold{fold}: train/validation coverage, schemas, frozen-weight fanout and branch probes complete; no test evaluation.',
        RUN+f'_fold{fold}_diagnostic',status='diagnostic_complete',artifacts=str(env['work'].relative_to(ROOT)))
    del model,env
    gc.collect()
    torch.cuda.empty_cache()


def refit(fold, arm):
    import numpy as np
    import torch
    from torch_geometric.seed import seed_everything
    env = setup(fold, categorical=(arm == 'categorical'))
    work = DEST/f'fold_{fold}'/arm
    work.mkdir(parents=True,exist_ok=True)
    if (work/'result.json').exists():
        print('REUSE',fold,arm,flush=True)
        return
    fanout = [64,32] if arm == 'fanout64' else [32,16]
    task,device,mod = env['task'],env['device'],env['module']
    model = env['make_model']('contextgnn')
    optimizer = torch.optim.Adam(model.parameters(),lr=.001)
    train_loader = loader(env,'train',fanout,shuffle=True)
    targets = labels(env,'val')
    np.save(DEST/f'fold_{fold}/diagnostic/val_customer_ids.npy',env['tables']['val'].df[task.src_entity_col].to_numpy())
    @torch.no_grad()
    def evaluate():
        model.eval()
        mod.clear_rhs(model)
        seed_everything(42)
        parts=[]
        for batch in loader(env,'val',fanout):
            batch=batch.to(device)
            check_time(batch,task)
            score=model(batch,task.src_entity_table,task.dst_entity_table)
            assert torch.isfinite(score).all()
            parts.append(score.cpu().numpy())
        scores=np.concatenate(parts)
        pred=np.argsort(-scores,axis=1,kind='stable')[:,:12]
        ap=aps(pred,targets)
        assert abs(float(ap.mean())-task.evaluate(pred,env['tables']['val'])['map'])<1e-10
        return pred,ap,scores
    run_id=RUN+f'_fold{fold}_{arm}'
    record('context_first3_refit_started',f'Fold{fold}: isolated {arm} ContextGNN ablation, seed42, original optimizer/early stopping; validation only.',run_id,status='training')
    history=[]
    best=-1.
    stale=0
    started=time.perf_counter()
    torch.cuda.reset_peak_memory_stats()
    for epoch in range(1,11):
        model.train()
        mod.clear_rhs(model)
        losses=[]
        for batch in train_loader:
            batch=batch.to(device)
            check_time(batch,task)
            src,dst=env['sparse_labels'][batch[task.src_entity_table].input_id]
            optimizer.zero_grad()
            output=model(batch,task.src_entity_table,task.dst_entity_table)
            loss=mod.sparse_ce(output,src,dst)
            assert torch.isfinite(loss)
            loss.backward()
            optimizer.step()
            losses.append(float(loss))
        pred,ap,scores=evaluate()
        metric=float(ap.mean())
        if metric>best:
            best=metric
            best_epoch=epoch
            stale=0
            torch.save({'model_state_dict':model.state_dict(),'epoch':epoch,'arm':arm,'fanout':fanout},work/'best.pt')
            np.save(work/'val_predictions.npy',pred)
            np.save(work/'val_ap.npy',ap)
            np.save(work/'val_scores.npy',scores)
        else:
            stale+=1
        history.append(dict(epoch=epoch,train_loss=float(np.mean(losses)),val_map=metric,steps=len(losses)))
        write(work/'history.json',history)
        print('EPOCH',fold,arm,json.dumps(history[-1]),flush=True)
        record('context_first3_epoch',f'Fold{fold} {arm}: epoch{epoch}, validation MAP={100*metric:.5f}%',run_id,status='training',epoch=epoch,val_metrics={'map':metric})
        if stale>=3:
            break
    checkpoint_hash=sha(work/'best.pt')
    model.load_state_dict(torch.load(work/'best.pt',map_location=device)['model_state_dict'])
    pred,ap,scores=evaluate()
    saved=np.load(work/'val_scores.npy',mmap_mode='r')
    tolerance=32*np.finfo(np.float32).eps*max(1.,float(np.abs(saved).max()))
    assert float(np.abs(saved-scores).max())<=tolerance
    assert np.array_equal(ap,np.load(work/'val_ap.npy'))
    assert sha(work/'best.pt')==checkpoint_hash
    result=dict(fold=fold,arm=arm,seed=42,fanout=fanout,changed_columns=CODE_COLUMNS if arm=='categorical' else [],
        val_map=float(ap.mean()),best_epoch=best_epoch,epochs=len(history),seconds=time.perf_counter()-started,
        checkpoint_sha256=checkpoint_hash,source_sha256=sha(Path(__file__)),
        validation_only=True,verification='reload: bounded FP32 scores and exact per-user AP; independent MAP',
        peak_cuda_bytes=torch.cuda.max_memory_allocated(),
        materialized_schema={t:{str(k):v for k,v in env['data'][t].tf.col_names_dict.items()} for t in env['data'].node_types})
    write(work/'result.json',result)
    record('context_first3_refit_complete',f'Fold{fold} {arm}: validation-only ablation complete; weights reloaded, independent AP verified.',run_id,status='validation_verified',val_metrics={'map':result['val_map']},artifacts=str(work.relative_to(ROOT)))
    del model,optimizer,env,train_loader
    gc.collect()
    torch.cuda.empty_cache()


def summarize():
    import numpy as np
    records=[]
    for fold in range(3):
        diag=read(DEST/f'fold_{fold}/diagnostic/diagnostics.json')
        for key,item in diag['fanouts'].items():
            for split,c in item['coverage'].items():
                records.append(dict(fold=fold,fanout=key,split=split,**{k:v for k,v in c.items() if k!='rows'}))
    variants={}
    baseline=np.concatenate([np.load(DEST/f'fold_{f}/diagnostic/32_16_original_ap.npy') for f in range(3)])
    customers=np.concatenate([np.load(DEST/f'fold_{f}/diagnostic/val_customer_ids.npy') for f in range(3)])
    unique,inverse=np.unique(customers,return_inverse=True)
    cluster_n=np.bincount(inverse)
    for name in ['original','global','blend25','blend50','blend75','fanout64_frozen','categorical_refit','fanout64_refit']:
        arrays=[]
        for f in range(3):
            if name.endswith('_refit'):
                path=DEST/f'fold_{f}'/name[:-6]/'val_ap.npy'
            else:
                path=DEST/f'fold_{f}/diagnostic'/('64_32_original_ap.npy' if name=='fanout64_frozen' else f'32_16_{name}_ap.npy')
            if not path.exists():
                break
            arrays.append(np.load(path))
        if len(arrays)!=3:
            continue
        value=np.concatenate(arrays)
        difference=value-baseline
        cluster_sum=np.bincount(inverse,weights=difference)
        rng=np.random.default_rng(42)
        boot=[]
        for _ in range(5000):
            ix=rng.integers(0,len(unique),size=len(unique))
            boot.append(cluster_sum[ix].sum()/cluster_n[ix].sum())
        variants[name]=dict(fold_map=[float(v.mean()) for v in arrays],pooled_map=float(value.mean()),
            delta_map=float(difference.mean()),delta_customer_bootstrap95=list(map(float,np.quantile(boot,[.025,.975]))))
    result=dict(validation_only=True,validation_rows=len(baseline),unique_customers=len(unique),
        caveat='Exploratory on checkpoint-selection validation; intervals conditional on trained models, unadjusted. No independent improvement claim.',coverage=records,variants=variants)
    write(REP/'summary.json',result)
    print(json.dumps(result,indent=2),flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage',choices=['diagnose','refit','summary'])
    parser.add_argument('--arm',choices=['categorical','fanout64'],default='categorical')
    parser.add_argument('--fold',type=int,choices=[0,1,2])
    args = parser.parse_args()
    REP.mkdir(parents=True,exist_ok=True)
    if args.stage=='summary':
        summarize()
        return
    record('context_first3_started','Authorized first three ContextGNN checks: validation-only subgraph coverage/fanout, materialized feature types, local/global branch probes. Existing H010 CPU/API process left untouched.',RUN,status='diagnosing',artifacts=str(REP.relative_to(ROOT)))
    for fold in ([args.fold] if args.fold is not None else range(3)):
        if args.stage=='diagnose':
            diagnose(fold)
        else:
            refit(fold,args.arm)
    write(REP/'diagnostics.json',{str(f):read(DEST/f'fold_{f}/diagnostic/diagnostics.json')
                                for f in range(3) if (DEST/f'fold_{f}/diagnostic/diagnostics.json').exists()})


if __name__ == '__main__':
    main()
