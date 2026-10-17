"""Shared paths, paired metric implementation and source provenance."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/hm-cv-medium-v2'
OUT=ROOT/'CVBenchmark/results/medium_v2'
REPORT=ROOT/'reports/medium_cv_v2'
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record

def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');tmp.replace(p)
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def paths(fold):return DATA/f'fold_{fold}',OUT/f'fold_{fold}'
def metrics(pred,target):
    pred=np.asarray(pred)
    assert pred.shape==(len(target),12) and ((pred>=0)&(pred<10000)).all()
    assert all(len(np.unique(p))==12 for p in pred)
    hits=np.asarray([np.isin(p,np.unique(t)) for p,t in zip(pred,target.article_id)])
    sizes=np.asarray([len(np.unique(t)) for t in target.article_id]);assert (sizes>0).all()
    ap=(hits*np.cumsum(hits,axis=1)/np.arange(1,13)).sum(1)/np.minimum(12,sizes)
    available=np.asarray([np.sum(np.unique(t)<10000) for t in target.article_id])
    eligible=available>0
    conditional=(hits*np.cumsum(hits,axis=1)/np.arange(1,13)).sum(1)[eligible]/np.minimum(12,available[eligible])
    return {'map':float(ap.mean()),'recall12':float((hits.sum(1)/sizes).mean()),'hit12':float(hits.any(1).mean()),'users':len(target),
            'conditional_catalog_map':float(conditional.mean()) if len(conditional) else None,
            'conditional_users':int(eligible.sum()),'zero_retrievable_users':int((~eligible).sum())},ap
def save_predictions(folder,split,pred,target):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    result,ap=metrics(pred,target)
    np.save(folder/f'{split}_predictions.npy',pred);np.save(folder/f'{split}_ap.npy',ap)
    np.save(folder/f'{split}_users.npy',target.customer_id.to_numpy())
    write(folder/f'{split}_metrics.json',result)
    return result
def frozen_source(source,destination,replacements=()):
    text=Path(source).read_text(encoding='utf-8')
    for old,new in replacements:
        assert old in text,old[:120]
        text=text.replace(old,new)
    compile(text,str(destination),'exec')
    destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
    if destination.exists():assert destination.read_text(encoding='utf-8')==text,'Changed source under existing run'
    else:destination.write_text(text,encoding='utf-8')
    return destination
