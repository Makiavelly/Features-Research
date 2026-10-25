"""Build a self-contained Kaggle notebook; preserve the original local-Qwen DSL."""
import ast
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VARIANT = HERE / 'small_compare'


def literal(source, name):
    return next(ast.literal_eval(node.value) for node in ast.parse(source).body
                if isinstance(node, ast.Assign) and any(isinstance(n, ast.Name) and n.id == name for n in node.targets))


def build():
    original = (ROOT / 'LLMFeatures/features.py').read_text(encoding='utf-8')
    # Freeze exactly the original implementation, materialize host input before disabling external access.
    original = original.replace('CREATE VIEW tx AS SELECT', 'CREATE TABLE tx AS SELECT')
    # Large sparse product/category codes create enormous LightGBM categorical bitsets.
    # Factorize statics once, identically for raw X and SQL history/grouping keys.
    marker = '        self.category_maps = {}\n'
    original = original.replace(marker, marker + '''        for column in ITEM_COLUMNS:
            encoded, categories = pd.factorize(self.items[column], sort=True)
            self.category_maps[column] = categories.tolist()
            self.items[column] = encoded.astype(np.int32)
''')
    (VARIANT / 'features.py').write_text(original, encoding='utf-8')
    source = (ROOT / 'LLMFeatures/h002_run.py').read_text(encoding='utf-8')
    function = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'program_key')
    key_source = ast.get_source_segment(source, function)
    instruction = literal((ROOT / 'LLMFeatures/run.py').read_text(encoding='utf-8'), 'INSTRUCTION')
    prompt = 'import hashlib, json, re\nINSTRUCTION = ' + repr(instruction) + '\n\n' + key_source + '\n'
    (VARIANT / 'original_prompt.py').write_text(prompt, encoding='utf-8')
    modules = {p.name: p.read_text(encoding='utf-8') for p in [VARIANT / n for n in ['features.py', 'original_prompt.py', 'worker.py', 'runtime.py']]}
    module_sha = {n: hashlib.sha256(s.encode()).hexdigest() for n, s in modules.items()}
    data_manifest = ROOT / 'data/kaggle_hm_small_sql_compare_v1/manifest.json'
    manifest_sha = hashlib.sha256(data_manifest.read_bytes()).hexdigest()
    cells = []

    def cell(kind, text):
        text = text.strip() + '\n'
        if kind == 'code':
            ast.parse(text)
        entry = {'cell_type': kind, 'id': hashlib.sha256(text.encode()).hexdigest()[:12],
                 'metadata': {}, 'source': text.splitlines(keepends=True)}
        if kind == 'code':
            entry.update(execution_count=None, outputs=[])
        cells.append(entry)

    cell('markdown', '''# Qwen и Llama: одинаковый SQL-интерфейс на малом H&M

Отдельный эксперимент для Kaggle T4. Сравниваются **Qwen2.5-Coder-7B-Instruct** и
**Llama-3.1-8B-Instruct**: JSON с SQL-агрегатами и производными выражениями, как у прежней
локальной Qwen. Используется исходный FeatureEngine локальной Qwen; joins и время контролирует host.
Ограничений токенов по грамматике здесь нет: это сопоставление на прежнем интерфейсе.

1. Импортируйте этот `.ipynb` в Kaggle, включите **Internet** и **GPU T4**.
2. Создайте Kaggle Dataset из **hm_small_sql_compare_v1.zip** и добавьте через **Input**.
   Прежний большой fulltrain_v2 архив здесь не нужен.
3. В конфиге выберите источник Llama: `hf` либо `unsloth`. Для официальной Meta нужен
   одобренный доступ и Kaggle Secret **HF_TOKEN**. Qwen публичная.
4. Нажмите **Run All** или **Save Version → Run All**. Модели работают последовательно на GPU0.
5. Скачайте `hm_small_qwen_llama_sql_v1_<hash>_results.zip` из Output.

Сохраняются prompts/responses, принадлежность к популяции, причины отказов, программы,
модели LightGBM, графики поиска, logloss, MAP-сравнение и гистограммы AP по пользователям.
Архив обновляется после каждого обращения и при исключении. Принудительная остановка Kaggle
может помешать публикации Output; это не гарантирует сохранность при Cancel.
''')
    cell('markdown', '''## Зафиксированные условия

- Датасет **rel-hm-small-v1** из пилота ContextGNN:5000 покупателей,5000 товаров,46442 транзакции.
- Ровно те же **72813 train-пар**, что у малого ручного LightGBM и IDGNN→LightGBM;
  4804 user-time,8 срезов. Новое семплирование не выполняется.
- Исходные val304/test250, оценка **всех5000 товаров**. Позитивы не добавляются в кандидаты.
- Validation делится seed42 на search128/confirmation88/heldout88 без пересечений.
  Итоговый val304 включает поисковые строки; отдельный heldout88 также сохраняется.
- Обе модели:NF4/double-quant/FP16,temperature0.8,2048 новых токенов,seed42+номер обращения−1.
  Ранее локальная Qwen работала через Ollama в Q4_K_M: квантизация теперь другая.
- Каждой модели:цель20 различных успешно оценённых наборов,до300 вызовов,до3 исправлений,
  3 независимые популяции,лучший предыдущий набор своей популяции в промпте.
- Raw15 контроль; никаких ручных исторических или GNN-признаков в LLM-входе.
  Статические товарные категории кодируются компактно и одинаково в raw/history для обеих LLM.
  LightGBM150rounds/31leaves/4CPUthreads,параметры одинаковые. Контроль также может победить.
- Top3 по search и raw сравниваются на confirmation88; **обе модели выбираются до test**.
  Итоговые прогнозы повторяются отдельными процессами из сохранённых моделей.
- Сохранённые IDGNN,ContextGNN,двухбашенная модель,manual/IDGNN→LightGBM и Recformer
  пересчитываются из top12 на тех же целях; их обучение в Kaggle не повторяется.

Один seed и250test пользователей дают предварительные результаты. Бюджеты обучения baseline
различаются; ручные деревья выбирали15/31 лист по полному val304. Их heldout88 не был закрыт
при первоначальном отборе. Результаты относятся к малому каталогу и не являются воспроизведением статьи.

Источники:[Qwen model card](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct),
[Transformers NF4](https://huggingface.co/docs/transformers/v4.57.1/quantization/bitsandbytes).
''')
    cell('code', '''import subprocess, sys
# Сохраняем предустановленные torch/CUDA. Запускайте в свежей Kaggle-сессии.
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q',
    'transformers==4.57.1', 'accelerate==1.10.1', 'bitsandbytes==0.48.1',
    'lightgbm==4.6.0', 'duckdb==1.4.1', 'sentencepiece==0.2.1', 'pyarrow>=18'])
''')
    cell('code', '''from pathlib import Path
import os, json, hashlib, time, traceback, importlib.metadata, gc, shutil
import numpy as np
import pandas as pd
from IPython.display import display, Image, FileLink

LLAMA_SOURCE = 'hf'  # 'hf' либо 'unsloth'; оба источника скачиваются с Hugging Face
MODELS = {
    'qwen': {'model_id': 'Qwen/Qwen2.5-Coder-7B-Instruct', 'revision': None},
    'llama': {
        'hf': {'model_id': 'meta-llama/Llama-3.1-8B-Instruct',
               'revision': '0e9e39f249a16976918f6564b8830bc894c89659'},
        'unsloth': {'model_id': 'unsloth/Meta-Llama-3.1-8B-Instruct', 'revision': None},
    }[LLAMA_SOURCE],
}
CONFIG = {
    'protocol': 'hm_small_qwen_llama_sql_v1', 'seed': 42,
    'target_successful_distinct': 20, 'max_llm_calls': 300, 'max_repairs_per_proposal': 3,
    'islands': 3, 'memory_programs_per_prompt': 1,
    'temperature': .8, 'max_input_tokens': 6144, 'max_new_tokens': 2048,
    'lightgbm_rounds': 150, 'cpu_threads': 4, 'scoring_user_batch': 16,
    'evaluation_timeout_seconds': 1800,
    'quantization': 'bnb NF4/double_quant/FP16',
    'feature_interface': 'original_local_qwen_SQL_aggregates_and_derived',
    'search_users': 128, 'confirmation_users': 88, 'heldout_val_users': 88,
    'validation_users': 304, 'test_users': 250, 'evaluation_catalog': 5000,
    'llama_source': LLAMA_SOURCE,
}
WORK = Path('/kaggle/working')
# Download caches excluded from Output; remove dedicated model cache after unloading to save disk.
CACHE_ROOT = Path('/tmp/hm_small_qwen_llama_cache')
CACHE_ROOT.mkdir(parents=True, exist_ok=True)
os.environ['HF_HOME'] = str(CACHE_ROOT)
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
''')
    cell('code', 'MODULES = ' + repr(modules) + '\nMODULE_SHA = ' + repr(module_sha) + '\nEXPECTED_MANIFEST = ' + repr(manifest_sha) + '''
CODE = WORK / 'hm_small_sql_runtime'
CODE.mkdir(exist_ok=True)
for name, source in MODULES.items():
    (CODE / name).write_text(source, encoding='utf-8')
sys.path.insert(0, str(CODE))
import runtime as experiment
DATA, MANIFEST = experiment.locate_bundle('/kaggle/input', WORK, EXPECTED_MANIFEST)
print('Bundle:', MANIFEST['bundle_id'], '| train pairs:', MANIFEST['train_pairs'], '| catalog:', MANIFEST['catalog'])
''')
    cell('code', '''# Проверяем доступ к обеим моделям до начала первого поиска. Токен не сохраняется в конфиг.
TOKEN = os.environ.get('HF_TOKEN')
if TOKEN is None:
    try:
        from kaggle_secrets import UserSecretsClient
        TOKEN = UserSecretsClient().get_secret('HF_TOKEN')
    except Exception:
        TOKEN = None
from huggingface_hub import HfApi, hf_hub_download
for label, spec in MODELS.items():
    info = HfApi().model_info(spec['model_id'], revision=spec['revision'], token=TOKEN)
    spec['revision'] = info.sha
    hf_hub_download(spec['model_id'], 'config.json', revision=spec['revision'], token=TOKEN,
                    cache_dir=str(CACHE_ROOT / label))
CONFIG.update(models=MODELS, bundle_manifest_sha256=EXPECTED_MANIFEST, runtime_sha256=MODULE_SHA,
              train_pairs=MANIFEST['train_pairs'], train_pair_sha256=MANIFEST['train_pair_sha256'])
CONFIG['versions'] = {name: importlib.metadata.version(name) for name in
    ['torch', 'transformers', 'bitsandbytes', 'accelerate', 'lightgbm', 'duckdb', 'numpy', 'pandas', 'pyarrow']}
import torch
assert torch.cuda.is_available(), 'Enable GPU T4 in Kaggle settings'
CONFIG['gpu'] = torch.cuda.get_device_name(0)
engine = experiment.FeatureEngine(WORK / 'example_scratch', DATA)
try:
    pairs = pd.read_parquet(DATA / 'train_pairs.parquet')
    sample = pairs[pairs.timestamp == pairs.timestamp.min()].head(3)
    engine.prepare(sample.timestamp.iloc[0], sample.customer_id.values, {'aggregates': [], 'derived': []})
    CONFIG['training_examples'] = engine.frame(sample).to_json(orient='records')
finally:
    engine.close()
fingerprint = hashlib.sha256(json.dumps(CONFIG, sort_keys=True).encode()).hexdigest()[:12]
OUT = WORK / (CONFIG['protocol'] + '_' + fingerprint)
OUT.mkdir(exist_ok=True)
CONFIG_PATH = OUT / 'run_config.json'
if CONFIG_PATH.exists():
    assert json.loads(CONFIG_PATH.read_text()) == CONFIG, 'Changed config requires another run ID'
experiment.write(CONFIG_PATH, CONFIG)
for name, source in MODULES.items():
    destination = OUT / 'runtime_sources' / name
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(source, encoding='utf-8')
shutil.copy2(DATA / 'manifest.json', OUT / 'input_manifest.json')
shutil.copy2(DATA / 'selection.json', OUT / 'validation_selection.json')
print('Run:', OUT.name, '| GPU:', CONFIG['gpu'])
print(json.dumps(MODELS, indent=2))
''')
    cell('code', '''raw = OUT / 'raw_control'
raw.mkdir(exist_ok=True)
experiment.write(raw / 'program.json', {'aggregates': [], 'derived': []})
try:
    baseline = experiment.evaluate(DATA, raw, 'search', CONFIG_PATH)
    print('Raw15 search MAP@12:', 100 * baseline['map'], '%')
finally:
    print('Checkpoint ZIP:', experiment.archive_run(OUT))
''')
    cell('code', '''# Только поиск/confirmation. Test обеих моделей откроется в следующей ячейке.
# Модели загружаются последовательно: одновременно в VRAM находится только одна.
for label in ['qwen', 'llama']:
    generator = None
    try:
        if not (OUT / label / 'selected.json').exists():
            generator = experiment.Generator(MODELS[label], CONFIG, token=TOKEN, cache_dir=CACHE_ROOT / label)
            experiment.search(DATA, OUT / label, generator, CONFIG_PATH)
        print(label, 'selection frozen:', json.loads((OUT / label / 'selected.json').read_text()))
    except BaseException:
        (OUT / ('failure_' + label + '.txt')).write_text(traceback.format_exc())
        raise
    finally:
        if generator is not None:
            generator.close()
            del generator
        # Delete only the cache created for this model by this notebook, outside the result directory.
        model_cache = (CACHE_ROOT / label).resolve()
        assert model_cache.parent == CACHE_ROOT.resolve() and label in {'qwen', 'llama'}
        if model_cache.exists():
            shutil.rmtree(model_cache)
        gc.collect()
        print('Checkpoint ZIP:', experiment.archive_run(OUT))
''')
    cell('code', '''try:
    comparison = experiment.finish(DATA, OUT, CONFIG_PATH)
    display(comparison)
    for name in ['comparison.png', 'test_histograms.png', 'lightgbm_training.png']:
        display(Image(filename=str(OUT / name)))
    for label in ['qwen', 'llama']:
        display(Image(filename=str(OUT / label / 'search_progress.png')))
except BaseException:
    (OUT / 'failure_final.txt').write_text(traceback.format_exc())
    raise
finally:
    archive = experiment.archive_run(OUT)
    print('Results ZIP:', archive)
    display(FileLink(str(archive)))
''')
    notebook = {'nbformat': 4, 'nbformat_minor': 5, 'cells': cells,
                'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                             'language_info': {'name': 'python', 'version': '3.12'},
                             'kaggle': {'accelerator': 'gpu', 'isInternetEnabled': True, 'language': 'python'}}}
    destination = HERE / 'hm_small_qwen_vs_llama_sql_kaggle_t4.ipynb'
    destination.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding='utf-8')
    manifest = {'protocol': 'hm_small_qwen_llama_sql_v1', 'notebook': destination.name,
                'notebook_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
                'modules': module_sha, 'bundle_manifest_sha256': manifest_sha,
                'dataset': 'hm_small_sql_compare_v1.zip',
                'dataset_sha256': hashlib.sha256((HERE / 'hm_small_sql_compare_v1.zip').read_bytes()).hexdigest(),
                'llm_inference_executed_locally': False}
    (VARIANT / 'delivery_manifest.json').write_text(json.dumps(manifest, indent=2))
    print('Created', destination, len(cells), 'cells')


if __name__ == '__main__':
    build()
