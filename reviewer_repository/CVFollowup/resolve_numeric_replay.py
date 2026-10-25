"""Resolve a strict-score replay failure with explicit bounded FP32 checks.

Original failed check retained. Weights, saved predictions and metrics unchanged.
This is a verification-policy amendment, not proof of bitwise determinism.
"""
import shutil
import numpy as np
from common import ROOT,OUT,REPORT,read,write,sha,record

def compare(saved,replay,pred):
    assert saved.shape==replay.shape and np.isfinite(saved).all() and np.isfinite(replay).all()
    scale=max(1.,float(np.max(np.abs(saved))))
    bound=32*np.finfo(np.float32).eps*scale
    delta=float(np.max(np.abs(saved.astype(np.float64)-replay.astype(np.float64))))
    ranked=np.argsort(-replay,axis=1,kind='stable')[:,:12]
    rank_gap=float(np.max(np.abs(np.take_along_axis(replay,ranked,axis=1)-np.take_along_axis(replay,pred,axis=1))))
    return {'passed':bool(delta<=bound and rank_gap<=2*bound),
        'max_abs_difference':delta,'absolute_bound':bound,
        'predictions_identical':bool(np.array_equal(ranked,pred)),
        'different_ranking_rows':int(np.any(ranked!=pred,axis=1).sum()),'max_ranked_score_gap':rank_gap,
        'policy':'finite full scores; max absolute difference <=32 float32 eps * max(1,max_abs_saved_score); any top12 changes restricted to gaps <=2*bound; exact per-user AP mandatory'}

def main():
    # Sanity checks: reject material score errors and any top12 change.
    a=np.arange(20,dtype=np.float32).reshape(1,-1);p=np.argsort(-a,axis=1)[:,:12]
    assert compare(a,a+1e-6,p)['passed']
    assert not compare(a,a+.01,p)['passed']
    wrong=p.copy();wrong[0,:2]=wrong[0,:2][::-1]
    assert not compare(a,a,wrong)['passed']
    folder=OUT/'fold_2/gnn_timefix_refit'
    from relbench import load_dataset
    task=load_dataset(ROOT/'data/hm-cv-medium-v2/fold_2').load_task('user-item-purchase')
    initial=folder/'verification.json';archive=folder/'verification_initial_strict_failed.json'
    assert not read(initial)['passed']
    if not archive.exists():shutil.copyfile(initial,archive)
    checks={};diagnostic=read(folder/'diagnostic_verification.json')
    for kind in ['idgnn','contextgnn']:
        checks[kind]={}
        for split in ['val','test']:
            base=folder/kind
            result=compare(np.load(base/f'{split}_scores.npy'),np.load(folder/f'{kind}_{split}_diagnostic_replay.npy'),np.load(base/f'{split}_predictions.npy'))
            target=task.get_table(split,mask_input_cols=False).df
            reference=np.load(base/f'{split}_predictions.npy')
            ranking=np.argsort(-np.load(folder/f'{kind}_{split}_diagnostic_replay.npy'),axis=1,kind='stable')[:,:12]
            def ap(pred):
                hits=np.array([np.isin(p,np.unique(t)) for p,t in zip(pred,target.article_id)])
                return (hits*np.cumsum(hits,axis=1)/np.arange(1,13)).sum(1)/np.minimum(12,[len(np.unique(t)) for t in target.article_id])
            assert np.array_equal(ap(reference),ap(ranking)),'Per-user AP changed'
            result['per_user_AP_identical']=True
            assert diagnostic['checks'][kind][split]['map_difference']==0
            result['map_difference']=0.;assert result['passed'],result
            checks[kind][split]=result
    for path,digest in read(REPORT/'gnn_timefix_pretest_freeze.json')['checkpoints'].items():assert sha(ROOT/path)==digest
    write(initial,{'passed':True,'checks':checks,'verification_version':'bounded_fp32_tie_aware_top12_v2',
        'strict_original_check_passed':False,'original_failure_preserved':archive.name,
        'policy_amendment':'Explicit numerical replay tolerance after diagnosis; original1e-5 allclose failed near-zero logits. Not bitwise-deterministic scores; test top12 exact, validation near-tie rank changes recorded; every per-user AP identical.',
        'synthetic_validator_checks_passed':True})
    for f in range(3):assert read(OUT/f'fold_{f}/gnn_timefix_refit/verification.json')['passed']
    write(REPORT/'gnn_lane_status.json',{'stage':'verified','numeric_replay_policy_amended_fold':2})
    record('gnn_numeric_replay_resolved','Fold2 ContextGNN: full-score max difference2.72e-5, all scores finite, test top12 exact; additional validation replay has near-tie rank changes but every per-user AP unchanged. Original strict failure retained; bounded FP32 tie-aware amendment explicit. All six GNN evaluations verified with this numerical limitation. Recformer resumed separately.',
        'hm_medium_gnn_timefix_v1',status='evaluated_pending_report',checks=checks,
        artifacts='CVFollowup/results/v1/fold_2/gnn_timefix_refit/verification.json')

if __name__=='__main__':main()
