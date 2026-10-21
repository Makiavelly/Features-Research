"""Isolated learned local/global mixing ablation; same baseline loss/training."""
import math
import types
import sys
from pathlib import Path
import context_first3 as base
from common import write, read, sha, record, ROOT


def attach_gate(model):
    import torch
    device=next(model.parameters()).device
    # Zero initialization consumes no RNG and initially gives local weight .9.
    model.blend_gate_weight=torch.nn.Parameter(torch.zeros(64,device=device))
    model.blend_gate_bias=torch.nn.Parameter(torch.tensor(math.log(9.),device=device))
    model._last_validation_gates=[]
    def construct(self,projected,lhs,rhs_gnn,rhs,groups,ids):
        global_scores=projected@rhs.t()+self.lin_offset_embgnn(projected).flatten()[:,None]
        local=self.head(rhs_gnn).flatten()+(lhs[groups]*rhs_gnn).sum(-1)
        local=local+self.lin_offset_idgnn(projected).flatten()[groups]
        alpha=torch.sigmoid(projected@self.blend_gate_weight+self.blend_gate_bias)
        mixed=(1-alpha[groups])*global_scores[groups,ids]+alpha[groups]*local
        output=global_scores.clone()
        output[groups,ids]=mixed
        if not self.training:
            self._last_validation_gates=(self._last_validation_gates+alpha.detach().cpu().tolist())[-256:]
        return output
    model.construct_logits=types.MethodType(construct,model)
    return model


def main():
    import numpy as np
    original_setup=base.setup
    captured={}
    def setup(fold,categorical=False):
        env=original_setup(fold,categorical=False)
        factory=env['make_model']
        def make(kind):
            model=attach_gate(factory(kind))
            captured['model']=model
            return model
        env['make_model']=make
        return env
    base.setup=setup
    protocol=dict(arm='gate',validation_only=True,initial_local_weight=.9,
        gate='sigmoid(projected_user @ learned_weight64 + learned_bias)',
        local_logit='(1-alpha)*global + alpha*local; nonlocal global unchanged',
        training='from scratch, original loss/Adam .001/seed42/fanout32-16/10 epochs/patience3',
        sources={str(Path(__file__).relative_to(ROOT)):sha(Path(__file__)),
                 str(Path(base.__file__).relative_to(ROOT)):sha(Path(base.__file__))})
    write(base.REP/'gate_protocol.json',protocol)
    for fold in range(3):
        base.refit(fold,'gate')
        model=captured.pop('model')
        path=base.DEST/f'fold_{fold}/gate/result.json'
        result=read(path)
        gates=np.array(model._last_validation_gates)
        weight_norm=float(model.blend_gate_weight.detach().norm())
        assert np.isfinite(weight_norm) and weight_norm>0, 'Gate did not learn'
        result['gate_protocol']=protocol
        result['validation_gate']=dict(min=float(gates.min()),mean=float(gates.mean()),max=float(gates.max()))
        result['gate_weight_norm']=weight_norm
        write(path,result)
        del model


if __name__=='__main__':
    main()
