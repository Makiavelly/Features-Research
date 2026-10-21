"""Quantify replay near-ties without refitting or replacing canonical scores."""
from pathlib import Path
import sys
import hashlib
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'CVFollowup'))
import context_global_aux_v3 as g
from common import read,write,sha,record
import torch
import numpy as np
from torch_geometric.seed import seed_everything

torch.set_num_threads(2)
g.base.RUN,g.base.DEST,g.base.REP=g.RUN,g.DEST,g.REP
work=g.DEST/'fold_2/global_ce'
assert not (work/'result.json').exists()
env=g.base.setup(2,categorical=True)
task,device,mod=env['task'],env['device'],env['module']
model=env['make_model']('contextgnn');initial=g.state_fingerprint(model)
assert initial==read(g.DEST/'fold_2/control/result.json')['initial_state_sha256']
checkpoint=sha(work/'best.pt')
state=torch.load(work/'best.pt',map_location=device)
model.load_state_dict(state['model_state_dict']);model.eval();mod.clear_rhs(model);seed_everything(42)
parts={'hybrid':[],'global':[]}
native_differences=[]
with torch.no_grad():
    for batch in g.base.loader(env,'val',g.FANOUT):
        batch=batch.to(device);g.base.check_time(batch,task)
        hybrid,glob=g.forward_pair(model,batch,task)
        native=model(batch,task.src_entity_table,task.dst_entity_table)
        bound=32*np.finfo(np.float32).eps*max(1.,float(native.abs().max()))
        difference=float((hybrid-native).abs().max());assert difference<=bound
        native_differences.append(dict(max_difference=difference,bound=bound))
        parts['hybrid'].append(hybrid.cpu().numpy());parts['global'].append(glob.cpu().numpy())
annotations=read(g.DEST/'fold_2/annotations.json')
mask=np.load(g.DEST/'fold_2/seen_mask.npy')
info={}
metric_comparisons=[]
for branch in ['hybrid','global']:
    replay=np.concatenate(parts[branch]);saved=np.load(work/f'val_{branch}_scores.npy')
    bound=32*np.finfo(np.float32).eps*max(1.,float(np.abs(saved).max()))
    difference=float(np.abs(replay-saved).max());assert difference<=bound
    np.save(work/f'verification_replay_{branch}_scores.npy',replay)
    a=np.argsort(-saved,axis=1,kind='stable')[:,:12];b=np.argsort(-replay,axis=1,kind='stable')[:,:12]
    changed=np.where(np.any(a!=b,axis=1))[0]
    for i in changed:
        # Any change must be explicable by the already documented FP32 bound.
        assert saved[i,b[i]].min()>=saved[i,a[i,-1]]-2*bound
        assert np.all(np.diff(saved[i,b[i]])<=2*bound)
    info[branch]=dict(max_score_difference=difference,bound=bound,changed_rows=changed.tolist(),changed_positions=int((a!=b).sum()),
        canonical_map=float(g.base.aps(a,g.base.labels(env,'val')).mean()),replay_map=float(g.base.aps(b,g.base.labels(env,'val')).mean()))
    modes=[(branch,a,b)]
    if branch=='hybrid':
        s=saved.copy();r=replay.copy();s[mask]=-np.inf;r[mask]=-np.inf
        modes.append(('new_only',np.argsort(-s,axis=1,kind='stable')[:,:12],np.argsort(-r,axis=1,kind='stable')[:,:12]))
    for mode,pred_a,pred_b in modes:
        for group in ['all','new']:
            for metric in ['map','available_recall']:
                values=[]
                for pred in [pred_a,pred_b]:
                    result=[g.novelty.per_user(rec,ann)[group][metric] for rec,ann in zip(pred,annotations)]
                    values.append(np.array([np.nan if x is None else x for x in result]))
                valid=np.isfinite(values[0]);assert np.array_equal(valid,np.isfinite(values[1]))
                metric_comparisons.append(dict(mode=mode,group=group,metric=metric,
                    canonical=float(values[0][valid].mean()),replay=float(values[1][valid].mean()),
                    max_per_user_difference=float(np.abs(values[0][valid]-values[1][valid]).max())))
history=read(work/'history.json');control=read(g.DEST/'fold_2/control/history.json')
for a,b in zip(history,control):assert a['training_graph_sha256']==b['training_graph_sha256']
assert sha(work/'best.pt')==checkpoint
verification=dict(passed_scores=True,canonical_scores_unchanged=True,checkpoint_unchanged=True,
    native_differences=native_differences,branches=info,metric_comparisons=metric_comparisons,
    all_compared_metrics_identical=all(x['max_per_user_difference']==0 for x in metric_comparisons))
write(g.REP/'last_fit_replay_diagnostics.json',verification)
print(verification,flush=True)
write(work/'result.json',dict(fold=2,arm='global_ce',lambda_global=1.,validation_only=True,
    val_map=float(np.load(work/'val_ap.npy').mean()),best_epoch=state['epoch'],epochs=len(history),
    checkpoint_sha256=checkpoint,protocol_sha256=sha(g.REP/'protocol.json'),initial_state_sha256=initial,
    verification='FP32-bounded replay; near-tie top12 differences explicitly quantified in last_fit_replay_diagnostics.json; canonical scores retained',
    recovery_source_sha256=sha(Path(__file__)),replay_all_compared_metrics_identical=verification['all_compared_metrics_identical']))
record('global_aux_replay_diagnosed','All six fits completed. Last-fit replay scores remain within original FP32 bound; canonical checkpoint/scores retained, ranking changes and metric sensitivity explicitly measured in last_fit_replay_diagnostics.json. No refitting or target-based selection.',g.RUN,status='report_pending',artifacts=str(g.REP.relative_to(ROOT)))
