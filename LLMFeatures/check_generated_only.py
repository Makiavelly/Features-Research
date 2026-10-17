"""Check the restricted validator and raw-column removal without fitting models."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / 'LLMFeatures/provider_generated_only_runtime_v1'
REPORT = ROOT / 'reports/provider_generated_only_v1'
sys.path.insert(0, str(CODE))
from python_features import FeatureEngine, compile_function, construct, parse, RAW
from worker import preflight, ap12

def main():
    passed = []
    # Reuse the existing synthetic validator suite without its raw15 host checks.
    old = (ROOT / 'LLMFeatures/check_python_features.py').read_text(encoding='utf-8')
    body = old[old.index('    passed=[]'):old.index("    data=ROOT/'data/kaggle_hm_small_sql_compare_v1'")]
    # This is trusted checked-in test source, not generated program execution.
    wrapper = 'def regression():\n' + body + '\n    return passed\n'
    scope = dict(globals())
    from python_features import program_key
    scope['program_key'] = program_key
    exec(compile(wrapper, '<trusted-validator-regressions>', 'exec'), scope)
    passed.extend(scope['regression']())
    X = pd.DataFrame({'customer_id': [0, 1], 'article_id': [1, 2]}, index=[5, 2])
    try:
        construct(compile_function(parse('def modify_features(X, history):\n    return pd.DataFrame(index=X.index)')), X, pd.DataFrame())
    except ValueError:
        passed.append('reject_zero_generated_columns')
    else:
        raise AssertionError('Zero-column program accepted')
    spec = importlib.util.spec_from_file_location('matched_previous_python', ROOT / 'LLMFeatures/provider_python_runtime_v2/python_features.py')
    previous = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(previous)
    data = ROOT / 'data/kaggle_hm_small_sql_compare_v1'
    pairs = pd.read_parquet(data / 'train_pairs.parquet')
    new = FeatureEngine(REPORT / 'validator_scratch/new', data)
    old_engine = previous.FeatureEngine(REPORT / 'validator_scratch/previous', data)
    program = parse('''def modify_features(X, history):
    counts=history.groupby('article_id').size()
    return pd.DataFrame({'f_count':X['article_id'].map(counts).fillna(0), 'f_age':X['raw_u_age']},index=X.index)
''')
    try:
        for cutoff, frame in pairs.groupby('timestamp', sort=True):
            sample = frame.head(128)
            new.prepare(cutoff, sample.customer_id.values, program)
            old_engine.prepare(cutoff, sample.customer_id.values, program)
            actual = new.matrix(sample)
            expected = old_engine.matrix(sample)[:, 15:]
            np.testing.assert_array_equal(actual, expected)
            assert actual.shape[1] == 2 and new.feature_names == ['f_count', 'f_age']
            assert all(n.startswith('f_') for n in new.feature_names)
            assert new.history.days_ago.min() >= 0
        passed.extend(['exact_previous_generated_values_all8_cutoffs', 'no_automatic_raw_columns', 'no_future_history'])
        assert preflight(new, pairs, program)['passed']
        passed.append('generated_only_permutation_batch_empty_absent_preflight')
        cutoff = pairs.timestamp.max()
        sample = pairs[pairs.timestamp == cutoff].head(128)
        new.prepare(cutoff, sample.customer_id.values, {'code': RAW})
        constant = new.matrix(sample)
        assert constant.shape == (len(sample), 1)
        np.testing.assert_array_equal(constant, 1)
        assert new.feature_names == ['f_control']
        passed.append('constant_control_one_column_no_raw15')
        preflight(new, pairs, {'code': RAW})
        passed.append('constant_control_preflight')
        new.prepare(cutoff, sample.customer_id.values, program)
        raw = new.con.sql('SELECT price FROM history').df().price.mean()
        assert np.isfinite(raw)
        passed.append('history_available_after_raw_join')
    finally:
        new.close()
        old_engine.close()
    prediction = np.arange(12)[None, :]
    np.testing.assert_allclose(ap12(prediction, [np.array([0, 2])]), [(1 + 2/3) / 2])
    passed.append('independent_AP12_reference')
    result = {'status': 'passed', 'checks': passed,
              'module_sha256': hashlib.sha256((CODE / 'python_features.py').read_bytes()).hexdigest(),
              'training_calls': 0, 'api_calls': 0}
    (REPORT / 'validator_verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2), flush=True)

if __name__ == '__main__':
    main()
