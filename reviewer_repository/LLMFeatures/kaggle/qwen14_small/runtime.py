"""Matched local-Qwen SQL protocol for two sequential Kaggle LLMs."""
import gc
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback
import zipfile
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from worker import ap12, sha, write
from features import FeatureEngine, validate_program
from original_prompt import INSTRUCTION, program_key


def locate_bundle(input_root, working, expected):
    matches = []
    for path in Path(input_root).rglob('manifest.json'):
        try:
            if json.loads(path.read_text()).get('bundle_id') == 'hm_small_sql_compare_v1':
                matches.append(path.parent)
        except (ValueError, OSError):
            pass
    if not matches:
        archives = list(Path(input_root).rglob('hm_small_sql_compare_v1.zip'))
        if len(archives) != 1:
            raise FileNotFoundError('Attach hm_small_sql_compare_v1.zip as a Kaggle Dataset/Input')
        destination = Path(working) / 'hm_small_sql_compare_input'
        destination.mkdir(exist_ok=True)
        with zipfile.ZipFile(archives[0]) as archive:
            for member in archive.infolist():
                if not (destination / member.filename).resolve().is_relative_to(destination.resolve()):
                    raise ValueError('Unsafe archive member')
            archive.extractall(destination)
        matches = [destination]
    if len(matches) != 1:
        raise ValueError('Attach exactly one small comparison bundle')
    root = matches[0]
    assert sha(root / 'manifest.json') == expected, 'Unexpected bundle version'
    manifest = json.loads((root / 'manifest.json').read_text())
    for name, digest in manifest['files'].items():
        assert sha(root / name) == digest, 'Checksum mismatch: ' + name
    return root, manifest


def archive_run(out):
    out = Path(out)
    temporary = out.parent / (out.name + '_results.partial')
    with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(out.rglob('*')):
            if p.is_file() and 'scratch' not in p.parts:
                archive.write(p, str(p.relative_to(out)))
    final = out.parent / (out.name + '_results.zip')
    temporary.replace(final)
    return final


def evaluate(data, directory, stage, config_path, replay=False):
    directory = Path(directory)
    result = directory / f'{stage}_metrics.json'
    if result.exists():
        metric = json.loads(result.read_text())
        if stage != 'preflight':
            assert metric['program_sha256'] == sha(directory / 'program.json')
            assert metric['model_sha256'] == sha(directory / 'model.txt')
        return metric
    config = json.loads(Path(config_path).read_text())
    env = {k: v for k, v in os.environ.items() if not any(s in k.upper() for s in ['TOKEN', 'SECRET', 'API_KEY'])}
    env.update(CUDA_VISIBLE_DEVICES='', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    command = [sys.executable, '-u', str(Path(__file__).with_name('worker.py')), '--data', str(data),
               '--directory', str(directory), '--stage', stage, '--config', str(config_path)]
    with (directory / f'{stage}.log').open('w') as log:
        completed = subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT,
                                   timeout=config['evaluation_timeout_seconds'], check=False)
    if completed.returncode or not result.exists():
        raise RuntimeError((directory / f'{stage}.log').read_text()[-3500:])
    return json.loads(result.read_text())


def parse(text):
    blocks = re.findall(r'```(?:json)?\s*\n(.*?)```', text, re.S | re.I)
    program = validate_program(json.loads(blocks[0] if blocks else text))
    if not program.get('aggregates') and not program.get('derived'):
        raise ValueError('Raw control is host-only: propose at least one feature')
    return program


