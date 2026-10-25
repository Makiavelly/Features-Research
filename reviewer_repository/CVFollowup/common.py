"""Isolated follow-up paths; the original experiment is immutable."""
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'CVBenchmark/results/medium_v2'
DATA=ROOT/'data/hm-cv-medium-v2'
OUT=ROOT/'CVFollowup/results/v1'
REPORT=ROOT/'reports/medium_followup_v1'
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record

def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def write(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');tmp.replace(path)
def freeze_text(path,text):
    path=Path(path);compile(text,str(path),'exec');path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():assert path.read_text(encoding='utf-8')==text,f'Frozen source changed: {path}'
    else:path.write_text(text,encoding='utf-8')
    return path
