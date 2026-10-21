from pathlib import Path
import copy
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'CVFollowup'))
import context_global_aux as g
import torch
import numpy as np
from torch_geometric.seed import seed_everything
from common import write

torch.set_num_threads(2)
g.base.DEST=g.DEST;g.base.REP=g.REP
env=g.base.setup(0,categorical=True)
task=env['task'];device=env['device'];mod=env['module']
model=env['make_model']('contextgnn')
model.load_state_dict(torch.load(g.DEST/'fold_0/control/best.pt',map_location=device)['model_state_dict'])
seed_everything(42)
batch=next(iter(g.base.loader(env,'val',g.FANOUT))).to(device)
model.eval();mod.clear_rhs(model)
with torch.no_grad():
    a,b=g.forward_pair(model,batch,task)
    c=model(batch,task.src_entity_table,task.dst_entity_table)
    d=model(batch,task.src_entity_table,task.dst_entity_table)
def diff(a,b):
    scale=max(1.,float(a.abs().max()));bound=32*np.finfo(np.float32).eps*scale
    return dict(max_difference=float((a-b).abs().max()),fp32_bound=bound,
        top12_equal=bool(torch.equal(a.argsort(descending=True,stable=True)[:,:12],b.argsort(descending=True,stable=True)[:,:12])))
out=dict(dual_vs_native=diff(a,c),native_vs_native=diff(c,d))
state=copy.deepcopy(model.state_dict());src,dst=env['sparse_labels'][batch[task.src_entity_table].input_id]
grads={};losses={}
for key in ['native','dual']:
    model.load_state_dict(state);model.train();mod.clear_rhs(model);model.zero_grad();seed_everything(43)
    logits=model(batch,task.src_entity_table,task.dst_entity_table) if key=='native' else g.forward_pair(model,batch,task)[0]
    loss=mod.sparse_ce(logits,src,dst);loss.backward()
    losses[key]=float(loss.detach())
    grads[key]={n:p.grad.detach().clone() for n,p in model.named_parameters() if p.grad is not None}
out['training_losses']=losses
out['max_parameter_gradient_difference']=max(float((grads['native'][n]-grads['dual'][n]).abs().max()) for n in grads['native'])
out['max_native_gradient']=max(float(x.abs().max()) for x in grads['native'].values())
write(g.REP/'numeric_probe.json',out)
print(out,flush=True)
