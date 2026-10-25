"""Export a fixed, small H&M experiment without touching local running experiments."""
import hashlib
import json
from pathlib import Path
import zipfile
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "data/kaggle_hm_llmfe_fulltrain_v2"
EXPORT = ROOT / "LLMFeatures/kaggle"
ITEM_COLUMNS = ['product_code','product_type_no','graphical_appearance_no','colour_group_code',
                'perceived_colour_value_id','perceived_colour_master_id','department_no',
                'index_group_no','section_no','garment_group_no']
USER_COLUMNS = ['age','FN','Active','club_member_status','fashion_news_frequency']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    if (DEST / 'manifest.json').exists():
        raise RuntimeError('Bundle already exists; use a new version for a changed sample')
    source = ROOT/'baseline/cache/llmfe_qwen25coder7b_v2/train_pairs.parquet'
    train = pd.read_parquet(source)
    snapshots = sorted(train.timestamp.unique())
    assert len(train)==803377 and len(train[['customer_id','timestamp']].drop_duplicates())==50000
    import shutil
    shutil.copy2(source,DEST/'train_pairs.parquet')
    assert sha(source)==sha(DEST/'train_pairs.parquet')
    cohort = set(train.customer_id)
    splits = {}
    for split in ['val','test']:
        targets = pd.read_parquet(ROOT/f'data/rel-hm/tasks/user-item-purchase/{split}.parquet')
        pools = pd.read_parquet(ROOT/f'RelBenchGNN/results/seed_42/inference/{split}_candidates.parquet')
        assert np.array_equal(targets.customer_id.values,pools.customer_id.values)
        order = np.random.default_rng(42 if split=='val' else 43).permutation(len(targets))
        selections = {'search':order[:256], 'confirm':order[256:768], 'val':order[768:1792]} if split=='val' else {'test':order[:2048]}
        native = np.load(ROOT/f'RelBenchGNN/results/seed_42/{split}_predictions.npy')
        for name, indices in selections.items():
            indices=np.sort(indices)
            target = targets.iloc[indices].reset_index(drop=True)
            pool = pools.iloc[indices].reset_index(drop=True)
            counts=pool.candidates.map(len).to_numpy()
            pairs=pd.DataFrame({'customer_id':np.repeat(target.customer_id.values,counts),
                                'article_id':np.concatenate(pool.candidates.values),
                                'timestamp':np.repeat(target.timestamp.values,counts)})
            target.to_parquet(DEST/f'{name}_targets.parquet',index=False)
            pairs.to_parquet(DEST/f'{name}_pairs.parquet',index=False)
            if name in ['val','test']:
                np.save(DEST/f'{name}_idgnn_reference.npy',native[indices])
                references={'manual_lightgbm':ROOT/f'baseline/results/manual_v1/lightgbm/seed_42/{split}_predictions.npy',
                            'gnn_lightgbm':ROOT/f'baseline/results/gnn_embeddings_v1/{split}_predictions.npy'}
                for label,file in references.items():
                    predictions=np.load(file)[indices]
                    assert all(np.isin(pred,c).all() for pred,c in zip(predictions,pool.candidates))
                    np.save(DEST/f'{name}_{label}_reference.npy',predictions)
            cohort.update(target.customer_id)
            splits[name]={'users':len(target),'pairs':len(pairs),
                          'cutoff':str(target.timestamp.iloc[0]),'source_split':split,
                          'original_row_indices':indices.tolist()}
    first=pd.Timestamp(min(snapshots))-pd.Timedelta(days=180)
    last=max(pd.Timestamp(s['cutoff']) for s in splits.values())
    tx_path=ROOT/'data/rel-hm/db/transactions.parquet'
    history=pq.read_table(tx_path, columns=['customer_id','article_id','t_dat','price','sales_channel_id'],
                          filters=[('customer_id','in',sorted(cohort)),('t_dat','>',first),('t_dat','<=',last)]).to_pandas()
    history.to_parquet(DEST/'history.parquet',index=False)
    articles=pd.read_parquet(ROOT/'data/rel-hm/db/article.parquet',columns=['article_id',*ITEM_COLUMNS])
    # Metadata for all catalog items is small; scoring still uses only fixed pools.
    articles.to_parquet(DEST/'articles.parquet',index=False)
    customers=pq.read_table(ROOT/'data/rel-hm/db/customer.parquet',columns=['customer_id',*USER_COLUMNS],
                            filters=[('customer_id','in',sorted(cohort))]).to_pandas()
    categories={}
    for column in ['club_member_status','fashion_news_frequency']:
        category=customers[column].astype('category')
        categories[column]=list(category.cat.categories.astype(str))
        customers[column]=category.cat.codes.astype('float32')
    customers.to_parquet(DEST/'customers.parquet',index=False)
    manifest={'bundle_id':'hm_llmfe_kaggle_fulltrain_v2','seed':42,
              'purpose':'bounded H&M ranking adaptation, NOT a reproduction of paper datasets',
              'train_user_times':len(train[['customer_id','timestamp']].drop_duplicates()),
              'train_pairs':len(train),'train_snapshots':[str(pd.Timestamp(s)) for s in snapshots],
              'train_source_sha256':sha(source),'history_rows':len(history),'history_cohort_users':len(cohort),
              'history_lookback_days':180,'history_scope':'only selected train/evaluation customer cohort; no population-wide sales statistics',
              'history_first_date':str(first),'history_last_cutoff':str(last),
              'splits':splits,'categories':categories,'item_columns':ITEM_COLUMNS,'user_columns':USER_COLUMNS,
              'candidate_protocol':'exact saved ID-GNN seed42 candidates on selected rows, no injected targets',
              'idgnn_reference':'GNN backbone trained on larger original graph budget; context only',
              'tree_reference_protocol':'manual and GNN→LightGBM reuse original803377 supervised pairs; selected same val/test candidate rows; tuning/seeds differ',
              'source_download_manifest_sha256':sha(ROOT/'data/download_manifest.json'),
              'files':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(DEST.iterdir()) if p.is_file()}}
    (DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    archive=EXPORT/'hm_llmfe_kaggle_fulltrain_v2.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=3) as z:
        for p in sorted(DEST.iterdir()):
            z.write(p,arcname=p.name)
    (EXPORT/'bundle_summary.json').write_text(json.dumps({
        'archive':archive.name,'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,
        **{k:v for k,v in manifest.items() if k not in ['files','splits']},
        'splits':{k:{n:v for n,v in d.items() if n!='original_row_indices'} for k,d in splits.items()}},indent=2),encoding='utf-8')
    print(json.dumps({'archive_mb':archive.stat().st_size/1e6,'train_pairs':len(train),
                      'train_user_times':manifest['train_user_times'],'history_rows':len(history),
                      'splits':{k:{'users':v['users'],'pairs':v['pairs']} for k,v in splits.items()}}))


if __name__=='__main__':
    main()
