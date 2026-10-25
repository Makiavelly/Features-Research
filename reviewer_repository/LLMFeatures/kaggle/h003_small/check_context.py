"""Measure exact Qwen chat-template tokens; download tokenizer only, not model."""
import json
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import runtime
from diagnostics import diagnose, DiagnosticError
os.environ['USE_TORCH'] = '0'
os.environ['USE_TF'] = '0'
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[3]
REPORT = ROOT / 'reports/kaggle_llmfe_validation/h003_small_v1'
SOURCE = ROOT / 'reports/hm_small_llms_v1/exports/qwen_llama'
config = json.loads((SOURCE / 'run_config.json').read_text())
trials = json.loads((SOURCE / 'qwen/search_state.json').read_text())['trials']
inventory = json.loads((ROOT / 'reports/qwen7b_generation_errors_v1/response_inventory.json').read_text())
rows = {r['call']: r for r in inventory}
tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen2.5-Coder-7B-Instruct',
    revision='c03e6d358207e414f1eca0bb1891e29f1db0e242', cache_dir='/tmp/h003_context_tokenizer')


def count(prompt):
    messages = [{'role': 'system', 'content': 'Return one complete JSON feature program following the user interface.'},
                {'role': 'user', 'content': prompt}]
    return len(tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True))


measured = []
raw_score = json.loads((SOURCE / 'raw_control/search_metrics.json').read_text())['map']
for arm in ['h003a', 'h003b', 'h003c']:
    memory = [[{'score': raw_score, 'program': {'aggregates': [], 'derived': []}}] for _ in range(3)]
    for trial in trials:
        previous = None
        if trial.get('parent_call'):
            parent = rows[trial['parent_call']]
            previous = {'text': parent['text'], 'error': parent['error']}
            issues = diagnose(parent['program'])
            if issues:
                previous['error'] = str(DiagnosticError(issues))
            elif parent['status'] == 'duplicate' and arm == 'h003c':
                previous['error'] += ('; duplicate of an earlier measured call. Matching formulas: '
                    + json.dumps(parent['program'], separators=(',', ':'))[:1800]
                    + '\nChange a meaningful axis: time window, statistic, or candidate grouping. '
                    + 'For example add/change customer+article/category history. Renaming is not a new set.')
        best = max(memory[trial['island']], key=lambda t: t['score'])
        prompt = runtime.make_prompt(None, best, previous, {**config, 'arm': arm})
        measured.append(dict(arm=arm, historical_call=trial['call'], repair=trial['repair'], input_tokens=count(prompt)))
        if trial['status'] == 'valid':
            memory[trial['island']].append(trial)
summary = {'tokenizer_model': 'Qwen/Qwen2.5-Coder-7B-Instruct',
           'revision': 'c03e6d358207e414f1eca0bb1891e29f1db0e242',
           'includes_system_and_chat_template': True, 'model_loaded': False,
           'input_limit': 6144, 'output_limit': 2048,
           'scope': 'Reconstructed H003 prompts on the historical 67-call trajectory; not a new LLM experiment or proof for all possible future outputs',
           'arms': {arm: {'min_input_tokens': min(r['input_tokens'] for r in measured if r['arm']==arm),
                         'max_input_tokens': max(r['input_tokens'] for r in measured if r['arm']==arm),
                         'over_limit': sum(r['input_tokens']>6144 for r in measured if r['arm']==arm)}
                    for arm in ['h003a', 'h003b', 'h003c']}, 'prompts': measured}
(REPORT / 'context_budget.json').write_text(json.dumps(summary, indent=2))
print(json.dumps({k:v for k,v in summary.items() if k != 'prompts'}, indent=2))
