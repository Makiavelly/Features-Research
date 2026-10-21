"""Post-hoc novelty diagnostics, preserving inaccessible targets and frozen models."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

os.environ.setdefault('OMP_NUM_THREADS','2')
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
os.environ.setdefault('MKL_NUM_THREADS','2')
from common import ROOT,DATA,OUT,OLD,REPORT,read,write,sha,record

RUN='hm_medium_novelty_audit_seed42_v1'
DEST=OUT/'novelty_audit_v1'
REP=REPORT/'novelty_audit_v1'
GROUPS=['repeat','new_variant','new_product_known_type','new_type','unknown_metadata']
LABELS={'repeat':'Повторный товар','new_variant':'Новый вариант знакомого продукта',
        'new_product_known_type':'Новый продукт знакомого типа','new_type':'Новый тип товара',
        'unknown_metadata':'Неизвестные атрибуты','new':'Все новые товары','all':'Все товары'}


def methods(fold):
    result={s['method']:dict(label=s['label'],prediction=ROOT/next(p for p in read(REPORT/'context_combined_test_v1/comparison.json')['prediction_sha256']
        if f'/fold_{fold}/' in p and method_token(s['method']) in p))
        for s in read(REPORT/'context_combined_test_v1/comparison.json')['summary']}
    result['contextgnn_old']=dict(label='ContextGNN corrected (previous)',prediction=OUT/f'fold_{fold}/gnn_timefix_refit/contextgnn/test_predictions.npy')
    return result


def method_token(key):
    tokens={'contextgnn':'/context_combined_test_v1/', 'idgnn':'/gnn_timefix_refit/idgnn/',
        'manual':'/lightgbm_manual/','raw15':'/lightgbm_raw15/','tdm':'/tdm/fixed/beam/',
        'recformer_zero':'/recformer/zero_shot/','recformer_baseline':'/recformer/finetuned/',
        'recformer_tuned':'/recformer_grid/'+read(REPORT/'recformer_pretest_freeze.json')['selected_label']+'/finetuned/'}
    if key in tokens:return tokens[key]
    mode,budget=key.rsplit('_',1)
    return f'/{mode}/budgets/{budget}/'


def output(fold,key):
    p=DEST/f'fold_{fold}'/key
    p.mkdir(parents=True,exist_ok=True)
    return p


def protocol():
    REP.mkdir(parents=True,exist_ok=True)
    frozen={}
    for fold in range(3):
        for item in methods(fold).values():
            p=item['prediction'];frozen[str(p.relative_to(ROOT))]=sha(p)
        for name in ['customer_id_map.csv','article_id_map.csv','bundle/test_targets.parquet','subset_manifest.json']:
            p=DATA/f'fold_{fold}'/name;frozen[str(p.relative_to(ROOT))]=sha(p)
    p=ROOT/'data/rel-hm/db/article.parquet';frozen[str(p.relative_to(ROOT))]=sha(p)
    value=dict(run_id=RUN,no_training=True,no_api=True,no_model_selection=True,
        history='ALL locally available source H&M transactions, for the evaluated customers, t_dat<=each cutoff; includes noncatalog purchases; original model inputs unchanged',
        groups=GROUPS,category='product_type_no; product_code identifies product variants; no manufacturer field assumed',
        targets='All original targets including IDs>=10000; decode to original_article_id=target-10000 outside catalog',
        metrics='Group recall/hit on users with group targets; conditional available-target diagnostics separately; AP contributions retain original denominator; new-only ranking masks ALL past purchased candidate IDs',
        tdm='Original beam64 search unchanged; exclude seen items before final leaf top12, using all scored final leaves, not only saved top12; inaccessible/pruned targets remain in denominators',
        idgnn='Novel zero-score tie fillers measured but explicitly identified as unscored/unpersonalized',
        bootstrap='5000 paired original-customer clusters across three folds for principal new-item contrasts',
        reference_hashes=frozen,sources={n:sha(ROOT/'CVFollowup'/n) for n in ['novelty_audit.py','novelty_scores.py','novelty_tdm.py','novelty_report.py']},
        limitation='Post-hoc diagnostics on already inspected test; no independent confirmation.')
    path=REP/'protocol.json'
    if path.exists():assert read(path)==value,'Changed protocol: new ID required'
    else:write(path,value)
    return value


def classify(article,seen,products,types,product,typecode):
    if article in seen:return 0
    p=product.get(article);t=typecode.get(article)
    if p is not None and p in products:return 1
    if t is None:return 4
    return 2 if t in types else 3


def prepare():
    import duckdb
    import numpy as np
    import pandas as pd
    if (DEST/'data_ready.json').exists():return
    DEST.mkdir(parents=True,exist_ok=True)
    article=pd.read_parquet(ROOT/'data/rel-hm/db/article.parquet',columns=['article_id','product_code','product_type_no'])
    product={int(a):None if pd.isna(p) else int(p) for a,p in zip(article.article_id,article.product_code)}
    types={int(a):None if pd.isna(t) else int(t) for a,t in zip(article.article_id,article.product_type_no)}
    imap=pd.read_csv(DATA/'fold_0/article_id_map.csv').sort_values('article_id')
    candidate=imap.original_article_id.to_numpy(dtype=np.int64)
    assert np.array_equal(imap.article_id,np.arange(10000))
    umap=pd.read_csv(DATA/'fold_0/customer_id_map.csv').set_index('customer_id').original_customer_id
    wanted=set()
    for fold in range(3):
        table=pd.read_parquet(DATA/f'fold_{fold}/bundle/test_targets.parquet')
        wanted.update(map(int,umap.loc[table.customer_id]))
        assert np.array_equal(pd.read_csv(DATA/f'fold_{fold}/article_id_map.csv').original_article_id,candidate)
    con=duckdb.connect();con.execute('SET threads=2');con.execute("SET memory_limit='1GB'")
    con.register('wanted',pd.DataFrame({'customer_id':sorted(wanted)}))
    hist=con.execute('SELECT t.customer_id,t.article_id,t.t_dat FROM read_parquet(?) t JOIN wanted w USING(customer_id) WHERE t.t_dat<=? ORDER BY t.customer_id,t.t_dat,t.article_id',
        [str(ROOT/'data/rel-hm/db/transactions.parquet'),pd.Timestamp('2020-09-14')]).fetchdf()
    con.close()
    history={int(u):(g.t_dat.to_numpy(dtype='datetime64[ns]'),g.article_id.to_numpy(dtype=np.int64)) for u,g in hist.groupby('customer_id',sort=False)}
    audit=[]
    for fold in range(3):
        table=pd.read_parquet(DATA/f'fold_{fold}/bundle/test_targets.parquet')
        masks=np.zeros((len(table),10000),dtype=bool)
        annotations=[]
        for i,row in enumerate(table.itertuples(index=False)):
            original_user=int(umap.loc[row.customer_id])
            times,items=history.get(original_user,(np.array([],dtype='datetime64[ns]'),np.array([],dtype=np.int64)))
            stop=np.searchsorted(times,np.datetime64(row.timestamp,'ns'),side='right')
            assert stop==0 or times[stop-1]<=np.datetime64(row.timestamp,'ns')
            seen=set(map(int,items[:stop]));ps={product[x] for x in seen if product.get(x) is not None};ts={types[x] for x in seen if types.get(x) is not None}
            masks[i]=np.isin(candidate,list(seen))
            target=sorted(set(map(int,row.article_id)))
            original=[int(candidate[x]) if x<10000 else x-10000 for x in target]
            assert all(x in product for x in original),'Unknown source article ID'
            groups=[classify(a,seen,ps,ts,product,types) for a in original]
            annotations.append(dict(fold=fold,row=i,customer_id=int(row.customer_id),original_customer_id=original_user,
                cutoff=str(row.timestamp),targets=target,original_targets=original,groups=groups,
                available=[x<10000 for x in target],source_history_purchases=stop,source_history_unique=len(seen),
                seen_candidate_items=int(masks[i].sum())))
        folder=DEST/f'fold_{fold}';folder.mkdir(parents=True,exist_ok=True)
        np.save(folder/'seen_mask.npy',masks)
        write(folder/'annotations.json',annotations)
        audit.append(dict(fold=fold,users=len(table),all_targets=sum(len(a['targets']) for a in annotations),
            available_targets=sum(sum(a['available']) for a in annotations),
            source_history_min=str(hist.t_dat.min()),cutoff=str(table.timestamp.iloc[0])))
    write(DEST/'data_ready.json',dict(source_history_rows=len(hist),unique_test_customers=len(wanted),folds=audit))
    record('novelty_data_ready','Novelty labels and exclusion masks built from full source past history, including out-of-catalog purchases; all future targets retained.',RUN,status='diagnosing',data_audit=audit)


def saved_scores():
    import numpy as np
    for fold in range(3):
        masks=np.load(DEST/f'fold_{fold}/seen_mask.npy',mmap_mode='r')
        for key,item in methods(fold).items():
            score=item['prediction'].with_name('test_scores.npy')
            if not score.exists():continue
            folder=output(fold,key)
            if (folder/'verification.json').exists():continue
            matrix=np.load(score,mmap_mode='r')
            expected=np.load(item['prediction'])
            predictions=[];positive=0
            for start in range(0,len(matrix),64):
                values=np.array(matrix[start:start+64],copy=True)
                pred=np.argsort(-values,axis=1,kind='stable')[:,:12]
                assert np.array_equal(pred,expected[start:start+64]),(fold,key,'normal replay')
                values[masks[start:start+64]]=-np.inf
                novel=np.argsort(-values,axis=1,kind='stable')[:,:12]
                assert np.isfinite(np.take_along_axis(values,novel,axis=1)).all()
                positive+=int((np.take_along_axis(values,novel,axis=1)>0).sum())
                predictions.append(novel)
            novel=np.concatenate(predictions)
            assert not masks[np.arange(len(novel))[:,None],novel].any()
            np.save(folder/'new_predictions.npy',novel)
            if key=='idgnn':assert positive==0,'Unexpected nonzero IDGNN scores for unseen items'
            write(folder/'verification.json',dict(passed=True,normal_top12_identical=True,
                source_scores_sha256=sha(score),new_recommendations=len(novel)*12,positive_new_scores=positive,
                policy='mask seen candidates, rerank full saved scores; stable item-ID ties',
                warning='IDGNN new recommendations are zero-score ties, not personalized scores' if key=='idgnn' else None))
            print('SAVED',fold,key,flush=True)


def per_user(pred,annotation):
    import numpy as np
    pred=np.asarray(pred)
    valid=pred>=0
    target=annotation['targets'];group=annotation['groups'];available=annotation['available']
    lookup=dict(zip(target,group))
    hits=np.array([int(p) in lookup for p in pred],dtype=float)
    precision=np.cumsum(hits)/np.arange(1,len(pred)+1)
    total=len(target)
    out={}
    for name in ['all',*GROUPS,'new']:
        wanted=list(range(len(target))) if name=='all' else [j for j,g in enumerate(group) if (g!=0 if name=='new' else GROUPS[g]==name)]
        truth={target[j] for j in wanted};avail={target[j] for j in wanted if available[j]}
        gh=np.array([int(p) in truth for p in pred],dtype=float)
        n=len(truth);a=len(avail);count=int(gh.sum())
        ap=float((gh*np.cumsum(gh)/np.arange(1,len(pred)+1)).sum()/min(12,n)) if n else None
        cap=min(12,a)/min(12,n) if n else None
        conditional_ap=float((gh*np.cumsum(gh)/np.arange(1,len(pred)+1)).sum()/min(12,a)) if a else None
        out[name]=dict(targets=n,available=a,hits=count,recall=count/n if n else None,
            available_recall=count/a if a else None,hit=float(count>0) if n else None,
            available_hit=float(count>0) if a else None,map=ap,available_map=conditional_ap,
            oracle_map=cap,ap_contribution=float((gh*precision).sum()/min(12,total)))
    assert abs(sum(out[g]['ap_contribution'] for g in GROUPS)-out['all']['map'])<1e-12
    return out


def metric_tests():
    import numpy as np
    a=dict(targets=[0,1,2,3,10004],groups=[0,1,2,3,3],available=[True,True,True,True,False])
    normal=per_user(np.array([0,1,2,3,*range(10,18)]),a)
    novel=per_user(np.array([1,2,3,*range(10,19)]),a)
    assert abs(normal['all']['map']-.8)<1e-12
    assert normal['new_type']['recall']==.5 and normal['new_type']['available_recall']==1.
    assert normal['new_type']['oracle_map']==.5
    assert abs(novel['new']['map']-.75)<1e-12
    assert abs(novel['new']['oracle_map']-.75)<1e-12
    assert novel['repeat']['hits']==0
    a=dict(targets=[10001],groups=[3],available=[False])
    empty=per_user(np.arange(12),a)
    assert empty['new']['recall']==0 and empty['new']['available_recall'] is None
    assert empty['all']['map']==0 and empty['new']['oracle_map']==0
    assert classify(5,{5},{1},{2},{5:1},{5:2})==0
    assert classify(6,{5},{1},{2},{6:1},{6:2})==1
    assert classify(6,{5},{1},{2},{6:3},{6:2})==2
    assert classify(6,{5},{1},{2},{6:3},{6:4})==3
    assert classify(6,{5},{1},{2},{6:3},{6:None})==4
    write(REP/'metric_verification.json',dict(passed=True,checks=['AP decomposition','unavailable targets penalize full denominator','conditional unavailable is NA, never perfect score','new-only denominator','group exclusivity']))


def analyze():
    import numpy as np
    import pandas as pd
    rows=[];inventory=[];model_info={}
    for fold in range(3):
        annotations=read(DEST/f'fold_{fold}/annotations.json')
        masks=np.load(DEST/f'fold_{fold}/seen_mask.npy',mmap_mode='r')
        for a in annotations:
            empty=per_user(np.full(12,-1),a)
            for name in ['all',*GROUPS,'new']:
                r=empty[name]
                inventory.append(dict(fold=fold,row=a['row'],customer=a['original_customer_id'],group=name,
                    targets=r['targets'],available=r['available'],oracle_map=r['oracle_map']))
        for key,item in methods(fold).items():
            folder=output(fold,key)
            assert read(folder/'verification.json')['passed'],(fold,key)
            prediction=np.load(folder/'new_predictions.npy')
            for mode,pred in [('normal',np.load(item['prediction'])),('new_only',prediction)]:
                assert pred.shape==(len(annotations),12)
                for i,(rec,a) in enumerate(zip(pred,annotations)):
                    valid=rec[rec>=0]
                    assert len(valid)==len(set(map(int,valid)))
                    if mode=='new_only':assert not masks[i,valid].any()
                    metrics=per_user(rec,a)
                    for group,value in metrics.items():
                        rows.append(dict(fold=fold,row=i,customer=a['original_customer_id'],method=key,label=item['label'],mode=mode,group=group,
                            recommendation_count=len(valid),repeat_recommendations=int(masks[i,valid].sum()),**value))
            model_info[f'{fold}/{key}']=read(folder/'verification.json')
    table=pd.DataFrame(rows)
    table.to_parquet(REP/'per_user_metrics.parquet',index=False)
    table.groupby(['method','label','mode','group'],sort=False).apply(aggregate,include_groups=False).reset_index().to_csv(REP/'metrics.csv',index=False)
    table.groupby(['fold','method','label','mode','group'],sort=False).apply(aggregate,include_groups=False).reset_index().to_csv(REP/'fold_metrics.csv',index=False)
    inv=pd.DataFrame(inventory)
    inv.to_parquet(REP/'target_inventory.parquet',index=False)
    coverage=[]
    for group,g in inv.groupby('group',sort=False):
        eligible=g[g.targets>0];accessible=g[g.available>0]
        coverage.append(dict(group=group,targets=int(g.targets.sum()),available=int(g.available.sum()),
            unavailable=int((g.targets-g.available).sum()),coverage=float(g.available.sum()/g.targets.sum()) if g.targets.sum() else None,
            users_with_targets=len(eligible),users_with_available_targets=len(accessible),users_only_unavailable=len(eligible)-len(accessible),
            oracle_map=float(eligible.oracle_map.mean()) if len(eligible) else None))
    write(REP/'coverage.json',coverage)
    write(REP/'model_verification.json',model_info)
    for path,digest in read(REP/'protocol.json')['reference_hashes'].items():assert sha(ROOT/path)==digest
    record('novelty_analysis_ready','All frozen-model ordinary/new-only rankings evaluated by novelty groups; unavailable targets retained and separately counted; reference hashes unchanged.',RUN,status='report_pending',artifacts=str(REP.relative_to(ROOT)))


def aggregate(g):
    import pandas as pd
    eligible=g[g.targets>0];available=g[g.available>0]
    return pd.Series(dict(users=len(g),eligible_users=len(eligible),available_users=len(available),
        targets=int(g.targets.sum()),available_targets=int(g.available.sum()),hits=int(g.hits.sum()),
        macro_recall=eligible.recall.mean(),micro_recall=g.hits.sum()/g.targets.sum() if g.targets.sum() else None,
        available_macro_recall=available.available_recall.mean(),available_micro_recall=g.hits.sum()/g.available.sum() if g.available.sum() else None,
        hit_rate=eligible.hit.mean(),available_hit_rate=available.available_hit.mean(),
        map=eligible['map'].mean(),available_map=available.available_map.mean(),
        ap_contribution=g.ap_contribution.mean(),oracle_map=eligible.oracle_map.mean(),
        repeat_slot_fraction=g.repeat_recommendations.sum()/g.recommendation_count.sum() if g.recommendation_count.sum() else None))


def run():
    import fcntl
    DEST.mkdir(parents=True,exist_ok=True)
    with (DEST/'execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        protocol();metric_tests()
        record('novelty_started','Authorized novelty diagnostics for all comparison methods, full source history and inaccessible future items; no fitting or API requests.',RUN,status='diagnosing',artifacts=str(REP.relative_to(ROOT)))
        prepare();saved_scores()
        for fold in range(3):
            for kind in ['raw15','manual','api']:
                log=REP/f'fold_{fold}_{kind}.log'
                with log.open('a') as stream:
                    subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/novelty_scores.py'),str(fold),kind],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True)
        log=REP/'tdm.log'
        with log.open('a') as stream:
            subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/novelty_tdm.py')],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True)
        analyze()
        subprocess.run([sys.executable,'-u',str(ROOT/'CVFollowup/novelty_report.py')],cwd=ROOT,check=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['run','prepare','analyze','test'],default='run',nargs='?');a=p.parse_args()
    REP.mkdir(parents=True,exist_ok=True)
    if a.stage=='run':run()
    elif a.stage=='prepare':prepare()
    elif a.stage=='analyze':analyze()
    else:metric_tests()
