"""Create immutable common input archive and two self-contained Kaggle notebooks."""
import ast
import importlib.metadata
import json
from pathlib import Path
import shutil
import sys
import zipfile
import pandas as pd
from common import ROOT,DATA,OUT,REPORT,read,write,sha,freeze_text,record
from recformer_grid import build

KAGGLE=ROOT/'CVFollowup/kaggle'
PACKAGE=ROOT/'CVFollowup/cache/kaggle_recformer_v1'
LABELS=['lr3e6_w100','lr1e5_w300']

def copy(source,dest):
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)

def cell(text,markdown=False):
    import hashlib
    value={'cell_type':'markdown' if markdown else 'code','id':hashlib.sha256(text.encode()).hexdigest()[:12],'metadata':{},'source':text.splitlines(keepends=True)}
    if not markdown:value.update(execution_count=None,outputs=[])
    return value

def notebook(label,digest):
    title=f'Recformer medium CV — {label} — 3 folds, train only'
    setup='''from pathlib import Path
import hashlib, json, os, subprocess, sys, zipfile
LABEL = LABEL_VALUE
EXPECTED_BUNDLE_SHA256 = SHA_VALUE
EXPECTED_INPUT_MANIFEST_SHA256 = MANIFEST_VALUE
# Attach recformer_medium_cv_inputs_v1.zip as Kaggle Input; Internet ON; Accelerator GPU T4.
WORK = Path('/kaggle/working')
INPUT_ROOT = Path('/tmp/recformer_inputs_v1')
INPUT_ROOT.mkdir(exist_ok=True)
matches = list(Path('/kaggle/input').rglob('recformer_medium_cv_inputs_v1.zip'))
if matches:
    assert len(matches) == 1, f'Multiple matching archives: {matches}'
    INPUT_ZIP = matches[0]
    with INPUT_ZIP.open('rb') as f:
        assert hashlib.file_digest(f, 'sha256').hexdigest() == EXPECTED_BUNDLE_SHA256, 'Input archive checksum mismatch'
    with zipfile.ZipFile(INPUT_ZIP) as z:
        for name in z.namelist():
            assert (INPUT_ROOT / name).resolve().is_relative_to(INPUT_ROOT.resolve()), 'Unsafe archive member'
        z.extractall(INPUT_ROOT)
else:
    # Kaggle may automatically expand ZIP uploads into a Dataset.
    import shutil
    candidates = []
    for p in Path('/kaggle/input').rglob('input_manifest.json'):
        with p.open('rb') as f:
            if hashlib.file_digest(f, 'sha256').hexdigest() == EXPECTED_INPUT_MANIFEST_SHA256:
                candidates.append(p.parent)
    assert len(candidates) == 1, f'Attach the shared input Dataset; found {candidates}'
    shutil.copytree(candidates[0], INPUT_ROOT, dirs_exist_ok=True)
with (INPUT_ROOT / 'input_manifest.json').open('rb') as f:
    assert hashlib.file_digest(f, 'sha256').hexdigest() == EXPECTED_INPUT_MANIFEST_SHA256
print('Verified inputs:', INPUT_ROOT)
'''.replace('LABEL_VALUE',repr(label)).replace('SHA_VALUE',repr(digest)).replace('MANIFEST_VALUE',repr(sha(PACKAGE/'input_manifest.json')))
    env='''# Separate Python3.11 environment: works even if Kaggle kernel uses Python3.13.
# Does not change notebook kernel packages. Downloads need Internet.
INSTALLER = Path('/tmp/recformer_uv_installer')
if not (INSTALLER / 'uv').exists():
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', '--target', str(INSTALLER), 'uv==0.9.4'], check=True)
uv_env = os.environ.copy()
uv_binary = INSTALLER / 'bin/uv'
if not uv_binary.is_file():
    binaries = [p for p in INSTALLER.rglob('uv') if p.is_file()]
    assert len(binaries) == 1, f'uv executable missing: {binaries}'
    uv_binary = binaries[0]
uv = [str(uv_binary)]
ENV = Path('/tmp/recformer_py311')
if not (ENV / 'bin/python').exists():
    subprocess.run(uv + ['venv', '--python', '3.11', str(ENV)], env=uv_env, check=True)
PYTHON = ENV / 'bin/python'
subprocess.run(uv + ['pip', 'install', '--python', str(PYTHON), '--index-url',
    'https://download.pytorch.org/whl/cu118', 'torch==2.2.2+cu118'], env=uv_env, check=True)
requirements = json.loads((INPUT_ROOT / 'requirements.json').read_text())
subprocess.run(uv + ['pip', 'install', '--python', str(PYTHON), *requirements], env=uv_env, check=True)
subprocess.run([str(PYTHON), '-c', 'import torch,transformers; print(torch.__version__, transformers.__version__); print(torch.cuda.get_device_name()); assert torch.cuda.is_available()'], check=True)
'''
    run='''OUTPUT = WORK / f'recformer_medium_{LABEL}_kaggle_v1'
command = [str(PYTHON), '-u', str(INPUT_ROOT / 'kaggle_runtime.py'),
    '--input', str(INPUT_ROOT), '--output', str(OUTPUT), '--label', LABEL]
subprocess.run(command + ['--check-only'], check=True)
subprocess.run(command, check=True)
'''
    final='''archive = WORK / f'{OUTPUT.name}_results.zip'
assert archive.exists(), 'Result archive missing; inspect earlier errors'
print('Download from Save Version -> Output:', archive.name)
print((OUTPUT / 'completed_folds.json').read_text())
from IPython.display import FileLink, display
display(FileLink(str(archive)))
'''
    data={'cells':[cell(f'# {title}\n\nНастройки фиксированы: seed42, batch4, accumulation4, FP16, 2+2 эпохи. Те же три medium-фолда и pretrained weights.\n\n1. Создайте Kaggle Dataset с общим ZIP и подключите через Add Input.\n2. Включите Internet и GPU T4. HF_TOKEN не нужен: веса уже в ZIP.\n3. Запустите Save Version → Save & Run All. По окончании скачайте `*_results.zip` из Output и верните в локальный проект.\n\nЭтот ноутбук обучает только назначенную настройку. Test не оценивается; общую настройку выберем локально по validation трёх фолдов. Другая GPU может давать отличия FP16/AMP; версии и skipped updates сохраняются.\n',True),cell(setup),cell(env),cell(run),cell(final)],
        'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'accelerator':'GPU'},'nbformat':4,'nbformat_minor':5}
    for c in data['cells']:
        if c['cell_type']=='code':ast.parse(''.join(c['source']))
    path=KAGGLE/f'recformer_medium_{label}_kaggle_t4.ipynb';write(path,data)
    return path

def refresh():
    archive=KAGGLE/'recformer_medium_cv_inputs_v1.zip'
    digest=sha(archive);notebooks=[notebook(label,digest) for label in LABELS]
    write(KAGGLE/'bundle_manifest.json',{'zip':archive.name,'bytes':archive.stat().st_size,'sha256':digest,
        'input_manifest_sha256':sha(PACKAGE/'input_manifest.json'),'notebooks':{p.name:sha(p) for p in notebooks}})
    return archive,digest

def main():
    KAGGLE.mkdir(parents=True,exist_ok=True);PACKAGE.mkdir(parents=True,exist_ok=True)
    for fold in range(3):
        data=DATA/f'fold_{fold}'
        for file in [data/'manifest.yaml',data/'subset_manifest.json',*sorted((data/'db').glob('*.parquet')),*sorted((data/'tasks').rglob('*'))]:
            if file.is_file():copy(file,PACKAGE/file.relative_to(ROOT))
        for label in LABELS:
            folder,source=build(fold,label);text=source.read_text(encoding='utf-8')
            oldroot="ROOT = Path('/mnt/c/Users/Мишаня/ml/projs/tbank/Features')"
            assert oldroot in text;text=text.replace(oldroot,"import os\nROOT = Path(os.environ['RECFORMER_BUNDLE_ROOT'])")
            text=text.replace(f'DATA = Path({str(data)!r})',f"DATA = ROOT/'data/hm-cv-medium-v2/fold_{fold}'")
            text=text.replace(f'OUT=Path({str(folder)!r})',f"OUT=Path(os.environ['RECFORMER_KAGGLE_OUT'])/'fold_{fold}/recformer_grid/{label}'")
            text=text.replace(f"RUN='hm_medium_recformer_tune_f{fold}_{label}_seed42_v1'",f"RUN='hm_medium_recformer_kaggle_f{fold}_{label}_seed42_v1'")
            needle='    args=parser.parse_args()';assert needle in text
            text=text.replace(needle,needle+"\n    assert args.train_only and not args.evaluate_only and not args.verify_only and not args.probe, 'Kaggle runner is train-only'")
            assert '/mnt/c/' not in text
            freeze_text(PACKAGE/f'runtime/fold_{fold}/recformer_{label}.py',text)
    for folder in ['Recformer/upstream/recformer','RelBenchGNN/upstream/relbench']:
        for file in (ROOT/folder).rglob('*.py'):copy(file,PACKAGE/file.relative_to(ROOT))
    for folder in ['Recformer/upstream','RelBenchGNN/upstream']:
        for name in ['LICENSE','LICENSE.txt']:
            if (ROOT/folder/name).exists():copy(ROOT/folder/name,PACKAGE/folder/name)
    copy(ROOT/'RelBenchGNN/tracking.py',PACKAGE/'RelBenchGNN/tracking.py')
    for file in (ROOT/'data/models/recformer').iterdir():
        if file.is_file():copy(file,PACKAGE/file.relative_to(ROOT))
    copy(ROOT/'CVFollowup/kaggle_runtime.py',PACKAGE/'kaggle_runtime.py')
    names=['transformers','tokenizers','numpy','pandas','pyarrow','duckdb','scikit-learn','PyYAML','huggingface-hub','tqdm']
    requirements=[f'{n}=={importlib.metadata.version(n)}' for n in names]
    write(PACKAGE/'requirements.json',requirements)
    manifest={'protocol':'hm_medium_recformer_kaggle_inputs_v1',
        'settings':{'lr3e6_w100':{'peak_lr':3e-6,'warmup':100},'lr1e5_w300':{'peak_lr':1e-5,'warmup':300}},
        'folds':{str(f):{'subset_sha256':sha(DATA/f'fold_{f}/subset_manifest.json'),
            'train_rows':len(pd.read_parquet(DATA/f'fold_{f}/tasks/user-item-purchase/train.parquet')),
            'val_rows':len(pd.read_parquet(DATA/f'fold_{f}/tasks/user-item-purchase/val.parquet'))} for f in range(3)},
        'files':{str(p.relative_to(PACKAGE)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name!='input_manifest.json' and '__pycache__' not in p.parts}}
    write(PACKAGE/'input_manifest.json',manifest)
    archive=KAGGLE/'recformer_medium_cv_inputs_v1.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED) as z:
        for name in [*manifest['files'],'input_manifest.json']:z.write(PACKAGE/name,name)
    archive,digest=refresh()
    record('recformer_kaggle_prepared','Prepared two Kaggle train-only notebooks and shared immutable data/weights bundle for predeclared LR/warmup settings; cross-hardware caveat retained.',
        'hm_medium_recformer_kaggle_split_v1',status='prepared_pending_checks',artifacts=str(KAGGLE.relative_to(ROOT)))
    print('BUNDLE',archive,'BYTES',archive.stat().st_size,'SHA256',digest,flush=True)

if __name__=='__main__':
    if '--notebooks-only' in sys.argv:refresh()
    else:main()
