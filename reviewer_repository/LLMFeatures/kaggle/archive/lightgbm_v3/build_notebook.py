"""Build a self-contained Kaggle notebook; no repository checkout is required."""
import ast
import hashlib
import json
from pathlib import Path
import textwrap

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATA=ROOT/'data/kaggle_hm_llmfe_fulltrain_v2'
cells=[]


def cell(kind,text):
    text=textwrap.dedent(text).strip()+'\n'
    item={'cell_type':kind,'id':hashlib.sha256((str(len(cells))+text).encode()).hexdigest()[:12],
          'metadata':{},'source':text.splitlines(keepends=True)}
    if kind=='code':
        ast.parse(text)
        item.update(execution_count=None,outputs=[])
    cells.append(item)


cell('markdown','''
# LLM-FE на H&M: Llama‑3.1‑8B‑Instruct, Kaggle T4

Llama создаёт Python-программы признаков; LightGBM измеряет их качество и направляет
поиск в трёх популяциях. LightGBM используется на всех этапах: контроль, search,
confirmation и итоговая оценка. Ручной LightGBM и GNN→LightGBM сравниваются по сохранённым предсказаниям
на **тех же пользователях и кандидатах**. Это адаптация исследования, не его точное воспроизведение.

**Как запустить:**
1. В Kaggle импортируйте этот `.ipynb` через **File → Import Notebook**.
2. Выберите GPU **T4** (достаточно одной; при T4×2 используется GPU0), включите Internet.
3. Создайте Kaggle Dataset из `hm_llmfe_kaggle_fulltrain_v2.zip` и добавьте его через Input.
   Поддерживаются и исходный ZIP, и автоматически распакованные Kaggle файлы.
4. В конфиге выберите `MODEL_SOURCE = 'unsloth'` (по умолчанию, без токена) или `'hf'`.
   Для `'hf'` получите доступ к [официальной Llama](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)
   и добавьте `HF_TOKEN` в **Add-ons → Secrets**. Оба источника размещены на Hugging Face.
5. Выполните **Run All**. Модель скачивается автоматически; веса не входят в архив данных.
6. Скачайте итоговый `*_results.zip` из Output. В нём программы, модели деревьев, метрики и графики.

В ZIP данных находятся **те же803377 обучающих пар /50000 user-time строк /52 снимка**, что
в локальных сравнениях. Новое отрицательное семплирование не выполняется.
Ограничена только оценка: search256, confirmation512, отдельная val1024, test2048 пользователей.
Поисковые/confirmation/итоговые val строки не пересекаются. Кандидаты ID-GNN неизменны;
позитивные test-товары в пул дополнительно не добавляются.
''')
cell('markdown','''
## Условия и отличия от статьи

| Параметр | Этот ноутбук |
|---|---|
| LLM | Llama-3.1-8B-Instruct: официальный источник Meta (`hf`) или публикация Unsloth (`unsloth`) |
| Размещение на T4 | NF4 4-bit, вычисления float16; квантизация — наше отличие |
| Генерация | temperature0.8,3 программы на один prompt, всего20 программ |
| Память поиска | 3 независимые популяции; до3 демонстраций, кластеры по validation MAP, Boltzmann sampling |
| Форма признаков | Python/pandas, `modify_features(X, history)`; без старых ручных/GNN-признаков |
| Основной evaluator | LightGBM, binary objective,150 boosting rounds,31 лист; подбор через MAP@12 |
| Проверка сопоставимости | Raw/LLM LightGBM на одних парах; те же деревья проходят confirmation и финал |
| История | Только выбранная когорта клиентов, до cutoff, последние180 дней; global counts относятся к этой когорте |
| Ресурсы | 30секунд на вызов функции признаков,4GiB на отдельный evaluator,1800секунд на обучение+оценку |
| Отбор | search→confirmation; итоговые val/test открываются после фиксации программы |

В статье рассматриваются табличные classification/regression, используются другие датасеты,
а лимит30секунд относится к полной оценке. Здесь сохраняем оригинальные803377 пар, поэтому
выделяем отдельный больший лимит для полного обучения и4GiB вместо2GiB. По прямому указанию
пользователя весь отбор переведён на LightGBM; XGBoost в этом протоколе не используется.
В Kaggle нет повторного обучения GNN. Это новый протокол v3, результаты v2 не переиспользуются.
Референсные деревья использовали те же пары, но другие схемы подбора/производные seeds;
GNN дополнительно обучалась на графе. Это сравнение качества конвейеров, не изолированный
эффект способа генерации признаков. Полные старые MAP нельзя подставлять вместо MAP этой выборки.

Источники: [LLM-FE §4.3, Appendix B](https://arxiv.org/html/2503.14434v3),
[код авторов](https://github.com/nikhilsab/LLMFE),
[NF4](https://huggingface.co/docs/transformers/v4.57.1/quantization/bitsandbytes).
''')
cell('code','''
import subprocess, sys
# Не переустанавливаем torch/CUDA из готового окружения Kaggle.
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q',
    'transformers==4.57.1', 'accelerate==1.10.1', 'bitsandbytes==0.48.1',
    'lightgbm==4.6.0', 'sentencepiece==0.2.1'])
''')
cell('code','''
from pathlib import Path
import os, json, hashlib, time, gc, importlib.metadata
import numpy as np
import pandas as pd
from IPython.display import display, Markdown, Image, FileLink

# Оба варианта скачиваются с Hugging Face; различается издатель репозитория.
MODEL_SOURCE = 'unsloth'  # 'unsloth' без токена; 'hf' официальный Meta с доступом/HF_TOKEN
MODEL_SOURCES = {
    'hf': {'repo_id':'meta-llama/Llama-3.1-8B-Instruct', 'requires_token':True},
    'unsloth': {'repo_id':'unsloth/Meta-Llama-3.1-8B-Instruct', 'requires_token':False},
}
if MODEL_SOURCE not in MODEL_SOURCES:
    raise ValueError("MODEL_SOURCE должен быть 'hf' или 'unsloth'")
MODEL_ID = MODEL_SOURCES[MODEL_SOURCE]['repo_id']

def resolve_auth(source, environ, load_secret):
    if source not in MODEL_SOURCES:
        raise ValueError("MODEL_SOURCE должен быть 'hf' или 'unsloth'")
    if not MODEL_SOURCES[source]['requires_token']:
        # False запрещает также автоматическое использование старого токена из HF-кэша.
        return False
    value = environ.get('HF_TOKEN')
    if not value:
        try:
            value = load_secret()
        except Exception:
            value = None
    if not value:
        raise RuntimeError('Для hf нужны одобренный доступ Meta и Kaggle Secret HF_TOKEN; либо выберите unsloth')
    return value

# При повторе можно указать SHA из предыдущего run_config.json; пустая строка разрешит текущую ревизию.
MODEL_REVISION = ''
WORK = Path('/kaggle/working')
INPUT_ROOT = Path('/kaggle/input')
WORK.mkdir(parents=True, exist_ok=True)
os.environ['HF_HOME'] = str(WORK / 'hf_cache')
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

CONFIG = {
    'protocol': 'hm_llmfe_llama31_8b_lightgbm_fulltrain_v3', 'seed':42,
    'search_backend':'lightgbm',
    'model_id':MODEL_ID, 'model_source':MODEL_SOURCE,
    'quantization':'bnb NF4 4bit/double_quant, FP16 compute',
    'temperature':0.8, 'top_p':1.0, 'top_k':0,
    'islands':3, 'programs_per_prompt':3, 'llm_samples':20, 'max_demonstrations':3,
    'max_input_tokens':6144, 'max_new_tokens':2048,
    'train_pairs':803377, 'train_user_times':50000,
    'search_users':256, 'confirmation_users':512, 'heldout_val_users':1024, 'test_users':2048,
    'cpu_threads':min(4, os.cpu_count() or 1),
    'evaluation_memory_gb':4, 'evaluation_timeout_seconds':1800,
    'feature_call_timeout_seconds':30, 'lightgbm_rounds':150,
    'paper_reproduction':False, 'candidate_protocol':'exact saved ID-GNN seed42 pools',
}
''')
assets={name:(HERE/name).read_text() for name in ['worker.py','runtime.py']}
cell('code','''
# Код evaluator встроен в ноутбук: клонировать репозиторий не требуется.
MODULES = '''+repr(assets)+'''
CODE = WORK / 'llmfe_runtime'
CODE.mkdir(exist_ok=True)
for name, source in MODULES.items():
    (CODE / name).write_text(source, encoding='utf-8')
sys.path.insert(0, str(CODE))
import importlib
import worker as feature_worker
importlib.reload(feature_worker)
import runtime as experiment
importlib.reload(experiment)
''')
manifest_sha=hashlib.sha256((DATA/'manifest.json').read_bytes()).hexdigest()
cell('code',f'''
DATA, manifest = experiment.locate_bundle(INPUT_ROOT, WORK, '{manifest_sha}')
assert manifest['train_pairs'] == 803377 and manifest['train_user_times'] == 50000
assert manifest['files']['train_pairs.parquet']['sha256'] == manifest['train_source_sha256']
CONFIG['bundle_manifest_sha256'] = '{manifest_sha}'
display(pd.DataFrame([{{'split':k,'users':v['users'],'pairs':v['pairs']}} for k,v in manifest['splits'].items()]))
print('Training pairs:', manifest['train_pairs'], 'history rows:', manifest['history_rows'])
print('Data checksums: OK')
''')
cell('markdown','''
## Доступ к Llama и фиксация запуска

`unsloth` скачивается анонимно, без чтения Kaggle Secrets и сохранённых HF-токенов.
Это полноразмерная публикация весов; NF4-квантизация выполняется при загрузке одинаково
для обоих источников. Unsloth-библиотека и её отдельное окружение не требуются.
`hf` требует одобрения Meta и `HF_TOKEN`. При403 проверьте доступ, при401 — токен.
Автоматического переключения источника нет. Ревизия публикации фиксируется отдельно;
побитовое совпадение весов двух издателей здесь не проверено. Лицензия Llama сохраняется.
Конфигурация, ревизия модели, версии пакетов, хеши данных и evaluator определяют новый run ID;
старые результаты не перезаписываются. Токен не сохраняется в артефакты и не выводится.
''')
cell('code','''
import torch
from huggingface_hub import HfApi, hf_hub_download
if not torch.cuda.is_available():
    raise RuntimeError('Включите GPU T4 в настройках Kaggle')
gpu = torch.cuda.get_device_properties(0)
if gpu.total_memory < 14 * 1024**3:
    raise RuntimeError('Нужно не менее14GiB GPU RAM; выбранная карта не подходит для этой конфигурации')

def load_kaggle_secret():
    from kaggle_secrets import UserSecretsClient
    return UserSecretsClient().get_secret('HF_TOKEN')

token = resolve_auth(MODEL_SOURCE, os.environ, load_kaggle_secret)
try:
    revision = HfApi(token=token).model_info(MODEL_ID, revision=MODEL_REVISION or 'main').sha
    hf_hub_download(MODEL_ID, 'config.json', revision=revision, token=token)
except Exception:
    hint = 'Internet и существование ревизии' if MODEL_SOURCE == 'unsloth' else 'Internet, HF_TOKEN и одобрение доступа Meta'
    raise RuntimeError('Не удалось прочитать ' + MODEL_ID + '. Проверьте ' + hint) from None

CONFIG['model_revision'] = revision
CONFIG['gpu'] = gpu.name
CONFIG['versions'] = {p:importlib.metadata.version(p) for p in
    ['torch','transformers','accelerate','bitsandbytes','lightgbm','pandas','numpy','pyarrow']}
CONFIG['runtime_sha256'] = {name:hashlib.sha256(source.encode()).hexdigest() for name,source in MODULES.items()}
fingerprint = hashlib.sha256(json.dumps(CONFIG,sort_keys=True).encode()).hexdigest()[:12]
RUN_ID = CONFIG['protocol'] + '_' + fingerprint
OUT = WORK / RUN_ID
OUT.mkdir(exist_ok=True)
config_path = OUT / 'run_config.json'
if config_path.exists() and json.loads(config_path.read_text()) != CONFIG:
    raise RuntimeError('Config mismatch: start a new run directory')
experiment.write_json(config_path, CONFIG)
print('Run:', RUN_ID, '| source:', MODEL_SOURCE, '| model:', MODEL_ID, '| GPU:', gpu.name, '| revision:', revision)
''')
cell('code','''
# Контроль без LLM-признаков: реальное обучение на всех803377 парах.
control = OUT / 'raw_control'
control.mkdir(exist_ok=True)
(control / 'program.py').write_text(experiment.RAW, encoding='utf-8')
baseline = experiment.evaluate(DATA, control, 'search', CONFIG)
print('Raw LightGBM search MAP@12:', 100 * baseline['map'], '%')
print('Control training/evaluation seconds:', baseline['seconds'])
''')
cell('markdown','''
## Загрузка Llama на GPU0

Это инференс, без fine-tuning. NF4 позволяет разместить веса и KV-кеш на одной T4.
Используется float16; BF16 и FlashAttention2 не требуются. CPU-деревья обучаются
в отдельном процессе и не занимают VRAM. Первое скачивание весов может быть долгим.
''')
cell('code','''
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, set_seed
set_seed(CONFIG['seed'])
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=revision, token=token, trust_remote_code=False)
quantization = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, revision=revision, token=token,
    quantization_config=quantization, torch_dtype=torch.float16, device_map={'':0},
    attn_implementation='sdpa', trust_remote_code=False, low_cpu_mem_usage=True)
model.eval()
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = 'left'
print('Model GPU footprint GiB:', model.get_memory_footprint()/1024**3)
experiment.write_json(OUT / 'model_runtime.json', {
    'model':MODEL_ID, 'model_source':MODEL_SOURCE, 'revision':revision, 'is_loaded_in_4bit':bool(model.is_loaded_in_4bit),
    'gpu':gpu.name, 'footprint_bytes':int(model.get_memory_footprint()),
    'allocated_vram_bytes':int(torch.cuda.memory_allocated(0))})
''')
cell('code','''
def generate_program(prompt, seed):
    set_seed(seed)
    messages = [
        {'role':'system','content':'You are a feature engineering researcher. Follow the Python interface exactly.'},
        {'role':'user','content':prompt},
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors='pt', add_special_tokens=False).to('cuda:0')
    prompt_tokens = inputs['input_ids'].shape[1]
    if prompt_tokens > CONFIG['max_input_tokens']:
        raise ValueError('Prompt exceeds input budget; no silent context truncation')
    endings = [tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids('<|eot_id|>')]
    endings = list({int(i) for i in endings if i is not None})
    tick = time.perf_counter()
    with torch.inference_mode():
        output = model.generate(**inputs, max_new_tokens=CONFIG['max_new_tokens'],
            do_sample=True, temperature=CONFIG['temperature'], top_p=CONFIG['top_p'], top_k=CONFIG['top_k'],
            num_return_sequences=1, eos_token_id=endings, pad_token_id=tokenizer.pad_token_id, use_cache=True)
    generated = output[0, prompt_tokens:]
    result = {'text':tokenizer.decode(generated, skip_special_tokens=True),
        'seed':seed, 'prompt_tokens':int(prompt_tokens), 'generated_tokens':int(len(generated)),
        'seconds':time.perf_counter()-tick,
        'truncated':len(generated)>=CONFIG['max_new_tokens'] and int(generated[-1]) not in endings}
    del output, inputs, generated
    return result

# b=3: одинаковый prompt, три независимых последовательных сэмпла; это экономит VRAM T4.
#20 — общий бюджет программ, включая ошибочные; это отдельный протокол от локального H002.
selected = experiment.search(DATA, OUT, CONFIG, generate_program)
print('Selection frozen before test:', selected)
display(Image(filename=str(OUT / 'search_progress.png')))
display(Image(filename=str(OUT / 'training_and_rejections.png')))
''')
cell('markdown','''
## Программа, выбранная LightGBM → итоговая оценка

Выбранные признаки фиксируются по confirmation LightGBM; test не влияет на выбор. Контроль без новых признаков
тоже может победить. Оба новых LightGBM обучаются на тех же803377 парах, что прежние
ручной и GNN→LightGBM. Все методы оцениваются на одинаковых val/test строках и пулах.
Старые модели не перетренируются: их сохранённые top12 включены в архив данных.
Протоколы подбора/производные seeds различаются, GNN обучалась дополнительно на графе.
''')
cell('code','''
# Генерации больше не нужны; освобождаем VRAM.
del model
gc.collect()
torch.cuda.empty_cache()
report = experiment.final(DATA, OUT, CONFIG)
display(pd.read_csv(OUT / 'comparison.csv').assign(
    val_map=lambda x:100*x.val_map, test_map=lambda x:100*x.test_map))
print('Все новые модели: полный повтор предсказаний из сохранённых весов подтверждён.')
''')
cell('code','''
for name in ['comparison.png','ap_histograms.png','paired_comparison.png','lightgbm_comparison.png']:
    display(Image(filename=str(OUT / name)))
display(Markdown((OUT / 'report.md').read_text()))
''')
cell('code','''
import shutil
archive = shutil.make_archive(str(WORK / (RUN_ID + '_results')), 'zip', root_dir=OUT)
display(FileLink(archive))
print('Скачайте ZIP из Output. Веса Llama и HF_TOKEN в него не включены.')
''')
cell('markdown','''
## Что смотреть после запуска

- `report.md`, `comparison.csv`: MAP на одной и той же небольшой выборке, включая три способа + контроли.
- `comparison.png`, `ap_histograms.png`, `paired_comparison.png`, `lightgbm_comparison.png`: сравнение и распределения.
- `search_progress.png`, `training_and_rejections.png`: поиск, отказы и train logloss; loss не выбирает победителя.
- `candidates/candidate_*/program.py`, `response.json`, `trial.json`: полные программы, ответы и причины отказов.
- `selected.json`, `confirmation.json`: проверяемая история выбора только по validation.
- `model.json`/`model.txt`, `schema.json`, `*_metrics.json`, `*_predictions.npy`: новые деревья и независимый повтор.
- `run_config.json`, `model_runtime.json`: версия Llama, квантизация, пакеты, хеши кода/данных.

Проверки AST и отдельный CPU-процесс ограничивают интерфейс, время и память, но не являются
полноценной изоляцией произвольного враждебного Python-кода. Generated code не получает токен,
метки или будущую историю через функцию. Новые LLM-признаки не заимствуются из ручных/GNN-признаков.
''')

notebook={'nbformat':4,'nbformat_minor':5,'metadata':{
    'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
    'language_info':{'name':'python','version':'3.11'},'accelerator':'GPU'},'cells':cells}
path=HERE/'llmfe_llama31_hm_kaggle_t4.ipynb'
path.write_text(json.dumps(notebook,ensure_ascii=False,indent=1),encoding='utf-8')
print(f'Created {path.name}: {len(cells)} cells, {path.stat().st_size} bytes; all code cells parse')
