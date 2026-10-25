"""Isolated CPU evaluation using the original local Qwen SQL FeatureEngine."""
import os
if __name__ == '__main__':
    os.environ.update(CUDA_VISIBLE_DEVICES='', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
import argparse
import gc
import hashlib
import json
from pathlib import Path
import signal
import time
import numpy as np
import pandas as pd
import lightgbm as lgb
from features import FeatureEngine, validate_program


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    path = Path(path)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, indent=2), encoding='utf-8')
    temp.replace(path)


def ap12(pred, targets):
    pred = np.asarray(pred)
    assert pred.shape == (len(targets), 12)
    assert all(len(set(row)) == 12 for row in pred)
    hits = np.array([np.isin(row, np.unique(t)) for row, t in zip(pred, targets)])
    denominators = np.minimum(12, [len(np.unique(t)) for t in targets])
    assert (denominators > 0).all()
    return ((hits.cumsum(1) / np.arange(1, 13)) * hits).sum(1) / denominators


def timed_frame(engine, pairs):
    def timeout(*_):
        raise TimeoutError('Feature construction exceeded 60 seconds')
    previous = signal.signal(signal.SIGALRM, timeout)
    signal.alarm(60)
    try:
        return engine.matrix(pairs)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


def preflight(engine, pairs, program):
    for cutoff in sorted(pairs.timestamp.unique())[:1] + sorted(pairs.timestamp.unique())[-1:]:
        sample = pairs[pairs.timestamp == cutoff].head(128).reset_index(drop=True)
        engine.prepare(cutoff, sample.customer_id.values, program)
        whole = timed_frame(engine, sample)
        permutation = np.random.default_rng(42).permutation(len(sample))
        permuted = timed_frame(engine, sample.iloc[permutation].reset_index(drop=True))
        np.testing.assert_allclose(permuted[np.argsort(permutation)], whole, equal_nan=True)
        middle = len(sample) // 2
        chunks = np.concatenate([timed_frame(engine, sample.iloc[:middle]), timed_frame(engine, sample.iloc[middle:])])
        np.testing.assert_allclose(chunks, whole, equal_nan=True)
    return {'passed': True, 'row_permutation': True, 'batch_invariance': True}


def fit(engine, root, directory, program, config):
    pairs = pd.read_parquet(root / 'train_pairs.parquet')
    assert len(pairs) == config['train_pairs']
    checks = preflight(engine, pairs, program)
    parts = []
    labels = []
    for cutoff, frame in pairs.groupby('timestamp', sort=True):
        engine.prepare(cutoff, frame.customer_id.values, program)
        parts.append(timed_frame(engine, frame))
        labels.append(frame.label.to_numpy())
    values, y = np.concatenate(parts), np.concatenate(labels)
    params = dict(objective='binary', verbosity=-1, learning_rate=.05, num_leaves=31,
                  min_data_in_leaf=100, max_bin=127, feature_fraction=.9, bagging_fraction=.8,
                  bagging_freq=1, deterministic=True, force_col_wise=True, seed=42,
                  feature_fraction_seed=42, bagging_seed=42, data_random_seed=42,
                  num_threads=config['cpu_threads'])
    # Same fixed downstream settings for both LLMs; reference manual model tuned leaves15/31.
    names = engine.feature_names
    categorical = [n for n in names if n.startswith('raw_') and n not in {'raw_u_age', 'raw_u_fn', 'raw_u_active'}]
    dataset = lgb.Dataset(values, label=y, feature_name=names, categorical_feature=categorical)
    history = {}
    model = lgb.train(params, dataset, num_boost_round=config['lightgbm_rounds'], valid_sets=[dataset],
                      valid_names=['train'], callbacks=[lgb.record_evaluation(history)])
    model.save_model(str(directory / 'model.txt'))
    write(directory / 'learning_curve.json', history)
    write(directory / 'feature_schema.json', {'features': names, 'categorical': categorical,
          'train_pairs': len(y), 'train_pair_sha256': config['train_pair_sha256'], 'preflight': checks,
          'category_maps': engine.category_maps, 'params': params})
    del values, y, parts, dataset, model
    gc.collect()


def predict(engine, root, directory, stage, program, config, output_stage=None):
    split = 'test' if stage == 'test' else 'val'
    target = pd.read_parquet(root / f'{split}_targets.parquet')
    if stage in {'search', 'confirm', 'heldout_val'}:
        selected = json.loads((root / 'selection.json').read_text())[stage]
        target = target.iloc[selected].reset_index(drop=True)
    catalog = np.sort(engine.items.article_id.to_numpy(dtype=np.int64))
    assert np.array_equal(catalog, np.arange(5000))
    assert target.timestamp.nunique() == 1
    engine.prepare(target.timestamp.iloc[0], target.customer_id.values, program)
    model = lgb.Booster(model_file=str(directory / 'model.txt'))
    all_predictions = []
    for start in range(0, len(target), config['scoring_user_batch']):
        users = target.customer_id.iloc[start:start + config['scoring_user_batch']].to_numpy()
        pairs = pd.DataFrame({'customer_id': np.repeat(users, len(catalog)), 'article_id': np.tile(catalog, len(users))})
        scores = model.predict(timed_frame(engine, pairs), num_threads=config['cpu_threads']).reshape(len(users), len(catalog))
        assert np.isfinite(scores).all()
        all_predictions.extend([catalog[np.lexsort((catalog, -row))[:12]] for row in scores])
    pred = np.array(all_predictions)
    ap = ap12(pred, target.article_id)
    output_stage = output_stage or stage
    np.save(directory / f'{output_stage}_predictions.npy', pred)
    np.save(directory / f'{output_stage}_ap.npy', ap)
    np.save(directory / f'{output_stage}_users.npy', target.customer_id.to_numpy())
    return {'map': float(ap.mean()), 'users': len(target), 'pairs': len(target) * len(catalog),
            'full_catalog': 5000, 'predictions_sha256': sha(directory / f'{output_stage}_predictions.npy')}


def main():
    parser = argparse.ArgumentParser()
    for name in ['data', 'directory', 'stage', 'config']:
        parser.add_argument('--' + name, required=True)
    args = parser.parse_args()
    root, directory = Path(args.data), Path(args.directory)
    config = json.loads(Path(args.config).read_text())
    source = directory / 'program.json'
    program = validate_program(json.loads(source.read_text()))
    started = time.perf_counter()
    engine = FeatureEngine(directory / 'scratch', root)
    engine.con.execute('SET enable_external_access=false')
    try:
        if args.stage == 'search' and not (directory / 'model.txt').exists():
            fit(engine, root, directory, program, config)
        elif args.stage == 'preflight':
            checks = preflight(engine, pd.read_parquet(root / 'train_pairs.parquet'), program)
            write(directory / 'preflight_metrics.json', checks)
            return
        stage = args.stage.removeprefix('replay_')
        metric = predict(engine, root, directory, stage, program, config, output_stage=args.stage)
        metric.update(program_sha256=sha(source), model_sha256=sha(directory / 'model.txt'), seconds=time.perf_counter() - started)
        if args.stage.startswith('replay_'):
            # Save replay separately; original files are preserved by host before running replay.
            original = json.loads((directory / f'{stage}_metrics.json').read_text())
            assert metric['predictions_sha256'] == original['predictions_sha256'], 'Frozen model replay differs'
            assert metric['map'] == original['map']
            metric['passed'] = True
        write(directory / f'{args.stage}_metrics.json', metric)
    finally:
        engine.close()


if __name__ == '__main__':
    main()
