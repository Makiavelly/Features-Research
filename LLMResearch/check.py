"""No-network leakage, replay, isolation and original-validator checks."""
import json
from pathlib import Path
import sys
import tempfile
import duckdb
import numpy as np
import pandas as pd
from common import ROOT, SOURCE, OLD, OUT, REPORT, read, write, sha
from prepare import prepare


def main():
    prepared = [prepare(f) for f in range(3)]
    folder, runtime, bundle, cfg, cfgpath = prepared[0]
    sys.path.insert(0, str(runtime))
    from python_features import parse, compile_function, construct, program_key
    from agent import ResearchGenerator
    from query_worker import execute
    checks = []
    # Same meaningful validator suite as H009, against byte-identical evaluator.
    source = (ROOT / 'LLMFeatures/check_python_features.py').read_text(encoding='utf-8')
    body = source[source.index('    passed=[]'):source.index("    data=ROOT/'data/kaggle_hm_small_sql_compare_v1'")]
    scope = dict(globals(), parse=parse, compile_function=compile_function,
                 construct=construct, program_key=program_key)
    exec(compile('def regression():\n' + body + '\n    return passed', '<validator-regressions>', 'exec'), scope)
    checks.extend(scope['regression']())
    for fold, (foldpath, rt, data, config, path) in enumerate(prepared):
        original = read(OLD / f'fold_{fold}/h009/run_config.json')
        assert all(sha(rt / name) == digest for name, digest in original['runtime_sha256'].items())
        allowed = {'protocol', 'test_previously_inspected', 'runtime_sha256'}
        assert all(config[k] == v for k, v in original.items() if k not in allowed)
        manifest = read(foldpath / 'research_manifest.json')
        assert set(manifest['tables']) == {'history', 'train_history', 'train_pairs'}
        assert set(manifest['sources']) == {'train_pairs.parquet', 'transactions.parquet', 'article.parquet', 'customer.parquet'}
        assert not manifest['contains_validation_or_test']
        db = foldpath / 'research.duckdb'
        result = execute(db, 'SELECT count(*) n,min(days_ago) d FROM train_history')
        assert result['rows'][0][0] > 0 and result['rows'][0][1] >= 0
        result = execute(db, 'SELECT count(DISTINCT cutoff) n,max(cutoff) last_cutoff FROM train_history')
        assert result['rows'][0][0] == 6
        result = execute(db, 'SELECT count(*) n FROM train_pairs')
        assert result['rows'][0][0] == config['train_pairs']
    checks += ['all_three_original_H009_runtimes_byte_identical', 'only_treatment_config_added',
               'train_only_table_sources', 'six_time_filtered_snapshots_per_fold', 'unchanged_train_pairs']
    with tempfile.TemporaryDirectory(dir=REPORT) as scratch:
        scratch = Path(scratch)
        db = scratch / 'synthetic.duckdb'
        con = duckdb.connect(str(db))
        con.execute('CREATE TABLE train_pairs AS SELECT range AS x FROM range(100)')
        con.close()
        assert execute(db, 'WITH a AS (SELECT avg(x) x FROM train_pairs) SELECT * FROM a')['rows'] == [[49.5]]
        for sql in ['DELETE FROM train_pairs', 'SELECT 1; SELECT 2',
                    "COPY train_pairs TO '/tmp/h010_must_not_exist.csv'",
                    "SELECT * FROM read_parquet('/etc/passwd')",
                    "SELECT * FROM read_csv_auto('https://example.com/data.csv')",
                    'SELECT * FROM test_targets', 'PRAGMA database_list',
                    "ATTACH '/tmp/h010_other.duckdb' AS other"]:
            try:
                execute(db, sql)
            except Exception:
                pass
            else:
                raise AssertionError('Forbidden SQL accepted: ' + sql)
        limited = execute(db, 'SELECT * FROM train_pairs')
        assert len(limited['rows']) == 40 and limited['truncated_rows']
        try:
            execute(db, 'SELECT ' + ','.join(f'{i} AS c{i}' for i in range(25)))
        except ValueError:
            pass
        else:
            raise AssertionError('Column cap missing')
        checks += ['read_only_SELECT_CTE', 'writes_multistatements_and_external_access_denied',
                   'test_table_inaccessible', 'row_and_column_caps']

        class Fake(ResearchGenerator):
            def request(self, messages, seed, step):
                cache = step / 'response.json'
                if cache.exists():
                    return read(cache)
                self.requests.append(messages.copy())
                text = self.scripts[seed][int(step.name[-2:])]
                result = {'text': text, 'api_attempt': len(self.requests), 'seed': seed,
                          'prompt_tokens': 10, 'generated_tokens': 5, 'seconds': .1, 'truncated': False}
                write(cache, result)
                return result
        query = json.dumps({'action': 'query_train', 'sql': 'SELECT count(*) FROM train_pairs'})
        code = "def modify_features(X, history):\n    return pd.DataFrame({'f_x':np.ones(len(X))},index=X.index)\n"
        tests = scratch / 'dialog'
        tests.mkdir()
        local = {**cfg, 'research_island_budgets': [1, 0, 0]}
        invoked = []
        def runner(step, sql):
            invoked.append(sql)
            return {'ok': True, 'result': {'columns': ['n'], 'rows': [[100]]}}
        agent = Fake(local, tests, None, sender=lambda *args: None, runner=runner)
        agent.requests = []
        agent.scripts = {42: [query, query, code], 43: [code], 44: [code], 45: [code]}
        for call in range(1, 5):
            response = agent('unique task ' + str(call), 41 + call)
            assert response['text'] == code
            write(tests / cfg['arm'] / 'candidates' / f'candidate_{call:03d}' / 'trial.json',
                  {'call': call, 'island': (call - 1) % 3, 'proposal': call - 1,
                   'repair': 0, 'status': 'valid', 'score': .01})
        assert len(invoked) == 1 and agent.used(0) == 1
        message = json.dumps(agent.requests[-1])
        assert 'unique task 1' in message and 'QUERY_TRAIN_RESULT' in message
        assert 'unique task 2' not in message and 'unique task 3' not in message
        calls_before = len(agent.requests)
        assert agent('unique task 1', 42)['text'] == code and len(agent.requests) == calls_before
        assert json.dumps(read(tests / 'generations/call_001/final.json')).count('Research budget exhausted') > 0
        checks += ['full_own_island_tool_history', 'no_cross_island_messages',
                   'tool_budget_enforced', 'cached_final_no_duplicate_generation']

        # Crash after query execution: reload must replay saved tool output, not rerun.
        retry = Fake(cfg, scratch / 'resume', None, sender=lambda *args: None, runner=runner)
        retry.requests = []
        retry.scripts = {42: [query]}  # step1 crashes before program response
        try:
            retry('resume task', 42)
        except IndexError:
            pass
        else:
            raise AssertionError('Expected scripted interruption')
        query_calls = len(invoked)
        retry.scripts[42] = [query, code]
        assert retry('resume task', 42)['text'] == code and len(invoked) == query_calls
        checks.append('resume_does_not_repeat_saved_research')

        required = Fake(cfg, scratch / 'mandatory', None, sender=lambda *args: None, runner=runner)
        required.requests = []
        required.scripts = {42: [code, query, code]}
        assert required('mandatory initial research', 42)['text'] == code
        assert len(required.requests) == 3 and required.researched(0)
        assert (scratch / 'mandatory/generations/call_001/step_00/protocol_notice.json').exists()
        checks.append('initial_code_without_successful_research_not_scored')

    # Separate scripted smoke: real full train/control/search, not LLM performance.
    import runtime as api
    from python_features import RAW
    smoke = REPORT / 'cpu_smoke/control'
    smoke.mkdir(parents=True, exist_ok=True)
    write(smoke / 'program.json', {'code': RAW})
    (smoke / 'program.py').write_text(RAW)
    metric = api.evaluate(bundle, smoke, 'search', cfgpath)
    assert np.isfinite(metric['map'])
    write(REPORT / 'cpu_smoke/verification.json', {'passed': True, 'scripted_not_LLM': True,
          'scope': 'original constant control, real fold0 training pairs and search users',
          'search_map': metric['map'], 'real_api_calls': 0})
    checks.append('real_fold0_constant_control_CPU_smoke_not_LLM')
    write(REPORT / 'verification.json', {'passed': True, 'checks': checks,
          'real_api_calls': 0, 'protocol_sha256': sha(SOURCE / 'PROTOCOL.md'),
          'fold_runtime_sha256': {str(f): c['runtime_sha256'] for f, (_, _, _, c, _) in enumerate(prepared)}})
    print('H010:', len(checks), 'checks passed;0 API calls', flush=True)


if __name__ == '__main__':
    REPORT.mkdir(parents=True, exist_ok=True)
    main()
