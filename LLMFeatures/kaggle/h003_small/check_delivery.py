"""CPU integration; scripted responses are not H003 model results."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import runtime
from diagnostics import diagnose
from worker import write


def main():
    started = time.perf_counter()
    notebook = json.loads((HERE.parent / 'hm_small_qwen7b_h003_kaggle_t4.ipynb').read_text())
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            ast.parse(''.join(cell['source']))
    embedded = next(ast.literal_eval(n.value) for c in notebook['cells'] if c['cell_type'] == 'code'
                    for n in ast.parse(''.join(c['source'])).body if isinstance(n, ast.Assign)
                    and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'MODULES')
    for name, source in embedded.items():
        assert source == (HERE / name).read_text(), name
    import nbformat
    nbformat.validate(nbformat.from_dict(notebook))
    for name in ['features.py', 'worker.py', 'original_prompt.py']:
        assert embedded[name] == (HERE.parent / 'small_compare' / name).read_text()
    inventory = json.loads((ROOT / 'reports/qwen7b_generation_errors_v1/response_inventory.json').read_text())
    accepted, rejected = [], []
    for row in inventory:
        issues = diagnose(row['program'])
        if row['status'] in {'valid', 'duplicate'}:
            assert not issues, (row['call'], issues)
            accepted.append(row['call'])
        else:
            assert issues, row['call']
            rejected.append(row['call'])
    data = ROOT / 'data/kaggle_hm_small_sql_compare_v1'
    manifest = json.loads((data / 'manifest.json').read_text())
    for name, digest in manifest['files'].items():
        assert runtime.sha(data / name) == digest
    out = ROOT / 'reports/kaggle_llmfe_validation/h003_small_v1/cpu_smoke'
    out.mkdir(parents=True, exist_ok=True)
    config = dict(train_pairs=72813, train_pair_sha256=manifest['train_pair_sha256'], lightgbm_rounds=3,
                  validation_only_fake_callbacks=True, test_previously_inspected=True,
                  cpu_threads=4, scoring_user_batch=16, evaluation_timeout_seconds=1800,
                  target_successful_distinct=2, max_llm_calls=8, max_repairs_per_proposal=3,
                  training_examples='[]', arms=['h003a', 'h003b', 'h003c'])
    config_path = out / 'run_config.json'
    write(config_path, config)
    a = {'aggregates': [{'name': 'f_recent', 'keys': ['article_id'], 'sql': 'count(*) FILTER(WHERE days_ago<=7)'}], 'derived': []}
    b = {'aggregates': [{'name': 'f_recent', 'keys': ['article_id'], 'sql': 'count(*) FILTER(WHERE days_ago<=30)'}], 'derived': []}
    bad = {'aggregates': [{'name': 'f_bad_keys', 'keys': ['sales_channel_id'], 'sql': 'count(*)'},
                          {'name': 'f_bad_age', 'keys': ['customer_id'], 'sql': "CASE WHEN raw_u_age<30 THEN 'young' ELSE 'old' END"}],
           'derived': [{'name': 'f_bad_history', 'sql': 'sum(days_ago)'}]}
    assert len(diagnose(bad)) == 3
    # Inferred bool types must remain bool when referenced by later features.
    assert not diagnose({'aggregates': [], 'derived': [{'name': 'f_flag', 'sql': 'raw_u_age>30'},
                                                      {'name': 'f_flag_two', 'sql': 'CASE WHEN f_flag THEN 1 ELSE 0 END'}]})
    raw = out / 'raw_control'
    raw.mkdir(exist_ok=True)
    write(raw / 'program.json', {'aggregates': [], 'derived': []})
    runtime.evaluate(data, raw, 'search', config_path)
    for arm in config['arms']:
        arm_config = {**config, 'arm': arm}
        arm_path = out / ('config_' + arm + '.json')
        write(arm_path, arm_config)
        prompts = []
        def fake(prompt, seed):
            prompts.append(prompt)
            call = len(prompts)
            assert seed == 42 + call - 1
            response = bad if call == 1 else (b if call >= 5 else a)
            return {'text': json.dumps(response), 'seed': seed, 'truncated': False,
                    'generated_tokens': 1, 'seconds': 0.}
        result = runtime.search(data, out / arm, fake, arm_path)
        assert result['successful_distinct'] == 2 and result['llm_calls'] == 5
        if prompts:
            assert all(x in prompts[1] for x in ['aggregates[0]', 'aggregates[1]', 'derived[0]'])
            assert ('TWO DIFFERENT namespaces' in prompts[0]) == (arm in {'h003b', 'h003c'})
            assert ('duplicate of call2' in prompts[3]) == (arm == 'h003c')
        trials = json.loads((out / arm / 'search_state.json').read_text())['trials']
        assert [t['status'] for t in trials] == ['rejected', 'valid', 'duplicate', 'duplicate', 'valid']
        assert trials[3]['unchanged_repair']
        assert trials[4]['repair'] == (0 if arm == 'h003c' else 2)
        assert trials[4]['proposal'] == (2 if arm == 'h003c' else 1)
        runtime.search(data, out / arm, lambda *_: (_ for _ in ()).throw(AssertionError('Resume requested generation')), arm_path)
    frame = runtime.finish(data, out, config_path)
    assert len(frame) == 12 and json.loads((out / 'complete.json').read_text())['independent_frozen_replays']
    efficiency = __import__('pandas').read_csv(out / 'generation_efficiency.csv')
    assert efficiency.calls.tolist() == [5, 5, 5] and efficiency.valid.tolist() == [2, 2, 2]
    report = dict(status='passed', scope='CPU smoke only: scripted callbacks, 3 LightGBM rounds; not actual LLM results',
                  historical_responses_checked=len(inventory), historical_valid_or_duplicate_accepted=len(accepted),
                  historical_rejected_diagnosed=len(rejected), arms=config['arms'], train_pairs=72813,
                  checks=['notebook schema/embedded hashes', 'frozen feature/worker/prompt code', 'all input hashes',
                          'multi-feature diagnosis', 'BOOL references', 'repair/duplicate/island/unchanged routing',
                          'resume', 'independent model replay', 'full5000 scoring', 'references/plots/ZIP'],
                  seconds=time.perf_counter() - started)
    write(out.parent / 'verification.json', report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
