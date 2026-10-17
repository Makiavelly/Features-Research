"""Audit real H003 outputs, compare to frozen control, never train or reselect."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import sys
import time
import zipfile
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'reports/h003_small_v1'
DATA = ROOT / 'data/kaggle_hm_small_sql_compare_v1'
ARCHIVE = ROOT / 'hm_small_qwen7b_h003_v1_6852748fc0e4_results.zip'
import audit_small_llms as helpers
from audit_small_llms import sha, read, saved_metrics, chosen_path, program_key, validate_program, FeatureEngine, write


def main():
    started = time.perf_counter()
    export = OUT / 'exports'
    export.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        for item in z.infolist():
            assert (export / item.filename).resolve().is_relative_to(export.resolve())
            if (export / item.filename).exists():
                assert (export / item.filename).read_bytes() == z.read(item.filename)
            else:
                z.extract(item, export)
    config = read(export / 'run_config.json')
    control = ROOT / 'reports/hm_small_llms_v1/exports/qwen_llama'
    old = read(control / 'run_config.json')
    assert all(config[k] == old[k] for k in helpers.MATCH)
    assert config['models']['qwen'] == old['models']['qwen']
    assert config['test_previously_inspected'] and config['arms'] == ['h003a', 'h003b', 'h003c']
    assert not config.get('validation_only_fake_callbacks')
    fingerprint = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()[:12]
    assert ARCHIVE.name == config['protocol'] + '_' + fingerprint + '_results.zip'
    delivery = read(HERE / 'h003_small/delivery_manifest.json')
    for name, digest in config['runtime_sha256'].items():
        assert sha(export / 'runtime_sources' / name) == digest == delivery['modules'][name]
    for name in ['features.py', 'worker.py', 'original_prompt.py']:
        assert config['runtime_sha256'][name] == old['runtime_sha256'][name]
    versions = {n: importlib.metadata.version(n) for n in ['numpy', 'pandas', 'duckdb', 'pyarrow', 'lightgbm']}
    assert all(versions[n] == config['versions'][n] for n in versions)
    manifest = read(DATA / 'manifest.json')
    assert sha(DATA / 'manifest.json') == config['bundle_manifest_sha256']
    assert sha(export / 'input_manifest.json') == sha(DATA / 'manifest.json')
    assert sha(export / 'validation_selection.json') == sha(DATA / 'selection.json')
    for name, digest in manifest['files'].items():
        assert sha(DATA / name) == digest
    complete = read(export / 'complete.json')
    assert complete['status'] == 'complete' and complete['search_budgets_complete']
    selection = read(DATA / 'selection.json')
    assert sorted(sum(selection.values(), [])) == list(range(304))
    targets = {s: pd.read_parquet(DATA / f'{s}_targets.parquet') for s in ['val', 'test']}
    targets.update({stage: targets['val'].iloc[ids].reset_index(drop=True) for stage, ids in selection.items()})
    audit = dict(status='checking', run_id=config['protocol'] + '_' + fingerprint,
                 archive_sha256=sha(ARCHIVE), archive_bytes=ARCHIVE.stat().st_size,
                 matched_control_fields=helpers.MATCH, config=config, local_cpu_versions=versions,
                 data_source_checks_passed=True, source_hashes_match_delivery=True,
                 arms={}, replays=[], test_previously_inspected=True)
    rows, quality, jobs = [], {}, []
    states = {'Qwen7B_control': read(control / 'qwen/search_state.json')['trials']}

    def score_folder(label, folder):
        row = {'model': label, 'source': str(folder.relative_to(ROOT))}
        quality[label] = {}
        for stage in ['search', 'confirm', 'heldout_val', 'val', 'test']:
            metric, ap, pred = saved_metrics(folder, stage, targets[stage])
            row[stage + '_map_percent'] = 100 * metric['map']
            quality[label][stage] = ap
        rows.append(row)

    raw = export / 'raw_control'
    score_folder('Raw15', raw)
    assert sha(raw / 'model.txt') == sha(control / 'raw_control/model.txt')
    for stage in targets:
        assert sha(raw / f'{stage}_predictions.npy') == sha(control / f'raw_control/{stage}_predictions.npy')
    audit['raw_control_identical'] = True
    old_selected = read(control / 'qwen/selected.json')
    control_folder = chosen_path(control, old_selected['directory'])
    score_folder('Qwen7B_control', control_folder)
    jobs.append(('Raw15', raw, export / 'run_config.json'))
    issues_rows, efficiency, failures = [], [], []
    for arm in config['arms']:
        arm_config = read(export / ('config_' + arm + '.json'))
        assert arm_config == {**config, 'arm': arm, 'arm_protocol': config['protocol'] + '_' + arm}
        trials = read(export / arm / 'search_state.json')['trials']
        states[arm] = trials
        keys, previous, repair, proposal = {}, None, 0, 0
        for number, trial in enumerate(trials, 1):
            assert trial['call'] == number and trial['island'] == proposal % 3
            assert trial['proposal'] == proposal and trial['repair'] == repair
            assert trial['parent_call'] == (previous['call'] if previous else None)
            folder = export / arm / 'candidates' / f'candidate_{number:03d}'
            assert read(folder / 'trial.json') == trial
            response = read(folder / 'response.json')
            assert response['seed'] == 42 + number - 1
            assert not response['truncated'] and response['prompt_tokens'] <= 6144
            prompt = (folder / 'prompt.txt').read_text()
            assert ('TWO DIFFERENT namespaces' in prompt) == (arm in ['h003b', 'h003c'])
            assert 'REPAIR:' in prompt if previous else 'REPAIR:' not in prompt
            if trial['status'] == 'valid':
                program = validate_program(read(folder / 'program.json'))
                key = program_key(program)
                assert key == trial['program_key'] and key not in keys
                keys[key] = number
                schema = read(folder / 'feature_schema.json')
                assert schema['train_pairs'] == 72813 and schema['train_pair_sha256'] == manifest['train_pair_sha256']
                assert schema['preflight']['passed'] and schema['preflight']['row_permutation'] and schema['preflight']['batch_invariance']
                metric, _, _ = saved_metrics(folder, 'search', targets['search'])
                assert metric['map'] == trial['score']
            elif trial['status'] == 'duplicate':
                assert trial['program_key'] in keys and trial['duplicate_of'] == keys[trial['program_key']]
            else:
                failures.append(dict(arm=arm, call=number, stage=trial['failure_stage'], error=trial['error']))
                if (folder / 'diagnostics.json').exists():
                    diagnostics = read(folder / 'diagnostics.json')
                    for issue in diagnostics:
                        issues_rows.append(dict(arm=arm, call=number, **issue))
            stop = arm == 'h003c' and trial.get('unchanged_repair', False)
            if trial['status'] != 'valid' and repair < 3 and not stop:
                previous, repair = trial, repair + 1
            else:
                previous, repair, proposal = None, 0, proposal + 1
        assert len(keys) == 20
        selected = read(export / arm / 'selected.json')
        assert selected['successful_distinct'] == 20 and selected['llm_calls'] == len(trials) and selected['budget_complete']
        valid = [t for t in trials if t['status'] == 'valid']
        top3 = sorted(valid, key=lambda t: (-t['score'], t['call']))[:3]
        assert [t['call'] for t in selected['confirmation']] == [None] + [t['call'] for t in top3]
        for candidate in selected['confirmation']:
            metric, _, _ = saved_metrics(chosen_path(export, candidate['directory']), 'confirm', targets['confirm'])
            assert metric['map'] == candidate['confirmation_map']
        assert max(selected['confirmation'], key=lambda x:x['confirmation_map'])['directory'] == selected['directory']
        folder = chosen_path(export, selected['directory'])
        assert sha(folder / 'model.txt') == selected['model_sha256']
        assert sha(folder / 'program.json') == selected['program_sha256']
        score_folder(arm, folder)
        for stage in ['heldout_val', 'val', 'test']:
            replay = read(folder / f'replay_{stage}_metrics.json')
            assert replay['passed'] and replay['map'] == read(folder / f'{stage}_metrics.json')['map']
            assert replay['predictions_sha256'] == sha(folder / f'{stage}_predictions.npy')
            np.testing.assert_array_equal(np.load(folder / f'replay_{stage}_predictions.npy'), np.load(folder / f'{stage}_predictions.npy'))
        program = read(folder / 'program.json')
        engine = FeatureEngine(OUT / 'probe_scratch' / arm, DATA)
        users = targets['search'].customer_id.iloc[:8].to_numpy()
        pairs = pd.DataFrame({'customer_id': np.repeat(users, 16), 'article_id': np.tile(np.arange(16), len(users))})
        engine.prepare(targets['search'].timestamp.iloc[0], users, program)
        whole = engine.matrix(pairs)
        perm = np.random.default_rng(42).permutation(len(pairs))
        np.testing.assert_allclose(whole, engine.matrix(pairs.iloc[perm].reset_index(drop=True))[np.argsort(perm)], equal_nan=True)
        np.testing.assert_allclose(whole, np.concatenate([engine.matrix(pairs.iloc[:64]), engine.matrix(pairs.iloc[64:])]), equal_nan=True)
        engine.close()
        audit['arms'][arm] = dict(selected_call=selected['call'], selected=selected, program=program,
                                  groupings=[e['keys'] for e in program['aggregates']],
                                  row_permutation_and_batch_checks=True,
                                  failure_stages=dict(Counter(t.get('failure_stage') for t in trials if t['status']=='rejected')))
        jobs.append((arm, folder, export / ('config_' + arm + '.json')))
        print(arm, 'verified:', len(trials), 'calls; selected', selected['call'], flush=True)
    for label, trials in states.items():
        counts = Counter(t['status'] for t in trials)
        efficiency.append(dict(model=label, calls=len(trials), **counts,
                               repair_calls=sum(t['repair']>0 for t in trials),
                               unchanged_repairs=sum(t.get('unchanged_repair', False) for t in trials) if label!='Qwen7B_control' else 13,
                               generation_minutes=sum(t.get('seconds', 0) for t in trials)/60,
                               generated_tokens=sum(t.get('generated_tokens',0) for t in trials),
                               max_input_tokens=max(t.get('prompt_tokens',0) for t in trials),
                               target_reached=counts['valid']==20))
    pd.DataFrame(rows).to_csv(OUT / 'comparison.csv', index=False)
    pd.DataFrame(efficiency).to_csv(OUT / 'generation_efficiency.csv', index=False)
    write(OUT / 'quality.json', {name:{s:v.tolist() for s,v in stages.items()} for name,stages in quality.items()})
    write(OUT / 'diagnostics.json', issues_rows)
    write(OUT / 'failures.json', failures)
    write(OUT / 'states.json', states)
    write(OUT / 'audit_pre_replay.json', audit)
    # Read-only inference; frozen saved models, no training.
    helpers.OUT = OUT
    helpers.CODE = export / 'runtime_sources'
    with ThreadPoolExecutor(max_workers=2) as pool:
        audit['replays'] = list(pool.map(helpers.run_replay, jobs))
    audit.update(status='passed', seconds=time.perf_counter()-started)
    write(OUT / 'audit.json', audit)
    print('AUDIT PASSED', flush=True)


if __name__ == '__main__':
    main()
