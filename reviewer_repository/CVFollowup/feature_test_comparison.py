"""Frozen FEATURE test inference and immutable 16-method chart extension."""
import os
os.environ.setdefault('OMP_NUM_THREADS','2')
os.environ.setdefault('MKL_NUM_THREADS','2')
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
import argparse
import ast
import copy
import gc
from pathlib import Path
import shutil
import subprocess
import sys
import numpy as np
import pandas as pd
import torch
import context_first3 as base
import context_global_aux_v3 as resources
from common import ROOT,DATA,OUT,read,write,sha,record

RUN='hm_medium_feature_test_all_methods_seed42_v1'
MODELS=OUT/'item_encoder_followup_v1'
DEST=OUT/'feature_test_comparison_v1'
REP=ROOT/'reports/medium_all_methods_h011_feature_v1'
ORIGINAL=ROOT/'reports/medium_all_methods_h011_v1'


def freeze():
    refs={}
    for f in range(3):
        p=MODELS/f'fold_{f}/feature';r=read(p/'result.json')
        assert r['no_auxiliary_loss'] and r['item_encoder_arm']=='feature'
        assert sha(p/'best.pt')==r['checkpoint_sha256']
        for n in ['best.pt','result.json']:
            file=p/n;refs[str(file.relative_to(ROOT))]=sha(file)
        for n in ['bundle/test_targets.parquet','article_id_map.csv','customer_id_map.csv','db/article.parquet']:
            file=DATA/f'fold_{f}'/n;refs[str(file.relative_to(ROOT))]=sha(file)
    for n in ['comparison.json','comparison_all.png','comparison_all.svg','summary.csv','summary_ru.md']:
        p=ORIGINAL/n;refs[str(p.relative_to(ROOT))]=sha(p)
    for name,digest in read(ORIGINAL/'comparison.json')['sources_sha256'].items():
        assert sha(ROOT/name)==digest;refs[name]=digest
    sources={n:sha(ROOT/n) for n in ['CVFollowup/feature_test_comparison.py','CVFollowup/context_first3.py',
        'ContextGNN/upstream/contextgnn/nn/rhs_embedding.py','LLMResearch/compare_all.py']}
    value=dict(run_id=RUN,no_training=True,no_reselection=True,no_api=True,
        model='Existing FEATURE checkpoints, fanout64/32, eight categorical article codes, original CE; local branch unchanged',
        checkpoint_selection='Fixed on validation before this test request',seed=42,pythonhashseed='42',
        expected_test_rows=[1839,1982,1698],metric='Original full-target pooled test MAP@12 including unavailable targets',
        chart='Add one FEATURE row; preserve all 16 original method numbers and confidence intervals; original PNG/SVG unchanged',
        bootstrap='5000 original-customer clusters across folds, seed42',
        replay='FP32 score bound and explicit top12/AP sensitivity; canonical first-pass scores retained, no best replay selection',
        reference_hashes=refs,sources=sources,limitation='One seed; these test weeks have been inspected before, internal comparison')
    p=REP/'pretest_freeze.json'
    if p.exists():assert read(p)==value
    else:write(p,value)
    for n in sources:
        p=REP/'frozen_source'/n;p.parent.mkdir(parents=True,exist_ok=True)
        if p.exists():assert sha(p)==sha(ROOT/n)
        else:shutil.copyfile(ROOT/n,p)


