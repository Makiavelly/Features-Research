"""Derive a single-model14B notebook from the frozen running7B/Llama notebook."""
import ast
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
VARIANT = HERE / 'qwen14_small'
PARENT = HERE / 'hm_small_qwen_vs_llama_sql_kaggle_t4.ipynb'
OUTPUT = HERE / 'hm_small_qwen14b_sql_kaggle_t4.ipynb'


def assigned(source, name):
    return next(ast.literal_eval(node.value) for node in ast.parse(source).body
                if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == name)


def main():
    parent = json.loads(PARENT.read_text(encoding='utf-8'))
    cells = copy.deepcopy(parent['cells'])
    module_cell = next(c for c in cells if 'MODULES = ' in ''.join(c['source']))
    modules = assigned(''.join(module_cell['source']), 'MODULES')
    original_hashes = {name: hashlib.sha256(source.encode()).hexdigest() for name, source in modules.items()}
    # Keep all four existing modules byte-identical, including Generator, prompts and search.
    # Only the final report adapter changes from two selected LLMs to one.
    node = next(n for n in ast.parse(modules['runtime.py']).body if isinstance(n, ast.FunctionDef) and n.name == 'finish')
    finish = ast.get_source_segment(modules['runtime.py'], node)
    finish = finish.replace("['qwen', 'llama']", "['qwen14b']")
    finish = finish.replace("['qwen_LightGBM', 'llama_LightGBM', 'raw_control', 'contextgnn', 'lightgbm_manual']",
                            "['qwen14b_LightGBM', 'raw_control', 'contextgnn', 'lightgbm_manual']")
    finish = finish.replace("aps['llama_LightGBM'] - aps['qwen_LightGBM']", "aps['qwen14b_LightGBM'] - aps['raw_control']")
    finish = finish.replace('llama_minus_qwen_pp', 'qwen14b_minus_raw_pp')
    finish = finish.replace('both feature selections', 'the14B feature selection').replace('Both models must be selected before test', 'Select Qwen14B before test')
    finish = finish.replace('Qwen vs Llama', 'Qwen14B').replace('Both LLMs use', 'Qwen14B uses')
    finish = finish.replace('Both selections frozen', 'Selection frozen').replace('fake Qwen/Llama responses', 'fake Qwen14B responses')
    modules['runtime14.py'] = '"""Single-model reporting adapter; search/evaluator modules unchanged."""\nfrom runtime import *\n\n' + finish + '\n'
    hashes = {name: hashlib.sha256(source.encode()).hexdigest() for name, source in modules.items()}
    VARIANT.mkdir(exist_ok=True)
    for name, source in modules.items():
        ast.parse(source)
        (VARIANT / name).write_text(source, encoding='utf-8')
    for index, cell in enumerate(cells):
        source = ''.join(cell['source'])
        if cell['cell_type'] == 'markdown' and index == 0:
            source = '''# Qwen2.5-Coder-14B-Instruct: малый H&M, прежний SQL-интерфейс

Отдельный Kaggle T4 эксперимент для сравнения с уже запущенными Qwen7B и Llama8B.
Здесь запускается **только Qwen2.5-Coder-14B-Instruct**. Результаты других LLM не нужны
как Input: все три отчёта будут сопоставлены позже локально в репозитории.

1. Импортируйте этот `.ipynb` в свежую Kaggle-сессию, включите **Internet** и **GPU T4**.
2. Добавьте прежний **hm_small_sql_compare_v1.zip** через Dataset/Input — тот же архив,
   что используется в ноутбуке Qwen7B/Llama. Новый архив данных не требуется.
3. Выполните **Run All** или **Save Version → Run All**.
4. Скачайте `hm_small_qwen14b_sql_v1_<hash>_results.zip` из Output и передайте вместе
   с отчётом двух предыдущих моделей для локального сравнения.

Qwen14B публична: запрашивать доступ на Hugging Face и добавлять HF_TOKEN не нужно.
Используется одна T4/GPU0,NF4/double-quant/FP16,batch1 генерации,SDPA. Длина промпта
и ответа сохранена прежней:6144+2048 токенов. Реальный пик памяти14B ещё не измерен;
при OOM сохраняется failure/ZIP, контекст и протокол автоматически не уменьшаются.

Сохраняются prompts/responses,call/proposal/island/repair/parent,status/error,
программы признаков,деревья,метрики и прогнозы,графики поиска/logloss/MAP и AP-гистограммы.
ZIP обновляется после каждого вызова и при исключениях. Cancel Kaggle может помешать
публикации Output. Этот ноутбук не загружает и не переобучает Qwen7B или Llama.
'''
        elif cell['cell_type'] == 'markdown':
            source = source.replace('Обе модели:', 'Qwen14B:').replace('Ранее локальная Qwen', 'Ранее локальная Qwen7B')
            source = source.replace('Каждой модели:', 'Qwen14B:').replace('для обеих LLM', 'как у обеих предыдущих LLM')
            source = source.replace('параметры одинаковые', 'параметры сохранены прежними')
            source = source.replace('**обе модели выбираются до test**', '**Qwen14B выбирается до test**')
            source = source.replace('[Qwen model card](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct)',
                                    '[Qwen14B model card](https://huggingface.co/Qwen/Qwen2.5-Coder-14B-Instruct)')
        elif 'LLAMA_SOURCE = ' in source:
            start = source.index('LLAMA_SOURCE = ')
            end = source.index('CONFIG = ', start)
            source = source[:start] + "MODELS = {'qwen14b': {'model_id': 'Qwen/Qwen2.5-Coder-14B-Instruct', 'revision': None}}\n" + source[end:]
            source = source.replace("'protocol': 'hm_small_qwen_llama_sql_v1'", "'protocol': 'hm_small_qwen14b_sql_v1'")
            source = source.replace("    'llama_source': LLAMA_SOURCE,\n", '')
            source = source.replace('/tmp/hm_small_qwen_llama_cache', '/tmp/hm_small_qwen14b_cache')
        elif 'MODULES = ' in source:
            start = source.index('MODULES = ')
            end = source.index('EXPECTED_MANIFEST = ', start)
            source = source[:start] + 'MODULES = ' + repr(modules) + '\nMODULE_SHA = ' + repr(hashes) + '\n' + source[end:]
            source = source.replace("WORK / 'hm_small_sql_runtime'", "WORK / 'hm_small_qwen14b_runtime'")
            source = source.replace('import runtime as experiment', 'import runtime14 as experiment')
        elif 'HfApi' in source:
            start = source.index('TOKEN = ')
            end = source.index('from huggingface_hub', start)
            source = source[:start] + 'TOKEN = None  # public model; no login or Kaggle Secret required\n' + source[end:]
            source = source.replace('Проверяем доступ к обеим моделям до начала первого поиска.', 'Фиксируем immutable revision публичной Qwen14B перед поиском.')
            source = source.replace("WORK / 'example_scratch'", "WORK / 'qwen14b_example_scratch'")
            # Record unchanged parent modules/version, without importing previous results.
            source = source.replace('CONFIG.update(models=MODELS,', "CONFIG.update(parent_protocol='hm_small_qwen_llama_sql_v1', models=MODELS,")
        elif "for label in ['qwen', 'llama']" in source and 'Generator' in source:
            source = source.replace("['qwen', 'llama']", "['qwen14b']")
            source = source.replace("{'qwen', 'llama'}", "{'qwen14b'}")
            source = source.replace('Test обеих моделей', 'Test Qwen14B')
            source = source.replace('# Модели загружаются последовательно: одновременно в VRAM находится только одна.', '# Загружается только Qwen14B; предыдущие LLM не запускаются.')
        elif 'comparison = experiment.finish' in source:
            source = source.replace("['qwen', 'llama']", "['qwen14b']")
        if cell['cell_type'] == 'code':
            ast.parse(source)
            cell['execution_count'], cell['outputs'] = None, []
        cell['source'] = source.splitlines(keepends=True)
        cell['id'] = hashlib.sha256(source.encode()).hexdigest()[:12]
    notebook = {**parent, 'cells': cells}
    OUTPUT.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding='utf-8')
    parent_manifest = json.loads((HERE / 'small_compare/delivery_manifest.json').read_text())
    delivery = {'protocol': 'hm_small_qwen14b_sql_v1', 'notebook': OUTPUT.name,
                'notebook_sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                'parent_notebook_sha256': hashlib.sha256(PARENT.read_bytes()).hexdigest(),
                'parent_protocol': parent_manifest['protocol'], 'shared_modules_identical': original_hashes,
                'modules': hashes, 'dataset': parent_manifest['dataset'],
                'dataset_sha256': parent_manifest['dataset_sha256'],
                'bundle_manifest_sha256': parent_manifest['bundle_manifest_sha256'],
                'previous_llms_required_as_input': False, 'llm_inference_executed_locally': False}
    (VARIANT / 'delivery_manifest.json').write_text(json.dumps(delivery, indent=2), encoding='utf-8')
    print('Created', OUTPUT, len(cells), 'cells; shared4 modules unchanged')


if __name__ == '__main__':
    main()
