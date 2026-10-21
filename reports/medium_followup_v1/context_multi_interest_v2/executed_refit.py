def fit(fold,arm,weight):
    from torch_geometric.seed import seed_everything
    work=DEST/f'fold_{fold}'/arm;work.mkdir(parents=True,exist_ok=True)
    if (work/'result.json').exists():
        result=read(work/'result.json');assert sha(work/'best.pt')==result['checkpoint_sha256'];return
    assert not (work/'history.json').exists(),'Partial training preserved; investigate before restart'
    wait_for_resources(f'f{fold}_{arm}')
    env=base.setup(fold,categorical=True)
    task,device,mod=env['task'],env['device'],env['module']
    assert device.type=='cuda'
    annotations=read(DEST/f'fold_{fold}/annotations.json')
    assert [a['targets'] for a in annotations]==[sorted(t) for t in base.labels(env,'val')]
    assert [a['mapped_customer'] for a in annotations]==env['tables']['val'].df[task.src_entity_col].tolist()
    model=env['make_model']('contextgnn')
    initial_state=model._fusion_initial_fingerprint
    if arm in ('interest1','interest4'):
        assert initial_state==read(DEST/f'fold_{fold}/control/result.json')['initial_state_sha256']
    optimizer=torch.optim.Adam(model.parameters(),lr=.001)
    train_loader=base.loader(env,'train',FANOUT,shuffle=True)
    targets=base.labels(env,'val')
    native_checks=[]
    replay_checks={}
    @torch.no_grad()
    def evaluate(check_native=False):
        model.eval();mod.clear_rhs(model);seed_everything(42)
        parts={'hybrid':[],'global':[]}
        for batch in base.loader(env,'val',FANOUT):
            batch=batch.to(device);base.check_time(batch,task)
            hybrid,global_scores=forward_pair(model,batch,task)
            if check_native:
                native=model(batch,task.src_entity_table,task.dst_entity_table)
                bound=32*torch.finfo(hybrid.dtype).eps*max(1.,float(native.abs().max()))
                assert float((hybrid-native).abs().max())<=bound,'Dual forward exceeds FP32 bound'
                native_checks.append(replay_check(hybrid.cpu().numpy(),native.cpu().numpy(),[targets[int(i)] for i in batch[task.src_entity_table].input_id.cpu()]))
            for key,score in [('hybrid',hybrid),('global',global_scores)]:
                assert torch.isfinite(score).all();parts[key].append(score.cpu().numpy())
        return {key:np.concatenate(value) for key,value in parts.items()}
    run_id=RUN+f'_f{fold}_{arm}'
    record('multi_interest_fit_started',f'Fold{fold} {arm}: lambda={weight}, matched initialization/training, validation only.',run_id,status='training',artifacts=str(work.relative_to(ROOT)))
    best=-1.;stale=0;history=[];started=time.perf_counter();torch.cuda.reset_peak_memory_stats()
    for epoch in range(1,11):
        model.train();mod.clear_rhs(model);losses=[]
        graph_hash=hashlib.sha256()
        for batch in train_loader:
            graph_hash.update(batch[task.src_entity_table].input_id.numpy().tobytes())
            for node_type in sorted(batch.node_types):
                graph_hash.update(node_type.encode());graph_hash.update(batch[node_type].n_id.numpy().tobytes())
            for edge_type in sorted(batch.edge_types):
                graph_hash.update(str(edge_type).encode());graph_hash.update(batch[edge_type].edge_index.numpy().tobytes())
            batch=batch.to(device);base.check_time(batch,task)
            src,dst=env['sparse_labels'][batch[task.src_entity_table].input_id]
            optimizer.zero_grad()
            hybrid,global_scores=forward_pair(model,batch,task)
            mixed_loss=mod.sparse_ce(hybrid,src,dst);global_loss=mod.sparse_ce(global_scores,src,dst)
            loss=mixed_loss+weight*global_loss if weight else mixed_loss
            assert torch.isfinite(loss);loss.backward();optimizer.step()
            losses.append((float(mixed_loss.detach()),float(global_loss.detach()),float(loss.detach())))
        scores=evaluate()
        pred=np.argsort(-scores['hybrid'],axis=1,kind='stable')[:,:12]
        ap=base.aps(pred,targets);metric=float(ap.mean())
        assert abs(metric-task.evaluate(pred,env['tables']['val'])['map'])<1e-10
        global_ap=base.aps(np.argsort(-scores['global'],axis=1,kind='stable')[:,:12],targets)
        if metric>best:
            best=metric;best_epoch=epoch;stale=0
            torch.save(dict(model_state_dict=model.state_dict(),epoch=epoch,lambda_global=weight,arm=arm),work/'best.pt')
            for key,value in scores.items():np.save(work/f'val_{key}_scores.npy',value)
            np.save(work/'val_ap.npy',ap);np.save(work/'val_predictions.npy',pred)
        else:stale+=1
        means=np.mean(losses,axis=0)
        item=dict(epoch=epoch,mixed_loss=float(means[0]),global_loss=float(means[1]),total_loss=float(means[2]),val_map=metric,global_map=float(global_ap.mean()),steps=len(losses),training_graph_sha256=graph_hash.hexdigest())
        if arm in ('interest1','interest4'):
            control_history=read(DEST/f'fold_{fold}/control/history.json')
            if epoch<=len(control_history):assert item['training_graph_sha256']==control_history[epoch-1]['training_graph_sha256']
        history.append(item);write(work/'history.json',history)
        print('EPOCH',fold,arm,json.dumps(item),flush=True)
        record('multi_interest_epoch',f'Fold{fold} {arm} epoch{epoch}: hybrid MAP {100*metric:.5f}%, global MAP {100*global_ap.mean():.5f}%.',run_id,status='training',epoch=epoch,val_metrics={'map':metric})
        if stale>=3:break
    checkpoint=sha(work/'best.pt')
    model.load_state_dict(torch.load(work/'best.pt',map_location=device)['model_state_dict'])
    replay=evaluate(check_native=True)
    for key,value in replay.items():
        saved=np.load(work/f'val_{key}_scores.npy')
        tolerance=32*np.finfo(np.float32).eps*max(1.,float(np.abs(saved).max()))
        assert np.max(np.abs(saved-value))<=tolerance
        replay_checks[key]=replay_check(saved,value,targets)
        np.save(work/f'verification_replay_{key}_scores.npy',value)
    write(work/'replay_verification.json',dict(native=native_checks,reload=replay_checks,canonical_scores_retained=True))
    historical_equal=None
    if arm=='control':
        prior=np.load(REF/f'fold_{fold}/combined/val_scores.npy')
        historical_equal=bool(np.array_equal(np.load(work/'val_ap.npy'),np.load(REF/f'fold_{fold}/combined/val_ap.npy')))
    assert sha(work/'best.pt')==checkpoint
    write(work/'result.json',dict(fold=fold,arm=arm,lambda_global=weight,validation_only=True,val_map=best,
        best_epoch=best_epoch,epochs=len(history),seconds=time.perf_counter()-started,peak_cuda_bytes=torch.cuda.max_memory_allocated(),
        checkpoint_sha256=checkpoint,protocol_sha256=sha(REP/'protocol.json'),
        verification='FP32-bounded reload, quantified rank/AP sensitivity, independent canonical AP',
        initial_state_sha256=initial_state,previous_control_ap_equal=historical_equal,
        comparison_control='Fresh lambda0 fit with identical initial state and same epoch training graphs; historical metrics are contextual only'))
    record('multi_interest_fit_verified',f'Fold{fold} {arm}: checkpoint and both ranking branches reloaded and verified.',run_id,status='validation_verified',val_metrics={'map':best},artifacts=str(work.relative_to(ROOT)))
    del model,optimizer,env,train_loader,replay,scores
    gc.collect();torch.cuda.empty_cache()
