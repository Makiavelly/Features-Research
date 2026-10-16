"""Additional artifact audit: scorer consistency, selection ordering and saved index."""
from pathlib import Path
import json
import sys
import numpy as np
import torch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'TDM'))
from common import OUT,Dataset,dump,sha,ap_per_user

def main():
    data=Dataset()
    selection_path=OUT/'selection_pretest.json'
    selection=json.loads(selection_path.read_text())
    check={}
    for variant in ['fixed','cluster']:
        folder=OUT/variant
        ck=torch.load(folder/'best.pt',map_location='cpu',weights_only=False)
        hist=json.loads((folder/'history.json').read_text())
        summary=json.loads((folder/'training_summary.json').read_text())
        best=1+int(np.argmax([x['val_metrics']['map'] for x in hist]))
        assert best==summary['best_epoch']==ck['epoch']
        assert sha(folder/'best.pt')==selection['selections'][variant]['checkpoint_sha256']
        assert all(x['train_rows']==4804 for x in hist)
        assert all(torch.isfinite(x).all() for x in ck['state'].values() if x.is_floating_point())
        leaf_to_item=ck['tree']['node_to_item']
        checks={}
        for split in ['val','test']:
            full=np.load(folder/'full'/f'{split}_scores.npy')
            bpred=np.load(folder/'beam'/f'{split}_predictions.npy')
            bscores=np.load(folder/'beam'/f'{split}_scores.npy')
            assert full.shape==(len(data.targets[split]),5000)
            assert np.isfinite(full).all() and np.isfinite(bscores).all()
            difference=np.abs(np.take_along_axis(full,bpred,axis=1)-bscores)
            assert difference.max()<1e-5
            beam_ap=ap_per_user(bpred,data.targets[split])
            assert np.array_equal(beam_ap,np.load(folder/'beam'/f'{split}_ap_per_user.npy'))
            for mode in ['beam','full']:
                pred=np.load(folder/mode/f'{split}_predictions.npy')
                assert np.all(np.diff(np.sort(pred,axis=1),axis=1)>0)
                assert np.array_equal(np.load(folder/mode/f'{split}_user_ids.npy'),data.tables[split].df.customer_id.to_numpy())
                assert np.array_equal(np.load(folder/mode/f'{split}_timestamps.npy'),data.tables[split].df.timestamp.astype('int64').to_numpy())
                if split=='test': assert (folder/mode/f'{split}_predictions.npy').stat().st_mtime>=selection_path.stat().st_mtime
            trace_nodes=np.load(folder/'beam'/f'{split}_trace_nodes.npy')
            trace_scores=np.load(folder/'beam'/f'{split}_trace_scores.npy')
            offsets=np.load(folder/'beam'/f'{split}_trace_offsets.npy')
            leafdiff=0.
            for i in range(len(bpred)):
                nodes=trace_nodes[offsets[i]:offsets[i+1]]
                score=trace_scores[offsets[i]:offsets[i+1]]
                items=leaf_to_item[nodes]
                is_leaf=items>=0
                leafdiff=max(leafdiff,float(np.abs(full[i,items[is_leaf]]-score[is_leaf]).max()))
            assert leafdiff<1e-5
            checks[split]=dict(max_selected_score_difference=float(difference.max()),max_all_visited_leaf_score_difference=leafdiff,
                               same_top12_beam_full_users=int(np.all(bpred==np.load(folder/'full'/f'{split}_predictions.npy'),axis=1).sum()))
        check[variant]=dict(selected_epoch=best,all_train_rows_each_epoch=True,split_checks=checks)
    fixed=torch.load(OUT/'fixed/best.pt',map_location='cpu',weights_only=False)
    emb=fixed['state']['embedding.weight'].numpy()[fixed['tree']['leaves']]
    assert np.array_equal(emb,np.load(OUT/'fixed/cluster_source_embeddings.npy'))
    assert json.loads((OUT/'cluster_provenance.json').read_text())['source_checkpoint_sha256']==sha(OUT/'fixed/best.pt')
    dump(ROOT/'reports/tdm_small_v1/final_audit.json',dict(passed=True,checks=check,
         cluster_source_embeddings_exact=True,test_predictions_written_after_both_selections=True,
         caveat='Timing is one loaded-model pass per mode; no repeated timing benchmark or explicit warmup before every mode.'))
    print(json.dumps(check),flush=True)

if __name__=='__main__': main()
