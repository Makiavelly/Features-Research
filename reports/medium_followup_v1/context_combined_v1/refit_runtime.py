def refit(fold, arm):
    import numpy as np
    import torch
    from torch_geometric.seed import seed_everything
    env = setup(fold, categorical=(arm in ('categorical','combined')))
    work = DEST/f'fold_{fold}'/arm
    work.mkdir(parents=True,exist_ok=True)
    if (work/'result.json').exists():
        print('REUSE',fold,arm,flush=True)
        return
    fanout = [64,32] if arm in ('fanout64','combined') else [32,16]
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
    result=dict(fold=fold,arm=arm,seed=42,fanout=fanout,changed_columns=CODE_COLUMNS if arm in ('categorical','combined') else [],
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
