"""Keep TDM's native beam64 search; exclude seen items at final leaf ranking."""
import os
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
import importlib.util
import sys
import gc
import novelty_audit as audit
from common import ROOT,DATA,OLD,write,read,sha,record


def run():
    import numpy as np
    import torch
    for fold in range(3):
        folder=audit.output(fold,'tdm')
        if (folder/'verification.json').exists():continue
        runtime=OLD/f'fold_{fold}/runtime'
        sys.path.insert(0,str(runtime))
        sys.modules.pop('tdm_common',None);sys.modules.pop('tdm_train',None)
        import tdm_common as c
        import tdm_train as trainer
        c.seed();torch.set_num_threads(2)
        dataset=c.Dataset()
        model,tree,checkpoint=trainer.load('fixed',torch.device('cuda'))
        model.eval()
        histories=c.mapped_history(dataset.history['test'],tree)
        masks=np.load(audit.DEST/f'fold_{fold}/seen_mask.npy',mmap_mode='r')
        expected=np.load(audit.methods(fold)['tdm']['prediction'])
        rows=[];coverage=[];minimum=10000
        with torch.no_grad():
            for i,hist in enumerate(histories):
                frontier=np.array([1],dtype=np.int64)
                for level in range(tree['paths'].shape[1]):
                    nodes=np.sort(np.concatenate([frontier*2,frontier*2+1]))
                    nodes=nodes[tree['valid'][nodes]]
                    scores=c.score_nodes(model,hist,nodes,torch.device('cuda'))
                    tie=tree['node_to_item'][nodes] if level==tree['paths'].shape[1]-1 else nodes
                    order=np.lexsort((tie,-scores))
                    frontier=nodes[order[:c.CONFIG['beam']]]
                items=tree['node_to_item'][nodes]
                assert (items>=0).all()
                assert np.array_equal(items[order[:12]],expected[i]),(fold,i,'TDM original replay')
                valid=~masks[i,items]
                eligible=items[valid];values=scores[valid]
                ranking=eligible[np.lexsort((eligible,-values))[:12]]
                minimum=min(minimum,len(ranking))
                row=np.full(12,-1,dtype=np.int64);row[:len(ranking)]=ranking
                rows.append(row)
                coverage.append(dict(row=i,scored_final_leaves=len(items),unseen_scored_leaves=len(eligible)))
                if i%128==0:
                    print('TDM',fold,i+1,'/',len(histories),flush=True)
                    write(folder/'progress.json',dict(users_done=i+1,users=len(histories)))
        np.save(folder/'new_predictions.npy',np.asarray(rows))
        write(folder/'beam_coverage.json',coverage)
        write(folder/'verification.json',dict(passed=True,normal_top12_identical=True,model_sha256=sha(c.OUT/'fixed/best.pt'),
            beam=64,unchanged_internal_search=True,minimum_new_recommendations=minimum,
            mean_scored_final_leaves=float(np.mean([x['scored_final_leaves'] for x in coverage])),
            policy='Mask seen items before final leaf top12; native beam64 pruning unchanged; never exclude pruned targets from denominators'))
        record('novelty_tdm_verified',f'Fold{fold}: TDM beam64 original top12 reproduced exactly; seen products excluded before final leaf top12.',audit.RUN+f'_f{fold}_tdm',status='verified',artifacts=str(folder.relative_to(ROOT)))
        del model,dataset,histories
        gc.collect();torch.cuda.empty_cache()


if __name__=='__main__':run()
