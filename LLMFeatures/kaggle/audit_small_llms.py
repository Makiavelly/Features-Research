"""Audit user-supplied real Kaggle exports; never retrain or reselect on test."""
import hashlib
import json
from pathlib import Path
import os
import shutil
import subprocess
import sys
import time
import importlib.metadata
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import zipfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/hm_small_llms_v1'
ARCHIVES = {
    'qwen_llama': ROOT / 'hm_small_qwen_llama_sql_v1_2ecc60d61fd4_results.zip',
    'qwen14b': ROOT / 'hm_small_qwen14b_sql_v1_f373011050bf_results.zip',
}
DATA = ROOT / 'data/kaggle_hm_small_sql_compare_v1'
CODE = ROOT / 'LLMFeatures/kaggle/qwen14_small'
sys.path.insert(0, str(CODE))
from worker import ap12, write
from original_prompt import program_key
from features import FeatureEngine, validate_program

MATCH = ['seed', 'target_successful_distinct', 'max_llm_calls', 'max_repairs_per_proposal', 'islands',
         'memory_programs_per_prompt', 'temperature', 'max_input_tokens', 'max_new_tokens',
         'lightgbm_rounds', 'cpu_threads', 'scoring_user_batch', 'evaluation_timeout_seconds', 'quantization',
         'feature_interface', 'search_users', 'confirmation_users', 'heldout_val_users', 'validation_users',
         'test_users', 'evaluation_catalog', 'bundle_manifest_sha256', 'train_pairs', 'train_pair_sha256',
         'training_examples', 'versions', 'gpu']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unpack():
    roots = {}
    for label, archive in ARCHIVES.items():
        destination = OUT / 'exports' / label
        destination.mkdir(parents=True, exist_ok=True)
        if not (destination / 'run_config.json').exists():
            with zipfile.ZipFile(archive) as z:
                for entry in z.infolist():
                    if not (destination / entry.filename).resolve().is_relative_to(destination.resolve()):
                        raise ValueError('Unsafe ZIP member')
                z.extractall(destination)
        configs = list(destination.rglob('run_config.json'))
        assert len(configs) == 1
        root = configs[0].parent
        roots[label] = root
    return roots


def read(path):
    return json.loads(Path(path).read_text())


def saved_metrics(folder, stage, target):
    metric = read(folder / f'{stage}_metrics.json')
    assert metric['program_sha256'] == sha(folder / 'program.json')
    assert metric['model_sha256'] == sha(folder / 'model.txt')
    assert metric['predictions_sha256'] == sha(folder / f'{stage}_predictions.npy')
    pred = np.load(folder / f'{stage}_predictions.npy')
    assert np.array_equal(np.load(folder / f'{stage}_users.npy'), target.customer_id.to_numpy())
    assert ((pred >= 0) & (pred < 5000)).all()
    assert metric['full_catalog'] == 5000 and metric['pairs'] == len(target) * 5000
    ap = ap12(pred, target.article_id)
    assert abs(float(ap.mean()) - metric['map']) < 1e-12
    np.testing.assert_allclose(ap, np.load(folder / f'{stage}_ap.npy'), atol=0, rtol=0)
    return metric, ap, pred


def chosen_path(export, value):
    path = Path(value)
    if path.name == 'raw_control':
        return export / 'raw_control'
    return export / path.parent.parent.name / 'candidates' / path.name


def run_replay(job):
    label, source, config = job
    destination = OUT / 'independent_replay_kaggle_cpu' / label
    destination.mkdir(parents=True, exist_ok=True)
    for name in ['program.json', 'model.txt', 'val_metrics.json', 'test_metrics.json']:
        shutil.copy2(source / name, destination / name)
    results = {}
    env = {key: value for key, value in os.environ.items() if not any(x in key.upper() for x in ['TOKEN', 'SECRET', 'API_KEY'])}
    env.update(CUDA_VISIBLE_DEVICES='', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    for stage in ['val', 'test']:
        result = destination / f'replay_{stage}_metrics.json'
        if not result.exists():
            command = [sys.executable, str(CODE / 'worker.py'), '--data', str(DATA), '--directory', str(destination),
                       '--stage', 'replay_' + stage, '--config', str(config)]
            with (destination / f'replay_{stage}.log').open('w') as log:
                completed = subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=1800)
            if completed.returncode:
                raise RuntimeError(label + '/' + stage + ': ' + (destination / f'replay_{stage}.log').read_text()[-2000:])
        metric = read(result)
        assert metric['passed'] and metric['model_sha256'] == sha(source / 'model.txt')
        assert metric['predictions_sha256'] == sha(source / f'{stage}_predictions.npy')
        np.testing.assert_array_equal(np.load(destination / f'replay_{stage}_predictions.npy'), np.load(source / f'{stage}_predictions.npy'))
        np.testing.assert_array_equal(np.load(destination / f'replay_{stage}_ap.npy'), np.load(source / f'{stage}_ap.npy'))
        results[stage] = metric
    print('Frozen replay passed:', label, flush=True)
    return {'model': label, 'checks': results}


