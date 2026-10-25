"""Build a separate cumulative H003 A / A+B / A+B+C Kaggle experiment."""
import ast
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
VARIANT = HERE / 'h003_small'
OUTPUT = HERE / 'hm_small_qwen7b_h003_kaggle_t4.ipynb'
PARENT = HERE / 'hm_small_qwen_vs_llama_sql_kaggle_t4.ipynb'


def assigned(source, name):
    return next(ast.literal_eval(n.value) for n in ast.parse(source).body
                if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name)


def replace(source, old, new):
    assert old in source, old
    return source.replace(old, new)


def build():
    notebook = json.loads(PARENT.read_text(encoding='utf-8'))
    cells = copy.deepcopy(notebook['cells'])
    module_cell = next(c for c in cells if 'MODULES = ' in ''.join(c['source']))
    modules = assigned(''.join(module_cell['source']), 'MODULES')
    original = {n: hashlib.sha256(s.encode()).hexdigest() for n, s in modules.items()}
    runtime = modules['runtime.py']
    runtime += '\n\n' + (VARIANT / 'report_addon.py').read_text(encoding='utf-8')
    runtime = replace(runtime, 'from original_prompt import INSTRUCTION, program_key',
                      'from original_prompt import INSTRUCTION, program_key\nfrom diagnostics import decode, diagnose, DiagnosticError, signature')
    start, end = runtime.index('    blocks = ', runtime.index('def parse(')), runtime.index('\n    if not program.get', runtime.index('def parse('))
    runtime = runtime[:start] + '''    decoded = decode(text)
    issues = diagnose(decoded)
    if issues:
        raise DiagnosticError(issues)
    program = validate_program(decoded)''' + runtime[end:]
    runtime = replace(runtime, "    if previous:\n        prompt +=", "    if config.get('arm') in {'h003b', 'h003c'}:\n        prompt += '\\n' + PROMPT_ADDENDUM\n    if previous:\n        prompt +=")
    runtime = replace(runtime, "previous['error'][-1600:]", "previous['error']")
    runtime = replace(runtime, "                text = response['text']", "                text = response['text']\n                trial['response_signature'] = signature(text)\n                trial['unchanged_repair'] = bool(previous and trial['response_signature'] and trial['response_signature'] == previous.get('response_signature'))")
    runtime = replace(runtime, "                trial['program_key'] = key", "                trial['program_key'] = key\n                if previous and key == previous.get('program_key'):\n                    trial['unchanged_repair'] = True")
    runtime = replace(runtime, "                    trial.update(status='duplicate', error='Already evaluated feature set; choose a distinct complete set', failure_stage='deduplication')", '''                    matched = next(t for t in trials if t['status'] == 'valid' and t['program_key'] == key)
                    error = 'Already evaluated feature set; choose a distinct complete set'
                    if config.get('arm') == 'h003c':
                        error += ('; duplicate of call' + str(matched['call']) + '. Matching formulas: '
                                  + json.dumps(matched['program'], separators=(',', ':'))[:1800]
                                  + '\\nChange a meaningful axis: time window, statistic, or candidate grouping. '
                                  + 'For example add/change customer+article/category history. Renaming is not a new set.')
                    trial.update(status='duplicate', error=error, failure_stage='deduplication', duplicate_of=matched['call'])''')
    runtime = replace(runtime, "            except Exception as error:\n                trial.update", "            except Exception as error:\n                if isinstance(error, DiagnosticError):\n                    write(directory / 'diagnostics.json', error.issues)\n                    trial['diagnostic_features'] = len(error.issues)\n                trial.update")
    runtime = replace(runtime, "        if trial['status'] != 'valid' and repair < config['max_repairs_per_proposal']:", "        stop_unchanged = config.get('arm') == 'h003c' and trial.get('unchanged_repair', False)\n        if trial['status'] != 'valid' and repair < config['max_repairs_per_proposal'] and not stop_unchanged:")
    # Every variant selection must be frozen before any final evaluation.
    runtime = replace(runtime, "['qwen', 'llama']", "config['arms']")
    runtime = replace(runtime, "['qwen_LightGBM', 'llama_LightGBM', 'raw_control', 'contextgnn', 'lightgbm_manual']", "[n + '_LightGBM' for n in config['arms']] + ['raw_control', 'contextgnn', 'lightgbm_manual']")
    runtime = replace(runtime, "aps['llama_LightGBM'] - aps['qwen_LightGBM']", "aps[config['arms'][0] + '_LightGBM'] - aps['raw_control']")
    runtime = runtime.replace('llama_minus_qwen_pp', 'first_arm_minus_raw_pp').replace('Qwen vs Llama', 'Qwen7B H003')
    runtime = runtime.replace('Both LLMs use', 'All H003 arms use').replace('both feature selections', 'all H003 feature selections')
    runtime = runtime.replace('Both models must be selected before test', 'All H003 arms must be selected before test')
    runtime = runtime.replace('Both selections frozen', 'All selections frozen').replace('fake Qwen/Llama responses', 'fake H003 responses')
    runtime = replace(runtime, "    archive_run(out)\n    return frame", "    efficiency_report(out, config)\n    archive_run(out)\n    return frame")
    runtime = replace(runtime, "             'Old local Qwen used", "             'Test250 has been inspected in earlier experiments: this is a repeated diagnostic evaluation, not a new untouched test.',\n             'Old local Qwen used")
    addendum = (HERE.parents[1] / 'reports/qwen7b_generation_errors_v1/proposed_prompt_addendum.txt').read_text(encoding='utf-8')
    addendum = addendum.replace('PROPOSED ADDENDUM — NOT AN EXECUTED EXPERIMENT\n', 'SQL INTERFACE EXAMPLES\n')
    runtime += '\nPROMPT_ADDENDUM = ' + repr(addendum) + '\n'
    modules['runtime.py'] = runtime
    modules['diagnostics.py'] = (VARIANT / 'diagnostics.py').read_text(encoding='utf-8')
    hashes = {n: hashlib.sha256(s.encode()).hexdigest() for n, s in modules.items()}
    for name, source in modules.items():
        ast.parse(source)
        (VARIANT / name).write_text(source, encoding='utf-8')
    for i, cell in enumerate(cells):
        source = ''.join(cell['source'])
        if i == 0:
            source = '''# H003: Qwen2.5-Coder-7B-Instruct — диагностика ошибок и повторов

Отдельный эксперимент Kaggle T4 с исходным SQL JSON интерфейсом Qwen.
**A:** все ошибки признаков с адресом/причиной/подсказкой; EXPLAIN на пустой схеме.
**B:** A + компактные корректные примеры в основном промпте.
**C:** A+B + адресная обратная связь о дубликатах и остановка неизменённого repair.
Это три последовательных варианта, каждый с отдельными 20 успешными наборами,
лимитом 300 обращений, 3 исправлениями и 3 популяциями. Модель загружается один раз.
Сравнивайте A со старым Qwen7B, B с A, C с B. Старые результаты не требуются как Input.

1. Импортируйте этот `.ipynb` в Kaggle. Включите **Internet** и **GPU T4**.
2. Добавьте прежний **hm_small_sql_compare_v1.zip** через Dataset/Input.
3. В `ARMS` можно оставить один вариант, например `['h003a']`, либо все три (по умолчанию).
4. **Save Version → Run All**. Qwen публична: HF_TOKEN и разрешение не нужны.
5. Скачайте `hm_small_qwen7b_h003_v1_<hash>_results.zip` из Output.

Те же 72813 train-пар, LightGBM150/31/4CPU, validation304/test250, каталог5000.
Test уже просматривался ранее: итоговая оценка повторная; промпты по нему не выбираются.
Все варианты выбираются по search128 → confirmation88 до открытия итоговых test-метрик.
Никаких автоматических исправлений/удалений признаков; smoke и дубликаты не считаются успехами.
В Output: prompts/responses/diagnostics, принятые/отклонённые наборы, модели, метрики,
графики поиска/logloss/сравнения, гистограммы AP, эффективность и повторы.
ZIP обновляется после каждого обращения; Cancel Kaggle не гарантирует публикацию Output.
'''
        elif cell['cell_type'] == 'markdown':
            source = source.replace('Обе модели:', 'Каждый вариант Qwen7B:').replace('Каждой модели:', 'Каждому варианту:')
            source = source.replace('для обеих LLM', 'как в контрольном запуске').replace('**обе модели выбираются до test**', '**все варианты выбираются до test**')
        elif 'LLAMA_SOURCE = ' in source:
            start, end = source.index('LLAMA_SOURCE = '), source.index('CONFIG = ')
            source = source[:start] + "ARMS = ['h003a', 'h003b', 'h003c']  # cumulative A, A+B, A+B+C\nassert ARMS and len(set(ARMS)) == len(ARMS) and set(ARMS) <= {'h003a', 'h003b', 'h003c'}\nMODELS = {'qwen': {'model_id': 'Qwen/Qwen2.5-Coder-7B-Instruct', 'revision': 'c03e6d358207e414f1eca0bb1891e29f1db0e242'}}\n" + source[end:]
            source = source.replace("'protocol': 'hm_small_qwen_llama_sql_v1'", "'protocol': 'hm_small_qwen7b_h003_v1', 'arms': ARMS, 'test_previously_inspected': True")
            source = source.replace("    'llama_source': LLAMA_SOURCE,", "    'hypothesis': 'H003 cumulative A/AB/ABC',")
            source = source.replace('/tmp/hm_small_qwen_llama_cache', '/tmp/hm_small_qwen7b_h003_cache')
        elif 'MODULES = ' in source:
            start, end = source.index('MODULES = '), source.index('EXPECTED_MANIFEST = ')
            source = source[:start] + 'MODULES = ' + repr(modules) + '\nMODULE_SHA = ' + repr(hashes) + '\n' + source[end:]
            source = source.replace("WORK / 'hm_small_sql_runtime'", "WORK / 'hm_small_h003_runtime'")
        elif 'HfApi' in source:
            start, end = source.index('TOKEN = '), source.index('from huggingface_hub')
            source = source[:start] + 'TOKEN = None  # Public Qwen, pinned revision matches the control\n' + source[end:]
            source = source.replace('Проверяем доступ к обеим моделям', 'Проверяем доступ к Qwen7B')
        elif "for label in ['qwen', 'llama']" in source and 'Generator' in source:
            source = '''# All searches/confirmation are completed before final test evaluation.
generator = None
try:
    pending = [arm for arm in ARMS if not (OUT / arm / 'selected.json').exists()]
    if pending:
        generator = experiment.Generator(MODELS['qwen'], CONFIG, token=TOKEN, cache_dir=CACHE_ROOT / 'qwen')
    for arm in ARMS:
        arm_config = {**CONFIG, 'arm': arm, 'arm_protocol': CONFIG['protocol'] + '_' + arm}
        arm_path = OUT / ('config_' + arm + '.json')
        experiment.write(arm_path, arm_config)
        if not (OUT / arm / 'selected.json').exists():
            experiment.search(DATA, OUT / arm, generator, arm_path)
        print(arm, 'selection frozen:', json.loads((OUT / arm / 'selected.json').read_text()))
except BaseException:
    (OUT / 'failure_search.txt').write_text(traceback.format_exc())
    raise
finally:
    if generator is not None:
        generator.close()
        del generator
    gc.collect()
    print('Checkpoint ZIP:', experiment.archive_run(OUT))
'''
        elif 'comparison = experiment.finish' in source:
            source = source.replace("['qwen', 'llama']", 'ARMS')
            source = source.replace("'lightgbm_training.png'", "'lightgbm_training.png', 'generation_efficiency.png'")
        if cell['cell_type'] == 'code':
            ast.parse(source)
            cell.update(outputs=[], execution_count=None)
        cell['source'] = source.splitlines(keepends=True)
        cell['id'] = hashlib.sha256(source.encode()).hexdigest()[:12]
    notebook['cells'] = cells
    OUTPUT.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding='utf-8')
    manifest = json.loads((HERE / 'small_compare/delivery_manifest.json').read_text())
    manifest.update(protocol='hm_small_qwen7b_h003_v1', notebook=OUTPUT.name,
                    notebook_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(), modules=hashes,
                    parent_modules=original, default_arms=['h003a', 'h003b', 'h003c'],
                    unchanged_modules=[n for n in original if original[n] == hashes[n]],
                    test_previously_inspected=True, llm_inference_executed_locally=False)
    (VARIANT / 'delivery_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print('Created', OUTPUT, len(cells), 'cells')


if __name__ == '__main__':
    build()
