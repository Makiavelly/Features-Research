"""Measure numeric diversity of saved programs; never affects model selection."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]


def main():
    current=json.loads((ROOT/'reports/provider_python_v1/current_run.json').read_text())
    source=Path(current['directory'])
    assert current['status']=='finished', 'Diagnostic must not change ongoing selection'
    sys.path.insert(0,str(source/'runtime_sources'))
    from python_features import FeatureEngine
    data=ROOT/'data/kaggle_hm_small_sql_compare_v1'
    pairs=pd.read_parquet(data/'train_pairs.parquet')
    state=json.loads((source/'gpt61sol_python/search_state.json').read_text())
    out=ROOT/'reports/gpt61sol_python_v1'
    engine=FeatureEngine(out/'diversity_scratch',data)
    rows=[]
    try:
        for trial in state['trials']:
            if trial['status']!='valid':continue
            folder=source/'gpt61sol_python/candidates'/f"candidate_{trial['call']:03d}"
            program=json.loads((folder/'program.json').read_text())
            parts=[]
            for cutoff,group in pairs.groupby('timestamp',sort=True):
                engine.prepare(cutoff,group.customer_id.values,program)
                parts.append(engine.matrix(group))
            values=np.concatenate(parts)
            assert len(values)==72813
            ordered=hashlib.sha256(values.shape[1].to_bytes(4,'little')+values.tobytes()).hexdigest()
            columns=[hashlib.sha256(np.ascontiguousarray(values[:,i]).tobytes()).hexdigest() for i in range(values.shape[1])]
            unordered=hashlib.sha256(''.join(sorted(columns)).encode()).hexdigest()
            row={'call':trial['call'],'columns':values.shape[1],'ordered_float32_sha256':ordered,
                 'column_multiset_sha256':unordered}
            rows.append(row)
            print('Numeric training-matrix audit:',trial['call'],flush=True)
    finally:engine.close()
    groups={}
    for mode in ['ordered_float32_sha256','column_multiset_sha256']:
        matching=defaultdict(list)
        for row in rows:matching[row[mode]].append(row['call'])
        groups[mode]={'distinct':len(matching),'duplicate_groups':[v for v in matching.values() if len(v)>1]}
    result={'status':'passed','rows':rows,'groups':groups,'api_calls':0,'training_runs':0,
            'scope':'Float32 training matrices over all8cutoffs after host missing handling; semantic equality outside this train data is not established. Diagnostic only, no re-selection.'}
    (out/'feature_diversity.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(groups,indent=2))


if __name__=='__main__':main()
