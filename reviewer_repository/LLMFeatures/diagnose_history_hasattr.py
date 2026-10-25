"""Isolated capability diagnostic: allow ONLY hasattr in a separate copy.

Keeps AST/I/O restrictions intact; does not modify the live run, score a new
candidate, fit a model or call the API.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/provider_history_v1'
info=json.loads((OUT/'current_run.json').read_text())
source=Path(info['directory'])
sys.path.insert(0,str(source/'runtime_sources'))
from python_features import FeatureEngine,parse
from worker import preflight

def main():
    resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3))
    module=(source/'runtime_sources/python_features.py').read_text()
    assert "'str','sum','tuple'" in module
    modified=module.replace("'str','sum','tuple'", "'str','hasattr','sum','tuple'")
    copy=OUT/'hasattr_diagnostic_features.py'
    copy.write_text(modified,encoding='utf-8')
    spec=importlib.util.spec_from_file_location('hasattr_diagnostic_features',copy)
    diagnostic=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(diagnostic)
    data=ROOT/'data/kaggle_hm_small_sql_compare_v1'
    pairs=pd.read_parquet(data/'train_pairs.parquet')
    candidates=source/'gpt61sol_generated_only/candidates'
    code15=json.loads((candidates/'candidate_015/program.json').read_text())
    code16=json.loads((candidates/'candidate_016/program.json').read_text())
    old=FeatureEngine(OUT/'validator_diagnostic_scratch/original',data)
    enabled=diagnostic.FeatureEngine(OUT/'validator_diagnostic_scratch/hasattr_only',data)
    try:
        try:preflight(old,pairs,parse(code15['code']))
        except NameError as error:
            assert "hasattr" in str(error)
        else:raise AssertionError('Original hasattr rejection not reproduced')
        checks=preflight(enabled,pairs,diagnostic.parse(code15['code']))
        assert checks['passed']
        for cutoff,frame in pairs.groupby('timestamp',sort=True):
            enabled.prepare(cutoff,frame.customer_id.values,code15)
            old.prepare(cutoff,frame.customer_id.values,code16)
            np.testing.assert_array_equal(enabled.matrix(frame),old.matrix(frame))
            assert enabled.feature_names==old.feature_names
    finally:
        old.close()
        enabled.close()
    result={'status':'passed','call':15,'classification':'host builtin capability limitation; not invalid ordinary Python',
            'diagnostic_change':'add hasattr only to a separate restricted builtin namespace; AST/I/O restrictions preserved',
            'live_runtime_changed':False,'additional_training_calls':0,'additional_api_calls':0,
            'preflight_passes_with_hasattr':True,'identical_to_accepted_call16_all72813_train_pairs':True,
            'original_module_sha256':hashlib.sha256(module.encode()).hexdigest(),
            'diagnostic_module_sha256':hashlib.sha256(modified.encode()).hexdigest()}
    (OUT/'host_builtin_diagnostic.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':main()