def evaluate(fold):
    from torch_geometric.seed import seed_everything
    resources.REP=REP;resources.RUN=RUN
    folder=DEST/f'fold_{fold}/feature';folder.mkdir(parents=True,exist_ok=True)
    if (folder/'verification.json').exists():assert read(folder/'verification.json')['passed_scores'];return
    resources.wait_for_resources(f'f{fold}_feature_test')
    base.DEST=DEST
    env=base.setup(fold,categorical=True)
    task,device,mod=env['task'],env['device'],env['module']
    model=env['make_model']('contextgnn')
    from contextgnn.utils import RHSEmbeddingMode
    model.rhs_embedding.lookup_embedding=None
    model.rhs_embedding.emb_mode=RHSEmbeddingMode.FEATURE
    assert not any('lookup_embedding' in n for n,_ in model.named_parameters())
    checkpoint=MODELS/f'fold_{fold}/feature/best.pt';digest=sha(checkpoint)
    target=pd.read_parquet(DATA/f'fold_{fold}/bundle/test_targets.parquet')
    assert len(target)==[1839,1982,1698][fold]
    assert np.array_equal(target.customer_id,env['tables']['test'].df[task.src_entity_col])
    targets=[set(map(int,x)) for x in target[task.dst_entity_col]]
    @torch.no_grad()
    def infer():
        model.load_state_dict(torch.load(checkpoint,map_location=device)['model_state_dict'])
        model.eval();mod.clear_rhs(model);seed_everything(42)
        parts=[]
        for batch in base.loader(env,'test',[64,32]):
            batch=batch.to(device);base.check_time(batch,task)
            scores=model(batch,task.src_entity_table,task.dst_entity_table)
            assert torch.isfinite(scores).all();parts.append(scores.cpu().numpy())
        scores=np.concatenate(parts);pred=np.argsort(-scores,axis=1,kind='stable')[:,:12]
        ap=base.aps(pred,targets)
        assert abs(float(ap.mean())-task.evaluate(pred)['map'])<1e-10
        return scores,pred,ap
    print('INFER',fold,flush=True)
    scores,pred,ap=infer()
    np.save(folder/'test_scores.npy',scores);np.save(folder/'test_predictions.npy',pred);np.save(folder/'test_ap.npy',ap)
    bound=32*np.finfo(np.float32).eps*max(1.,float(np.abs(scores).max()))
    del scores;gc.collect()
    print('REPLAY',fold,flush=True)
    replay,rpred,rap=infer()
    saved=np.load(folder/'test_scores.npy',mmap_mode='r')
    difference=max(float(np.abs(saved[i:i+128]-replay[i:i+128]).max()) for i in range(0,len(replay),128))
    assert difference<=bound
    changed=np.where(np.any(pred!=rpred,axis=1))[0]
    for i in changed:
        assert saved[i,rpred[i]].min()>=saved[i,pred[i,-1]]-2*bound
        assert np.all(np.diff(saved[i,rpred[i]])<=2*bound)
    assert sha(checkpoint)==digest
    verification=dict(passed_scores=True,fold=fold,rows=len(ap),checkpoint_sha256=digest,
        canonical_map=float(ap.mean()),replay_map=float(rap.mean()),max_score_difference=difference,fp32_bound=bound,
        top12_changed_rows=changed.tolist(),exact_per_user_ap=bool(np.array_equal(ap,rap)),
        max_per_user_ap_difference=float(np.abs(ap-rap).max()),canonical_scores_retained=True,no_training=True)
    write(folder/'verification.json',verification)
    record('feature_test_fold_verified',f'Fold{fold}: frozen FEATURE test/reload checked, original full-target MAP={100*ap.mean():.5f}%; rank/AP sensitivity recorded.',RUN+f'_f{fold}',
        status='test_verified',test_metrics={'map':float(ap.mean())},artifacts=str(folder.relative_to(ROOT)))
    print('VERIFIED',verification,flush=True)


