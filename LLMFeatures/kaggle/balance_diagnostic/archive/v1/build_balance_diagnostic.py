"""Self-contained balance-scale diagnostic; six calls, no evolutionary search."""
import ast
import hashlib
import json
from pathlib import Path
import textwrap

HERE=Path(__file__).resolve().parent
D=HERE/'balance_diagnostic'
base=json.loads((HERE/'llmfe_llama31_hm_kaggle_t4.ipynb').read_text(encoding='utf-8'))
def find(marker):return next(''.join(c['source']) for c in base['cells'] if c['cell_type']=='code' and marker in ''.join(c['source']))
cells=[]
def cell(kind,text):
    text=textwrap.dedent(text).strip()+'\n'
    if kind=='code':ast.parse(text)
    item={'cell_type':kind,'id':hashlib.sha256((str(len(cells))+text).encode()).hexdigest()[:12],
          'metadata':{},'source':text.splitlines(keepends=True)}
    if kind=='code':item.update(execution_count=None,outputs=[])
    cells.append(item)
cell('markdown','''
# Диагностика Llama на исходной задаче balance-scale

6 обращений:3 chat-template и3 текстовых completion с одинаковыми seeds42/43/44.
Исходные625 строк, задача и начальная Python-программа авторов LLM-FE встроены.
Данные H&M и архив Input **не нужны**. T4 + Internet; MODEL_SOURCE hf/unsloth.
Выберите тот же MODEL_SOURCE и MODEL_REVISION, что в проблемном запуске.
Загрузка прежняя: NF4/double quant/FP16, Transformers и temperature0.8.

Это диагностика соблюдения интерфейса, не воспроизведение итоговых метрик статьи.
Начальная функция взята без изменения формул; запрос собран из исходных
domain_head/domain_tail, спецификации,10 train-примеров и версии modify_features_v0.
Выбор примеров/сериализация/способ подачи адаптированы; текстовый completion
не гарантирует совпадения с внутренней обработкой авторского LLM-сервера.
Нет repairs, эволюции или20 успешных наборов. Все ответы и ошибки сохраняются.
Дерево — XGBoost, как в исходной спецификации, не H&M LightGBM.
Оцениваем4-fold CV только на500 train строках первого внешнего fold;125 heldout не оцениваем.
Числовая обработка упрощена; фиксированная версия XGBoost тоже отличается от неизвестного окружения статьи.

Запуск: импортировать .ipynb в отдельный Kaggle Notebook, включить T4/Internet,
выбрать источник/ревизию модели и Run All. Для hf необходим одобренный доступ/HF_TOKEN.
Источники: [код авторов](https://github.com/nikhilsab/LLMFE), [статья](https://arxiv.org/abs/2503.14434).
''')
cell('code',find("'transformers==4.57.1'").replace("'lightgbm==4.6.0'","'xgboost==3.0.5'"))
config=find('MODEL_SOURCES =').split('CONFIG = {',1)[0]
config=config.replace("MODEL_SOURCE = 'unsloth'", "MODEL_SOURCE = 'hf'")
config=config.replace("MODEL_REVISION = ''", "MODEL_REVISION = '0e9e39f249a16976918f6564b8830bc894c89659' if MODEL_SOURCE == 'hf' else ''")
config+='''CONFIG = {
    'protocol':'balance_scale_llama31_diagnostic_v1','seed':42,
    'model_id':MODEL_ID,'model_source':MODEL_SOURCE,
    'quantization':'bnb NF4 4bit/double_quant, FP16 compute',
    'temperature':0.8,'top_p':1.0,'top_k':0,
    'max_input_tokens':6144,'max_new_tokens':2048,
    'formats':['chat','completion'],'seeds':[42,43,44],'max_calls':6,
    'paper_reproduction':False,'heldout_evaluated':False,
}
'''
cell('code',config)
assets={name:(D/name).read_text(encoding='utf-8') for name in ['host.py','worker.py']}
inputs={str(p.relative_to(D/'upstream')):p.read_bytes().decode('utf-8') for p in (D/'upstream').rglob('*') if p.is_file()}
manifest=json.loads((D/'upstream_manifest.json').read_text())
cell('code','MODULES = '+repr(assets)+'\nINPUT_FILES = '+repr(inputs)+'\nUPSTREAM_MANIFEST = '+repr(manifest)+'''
import sys, importlib
CODE=WORK/'balance_diagnostic_runtime';CODE.mkdir(exist_ok=True)
for name,source in MODULES.items():(CODE/name).write_text(source,encoding='utf-8')
SOURCE=CODE/'upstream';SOURCE.mkdir(exist_ok=True)
for name,source in INPUT_FILES.items():
    path=SOURCE/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(source,encoding='utf-8')
    assert hashlib.sha256(path.read_bytes()).hexdigest()==UPSTREAM_MANIFEST['files'][name]['sha256']
sys.path.insert(0,str(CODE))
import host as experiment
importlib.reload(experiment)
CONFIG['upstream_revision']=UPSTREAM_MANIFEST['revision']
CONFIG['upstream_manifest_sha256']=hashlib.sha256(json.dumps(UPSTREAM_MANIFEST,sort_keys=True).encode()).hexdigest()
''')
cell('code',find('from huggingface_hub import HfApi').replace("'bitsandbytes','lightgbm'","'bitsandbytes','xgboost'"))
cell('code','''
# Эти контроли ручные, не ответы Llama. Evaluator проверяется до загрузки больших весов.
control_results=experiment.controls(SOURCE,OUT)
experiment.write_json(OUT/'upstream_manifest.json',UPSTREAM_MANIFEST)
''')
cell('code',find('from transformers import AutoTokenizer'))
generator=find('def generate_program(').split('# b=3:',1)[0]
generator=generator.replace('def generate_program(prompt, seed):',"def generate_program(prompt, seed, mode='chat'):")
generator=generator.replace("text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)",
                            "text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True) if mode=='chat' else prompt")
generator=generator.replace("'seed':seed, 'prompt_tokens'","'rendered_prompt':text, 'format':mode, 'seed':seed, 'prompt_tokens'")
cell('code',generator)
cell('code','''
trials=experiment.run_diagnostic(SOURCE,OUT,CONFIG,generate_program)
del model
gc.collect();torch.cuda.empty_cache()
summary=experiment.report(OUT,CONFIG,trials,control_results)
display(pd.DataFrame(summary))
display(pd.read_csv(OUT/'trials.csv'))
display(Image(filename=str(OUT/'diagnostic.png')))
display(Markdown((OUT/'report.md').read_text()))
import shutil
archive=shutil.make_archive(str(WORK/(RUN_ID+'_results')),'zip',root_dir=OUT)
display(FileLink(archive))
print('Download results ZIP: configuration, prompts, raw responses, errors and plots are included.')
''')
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
    'language_info':{'name':'python','version':'3.11'},'accelerator':'GPU'},'cells':cells}
output=HERE/'llmfe_llama31_balance_scale_diagnostic_t4.ipynb'
output.write_text(json.dumps(nb,ensure_ascii=False,indent=1),encoding='utf-8')
delivery={'notebook':output.name,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
          'upstream_revision':manifest['revision'],'max_llm_calls':6,'real_llama_executed':False}
(D/'delivery_manifest.json').write_text(json.dumps(delivery,indent=2)+'\n')
print('Built',output.name,'with',len(cells),'cells')
