"""H009: fresh GPT API search with complete own-island message histories."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import shutil
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/kaggle_hm_small_sql_compare_v1'
CODE = ROOT / 'LLMFeatures/provider_history_runtime_v1'
REPORT = ROOT / 'reports/provider_history_v1'
BASE = ROOT / 'LLMFeatures/results/hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde'
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(path)

def prepare():
    names = ['base_features.py', 'worker.py', 'runtime.py', 'python_features.py', 'provider_api.py', 'prompting.py', 'features.py']
    modules = {n: (BASE/'runtime_sources'/n).read_text(encoding='utf-8') for n in names}
    adapter = modules['provider_api.py']
    start = adapter.index("                 'messages':[")
    stop = adapter.index("                 'max_tokens':", start)
    adapter = adapter[:start] + "                 'messages':build_messages(self.config,self.out,prompt,seed),\n" + adapter[stop:]
    adapter = adapter.replace('import urllib.request\n', 'import urllib.request\nfrom dialog_history import build_messages\n')
    modules['provider_api.py'] = adapter
    for name in ['dialog_history.py', 'check_dialog_history.py', 'run_provider_history.py']:
        modules[name] = (ROOT/'LLMFeatures'/name).read_text(encoding='utf-8')
    for text in modules.values():
        ast.parse(text)
    config = read(BASE/'run_config.json')
    config.update(protocol='hm_small_gpt61sol_full_history_seed42_v1',
                  memory_protocol='all own-island user/assistant turns; explicit search feedback after every response; current best retained',
                  memory_programs_per_prompt=None, current_best_programs_per_task=1,
                  max_input_tokens=None,
                  history_policy='no silent truncation or summarization; preserve all turns; stop on provider context rejection',
                  context_window_guarantee='provider-specific limit is not independently known; input usage recorded',
                  history_comparison_run=BASE.name,
                  runtime_sha256={n: hashlib.sha256(s.encode()).hexdigest() for n,s in modules.items()})
    assert config['automatic_raw_features'] == 0
    assert config['arm'] == 'gpt61sol_generated_only'  # Same search/repair semantics as H008.
    assert sha(DATA/'manifest.json') == config['bundle_manifest_sha256']
    for n, digest in read(DATA/'manifest.json')['files'].items():
        assert sha(DATA/n) == digest
    fingerprint = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()[:12]
    out = ROOT/'LLMFeatures/results'/(config['protocol']+'_'+fingerprint)
    if (out/'run_config.json').exists():
        assert read(out/'run_config.json') == config
    write(out/'run_config.json', config)
    for folder in [CODE, out/'runtime_sources']:
        folder.mkdir(parents=True, exist_ok=True)
        for name, text in modules.items():
            path = folder/name
            if path.exists():
                assert path.read_text(encoding='utf-8') == text, 'Frozen source differs: '+name
            else:
                path.write_text(text, encoding='utf-8')
    for name in ['manifest.json','selection.json']:
        shutil.copy2(DATA/name, out/('input_'+name))
    registry = REPORT/'current_run.json'
    if not registry.exists():
        write(registry, {'run_id':out.name, 'directory':str(out), 'status':'prepared'})
        record('provider_history_prepared',
               'H009: fresh GPT API stream, full separate history of each island, including failures and search feedback. '
               'Same generated-only features/data/downstream/20 valid/300POST/3repairs as H008. No history truncation; input-token budget differs.',
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
    checks = read(REPORT/'dialog_verification.json')
    assert checks['status'] == 'passed'
    assert checks['dialog_module_sha256'] == sha(CODE/'dialog_history.py')
    assert checks['provider_module_sha256'] == sha(CODE/'provider_api.py')
    previous_checks = read(ROOT/'reports/provider_generated_only_v1/validator_verification.json')
    assert previous_checks['status'] == 'passed'
    assert previous_checks['module_sha256'] == sha(CODE/'python_features.py')
    for name in ['python_features.py', 'base_features.py', 'worker.py', 'prompting.py', 'runtime.py', 'features.py']:
        assert sha(CODE/name) == sha(BASE/'runtime_sources'/name)
    write(out/'validator_verification.json', {**previous_checks, 'reused_because_identical_engine_and_worker':True})
    shutil.copy2(REPORT/'dialog_verification.json', out/'dialog_verification.json')
    sys.path.insert(0, str(out/'runtime_sources'))
    import runtime
    from provider_api import ProviderGenerator
    from python_features import RAW
    control = out/'raw_control'
    write(control/'program.json', {'code':RAW})
    (control/'program.py').write_text(RAW, encoding='utf-8')
    original_progress = runtime.progress
    def progress(folder,trials,cfg):
        valid = original_progress(folder,trials,cfg)
        record('provider_history_progress',f'H009: {len(valid)}/20 valid; {len(trials)} responses.',out.name,
               status='searching',measured=len(valid),responses=len(trials),
               api_requests=len(list((out/'api_attempts').glob('attempt_*'))))
        return valid
    runtime.progress = progress
    try:
        write(REPORT/'current_run.json', {'run_id':out.name,'directory':str(out),'status':'running'})
        runtime.evaluate(DATA,control,'search',out/'run_config.json')
        for name in ['model.txt','search_predictions.npy','search_ap.npy']:
            assert sha(control/name) == sha(BASE/'raw_control'/name)
        generator = ProviderGenerator(config,out,ROOT/'.env')
        selected = runtime.search(DATA,out/config['arm'],generator,out/'run_config.json')
        record('provider_history_selection_frozen','Full-history selection frozen before final targets.',out.name,
               status='evaluating',selected_call=selected['call'])
        frame = runtime.finish(DATA,out,out/'run_config.json')
        write(REPORT/'current_run.json',{'run_id':out.name,'directory':str(out),'status':'finished'})
        print(frame.to_string(index=False),flush=True)
        print('Archive:',runtime.archive_run(out),flush=True)
        record('provider_history_finished','H009 final scoring completed; independent audit next.',out.name,
               status='completed_pending_audit',artifacts=str(out.relative_to(ROOT)))
    except BaseException as error:
        (out/'failure.txt').write_text(str(error)+'\n'+traceback.format_exc(),encoding='utf-8')
        write(REPORT/'current_run.json',{'run_id':out.name,'directory':str(out),'status':'interrupted','error':str(error)})
        record('provider_history_interrupted',str(error)[:600],out.name,status='interrupted')
        raise

if __name__ == '__main__':
    main()