def make_prompt(data, best, previous, config):
    instruction = INSTRUCTION.replace('105542', '5000')
    prompt = instruction + f'''\nMATCHED SMALL DATA PROTOCOL:
History is the frozen 5000-customer cohort, not the original H&M population. Only t_dat <= cutoff is visible.
Training: {config['train_pairs']} identical sampled pairs from4804 user-times,8 weekly snapshots.
LightGBM binary,150rounds,31leaves. Fitness: fixed128 validation users, ALL5000 articles per user.
Selection: separate88 confirmation users; heldout88 and test250 not used in search.
The host always appends15 raw fields. Same protocol applies to both LLMs.
Use about6-10 aggregates and2-4 derived formulas, at most24/12. Full JSON <=2048 tokens.
History is purchases, not views. Most recent purchase uses min(days_ago).
No raw_* fields in aggregates; raw_* fields belong only to derived formulas.
One complete proposal, not a patch. No markdown, explanations outside JSON or SQL statements.
Previous best complete program in this island and search MAP fraction:
''' + json.dumps({'search_map_fraction': best['score'], 'program': best['program']}, separators=(',', ':'))
    # Concrete raw training examples, chosen only from a training snapshot; no val/test targets.
    prompt += '\nRaw training examples (not new engineered features):\n' + config['training_examples']
    if previous:
        prompt += '\nREPAIR: return the complete corrected JSON. You may remove invalid features and dependent formulas.\n'
        prompt += 'Previous response:\n' + previous['text'] + '\nExact rejection:\n' + previous['error'][-1600:]
    return prompt


def progress(out, trials, config):
    valid = [t for t in trials if t['status'] == 'valid']
    state = {'calls': len(trials), 'measured': len(valid), 'target': config['target_successful_distinct'],
             'max_llm_calls': config['max_llm_calls'], 'trials': trials}
    write(Path(out) / 'search_state.json', state)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    if valid:
        calls = [t['call'] for t in valid]
        scores = np.array([t['score'] for t in valid]) * 100
        axes[0].scatter(calls, scores, c=[t['island'] for t in valid], cmap='viridis', vmin=0, vmax=2)
        axes[0].plot(calls, np.maximum.accumulate(scores), color='black', label='Best search MAP')
        axes[0].legend()
    axes[0].set(xlabel='LLM call', ylabel='Search MAP@12 (%)', title='Search only; color = island')
    counts = pd.Series([t['status'] + ':' + t.get('failure_stage', '') for t in trials]).value_counts()
    axes[1].barh(counts.index, counts.values)
    axes[1].set(title='Accepted / rejected / duplicate', xlabel='Calls')
    fig.tight_layout()
    fig.savefig(Path(out) / 'search_progress.png', dpi=140)
    plt.close(fig)
    return valid


