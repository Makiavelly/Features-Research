"""H008: fresh provider search; only explicitly generated features enter trees."""
import argparse
import ast
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/kaggle_hm_small_sql_compare_v1'
CODE = ROOT / 'LLMFeatures/provider_generated_only_runtime_v1'
REPORT = ROOT / 'reports/provider_generated_only_v1'
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(path)

def build_modules():
    base = ROOT / 'LLMFeatures/provider_python_runtime_v2'
    modules = {n: (base / n).read_text(encoding='utf-8') for n in
               ['base_features.py', 'worker.py', 'runtime.py', 'python_features.py', 'provider_api.py', 'prompting.py', 'features.py']}
    features = modules['python_features.py']
    old_raw = "RAW = 'def modify_features(X, history):\\n    return pd.DataFrame(index=X.index)\\n'"
    new_raw = "RAW = 'def modify_features(X, history):\\n    return pd.DataFrame({\"f_control\": np.ones(len(X))}, index=X.index)\\n'"
    assert old_raw in features
    features = features.replace(old_raw, new_raw)
    features = features.replace('if len(columns)>36 or', 'if not 1 <= len(columns) <= 36 or')
    features = features.replace('Return 0..36 unique numeric', 'Return 1..36 unique numeric')
    start = features.index('    @property\n    def feature_names(self):', features.index('class FeatureEngine('))
    features = features[:start] + '''    @property
    def feature_names(self):
        return self.raw_names if getattr(self, '_building_raw', False) else (self.names or [])

    def frame(self, pairs):
        self._building_raw = True
        try:
            raw = RawEngine.frame(self, pairs)
        finally:
            self._building_raw = False
        X = pd.concat([pairs[['customer_id','article_id']].reset_index(drop=True), raw], axis=1)
        out = construct(self.function, X, self.history, expected=self.names)
        self.names = list(out)
        assert all(n.startswith('f_') for n in self.names)
        return out
'''
    modules['python_features.py'] = features
    worker = modules['worker.py']
    worker = worker.replace('    names = engine.feature_names\n',
        "    names = engine.feature_names\n    assert names and all(n.startswith('f_') for n in names), 'Only generated f_* inputs allowed'\n    assert values.shape[1] == len(names)\n")
    modules['worker.py'] = worker
    prompt = modules['prompting.py']
    assert 'Host appends the same 15 raw fields.' in prompt
    prompt = prompt.replace('Host appends the same 15 raw fields.',
        'Host passes ONLY your returned f_* columns to LightGBM. NO raw fields or IDs are appended. '
        'Static fields remain available in X as inputs. If you intentionally include a static attribute, '
        'return it explicitly as a numeric f_* column. Do not return customer/article identifiers as features.')
    prompt = prompt.replace('Top3search + raw compete', 'Top3search + constant-only control compete')
    prompt = prompt.replace('Previous best complete Python in YOUR island,',
                            'Previous best complete Python in YOUR island (initial control is one constant),')
    modules['prompting.py'] = prompt
    runtime = modules['runtime.py']
    runtime = runtime.replace("if config.get('arm') == 'gpt61sol_python':", "if config.get('arm') == 'gpt61sol_generated_only':")
    runtime = runtime.replace("config.get('arm') == 'gpt61sol_python' and", "config.get('arm') == 'gpt61sol_generated_only' and")
    runtime = runtime.replace('top3 search plus raw -> disjoint confirmation88',
                              'top3 search plus constant-only control -> disjoint confirmation88')
    # Preserve the actual request prompt when resuming an already paid response.
    runtime = runtime.replace("                (directory / 'prompt.txt').write_text(prompt, encoding='utf-8')\n",
        "                if not (directory / 'response.json').exists():\n                    (directory / 'prompt.txt').write_text(prompt, encoding='utf-8')\n")
    modules['runtime.py'] = runtime
    modules['run_provider_generated_only.py'] = Path(__file__).read_text(encoding='utf-8')
    modules['check_generated_only.py'] = (ROOT / 'LLMFeatures/check_generated_only.py').read_text(encoding='utf-8')
    for text in modules.values():
        ast.parse(text)
    return modules

