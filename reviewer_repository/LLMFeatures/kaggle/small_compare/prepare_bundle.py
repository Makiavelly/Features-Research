"""Freeze existing ContextGNN small data/pairs/references; no sampling or training."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
DEST = ROOT / 'data/kaggle_hm_small_sql_compare_v1'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    source = ROOT / 'data/rel-hm-small-v1'
    for name in ['article', 'customer', 'transactions']:
        shutil.copy2(source / f'db/{name}.parquet', DEST / f'{name}.parquet')
    shutil.copy2(source / 'subset_manifest.json', DEST / 'subset_manifest.json')
    for split in ['train', 'val', 'test']:
        shutil.copy2(source / f'tasks/user-item-purchase/{split}.parquet', DEST / f'{split}_targets.parquet')
    manual = json.loads((ROOT / 'ContextGNN/cache/hm_small_v1/manual/manifest.json').read_text())
    pairs = pd.concat([pd.read_parquet(ROOT / p, columns=['timestamp', 'customer_id', 'article_id', 'label'])
                       for p in manual['files']['train']], ignore_index=True)
    keys = pairs.sort_values(['timestamp', 'customer_id', 'article_id']).reset_index(drop=True)
    keys['timestamp'] = keys.timestamp.astype('datetime64[ns]')
    keys[['customer_id', 'article_id', 'label']] = keys[['customer_id', 'article_id', 'label']].astype(np.int64)
    digest = hashlib.sha256(pd.util.hash_pandas_object(keys, index=False).values.tobytes()).hexdigest()
    reference = json.loads((ROOT / 'ContextGNN/results/hm_small_v1/lightgbm_manual/metrics.json').read_text())
    assert len(pairs) == 72813 and digest == reference['train_pair_sha256']
    assert len(pairs[['timestamp', 'customer_id']].drop_duplicates()) == 4804
    pairs.to_parquet(DEST / 'train_pairs.parquet', index=False)
    # Fixed disjoint user-time rows within the original validation table.
    indices = np.random.default_rng(42).permutation(304)
    selection = {'search': sorted(indices[:128].tolist()), 'confirm': sorted(indices[128:216].tolist()),
                 'heldout_val': sorted(indices[216:].tolist())}
    (DEST / 'selection.json').write_text(json.dumps(selection, indent=2))
    refs = DEST / 'references'
    refs.mkdir(exist_ok=True)
    entries = []
    models = [(p.name, p) for p in (ROOT / 'ContextGNN/results/hm_small_v1').iterdir()
              if p.is_dir() and (p / 'metrics.json').exists() and (p / 'val_predictions.npy').exists()]
    models += [('recformer_' + p.name, p) for p in (ROOT / 'Recformer/results/hm_small_seed42_v1').iterdir()
               if p.is_dir() and (p / 'metrics.json').exists() and (p / 'val_predictions.npy').exists()]
    for label, folder in sorted(models):
        metrics = json.loads((folder / 'metrics.json').read_text())
        entry = {'model': label, 'source': str(folder.relative_to(ROOT)), 'metrics': metrics}
        for split in ['val', 'test']:
            pred = np.load(folder / f'{split}_predictions.npy')
            assert pred.shape == (304 if split == 'val' else 250, 12)
            assert ((pred >= 0) & (pred < 5000)).all()
            assert all(len(set(row)) == 12 for row in pred)
            shutil.copy2(folder / f'{split}_predictions.npy', refs / f'{label}_{split}.npy')
        entries.append(entry)
    (refs / 'sources.json').write_text(json.dumps(entries, indent=2))
    manifest = {'bundle_id': 'hm_small_sql_compare_v1', 'subset': 'rel-hm-small-v1', 'catalog': 5000,
                'train_pairs': len(pairs), 'train_user_times': 4804, 'train_pair_sha256': digest,
                'val_users': 304, 'test_users': 250, 'search_users': 128, 'confirmation_users': 88,
                'heldout_val_users': 88, 'evaluation': 'all 5000 items, no candidate sampling',
                'reference_models': [e['model'] for e in entries],
                'files': {str(p.relative_to(DEST)): sha(p) for p in sorted(DEST.rglob('*')) if p.is_file() and p.name != 'manifest.json'}}
    (DEST / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    archive = HERE.parent / 'hm_small_sql_compare_v1.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as output:
        for p in sorted(DEST.rglob('*')):
            if p.is_file():
                output.write(p, p.relative_to(DEST))
    print(json.dumps({'archive': str(archive), 'bytes': archive.stat().st_size,
                      'manifest_sha256': sha(DEST / 'manifest.json'), 'reference_models': manifest['reference_models']}, indent=2))


if __name__ == '__main__':
    main()