def main():
    started = time.perf_counter()
    exports = unpack()
    configs = {name: read(folder / 'run_config.json') for name, folder in exports.items()}
    assert all(configs['qwen_llama'][key] == configs['qwen14b'][key] for key in MATCH)
    manifest = read(DATA / 'manifest.json')
    assert sha(DATA / 'manifest.json') == configs['qwen_llama']['bundle_manifest_sha256']
    for name, digest in manifest['files'].items():
        assert sha(DATA / name) == digest
    local_versions = {name: importlib.metadata.version(name) for name in ['numpy', 'pandas', 'pyarrow', 'duckdb', 'lightgbm']}
    assert all(local_versions[name] == configs['qwen_llama']['versions'][name] for name in local_versions), local_versions
    audit = {'archives': {key: {'file': value.name, 'sha256': sha(value)} for key, value in ARCHIVES.items()},
             'matched_fields': MATCH, 'configs_matched': True, 'runs': {}, 'models': {}, 'replays': [],
             'local_replay_cpu_versions': local_versions,
             'initial_environment_issue': 'Original local dependency versions rejected nullable boolean Llama feature as non-numeric; use isolated exact Kaggle CPU versions without editing code/program/model. Earlier logs preserved in independent_replay/.'}
    for name, config in configs.items():
        suffix = ARCHIVES[name].name.removesuffix('_results.zip').rsplit('_', 1)[1]
        assert hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()[:12] == suffix
        for module, digest in config['runtime_sha256'].items():
            assert sha(exports[name] / 'runtime_sources' / module) == digest
            assert sha(CODE / module) == digest
        complete = read(exports[name] / 'complete.json')
        assert complete['status'] == 'complete' and complete['search_budgets_complete']
        audit['runs'][name] = {'fingerprint': suffix, 'source_hashes_verified': True, 'config': config}
    selection = read(DATA / 'selection.json')
    assert sorted(sum(selection.values(), [])) == list(range(304))
    target = {split: pd.read_parquet(DATA / f'{split}_targets.parquet') for split in ['val', 'test']}
    target.update({stage: target['val'].iloc[rows].reset_index(drop=True) for stage, rows in selection.items()})
    all_rows, quality, predictions, states, jobs = [], {}, {}, {}, []
    raw_exports = []
    for export_name, export in exports.items():
        config = configs[export_name]
        raw = export / 'raw_control'
        raw_schema = read(raw / 'feature_schema.json')
        assert raw_schema['train_pairs'] == 72813 and raw_schema['train_pair_sha256'] == manifest['train_pair_sha256']
        row = {'model': 'Raw15_LightGBM', 'source': str(raw.relative_to(ROOT))}
        raw_quality = {}
        for stage in ['search', 'confirm', 'heldout_val', 'val', 'test']:
            metric, ap, pred = saved_metrics(raw, stage, target[stage])
            row[stage + '_map_percent'] = 100 * metric['map']
            raw_quality[stage] = ap
            if export_name == 'qwen_llama':
                predictions[('Raw15_LightGBM', stage)] = pred
            else:
                np.testing.assert_array_equal(pred, predictions[('Raw15_LightGBM', stage)])
        raw_exports.append((raw, raw_quality))
        if export_name == 'qwen_llama':
            all_rows.append(row)
            quality['Raw15_LightGBM'] = raw_quality
            jobs.append(('Raw15_LightGBM', raw, export / 'run_config.json'))
    assert sha(raw_exports[0][0] / 'model.txt') == sha(raw_exports[1][0] / 'model.txt')
    audit['raw_controls_identical'] = True
    for export_name, label, title in [('qwen_llama', 'qwen', 'Qwen7B_LightGBM'),
                                     ('qwen_llama', 'llama', 'Llama8B_LightGBM'),
                                     ('qwen14b', 'qwen14b', 'Qwen14B_LightGBM')]:
        export = exports[export_name]
        state = read(export / label / 'search_state.json')
        trials = state['trials']
        assert state['calls'] == len(trials)
        valid = [trial for trial in trials if trial['status'] == 'valid']
        assert len(valid) == state['measured'] == 20
        keys = set()
        for number, trial in enumerate(trials, 1):
            assert trial['call'] == number and trial['island'] == trial['proposal'] % 3
            if trial['status'] != 'valid':
                continue
            folder = export / label / 'candidates' / f'candidate_{number:03d}'
            program = validate_program(read(folder / 'program.json'))
            key = program_key(program)
            assert key == trial['program_key'] and key not in keys
            keys.add(key)
            schema = read(folder / 'feature_schema.json')
            assert schema['train_pairs'] == 72813 and schema['train_pair_sha256'] == manifest['train_pair_sha256']
            assert schema['preflight']['passed'] and schema['preflight']['batch_invariance']
            metric, ap, pred = saved_metrics(folder, 'search', target['search'])
            assert metric['map'] == trial['score']
        selected = read(export / label / 'selected.json')
        folder = chosen_path(export, selected['directory'])
        assert sha(folder / 'model.txt') == selected['model_sha256']
        assert sha(folder / 'program.json') == selected['program_sha256']
        best = max(selected['confirmation'], key=lambda entry: entry['confirmation_map'])
        assert best['directory'] == selected['directory']
        top3 = sorted(valid, key=lambda entry: (-entry['score'], entry['call']))[:3]
        assert [entry['call'] for entry in selected['confirmation']] == [None] + [entry['call'] for entry in top3]
        for trial in selected['confirmation']:
            metric, ap, pred = saved_metrics(chosen_path(export, trial['directory']), 'confirm', target['confirm'])
            assert metric['map'] == trial['confirmation_map']
        program = read(folder / 'program.json')
        row = {'model': title, 'source': str(folder.relative_to(ROOT))}
        quality[title] = {}
        for stage in ['search', 'confirm', 'heldout_val', 'val', 'test']:
            metric, ap, pred = saved_metrics(folder, stage, target[stage])
            row[stage + '_map_percent'] = 100 * metric['map']
            quality[title][stage] = ap
            predictions[(title, stage)] = pred
        # Additional row-mapping/batch check of the selected SQL programs on real pairs.
        engine = FeatureEngine(OUT / 'probe_scratch' / label, DATA)
        users = target['search'].customer_id.iloc[:8].to_numpy()
        pairs = pd.DataFrame({'customer_id': np.repeat(users, 16), 'article_id': np.tile(np.arange(16), len(users))})
        engine.prepare(target['search'].timestamp.iloc[0], users, program)
        whole = engine.matrix(pairs)
        perm = np.random.default_rng(42).permutation(len(pairs))
        np.testing.assert_allclose(whole, engine.matrix(pairs.iloc[perm].reset_index(drop=True))[np.argsort(perm)], equal_nan=True)
        np.testing.assert_allclose(whole, np.concatenate([engine.matrix(pairs.iloc[:64]), engine.matrix(pairs.iloc[64:])]), equal_nan=True)
        engine.close()
        failures = Counter()
        for trial in trials:
            if trial['status'] == 'rejected':
                error = trial.get('error', '')
                # Last lines contain the DuckDB diagnostic; preserve full errors in exports.
                failures[error.splitlines()[0][:180]] += 1
        stats = {'calls': len(trials), 'valid': len(valid), 'statuses': dict(Counter(t['status'] for t in trials)),
                 'responses': sum((export / label / 'candidates' / f"candidate_{t['call']:03d}" / 'response.json').exists() for t in trials),
                 'repairs': sum(t['repair'] > 0 for t in trials), 'proposals': len({t['proposal'] for t in trials}),
                 'generation_seconds': sum(t.get('seconds', 0) for t in trials),
                 'generated_tokens': sum(t.get('generated_tokens', 0) for t in trials),
                 'failure_stages': dict(Counter(t.get('failure_stage') for t in trials if t['status'] == 'rejected')),
                 'top_errors': failures.most_common(8), 'selected_call': selected['call'],
                 'aggregates': len(program.get('aggregates', [])), 'derived': len(program.get('derived', [])),
                 'aggregate_groupings': [entry['keys'] for entry in program.get('aggregates', [])],
                 'selected': selected, 'program': program, 'row_mapping_probes_passed': True}
        audit['models'][title] = stats
        states[title] = trials
        all_rows.append(row)
        jobs.append((title, folder, export / 'run_config.json'))
        print(title, 'checked:', {k: stats[k] for k in ['calls', 'valid', 'responses', 'aggregates', 'derived']}, flush=True)
    write(OUT / 'audit_pre_replay.json', audit)
    # Two independent CPU workers at once; no training and no local LLM inference.
    with ThreadPoolExecutor(max_workers=2) as pool:
        audit['replays'] = list(pool.map(run_replay, jobs))
    finish_report(audit, all_rows, quality, states, target)
    audit['status'] = 'passed'
    audit['seconds'] = time.perf_counter() - started
    write(OUT / 'audit.json', audit)
    print('AUDIT PASSED', json.dumps({name: {k: value[k] for k in ['calls', 'valid', 'selected_call']} for name, value in audit['models'].items()}), flush=True)


def finish_report(audit, rows, quality, states, target):
    """Defined below; figures and persistent history are generated after replay."""
    pd.DataFrame(rows).to_csv(OUT / 'comparison.csv', index=False)
    write(OUT / 'quality.json', {name: {stage: values.tolist() for stage, values in splits.items()} for name, splits in quality.items()})
    print(pd.DataFrame(rows)[['model', 'val_map_percent', 'test_map_percent']].to_string(index=False), flush=True)


if __name__ == '__main__':
    main()
