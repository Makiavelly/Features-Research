"""CPU integration check on real small-v1 data. Fake callbacks are NOT LLM results."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import runtime
from features import FeatureEngine
from worker import ap12, write


def main():
    started = time.perf_counter()
    notebook = json.loads((HERE.parent / 'hm_small_qwen_vs_llama_sql_kaggle_t4.ipynb').read_text())
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            ast.parse(''.join(cell['source']))
    embedded = next(ast.literal_eval(node.value)
                    for cell in notebook['cells'] if cell['cell_type'] == 'code'
                    for node in ast.parse(''.join(cell['source'])).body
                    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'MODULES')
    for name, source in embedded.items():
        assert source == (HERE / name).read_text(encoding='utf-8'), 'Rebuild notebook: ' + name
    try:
        import nbformat
        nbformat.validate(nbformat.from_dict(notebook))
    except ImportError:
        raise RuntimeError('Run with project .check-deps on PYTHONPATH for nbformat validation')
    data = ROOT / 'data/kaggle_hm_small_sql_compare_v1'
    manifest = json.loads((data / 'manifest.json').read_text())
    for name, digest in manifest['files'].items():
        assert runtime.sha(data / name) == digest
    selection = json.loads((data / 'selection.json').read_text())
    assert sorted(sum(selection.values(), [])) == list(range(304))
    pairs = pd.read_parquet(data / 'train_pairs.parquet')
    assert len(pairs) == 72813 and len(pairs[['timestamp', 'customer_id']].drop_duplicates()) == 4804
    out = ROOT / 'reports/kaggle_llmfe_validation/small_compare_v1/cpu_smoke_dense_v2'
    out.mkdir(parents=True, exist_ok=True)
    config = dict(train_pairs=72813, train_pair_sha256=manifest['train_pair_sha256'], lightgbm_rounds=150,
                  validation_only_fake_callbacks=True,
                  cpu_threads=4, scoring_user_batch=16, evaluation_timeout_seconds=1800,
                  target_successful_distinct=2, max_llm_calls=8, max_repairs_per_proposal=1, training_examples='[]')
    config_path = out / 'run_config.json'
    write(config_path, config)
    program_a = {'aggregates': [{'name': 'f_item_count', 'keys': ['article_id'], 'sql': 'count(*) FILTER (WHERE days_ago <= 7)'},
                                {'name': 'f_customer_last', 'keys': ['customer_id'], 'sql': 'min(days_ago)'}],
                 'derived': [{'name': 'f_count_log', 'sql': 'ln(1 + coalesce(f_item_count,0))'}]}
    program_b = {'aggregates': [{'name': 'f_pair', 'keys': ['customer_id', 'article_id'], 'sql': 'count(*)'},
                                {'name': 'f_type', 'keys': ['customer_id', 'product_type_no'], 'sql': 'count(*) FILTER (WHERE days_ago <= 30)'}],
                 'derived': [{'name': 'f_type_ratio', 'sql': 'f_pair / nullif(f_type, 0)'}]}
    # Known-answer independent pandas check, plus future exclusion at an early training cutoff.
    engine = FeatureEngine(out / 'engine_scratch', data)
    cutoff = pairs.timestamp.min()
    sample = pairs[pairs.timestamp == cutoff].head(128)
    engine.prepare(cutoff, sample.customer_id.values, program_a)
    actual = engine.frame(sample)
    tx = pd.read_parquet(data / 'transactions.parquet')
    past = tx[tx.t_dat <= cutoff]
    recent = past[(cutoff - past.t_dat).dt.days <= 7].groupby('article_id').size()
    # SQL FILTER returns0 for an existing all-history group with no recent rows;
    # a group never seen before cutoff remains missing after the LEFT JOIN.
    recent = recent.reindex(past.article_id.unique(), fill_value=0)
    expected = sample.article_id.map(recent).to_numpy(dtype=float)
    np.testing.assert_allclose(actual.f_item_count, expected, equal_nan=True)
    recency = ((cutoff - past.t_dat).dt.days).groupby(past.customer_id).min()
    np.testing.assert_allclose(actual.f_customer_last, sample.customer_id.map(recency).to_numpy(), equal_nan=True)
    assert len(tx[tx.t_dat > cutoff]) > 0
    engine.close()
    raw = out / 'raw_control'
    raw.mkdir(exist_ok=True)
    write(raw / 'program.json', {'aggregates': [], 'derived': []})
    runtime.evaluate(data, raw, 'search', config_path)
    for label in ['qwen', 'llama']:
        seen_prompts = []
        def fake(prompt, seed):
            seen_prompts.append(prompt)
            if len(seen_prompts) == 1:
                response = 'not JSON'
            elif len(seen_prompts) in {2, 3}:
                response = json.dumps(program_a)
            else:
                response = json.dumps(program_b)
            return {'text': response, 'seed': seed, 'truncated': False, 'generated_tokens': 1, 'seconds': 0.}
        result = runtime.search(data, out / label, fake, config_path)
        assert result['successful_distinct'] == 2 and result['llm_calls'] == 4
        if seen_prompts:
            assert 'REPAIR:' in seen_prompts[1]
        state = json.loads((out / label / 'search_state.json').read_text())
        assert [t['status'] for t in state['trials']] == ['rejected', 'valid', 'duplicate', 'valid']
        assert [t['island'] for t in state['trials']] == [0, 0, 1, 1]
        runtime.search(data, out / label, lambda *_: (_ for _ in ()).throw(AssertionError('Resume generated again')), config_path)
    frame = runtime.finish(data, out, config_path)
    assert len(frame) == 11 and (out / 'complete.json').exists()
    # Known MAP formula sanity: one hit at rank2 among two positives -> AP=.25.
    assert ap12(np.array([[0, 1, *range(2, 12)]]), [[1, 99]])[0] == .25
    report = {'status': 'passed', 'scope': 'CPU integration only; fake model callbacks, NOT LLM performance',
              'train_pairs': 72813, 'snapshots': 8, 'references_recomputed': 7,
              'original_train_pair_sha256': manifest['train_pair_sha256'],
              'both_controls_and_generated_programs_trained': True, 'separate_frozen_replay': True,
              'checks': ['notebook AST/schema', 'input hashes', 'disjoint validation partitions',
                         'known-answer ID joins and recency', 'future transaction exclusion',
                         'permutation/batch invariance', 'repair/duplicate/island routing', 'resume',
                         'full5000 ranking', 'reference AP recomputation', 'plots and ZIP'],
              'seconds': time.perf_counter() - started}
    write(out.parent / 'verification.json', report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