def prepare():
    modules = build_modules()
    previous = ROOT / 'LLMFeatures/results/hm_small_gpt61sol_python_seed42_v2_db3ced2f4449/run_config.json'
    config = read(previous)
    for name in ['source_run', 'migration_note', 'sql_comparison_run']:
        config.pop(name, None)
    config.update(protocol='hm_small_gpt61sol_generated_only_seed42_v1',
                  arms=['gpt61sol_generated_only'], arm='gpt61sol_generated_only',
                  feature_interface='complete_Python_generated_columns_only',
                  automatic_raw_features=0, control='single_constant_f_control',
                  memory_protocol='best_complete_program_in_own_island_plus_current_repair; unchanged from H006',
                  independent_new_api_stream=True,
                  matched_reference_run=previous.parent.name,
                  deduplication='same conservative AST as H006; matrix diversity audited separately',
                  versions={n: importlib.metadata.version(n) for n in config['versions']},
                  runtime_sha256={n: hashlib.sha256(s.encode()).hexdigest() for n, s in modules.items()})
    assert config['model_id'] == 'gpt-6.1-sol'
    assert config['base_url'].rstrip('/') == 'https://tooken.club/v1'
    assert config['target_successful_distinct'] == 20 and config['max_llm_calls'] == 300
    assert config['max_repairs_per_proposal'] == 3
    manifest = read(DATA / 'manifest.json')
    assert sha(DATA / 'manifest.json') == config['bundle_manifest_sha256']
    for n, digest in manifest['files'].items():
        assert sha(DATA / n) == digest, n
    fingerprint = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()[:12]
    out = ROOT / 'LLMFeatures/results' / (config['protocol'] + '_' + fingerprint)
    config_path = out / 'run_config.json'
    if config_path.exists():
        assert read(config_path) == config
    write(config_path, config)
    CODE.mkdir(exist_ok=True)
    frozen = out / 'runtime_sources'
    frozen.mkdir(exist_ok=True)
    for n, text in modules.items():
        for folder in [CODE, frozen]:
            path = folder / n
            if path.exists():
                assert path.read_text(encoding='utf-8') == text, 'Frozen source changed: ' + n
            else:
                path.write_text(text, encoding='utf-8')
    for n in ['manifest.json', 'selection.json']:
        shutil.copy2(DATA / n, out / ('input_' + n))
    registry = REPORT / 'current_run.json'
    if not registry.exists():
        write(registry, {'run_id': out.name, 'directory': str(out), 'status': 'prepared'})
        record('provider_generated_only_prepared',
               'H008: new GPT-6.1 Sol API stream, only generated f_* features enter LightGBM. '
               'Same data/LightGBM/seed/best-only memory as H006; constant-only control,20 valid programs/300 POST/3 repairs/3 islands.',
               out.name, status='prepared', artifacts=str(out.relative_to(ROOT)))
    else:
        assert read(registry)['run_id'] == out.name
    return out, config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    out, config = prepare()
    print('Run:', out.name, flush=True)
    if args.prepare_only:
        return
    checks = read(REPORT / 'validator_verification.json')
    assert checks['status'] == 'passed'
    assert checks['module_sha256'] == sha(CODE / 'python_features.py')
    shutil.copy2(REPORT / 'validator_verification.json', out / 'validator_verification.json')
    sys.path.insert(0, str(out / 'runtime_sources'))
    import runtime
    from python_features import RAW
    from provider_api import ProviderGenerator
    config_path = out / 'run_config.json'
    control = out / 'raw_control'  # Compatibility path only; contains a CONSTANT, not raw15.
    write(control / 'program.json', {'code': RAW})
    (control / 'program.py').write_text(RAW, encoding='utf-8')
    original_progress = runtime.progress
    def progress(folder, trials, cfg):
        valid = original_progress(folder, trials, cfg)
        record('provider_generated_only_progress',
               f"H008: {len(valid)}/20 programs evaluated; {len(trials)} responses processed.",
               out.name, status='searching', measured=len(valid), responses=len(trials),
               api_requests=len(list((out / 'api_attempts').glob('attempt_*'))))
        return valid
    runtime.progress = progress
    try:
        write(REPORT / 'current_run.json', {'run_id': out.name, 'directory': str(out), 'status': 'running'})
        record('provider_generated_only_started', 'Validator verified; starting constant control and fresh API search.',
               out.name, status='searching', artifacts=str(out.relative_to(ROOT)))
        runtime.evaluate(DATA, control, 'search', config_path)
        generator = ProviderGenerator(config, out, ROOT / '.env')
        selected = runtime.search(DATA, out / config['arm'], generator, config_path)
        record('provider_generated_only_selection_frozen', 'Selection frozen on confirmation before final evaluation.',
               out.name, status='evaluating', selected_call=selected['call'], measured=selected['successful_distinct'])
        comparison = runtime.finish(DATA, out, config_path)
        write(REPORT / 'current_run.json', {'run_id': out.name, 'directory': str(out), 'status': 'finished'})
        print(comparison.to_string(index=False), flush=True)
        print('Archive:', runtime.archive_run(out), flush=True)
        record('provider_generated_only_finished', 'Search and final evaluation completed; independent audit required.',
               out.name, status='completed_pending_audit', artifacts=str(out.relative_to(ROOT)))
    except BaseException as error:
        detail = str(error)
        (out / 'failure.txt').write_text(detail + '\n' + traceback.format_exc(), encoding='utf-8')
        write(REPORT / 'current_run.json', {'run_id': out.name, 'directory': str(out), 'status': 'interrupted', 'error': detail})
        record('provider_generated_only_interrupted', detail[:600], out.name, status='interrupted')
        raise

if __name__ == '__main__':
    main()
