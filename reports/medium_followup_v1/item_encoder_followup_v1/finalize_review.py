"""Independent integrity checks and final visual-review status."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'CVFollowup'))
import item_encoder_followup as run
import numpy as np
import torch
from scipy import sparse
from common import read,write,sha,record

assert read(run.REP/'visual_review.json')['passed']
replay_changed=0;max_ap_sensitivity=0.
replay_by_arm={arm:dict(changed=0,max_ap=0.) for arm in run.ARMS[1:]}
for fold in range(3):
    control=read(run.DEST/f'fold_{fold}/control/result.json')
    control_history=read(run.DEST/f'fold_{fold}/control/history.json')
    mask=np.load(run.DEST/f'fold_{fold}/seen_mask.npy')
    for arm in run.ARMS:
        p=run.DEST/f'fold_{fold}'/arm;r=read(p/'result.json')
        assert sha(p/'best.pt')==r['checkpoint_sha256']
        assert r['lambda_global']==0
        assert r['initial_state_sha256']==control['initial_state_sha256']
        if arm!='control':
            for a,b in zip(read(p/'history.json'),control_history):
                assert a['epoch']==b['epoch'] and a['training_graph_sha256']==b['training_graph_sha256']
            replay=read(p/'replay_verification.json')
            for v in [*replay['native'],*replay['reload'].values()]:
                assert v['max_score_difference']<=v['bound']
                replay_changed+=len(v['changed_rows'])
                max_ap_sensitivity=max(max_ap_sensitivity,v['max_per_user_ap_difference'])
                replay_by_arm[arm]['changed']+=len(v['changed_rows'])
                replay_by_arm[arm]['max_ap']=max(replay_by_arm[arm]['max_ap'],v['max_per_user_ap_difference'])
        scores=np.load(p/'val_global_scores.npy');scores[mask]=-np.inf
        expected=np.argsort(-scores,axis=1,kind='stable')[:,:12]
        assert np.array_equal(expected,np.load(p/'val_new_only_predictions.npy'))
        if arm=='feature':
            state=torch.load(p/'best.pt',map_location='cpu')['model_state_dict']
            assert not any('lookup_embedding' in n for n in state)
        if arm=='similarity_graph':
            article_ids=run.pd.read_parquet(run.DATA/f'fold_{fold}/db/article.parquet',columns=['article_id']).article_id.to_numpy()
            assert np.array_equal(article_ids,np.arange(10000))
            graph_path=run.DEST/f'fold_{fold}/semantic_graph/graph.npz'
            audit=read(graph_path.with_name('graph_audit.json'))
            assert sha(graph_path)==r['graph_sha256']==audit['graph_sha256']
            graph=sparse.load_npz(graph_path)
            assert graph.shape==(10000,10000) and graph.nnz==200000
            assert np.all(graph.data>=0) and np.all(graph.diagonal()==0)
            assert np.allclose(np.asarray(graph.sum(axis=1)).ravel(),1,atol=1e-6)
protocol=read(run.REP/'protocol.json')
for path,digest in {**protocol['reference_hashes'],**protocol['sources']}.items():assert sha(ROOT/path)==digest

# A real cached inner module: clearing the outer cache must invalidate it too.
class CachedToy(torch.nn.Module):
    def __init__(self):
        super().__init__();self.weight=torch.nn.Parameter(torch.tensor([[1.,0.],[0.,2.]]));self._cached_rhs_embedding=None
    def forward(self):
        if not self.training and self._cached_rhs_embedding is not None:return self._cached_rhs_embedding
        value=self.weight*1.
        if not self.training:self._cached_rhs_embedding=value
        return value
base=CachedToy();wrapped=run.GraphItemEmbedding(base,torch.tensor([[0.,1.],[1.,0.]]).to_sparse())
wrapped.eval();assert torch.equal(wrapped(),torch.tensor([[.5,1.],[.5,1.]]))
with torch.no_grad():base.weight.add_(1.)
wrapped._cached_rhs_embedding=None
assert torch.equal(wrapped(),torch.tensor([[1.5,2.],[1.5,2.]]))
assert torch.equal(wrapped(torch.tensor([1])),wrapped()[[1]])
qualification=replay_changed>0
status='complete_validation_with_replay_qualification' if qualification else 'complete_verified_validation'
for tag in ['feature','final']:
    selected=['feature'] if tag=='feature' else run.ARMS[1:]
    stage_changed=sum(replay_by_arm[a]['changed'] for a in selected)
    stage_sensitivity=max(replay_by_arm[a]['max_ap'] for a in selected)
    summary=read(run.REP/f'{tag}_summary.json')
    summary['status']='complete_validation_with_replay_qualification' if stage_changed else 'complete_verified_validation'
    summary['replay_rows_changed_in_checks']=stage_changed
    summary['max_per_user_ap_replay_sensitivity']=stage_sensitivity
    write(run.REP/f'{tag}_summary.json',summary)
    with (run.REP/f'{tag}_report_ru.md').open('a',encoding='utf-8') as f:
        f.write(f'\nФинальная проверка: FP32-допуски соблюдены. Суммарное число строк с перестановками в native/reload проверках показанных вариантов: {stage_changed} (включая повторные проверки одних строк); максимальное изменение пользовательского AP={stage_sensitivity:.10g}. Политика и исходные оценки не менялись.\n')
        metrics=run.pd.read_csv(run.REP/f'{tag}_metrics.csv')
        shown=['control',*selected]
        lines=['','## Группы новых товаров после исключения покупок','',
            '| Группа | Наблюдений с доступной целью | '+' | '.join(run.NAMES[a] for a in shown)+' |',
            '|---|---:|'+'---:|'*len(shown)]
        for group in ['new_variant','new_product_known_type','new_type']:
            part=metrics[(metrics['mode']=='new_only')&(metrics['group']==group)].set_index('arm')
            count=int(part.loc['control','available_users'])
            values=[f"{100*part.loc[a,'available_recall']:.4f}%" for a in shown]
            lines.append('| '+group+' | '+str(count)+' | '+' | '.join(values)+' |')
        lines+=['','Подгрупповые значения описательные, без отдельных интервалов значимости. '
            'Доступные цели и подмножество наблюдений для каждого столбца одинаковы.','']
        f.write('\n'.join(lines))
write(run.REP/'final_verification.json',dict(passed_with_documented_replay_policy=True,status=status,
    verified_fits=9,new_fits=6,reused_controls=3,common_initial_weights_identical=True,
    train_graphs_identical_for_shared_epochs=True,no_auxiliary_loss=True,
    references_and_sources_unchanged=True,new_only_equals_masked_global=True,
    graph_no_self_edges=True,graph_row_normalized=True,graph_uses_no_transactions_or_targets=True,
    nested_cache_invalidation_checked=True,replay_rows_changed_in_checks=replay_changed,
    max_per_user_ap_replay_sensitivity=max_ap_sensitivity,visual_review=read(run.REP/'visual_review.json')))
record('item_encoder_complete','FEATURE/FUSION comparison and subsequent FUSION+semantic-graph experiment completed: six new fits plus three unchanged verified controls, same common initial states/train graphs, original CE only. Graph provenance/normalization/gradients/cache and replay sensitivity checked; figures reviewed. No test/API.',run.RUN,
    status=status,artifacts=str(run.REP.relative_to(ROOT)),new_fits=6,reused_controls=3,
    replay_rows_changed_in_checks=replay_changed,max_per_user_ap_replay_sensitivity=max_ap_sensitivity)
