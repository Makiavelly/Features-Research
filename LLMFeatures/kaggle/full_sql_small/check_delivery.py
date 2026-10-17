"""Meaningful SQL/host integration checks; scripted callbacks, no local LLM."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
import runtime
from full_sql import parse,program_key,FeatureEngine,validate_program,SQLProgramError
from worker import write

A='''WITH counts AS (
SELECT customer_id,count(*) AS total_count,count(*) FILTER(WHERE days_ago<=7) AS recent_count,
min(days_ago) AS recency FROM history GROUP BY customer_id)
SELECT customer_id,total_count AS f_count,recent_count AS f_recent,recency AS f_recency,
recent_count/nullif(total_count,0) AS f_share FROM counts;
SELECT article_id,count(*) FILTER(WHERE days_ago<=7) AS f_item_recent,
quantile_cont(price,0.5) AS f_item_median FROM history GROUP BY article_id;'''
B='''SELECT customer_id,article_id,count(*) AS f_pair_count FROM history GROUP BY customer_id,article_id;
SELECT customer_id,product_type_no,count(*) AS f_type_count FROM history GROUP BY customer_id,product_type_no;'''
WINDOW='''WITH ranked AS (SELECT customer_id,price,
ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY days_ago,price,product_code) AS rn FROM history)
SELECT customer_id,price AS f_last_price FROM ranked WHERE rn=1;'''


def main():
    tick=time.perf_counter()
    notebook=json.loads((HERE.parent/'hm_small_qwen7b_full_sql_kaggle_t4.ipynb').read_text())
    for cell in notebook['cells']:
        if cell['cell_type']=='code':ast.parse(''.join(cell['source']))
    modules=next(ast.literal_eval(n.value) for c in notebook['cells'] if c['cell_type']=='code'
                 for n in ast.parse(''.join(c['source'])).body if isinstance(n,ast.Assign)
                 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='MODULES')
    for name,source in modules.items():assert (HERE/name).read_text()==source,name
    import nbformat
    nbformat.validate(nbformat.from_dict(notebook))
    assert modules['worker.py']==(HERE.parent/'small_compare/worker.py').read_text()
    assert modules['base_features.py']==(HERE.parent/'small_compare/features.py').read_text()
    programs={name:parse(sql) for name,sql in [('a',A),('b',B),('window',WINDOW)]}
    assert program_key(programs['a'])==program_key(parse(A.replace('f_count','f_renamed_count').replace('f_recent','f_renamed_recent')))
    assert program_key(programs['a'])==program_key(parse('-- comment\n'+A))
    rejected=[]
    for name,sql in {
        'DDL':'CREATE TABLE x AS SELECT * FROM history;',
        'future_table':'SELECT customer_id,count(*) AS f_count FROM tx GROUP BY customer_id;',
        'external_file':"SELECT customer_id,count(*) AS f_count FROM read_parquet('/tmp/data') GROUP BY customer_id;",
        'unknown_column':'SELECT customer_id,avg(gender) AS f_gender FROM history GROUP BY customer_id;',
        'ID_predictor':'SELECT customer_id,customer_id AS f_id FROM history;',
        'transformed_key':'SELECT customer_id+1 AS customer_id,count(*) AS f_count FROM history GROUP BY customer_id;',
        'bad_grouping':'SELECT customer_id,sales_channel_id,count(*) AS f_count FROM history GROUP BY customer_id,sales_channel_id;',
        'string_output':"SELECT customer_id,'young' AS f_age FROM history GROUP BY customer_id;",
        'duplicate_feature_names':'SELECT customer_id,count(*) AS f_count FROM history GROUP BY customer_id; SELECT article_id,count(*) AS f_count FROM history GROUP BY article_id;',
        'random_sampling':'SELECT customer_id,count(*) AS f_count FROM history TABLESAMPLE 10 PERCENT GROUP BY customer_id;',
    }.items():
        try:parse(sql)
        except Exception:rejected.append(name)
        else:raise AssertionError('Accepted invalid SQL: '+name)
    data=ROOT/'data/kaggle_hm_small_sql_compare_v1'
    manifest=json.loads((data/'manifest.json').read_text())
    for name,digest in manifest['files'].items():assert runtime.sha(data/name)==digest
    pairs=pd.read_parquet(data/'train_pairs.parquet')
    assert len(pairs)==72813
    out=ROOT/'reports/kaggle_llmfe_validation/full_sql_small_v1/cpu_smoke'
    out.mkdir(parents=True,exist_ok=True)
    engine=FeatureEngine(out/'engine_scratch',data)
    cutoff=pairs.timestamp.min()
    sample=pairs[pairs.timestamp==cutoff].head(128).reset_index(drop=True)
    engine.prepare(cutoff,sample.customer_id.values,programs['a'])
    actual=engine.frame(sample)
    tx=pd.read_parquet(data/'transactions.parquet')
    past=tx[tx.t_dat<=cutoff].copy()
    past['days_ago']=(cutoff-past.t_dat).dt.days
    recent=past[past.days_ago<=7].groupby('article_id').size().reindex(past.article_id.unique(),fill_value=0)
    np.testing.assert_allclose(actual.f_item_recent,sample.article_id.map(recent),equal_nan=True)
    np.testing.assert_allclose(actual.f_count,sample.customer_id.map(past.groupby('customer_id').size()),equal_nan=True)
    np.testing.assert_allclose(actual.f_recency,sample.customer_id.map(past.groupby('customer_id').days_ago.min()),equal_nan=True)
    np.testing.assert_allclose(actual.f_item_median,sample.article_id.map(past.groupby('article_id').price.median()),equal_nan=True)
    # Independent database contains no future transaction rows or targets.
    assert engine.query_con.execute('SELECT count(*) FROM history').fetchone()[0]==len(past)<len(tx)
    try:engine.query_con.execute('SELECT * FROM tx')
    except Exception:pass
    else:raise AssertionError('LLM database exposed tx')
    engine.prepare(cutoff,sample.customer_id.values,programs['window'])
    window_values=engine.frame(sample)
    last=past.sort_values(['days_ago','price','article_id']).groupby('customer_id').first().price
    np.testing.assert_allclose(window_values.f_last_price,sample.customer_id.map(last),equal_nan=True)
    try:engine.prepare(cutoff,sample.customer_id.values,parse('SELECT customer_id,price AS f_price FROM history'))
    except ValueError as error:assert 'duplicate key rows' in str(error)
    else:raise AssertionError('Duplicate result keys accepted')
    engine.close()
    config=dict(protocol='full_sql_cpu_smoke',arms=['qwen_full_sql'],arm='qwen_full_sql',
                train_pairs=72813,train_pair_sha256=manifest['train_pair_sha256'],lightgbm_rounds=150,
                cpu_threads=4,scoring_user_batch=16,evaluation_timeout_seconds=1800,
                target_successful_distinct=2,max_llm_calls=8,max_repairs_per_proposal=3,
                training_examples='[]',validation_only_fake_callbacks=True,test_previously_inspected=True)
    config_path=out/'run_config.json'
    write(config_path,config)
    raw=out/'raw_control'
    raw.mkdir(exist_ok=True)
    write(raw/'program.json',{'queries':[]})
    runtime.evaluate(data,raw,'search',config_path)
    prompts=[]
    bad='SELECT customer_id,avg(gender) AS f_gender FROM history GROUP BY customer_id;'
    def fake(prompt,seed):
        prompts.append(prompt)
        call=len(prompts)
        assert seed==42+call-1
        return dict(text=bad if call==1 else (B if call>=5 else A),seed=seed,
                    prompt_tokens=1,generated_tokens=1,seconds=0.,truncated=False)
    selected=runtime.search(data,out/'qwen_full_sql',fake,config_path)
    assert selected['successful_distinct']==2 and selected['llm_calls']==5
    if prompts:
        assert 'REPAIR:' in prompts[1] and 'query1' in prompts[1]
        assert 'duplicate of call2' in prompts[3]
    state=json.loads((out/'qwen_full_sql/search_state.json').read_text())['trials']
    assert [t['status'] for t in state]==['rejected','valid','duplicate','duplicate','valid']
    assert state[4]['repair']==0 and state[4]['island']==2
    assert (out/'qwen_full_sql/candidates/candidate_002/program.sql').exists()
    runtime.search(data,out/'qwen_full_sql',lambda *_:(_ for _ in ()).throw(AssertionError('Repeated generation')),config_path)
    frame=runtime.finish(data,out,config_path)
    assert len(frame)==10
    # The raw tree must remain byte-identical to the old exact-stack control.
    oldraw=ROOT/'reports/hm_small_llms_v1/exports/qwen_llama/raw_control'
    assert runtime.sha(raw/'model.txt')==runtime.sha(oldraw/'model.txt')
    for split in ['val','test']:
        assert runtime.sha(raw/f'{split}_predictions.npy')==runtime.sha(oldraw/f'{split}_predictions.npy')
    report=dict(status='passed',scope='CPU integration with scripted SQL callbacks, not a Qwen experiment',
                train_pairs=72813,worker_unchanged=True,raw_control_byte_identical=True,
                rejected_programs=rejected,checks=['notebook schema/embedded sources','input hashes',
                'CTE/quantile/window SQL','pandas ID/count/recency/median checks','physical future exclusion',
                'duplicate result keys rejected','repair/duplicate/island/unchanged routing','resume',
                'full5000 scoring','frozen replay','references/plots/ZIP'],seconds=time.perf_counter()-tick)
    write(out.parent/'verification.json',report)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
