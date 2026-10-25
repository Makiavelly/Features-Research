"""Isolated checkpoint probes: preserve original outputs and split score components."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import shutil
import sys
import types
import numpy as np
import torch
import torch_frame
from common import ROOT,OLD,OUT,REPORT,read,write,sha,freeze_text,record

def cached_schema(cache):
    return {table:{column:kind for kind,columns in torch_frame.load(str(cache/f'{table}.pt'))[0].col_names_dict.items()
                   for column in columns} for table in ['article','customer','transactions']}

def run(case):
    torch.set_num_threads(4)
    old=case=='small'
    source=ROOT/'ContextGNN/run_small.py' if old else OLD/f'fold_{case}/runtime/gnn.py'
    original=ROOT/'ContextGNN/results/hm_small_v1' if old else OLD/f'fold_{case}/gnn'
    folder=OUT/'context_diagnostics'/str(case);folder.mkdir(parents=True,exist_ok=True)
    checkpoint=folder/'contextgnn';checkpoint.mkdir(exist_ok=True)
    for name in ['best.pt','metrics.json','val_predictions.npy','test_predictions.npy','val_scores.npy','test_scores.npy']:
        path=original/'contextgnn'/name
        if path.exists() and not(checkpoint/name).exists():shutil.copyfile(path,checkpoint/name)
    code=source.read_text(encoding='utf-8')
    code=code.replace('for kind in ["idgnn", "contextgnn"]:', 'for kind in ["contextgnn"]:')
    if old:
        code=code.replace('ROOT = Path(__file__).resolve().parents[1]',f'ROOT = Path({str(ROOT)!r})')
        code=code.replace('OUT = ROOT / "ContextGNN/results/hm_small_v1"',f'OUT = Path({str(folder)!r})')
        code=code.replace('get_stype_proposal(db)','FROZEN_STYPES')
        code=code.replace('run_id = "hm_contextgnn_small_pipeline_v1"','run_id = "hm_followup_context_small_probe_v1"')
        code=code.replace('model_run = f"hm_{kind}_small_seed_42_v1"','model_run = f"hm_followup_context_small_{kind}_probe_v1"')
        cache=ROOT/'ContextGNN/cache/hm_small_v1/materialized'
        args=['probe','--verify-only']
    else:
        code=code.replace(f'OUT = Path({str(original)!r})',f'OUT = Path({str(folder)!r})')
        code=code.replace(f'hm_medium_cv_v2_fold{case}_',f'hm_followup_context_f{case}_probe_')
        freeze_text(folder/'cv_graph.py',(OLD/f'fold_{case}/runtime/cv_graph.py').read_text(encoding='utf-8'))
        cache=OLD/f'fold_{case}/cache/gnn_seeded_past_v2/materialized'
        args=['probe','--evaluate-only']
    path=freeze_text(folder/'probe_runner.py',code)
    sys.path.insert(0,str(folder))
    spec=importlib.util.spec_from_file_location('context_probe_runner',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    if old:module.FROZEN_STYPES=cached_schema(cache)
    original_construct=module.ContextGNN.construct_logits
    rows=[]
    def instrument(model,lhs_projected,lhs,rhs_gnn,rhs,batch,index):
        output=original_construct(model,lhs_projected,lhs,rhs_gnn,rhs,batch,index)
        base=lhs_projected@rhs.t()+model.lin_offset_embgnn(lhs_projected).flatten()[:,None]
        local=model.head(rhs_gnn).flatten()+(lhs[batch]*rhs_gnn).sum(-1)
        local+=model.lin_offset_idgnn(lhs_projected).flatten()[batch]
        reconstructed=base.clone();reconstructed[batch,index]=local
        torch.testing.assert_close(output,reconstructed,rtol=0,atol=0)
        mask=torch.zeros_like(output,dtype=torch.bool);mask[batch,index]=True
        top=output.argsort(dim=1,descending=True,stable=True)[:,:12]
        best_local=torch.full((len(output),),-torch.inf,device=output.device)
        best_local.scatter_reduce_(0,batch,local,reduce='amax',include_self=True)
        row={'users':len(output),'local_article_nodes':len(local),
             'mean_local_candidates':float(mask.sum(1).float().mean()),
             'top12_fraction_from_local_context':float(mask.gather(1,top).float().mean()),
             'median_best_local_minus_best_final':float((best_local-output.max(1).values).median()),
             'base_score_std':float(base.std()),'local_score_mean':float(local.mean()),
             'base_score_mean':float(base.mean()),'global_max_mean':float(base.max(1).values.mean()),
             'local_max_mean':float(best_local.mean()),
             'lhs_norm_mean':float(lhs_projected.norm(dim=-1).mean()),
             'rhs_norm_mean':float(rhs.norm(dim=-1).mean())}
        rows.append(row)
        print('COMPONENT',case,json.dumps(row),flush=True)
        return output
    module.ContextGNN.construct_logits=instrument
    sys.argv=args
    with torch.no_grad():module.main()
    # The probe must reproduce saved scores, not change the checkpoint's behavior.
    for split in ['val','test']:
        before=np.load(original/'contextgnn'/f'{split}_scores.npy')
        after=np.load(checkpoint/f'{split}_scores.npy')
        np.testing.assert_allclose(before,after,rtol=1e-5,atol=1e-6)
    schema={table:{str(k):v for k,v in torch_frame.load(str(cache/f'{table}.pt'))[0].col_names_dict.items()}
            for table in ['article','customer','transactions']}
    write(folder/'component_probe.json',{'case':case,'original_checkpoint_sha256':sha(original/'contextgnn/best.pt'),
          'no_refitting':True,'original_scores_reproduced':True,'batches':rows,'materialized_schema':schema})
    record('followup_context_component_probe',f'ContextGNN {case}: original scores reproduced; component diagnostics saved, no fitting.',
           f'hm_followup_context_{case}_probe_v1',status='diagnostic_complete',artifacts=str(folder.relative_to(ROOT)))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('case',choices=['small','0','1','2'])
    run(parser.parse_args().case)
