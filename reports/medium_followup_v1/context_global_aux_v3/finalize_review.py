"""Finalize only after inspecting the generated figure."""
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'CVFollowup'))
import context_global_aux_v3 as run
from common import read,write,sha,record

assert read(run.REP/'visual_review.json')['passed']
fits=[]
for fold in range(3):
    pair=[]
    for arm,weight in [('control',0.),('global_ce',1.)]:
        p=run.DEST/f'fold_{fold}'/arm
        result=read(p/'result.json')
        assert result['lambda_global']==weight
        assert sha(p/'best.pt')==result['checkpoint_sha256']
        pair.append((result,read(p/'history.json')))
        fits.append(result)
        mask=np.load(run.DEST/f'fold_{fold}/seen_mask.npy')
        global_scores=np.load(p/'val_global_scores.npy')
        global_scores[mask]=-np.inf
        global_new=np.argsort(-global_scores,axis=1,kind='stable')[:,:12]
        assert np.array_equal(global_new,np.load(p/'val_new_only_predictions.npy'))
    assert pair[0][0]['initial_state_sha256']==pair[1][0]['initial_state_sha256']
    for a,b in zip(pair[0][1],pair[1][1]):
        assert a['epoch']==b['epoch']
        assert a['training_graph_sha256']==b['training_graph_sha256']
protocol=read(run.REP/'protocol.json')
for name,digest in {**protocol['reference_hashes'],**protocol['sources']}.items():assert sha(ROOT/name)==digest
replay=read(run.REP/'last_fit_replay_diagnostics.json')
assert replay['passed_scores'] and replay['canonical_scores_unchanged'] and replay['checkpoint_unchanged']
summary=read(run.REP/'summary.json');summary['status']='complete_validation_with_replay_qualification'
summary['last_fit_replay_diagnostics']=replay
write(run.REP/'summary.json',summary)
write(run.REP/'final_verification.json',dict(passed_with_replay_qualification=True,model_folds=6,
    exact_replay_top12_requirement_met_for_all_fits=False,
    last_fit_replay_diagnostics=replay,
    initial_states_identical_within_pairs=True,training_graphs_identical_for_shared_epochs=True,
    new_only_hybrid_equals_masked_global_for_all_six_fits=True,
    reference_hashes_unchanged=True,frozen_sources_unchanged=True,
    gradient_test=read(run.REP/'gradient_verification.json'),
    visual_review=read(run.REP/'visual_review.json'),
    reused_control=read(run.DEST/'fold_0/control/reuse_lineage.json')))
record('global_aux_complete_qualified','Six matched validation fits completed (one verified v2 control reused): paired initial weights/training graphs matched. Five fits passed exact-top12 replay; last-fit near-tie ranking variation is explicitly quantified, scores within original FP32 bound, canonical scores/weights unchanged. Do not claim all six exact-top12 replays passed. Metrics, bootstrap and plot reviewed with qualification; no test/API.',run.RUN,
    status='complete_validation_with_replay_qualification',artifacts=str(run.REP.relative_to(ROOT)),model_folds=6)