def plot():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    frozen=read(REP/'pretest_freeze.json')
    for p,h in {**frozen['reference_hashes'],**frozen['sources']}.items():assert sha(ROOT/p)==h
    reference=read(ORIGINAL/'comparison.json');rows=copy.deepcopy(reference['methods'])
    aps=[];ids=[];fold_maps=[]
    for f in range(3):
        folder=DEST/f'fold_{f}/feature';assert read(folder/'verification.json')['passed_scores']
        target=pd.read_parquet(DATA/f'fold_{f}/bundle/test_targets.parquet')
        ap=base.aps(np.load(folder/'test_predictions.npy'),[set(map(int,x)) for x in target.article_id])
        assert np.array_equal(ap,np.load(folder/'test_ap.npy'))
        aps.append(ap);fold_maps.append(float(ap.mean()))
        mapping=pd.read_csv(DATA/f'fold_{f}/customer_id_map.csv').set_index('customer_id').original_customer_id
        original=target.customer_id.map(mapping);assert original.notna().all();ids.extend(original)
    values=np.concatenate(aps);unique,inverse=np.unique(ids,return_inverse=True)
    counts=np.bincount(inverse);sums=np.bincount(inverse,weights=values);rng=np.random.default_rng(42);boot=[]
    for _ in range(5000):
        sample=rng.integers(0,len(unique),len(unique));boot.append(sums[sample].sum()/counts[sample].sum())
    lo,hi=np.quantile(boot,[.025,.975])
    feature=dict(method='contextgnn_feature',label='ContextGNN FEATURE (64/32)',pooled_map=float(values.mean()),
        ci95_low=float(lo),ci95_high=float(hi),fold_maps=fold_maps)
    assert not any(r['method']==feature['method'] for r in rows)
    rows.append(feature);rows.sort(key=lambda r:-r['pooled_map'])
    assert len(rows)==17
    for old in reference['methods']:assert next(x for x in rows if x['method']==old['method'])==old
    for row in rows:assert abs(np.average(row['fold_maps'],weights=[1839,1982,1698])-row['pooled_map'])<1e-12
    # Load only the original drawing function: importing its module would overwrite the original chart.
    source=(ROOT/'LLMResearch/compare_all.py').read_text(encoding='utf-8')
    tree=ast.parse(source);function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='draw')
    draw_source=ast.get_source_segment(source,function)
    colors={'h010_20':'#1976d2','h011_20':'#7c3aed','h009_20':'#ea8c24','contextgnn_feature':'#16a085'}
    namespace=dict(np=np,plt=plt,OUT=REP,colors=colors)
    exec(compile(draw_source,str(REP/'draw_runtime.py'),'exec'),namespace)
    (REP/'draw_runtime.py').write_text(draw_source+'\n',encoding='utf-8')
    xmax=max(1.72,float(hi)*100+.2)
    namespace['draw'](rows,'comparison_all','Сравнение всех методов с ContextGNN FEATURE',xmax,10.6)
    pd.DataFrame([{**r,'fold_maps':str(r['fold_maps'])} for r in rows]).to_csv(REP/'summary.csv',index=False)
    write(REP/'comparison.json',dict(status='pending_visual_review',methods=rows,feature=feature,
        users_times=len(values),customers=len(unique),weights=[1839,1982,1698],
        original_16_rows_unchanged=True,original_files_unchanged=True,pretest_freeze_sha256=sha(REP/'pretest_freeze.json'),
        no_training=True,no_reselection=True,no_api=True))
    lines=['# Все методы и ContextGNN FEATURE','',
        'FEATURE добавлен к прежним 16 строкам после test-инференса фиксированных checkpoint. '
        'Все остальные значения и интервалы сохранены. Исходный график не изменён. '
        'Обучения, переотбора эпох или API-запросов не было.', '',
        f"FEATURE test MAP@12: **{100*feature['pooled_map']:.4f}%**, 95% интервал "
        f"[{100*lo:.4f}%; {100*hi:.4f}%]. Фолды: "+' / '.join(f'{100*x:.4f}%' for x in fold_maps)+'.', '',
        'Те же 5519 наблюдений / 4548 покупателей, три medium-v2 недели, каталог10000. '
        'MAP по всем исходным целям, включая недоступные среди кандидатов. '
        'Интервал — 5000 bootstrap по исходным покупателям, seed42. '
        'Один seed, эти test-недели уже просматривались: внутреннее сравнение.', '',
        'FEATURE: fanout64/32, восемь categorical-кодов, без lookup ID-компоненты RHS, '
        'исходный CE без дополнительного global loss; выбранные ранее validation checkpoint. '
        'Строка прежнего ContextGNN corrected сохранена, её параметры отличаются от FEATURE '
        'также fanout и типами кодов; это не чистая парная FEATURE/FUSION абляция.', '',
        'H011: бюджет исследований вырос40→300 во время поиска; равное число программ '
        'не означает равные расходы. Все прежние ограничения сравнения сохраняются.', '',
        'Проверки reload, перестановки top12 и чувствительность AP — verification.json каждого фолда.', '',
        '![Сравнение](comparison_all.png)','']
    (REP/'summary_ru.md').write_text('\n'.join(lines),encoding='utf-8')
    record('feature_all_methods_plot_ready','FEATURE frozen-model test scoring completed and added to existing16 rows; original method metrics/intervals/files preserved. Same 5519 full-target test observations; plot visual review pending.',RUN,status='pending_visual_review',
        test_metrics={'map':feature['pooled_map']},artifacts=str(REP.relative_to(ROOT)))
    print('FEATURE_RESULT',feature,flush=True)


def main():
    import fcntl
    torch.set_num_threads(2);torch.set_num_interop_threads(2)
    os.nice(max(0,5-os.getpriority(os.PRIO_PROCESS,0)))
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['run','fold','plot'],default='run',nargs='?');p.add_argument('--fold',type=int);a=p.parse_args()
    DEST.mkdir(parents=True,exist_ok=True);REP.mkdir(parents=True,exist_ok=True)
    if a.stage=='fold':evaluate(a.fold);return
    if a.stage=='plot':plot();return
    with (DEST/'execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);freeze()
        record('feature_test_started','User authorized FEATURE comparison chart: freeze existing validation-selected weights, score/replay same test weeks, add row without replacing existing16. GPU free, no competing training; no fitting/API.',RUN,status='scoring',artifacts=str(REP.relative_to(ROOT)))
        for f in range(3):
            print('FOLD_START',f,flush=True)
            with (REP/f'fold_{f}.log').open('a') as stream:
                subprocess.run([sys.executable,'-u',str(Path(__file__)),'fold','--fold',str(f)],cwd=ROOT,
                    stdout=stream,stderr=subprocess.STDOUT,check=True,env={**os.environ,'PYTHONHASHSEED':'42'})
        plot()


if __name__=='__main__':main()
