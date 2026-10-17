"""Boolean-operator regression and notebook/source check; no LLM/training."""
import ast
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from full_sql import parse,FeatureEngine


def main():
    notebook=json.loads((HERE.parent/'hm_small_qwen7b_full_sql_v2_kaggle_t4.ipynb').read_text())
    import nbformat
    nbformat.validate(nbformat.from_dict(notebook))
    for cell in notebook['cells']:
        if cell['cell_type']=='code':ast.parse(''.join(cell['source']))
    embedded=next(ast.literal_eval(n.value) for c in notebook['cells'] if c['cell_type']=='code'
                  for n in ast.parse(''.join(c['source'])).body if isinstance(n,ast.Assign)
                  and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='MODULES')
    for name,source in embedded.items():assert source==(HERE/name).read_text()
    for name in ['base_features.py','features.py','worker.py','prompting.py','runtime.py']:
        assert embedded[name]==(HERE.parent/'full_sql_small'/name).read_text()
    predicates=['days_ago<=7 AND sales_channel_id=1','days_ago<=7 OR sales_channel_id=1',
                'NOT (days_ago>7)','days_ago BETWEEN 1 AND 7','sales_channel_id IN (1,2)','price IS NOT NULL']
    program=parse('SELECT customer_id,'+','.join('count(*) FILTER(WHERE '+p+') AS f_test_'+str(i) for i,p in enumerate(predicates))+
                  ' FROM history GROUP BY customer_id')
    data=ROOT/'data/kaggle_hm_small_sql_compare_v1'
    pairs=pd.read_parquet(data/'train_pairs.parquet')
    cutoff=pairs.timestamp.min()
    sample=pairs[pairs.timestamp==cutoff].head(128)
    engine=FeatureEngine(ROOT/'reports/kaggle_llmfe_validation/full_sql_small_v2/engine_scratch',data)
    try:
        engine.prepare(cutoff,sample.customer_id.values,program)
        actual=engine.frame(sample)
        tx=pd.read_parquet(data/'transactions.parquet')
        past=tx[tx.t_dat<=cutoff].copy()
        days=(cutoff-past.t_dat).dt.days
        flags=[(days<=7)&(past.sales_channel_id==1),(days<=7)|(past.sales_channel_id==1),
               ~(days>7),days.between(1,7),past.sales_channel_id.isin([1,2]),past.price.notna()]
        for i,flag in enumerate(flags):
            expected=flag.astype(int).groupby(past.customer_id).sum()
            np.testing.assert_allclose(actual['f_test_'+str(i)],sample.customer_id.map(expected),equal_nan=True)
    finally:engine.close()
    out=ROOT/'reports/kaggle_llmfe_validation/full_sql_small_v2/verification.json'
    out.write_text(json.dumps({'status':'passed','scope':'Boolean numeric regression, AST/notebook/source checks only; no Qwen run',
                               'AND_OR_NOT_BETWEEN_IN_IS_match_pandas':True,'other_modules_byte_identical_v1':True},indent=2))
    print(out.read_text())


if __name__=='__main__':main()