def search(data, out, generate, config_path):
    """Replay stored trials on resume; never request generation twice for a saved response."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    config = json.loads(Path(config_path).read_text())
    if (out / 'selected.json').exists():
        return json.loads((out / 'selected.json').read_text())
    raw = out.parent / 'raw_control'
    baseline = evaluate(data, raw, 'search', config_path)
    memories = [[{'directory': str(raw), 'score': baseline['map'], 'program': {'aggregates': [], 'derived': []}}] for _ in range(3)]
    trials, previous, repair, proposal = [], None, 0, 0
    seen = set()
    while sum(t['status'] == 'valid' for t in trials) < config['target_successful_distinct'] and len(trials) < config['max_llm_calls']:
        number = len(trials) + 1
        island = proposal % 3
        directory = out / 'candidates' / f'candidate_{number:03d}'
        directory.mkdir(parents=True, exist_ok=True)
        trial_path = directory / 'trial.json'
        if trial_path.exists():
            trial = json.loads(trial_path.read_text())
        else:
            trial = {'call': number, 'proposal': proposal, 'island': island, 'repair': repair,
                     'parent_call': previous['call'] if previous else None, 'directory': str(directory)}
            stage = 'generation'
            tick = time.perf_counter()
            text = ''
            try:
                best = max(memories[island], key=lambda x: x['score'])
                prompt = make_prompt(data, best, previous, config)
                (directory / 'prompt.txt').write_text(prompt, encoding='utf-8')
                response_path = directory / 'response.json'
                print(f"{out.name}: call{number}/{config['max_llm_calls']}, measured{len(seen)}/{config['target_successful_distinct']}, island{island}, repair{repair}/{config['max_repairs_per_proposal']}", flush=True)
                if response_path.exists():
                    response = json.loads(response_path.read_text())
                else:
                    response = generate(prompt, 42 + number - 1)
                    write(response_path, response)
                text = response['text']
                trial.update({k: v for k, v in response.items() if k != 'text'})
                stage = 'parse_and_validate'
                if response.get('truncated'):
                    raise ValueError('Output truncated; return a smaller complete feature program')
                program = parse(text)
                key = program_key(program)
                trial['program_key'] = key
                write(directory / 'program.json', program)
                if key in seen:
                    trial.update(status='duplicate', error='Already evaluated feature set; choose a distinct complete set', failure_stage='deduplication')
                else:
                    stage = 'preflight'
                    evaluate(data, directory, 'preflight', config_path)
                    print(f'call{number}: preflight passed; LightGBM training on72813 pairs', flush=True)
                    stage = 'training_and_search'
                    score = evaluate(data, directory, 'search', config_path)
                    trial.update(status='valid', score=score['map'], program=program)
            except Exception as error:
                trial.update(status='rejected', failure_stage=stage, error=str(error))
                (directory / 'error.txt').write_text(traceback.format_exc())
            trial.update(elapsed_seconds=time.perf_counter() - tick)
            write(trial_path, trial)
        trials.append(trial)
        if trial['status'] == 'valid':
            seen.add(trial['program_key'])
            memories[island].append(trial)
            print(f"ACCEPTED call{number}: MAP@12={100*trial['score']:.6f}%", flush=True)
        else:
            print(f"{trial['status'].upper()} call{number}: {trial['error']}", flush=True)
        progress(out, trials, config)
        archive_run(out.parent)
        if trial['status'] != 'valid' and repair < config['max_repairs_per_proposal']:
            text = json.loads((directory / 'response.json').read_text()).get('text', '') if (directory / 'response.json').exists() else ''
            previous = {**trial, 'text': text}
            repair += 1
        else:
            previous, repair, proposal = None, 0, proposal + 1
    valid = sorted([t for t in trials if t['status'] == 'valid'], key=lambda t: (-t['score'], t['call']))
    candidates = [{'directory': str(raw), 'call': None}] + valid[:3]
    confirmation = []
    for trial in candidates:
        metric = evaluate(data, trial['directory'], 'confirm', config_path)
        confirmation.append({'directory': trial['directory'], 'call': trial['call'], 'confirmation_map': metric['map']})
    # Stable ties prefer raw, then earlier higher-search candidate. No test selection.
    winner = max(confirmation, key=lambda t: t['confirmation_map'])
    selected = {**winner, 'selection': 'top3 search plus raw -> disjoint confirmation88',
                'program_sha256': sha(Path(winner['directory']) / 'program.json'),
                'model_sha256': sha(Path(winner['directory']) / 'model.txt'),
                'successful_distinct': len(valid), 'budget_complete': len(valid) == config['target_successful_distinct'],
                'llm_calls': len(trials), 'confirmation': confirmation}
    write(out / 'selected.json', selected)
    archive_run(out.parent)
    return selected


class Generator:
    def __init__(self, spec, config, token=None, cache_dir=None):
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
        if not torch.cuda.is_available():
            raise RuntimeError('Enable a Kaggle T4 GPU')
        self.config = config
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(spec['model_id'], revision=spec['revision'], token=token, cache_dir=cache_dir)
        quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4',
                                  bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
        self.model = AutoModelForCausalLM.from_pretrained(spec['model_id'], revision=spec['revision'], token=token,
                     quantization_config=quant, torch_dtype=torch.float16, device_map={'': 0}, attn_implementation='sdpa', cache_dir=cache_dir)
        self.model.eval()
        self.eos = self.model.generation_config.eos_token_id
        self.pad = self.tokenizer.eos_token_id

    def __call__(self, prompt, seed):
        from transformers import set_seed
        set_seed(seed)
        messages = [{'role': 'system', 'content': 'Return one complete JSON feature program following the user interface.'},
                    {'role': 'user', 'content': prompt}]
        inputs = self.tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True,
                                                    return_dict=True, return_tensors='pt').to('cuda:0')
        tokens = inputs['input_ids'].shape[1]
        if tokens > self.config['max_input_tokens']:
            raise ValueError(f'Prompt too long: {tokens}; no silent truncation')
        started = time.perf_counter()
        with self.torch.inference_mode():
            output = self.model.generate(**inputs, max_new_tokens=self.config['max_new_tokens'], do_sample=True,
                       temperature=self.config['temperature'], top_p=1., top_k=0, repetition_penalty=1.,
                       eos_token_id=self.eos, pad_token_id=self.pad)
        generated = output[0, tokens:]
        eos = self.eos if isinstance(self.eos, list) else [self.eos]
        return {'text': self.tokenizer.decode(generated, skip_special_tokens=True), 'seed': seed,
                'prompt_tokens': tokens, 'generated_tokens': len(generated),
                'seconds': time.perf_counter() - started,
                'truncated': len(generated) >= self.config['max_new_tokens'] and int(generated[-1]) not in eos}

    def close(self):
        del self.model, self.tokenizer
        gc.collect()
        self.torch.cuda.empty_cache()


def finish(data, out, config_path):
    """Open final targets/references only after both feature selections are frozen."""
    data, out = Path(data), Path(out)
    config = json.loads(Path(config_path).read_text())
    smoke = config.get('validation_only_fake_callbacks', False)
    for name in ['qwen', 'llama']:
        assert (out / name / 'selected.json').exists(), 'Both models must be selected before test'
    rows, aps = [], {}
    programs = {'raw_control': out / 'raw_control'}
    for name in ['qwen', 'llama']:
        selected = json.loads((out / name / 'selected.json').read_text())
        assert sha(Path(selected['directory']) / 'program.json') == selected['program_sha256']
        assert sha(Path(selected['directory']) / 'model.txt') == selected['model_sha256']
        programs[name + '_LightGBM'] = Path(selected['directory'])
    for name, directory in programs.items():
        row = {'model': name}
        for stage in ['heldout_val', 'val', 'test']:
            metric = evaluate(data, directory, stage, config_path)
            replay = evaluate(data, directory, 'replay_' + stage, config_path)
            assert replay['passed']
            row[stage + '_map_percent'] = 100 * metric['map']
            if stage == 'test':
                aps[name] = np.load(directory / 'test_ap.npy')
        rows.append(row)
    selection = json.loads((data / 'selection.json').read_text())
    sources = json.loads((data / 'references/sources.json').read_text())
    for source in sources:
        name = source['model']
        row = {'model': name}
        for split in ['val', 'test']:
            target = pd.read_parquet(data / f'{split}_targets.parquet')
            pred = np.load(data / f'references/{name}_{split}.npy')
            ap = ap12(pred, target.article_id)
            expected = source['metrics'][f'{split}_metrics']['map']
            assert abs(float(ap.mean()) - expected) < 1e-10, 'Reference alignment/metric mismatch: ' + name
            row[split + '_map_percent'] = 100 * float(ap.mean())
            if split == 'val':
                row['heldout_val_map_percent'] = 100 * float(ap[selection['heldout_val']].mean())
            else:
                aps[name] = ap
        rows.append(row)
    # Same time-safe popularity control used by the small ContextGNN report.
    tx = pd.read_parquet(data / 'transactions.parquet')
    row = {'model': 'popularity'}
    for split in ['val', 'test']:
        target = pd.read_parquet(data / f'{split}_targets.parquet')
        counts = tx[tx.t_dat <= target.timestamp.iloc[0]].article_id.value_counts().reindex(np.arange(5000), fill_value=0)
        ranking = np.lexsort((np.arange(5000), -counts.to_numpy()))[:12]
        ap = ap12(np.tile(ranking, (len(target), 1)), target.article_id)
        row[split + '_map_percent'] = 100 * float(ap.mean())
        if split == 'val':
            row['heldout_val_map_percent'] = 100 * float(ap[selection['heldout_val']].mean())
        else:
            aps['popularity'] = ap
    rows.append(row)
    frame = pd.DataFrame(rows)
    frame.to_csv(out / 'comparison.csv', index=False)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    for axis, split in zip(axes, ['val', 'test']):
        axis.barh(frame.model, frame[split + '_map_percent'])
        axis.set(title=split + ' — same small catalog5000', xlabel='MAP@12 (%)')
        axis.grid(axis='x', alpha=.2)
    if smoke:
        fig.suptitle('CPU SMOKE — fake Qwen/Llama responses; not LLM performance', color='darkred')
    fig.tight_layout()
    fig.savefig(out / 'comparison.png', dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for name in ['qwen_LightGBM', 'llama_LightGBM', 'raw_control', 'contextgnn', 'lightgbm_manual']:
        values = aps[name]
        axes[0].hist(values[values > 0] * 100, bins=np.linspace(0, 100, 21), histtype='step', label=name)
        axes[1].bar(name, 100 * np.mean(values == 0))
    axes[0].set(xlabel='Per-user AP@12 (%) among AP>0', ylabel='Users', title='Test distribution')
    axes[0].legend(fontsize=7)
    axes[1].set(ylabel='Users with AP@12=0 (%)', ylim=(0, 100))
    axes[1].tick_params(axis='x', labelrotation=35)
    if smoke:
        fig.suptitle('CPU SMOKE — fake Qwen/Llama responses', color='darkred')
    fig.tight_layout()
    fig.savefig(out / 'test_histograms.png', dpi=160)
    plt.close(fig)
    fig, axis = plt.subplots(figsize=(8, 4))
    for name, directory in programs.items():
        curve = json.loads((directory / 'learning_curve.json').read_text())['train']['binary_logloss']
        axis.plot(np.arange(1, len(curve) + 1), curve, label=name)
    axis.set(xlabel='LightGBM round', ylabel='Training binary logloss', title='Loss is diagnostic; selection uses MAP@12')
    axis.legend()
    fig.tight_layout()
    fig.savefig(out / 'lightgbm_training.png', dpi=160)
    plt.close(fig)
    diff = aps['llama_LightGBM'] - aps['qwen_LightGBM']
    rng = np.random.default_rng(42)
    bootstrap = diff[rng.integers(0, len(diff), size=(10000, len(diff)))].mean(1) * 100
    write(out / 'paired_bootstrap.json', {'llama_minus_qwen_pp': float(diff.mean() * 100),
          'ci95_pp': np.quantile(bootstrap, [.025, .975]).tolist(), 'test_users': len(diff), 'seed': 42,
          'note': 'Exploratory paired-user interval, not multi-seed uncertainty'})
    lines = ['# Qwen vs Llama — small H&M SQL feature search', '',
             'Same frozen small-v1 data,72813 train pairs,304val/250test users,all5000 catalog items.',
             'Both LLMs use the original local-Qwen SQL JSON interface and NF4/FP16 loading.',
             'Old local Qwen used Q4_K_M/Ollama: this is not byte-identical quantization.',
             'Both selections frozen before final test. Same20-success target/300-call cap/3repairs/3islands.',
             'Validation304 includes search/confirmation rows; heldout88 is separate for LLMs.',
             'References selected on original full validation, so their heldout88 is not an untouched selection set.',
             'Baselines have different model tuning/training/pretraining budgets. One seed;250test users.', '',
             '| Model | Val MAP,% | Test MAP,% |', '|---|---:|---:|']
    if smoke:
        lines.insert(1, '**CPU SMOKE ONLY: fake Qwen/Llama responses, not actual LLM performance.**')
    for record in rows:
        lines.append(f"| {record['model']} | {record['val_map_percent']:.5f} | {record['test_map_percent']:.5f} |")
    for name in ['qwen', 'llama']:
        selected = json.loads((out / name / 'selected.json').read_text())
        lines += ['', f"{name}: {selected['successful_distinct']} successful /{selected['llm_calls']} calls; budget_complete={selected['budget_complete']}; selected_call={selected['call']} (null=raw control)."]
    lines += ['', '![Comparison](comparison.png)', '', '![Test AP histograms](test_histograms.png)']
    (out / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    budgets_complete = all(json.loads((out / name / 'selected.json').read_text())['budget_complete'] for name in ['qwen', 'llama'])
    write(out / 'complete.json', {'status': 'complete' if budgets_complete else 'complete_with_incomplete_search',
                                'search_budgets_complete': budgets_complete, 'independent_frozen_replays': True,
                                'references_recomputed_from_predictions': True})
    archive_run(out)
    return frame
