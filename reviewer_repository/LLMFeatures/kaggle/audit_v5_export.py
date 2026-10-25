"""Audit v5 two-input Python experiment, including silent pandas alignment failures."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import zipfile
import numpy as np
import pandas as pd
import worker
from runtime import evaluate,write_json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ARCHIVE=ROOT/'hm_llmfe_llama31_8b_lightgbm_preflight_fulltrain_v5_949add5c4fef_results.zip'
OUT=ROOT/'reports/hm_llmfe_llama_v5_audit'
OUT.mkdir(parents=True,exist_ok=True)
NOTEBOOK=ROOT/'features-llama-plus-lightgbm-v3.ipynb'
with zipfile.ZipFile(ARCHIVE) as z:
    config=json.loads(z.read('run_config.json'));trials=json.loads(z.read('trials.json'))
    selected=json.loads(z.read('selected.json'));report=json.loads(z.read('report.json'))
    assert hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()[:12]=='949add5c4fef'
    modules=None
    notebook=json.loads(NOTEBOOK.read_text(encoding='utf-8'))
    for cell in notebook['cells']:
        if cell['cell_type']!='code':continue
        for node in ast.parse(''.join(cell['source'])).body:
            if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MODULES' for t in node.targets):modules=ast.literal_eval(node.value)
    assert modules is not None
    hashes={n:hashlib.sha256(s.encode()).hexdigest()==config['runtime_sha256'][n] for n,s in modules.items()}
    assert all(hashes.values())
    assert all(hashlib.sha256((HERE/n).read_bytes()).hexdigest()==config['runtime_sha256'][n] for n in modules)
    for name in z.namelist():
        destination=OUT/'export'/name
        if not destination.resolve().is_relative_to((OUT/'export').resolve()):raise ValueError('Unsafe zip member')
        if name.endswith('/'):continue
        destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(z.read(name))
    valid=[t for t in trials if t['status']=='valid']
    for t in valid:
        directory=OUT/'export/candidates'/f"candidate_{t['sample']:03d}"
        m=json.loads((directory/'search_metrics.json').read_text());schema=json.loads((directory/'schema.json').read_text())
        assert schema['train_pairs']==803377 and m['map']==t['score']
        assert hashlib.sha256((directory/'model.txt').read_bytes()).hexdigest()==m['model_sha256']
        assert hashlib.sha256((directory/'program.py').read_bytes()).hexdigest()==m['program_sha256']
    source=ROOT/'data/kaggle_hm_llmfe_fulltrain_v2'
    assert hashlib.sha256((source/'manifest.json').read_bytes()).hexdigest()==config['bundle_manifest_sha256']
    chosen=Path(selected['directory']).name
    replays=[]
    for label,relative in [('Raw LightGBM','raw_control'),('LLM-FE LightGBM','candidates/'+chosen)]:
        directory=OUT/'export'/relative
        for split in ['val','test']:
            truth=pd.read_parquet(source/f'{split}_targets.parquet')
            m,ap=worker.map_at_12(np.load(directory/f'{split}_predictions.npy'),truth.article_id)
            assert m==report['metrics'][label][split]['map']
            assert np.array_equal(ap,np.load(directory/f'{split}_user_ap.npy'))
            replay=OUT/'frozen_replay'/relative;replay.mkdir(parents=True,exist_ok=True)
            for name in ['program.py','model.txt','schema.json',f'{split}_predictions.npy',f'{split}_user_ap.npy']:
                (replay/name).write_bytes((directory/name).read_bytes())
            result=evaluate(source,replay,'replay_'+split,config)
            assert result['passed'] and result['map']==m
            replays.append({'model':label,'split':split,'map':m,'exact_replay':True})
            print('Frozen replay:',label,split,m,flush=True)
    # Persist only a small safe request; the bounded subprocess probes all20 observed programs.
    print('Frozen models checked; semantic probes next.',flush=True)
    write_json(OUT/'preaudit.json',{'config_fingerprint_matches':True,'notebook_runtime_hashes_match':hashes,
        'candidate_models_checked':len(valid),'frozen_replays':replays,'chosen':chosen,
        'budget':json.loads(z.read('search_state.json')),
        'failure_stages':dict(Counter(t.get('failure_stage') for t in trials if t['status']=='rejected'))})
