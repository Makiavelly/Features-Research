"""H009 memory with bounded train-statistics requests; no native tools required."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import provider_history as transport
from dialog_history import completed_trials, next_island, feedback


INSTRUCTIONS = '''
You have a research tool for THIS fold's TRAIN data only.
BEFORE your FIRST feature program in this population, you MUST ask at least
one statistical question using query_train. Choose the question yourself.
Later research requests are optional. A direct first program without research
will be returned for research without training or a search score.
Choose your own statistical questions and use the answers to develop feature
hypotheses. To call it, return only one JSON object (no Python in that response):
{{"action":"query_train","sql":"SELECT ..."}}
Otherwise return the complete Python program requested below. You may record
your hypothesis as a Python comment. Do not output prose outside these formats.
The host executes exactly one read-only DuckDB SELECT/WITH statement.
No files, network, libraries, database writes or model fitting are available.
Results: max40rows/24columns/12000characters;20second timeout. Prefer compact
aggregated statistics. Do NOT use the tool to output per-validation predictions.

Available tables (encoded categorical values match modify_features inputs):
{schema}
train_pairs has training labels and raw static inputs. Sampled negatives affect
label rates; this is not an unbiased sample of all possible customer-item pairs.
train_history contains past transactions independently at each TRAIN cutoff.
For relationships to train labels, JOIN train_history.cutoff=train_pairs.timestamp
and apply appropriate customer/article/category keys. days_ago is relative to
that row's cutoff. history is ONLY the LAST TRAIN snapshot, without cutoff;
it is suitable for descriptive statistics, not causal features at earlier dates.
All training history cutoffs: {cutoffs}
No validation/test data or labels are accessible here. Your feature program
receives fresh history at its own prediction cutoff and NEVER train labels.
No tool is callable from modify_features. Avoid hardcoding train IDs or labels.
All20 accepted program checks still use the existing LightGBM search evaluator.
Your research and feedback stay in this population's conversation. You can use
at most4 research calls before submitting the next program. Your population
has {remaining} research requests left; invalid requests also consume budget.
After the first research request, or when your budget is zero, you may submit
Python directly. When exhausted, submit Python directly.
'''


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp.replace(path)


def decode_command(text):
    value = text.strip()
    if value.startswith('```json') and value.endswith('```'):
        value = value[7:-3].strip()
    try:
        obj = json.loads(value)
    except ValueError:
        return None
    return obj if isinstance(obj, dict) else None


class ResearchGenerator:
    def __init__(self, config, out, secret_path, sender=None, runner=None):
        self.config, self.out = config, Path(out)
        self.sender = sender or transport.ProviderGenerator(config, out, secret_path)
        self.runner = runner or self.query

    def used(self, island):
        return sum(read(p)['island'] == island for p in
                   self.out.glob('generations/call_*/step_*/tool_request.json'))

    def researched(self, island):
        for path in self.out.glob('generations/call_*/step_*/tool_request.json'):
            result = path.with_name('tool_result.json')
            if read(path)['island'] == island and result.exists() and read(result).get('ok'):
                return True
        return False

    def query(self, step, sql):
        write(step / 'query_input.json', {'sql': sql})
        env = {k: v for k, v in os.environ.items()
               if not any(s in k.upper() for s in ['TOKEN', 'SECRET', 'API_KEY'])}
        env.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
        try:
            result = subprocess.run([sys.executable, str(Path(__file__).with_name('query_worker.py')),
                    '--database', str(self.out / 'research.duckdb'),
                    '--input', str(step / 'query_input.json'),
                    '--output', str(step / 'query_output.json')],
                    env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    timeout=self.config['research_query_timeout_seconds'])
            if result.returncode or not (step / 'query_output.json').exists():
                return {'ok': False, 'error': 'Research worker failed; reduce query complexity'}
            return read(step / 'query_output.json')
        except subprocess.TimeoutExpired:
            return {'ok': False, 'error': 'Research query exceeded20seconds'}

    def request(self, messages, seed, step):
        cache = step / 'response.json'
        if cache.exists():
            return read(cache)
        attempts = self.out / 'api_attempts'
        plan = step / 'request_plan.json'
        if not plan.exists():
            write(plan, {'api_attempt': len(list(attempts.glob('attempt_*'))) + 1})
        number = read(plan)['api_attempt']
        attempt = attempts / f'attempt_{number:03d}'
        if (attempt / 'response.json').exists():
            assert read(attempt / 'request.json')['messages'] == messages
            result = read(attempt / 'response.json')
            choice = result['choices'][0]
            content = choice['message'].get('content') or ''
            if isinstance(content, list):
                content = '\n'.join(x.get('text', '') for x in content if isinstance(x, dict))
            usage = result.get('usage', {})
            response = {'text': content, 'seed': seed, 'prompt_tokens': usage.get('prompt_tokens', 0),
                        'generated_tokens': usage.get('completion_tokens', 0), 'seconds': 0,
                        'truncated': choice.get('finish_reason') == 'length',
                        'finish_reason': choice.get('finish_reason'), 'api_attempt': number,
                        'provider_model': result.get('model'), 'usage': usage,
                        'recovered_paid_response': True}
        else:
            if attempt.exists():
                raise transport.ProviderUnavailable('Unresolved/failed API attempt; inspect saved request before retry')
            previous = transport.build_messages
            transport.build_messages = lambda *args: messages
            try:
                response = self.sender('', seed)
            finally:
                transport.build_messages = previous
        write(cache, response)
        return response

    def __call__(self, prompt, seed):
        number = seed - self.config['seed'] + 1
        folder = self.out / 'generations' / f'call_{number:03d}'
        final = folder / 'final.json'
        if final.exists():
            return read(final)['response']
        trials = completed_trials(self.config, self.out, number)
        island = next_island(self.config, trials)
        own = [t for t in trials if t['island'] == island]
        context = [{'role': 'system', 'content': self.config['system_message'] +
                    '\nThe query_train JSON research protocol below is also allowed. Before the first feature submission in each population, one train-statistics query is required; choose it yourself.'}]
        for trial in own:
            previous = read(self.out / 'generations' / f"call_{trial['call']:03d}" / 'final.json')
            assert previous['island'] == island
            context.extend(previous['turns'])
        initial = folder / 'initial.json'
        if not initial.exists():
            remaining = self.config['research_island_budgets'][island] - self.used(island)
            schema = '\n'.join(name + ': ' + ', '.join(f'{c[0]} {c[1]}' for c in cols)
                               for name, cols in self.config['research_tables'].items())
            instructions = INSTRUCTIONS.format(schema=schema,
                         cutoffs=self.config['research_history_cutoffs'], remaining=remaining)
            write(initial, {'island': island, 'prompt': prompt, 'turns': [
                {'role': 'user', 'content': (feedback(own[-1]) if own else '') +
                 instructions + '\nORIGINAL FEATURE TASK:\n' + prompt}]})
        start = read(initial)
        assert start['island'] == island and start['prompt'] == prompt
        turns = start['turns']
        responses = []
        queries_this_generation = 0
        for index in range(10):
            step = folder / f'step_{index:02d}'
            response = self.request(context + turns, seed, step)
            responses.append(response)
            turns.append({'role': 'assistant', 'content': response['text']})
            command = decode_command(response['text'])
            if command is None:
                if not self.researched(island) and self.config['research_island_budgets'][island] > 0:
                    if self.used(island) >= self.config['research_island_budgets'][island]:
                        raise transport.ProviderUnavailable('Research budget exhausted without a successful initial query; cannot submit unresearched program')
                    notice = {'ok': False, 'error': 'Before your first feature program, ask at least one train-statistics question of your own choice. Return query_train JSON now. This code has NOT been trained or scored.'}
                    write(step / 'protocol_notice.json', notice)
                    turns.append({'role': 'user', 'content': json.dumps(notice)})
                    continue
                combined = dict(response)
                for key in ['prompt_tokens', 'generated_tokens', 'seconds']:
                    combined[key] = sum(r.get(key, 0) for r in responses)
                combined['research_queries_this_generation'] = queries_this_generation
                combined['generation_api_attempts'] = [r.get('api_attempt') for r in responses]
                write(final, {'island': island, 'turns': turns, 'response': combined})
                return combined
            tool_result = step / 'tool_result.json'
            if not tool_result.exists():
                used = self.used(island)
                if command.get('action') != 'query_train':
                    result = {'ok': False, 'error': 'Only query_train JSON or complete Python is supported'}
                elif not (step / 'tool_request.json').exists() and (used >= self.config['research_island_budgets'][island] or queries_this_generation >= 4):
                    result = {'ok': False, 'error': 'Research budget exhausted. Submit complete Python now.'}
                else:
                    write(step / 'tool_request.json', {'island': island, 'command': command})
                    result = self.runner(step, command.get('sql'))
                write(tool_result, result)
            if (step / 'tool_request.json').exists():
                queries_this_generation += 1
            turns.append({'role': 'user', 'content': 'QUERY_TRAIN_RESULT:\n' +
                          json.dumps(read(tool_result), ensure_ascii=False) +
                          ('\nSubmit complete Python now; no more research in this generation.'
                           if queries_this_generation >= 4 else '\nContinue research or submit complete Python.')})
        raise transport.ProviderUnavailable('Model did not submit Python after10 research/protocol turns; outputs preserved')
