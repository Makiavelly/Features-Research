"""Interface and integration checks. Synthetic proposals are never Llama quality results."""
import ast
import json
from pathlib import Path
import shutil
import unittest
from unittest.mock import patch
import contextlib
import io
import numpy as np
import pandas as pd
from flat_features import prepare,Data,compile_program,check_program,matrix,SEED,RAW,RAW_ONLY,BASE_SPEC
from runtime import search,final,evaluate,write_json,source_key

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'reports/kaggle_llmfe_validation/flat_v1'
SOURCE=ROOT/'data/kaggle_hm_llmfe_fulltrain_v2'
FIXTURE='''def modify_features(X):
    F = X.copy()
    F['f_user_type_share'] = X['h_user_type_count_30'].fillna(0) / (X['h_user_count_30'].fillna(0) + 1)
    return F
'''


class Tests(unittest.TestCase):
    def test_base_spec(self):
        self.assertEqual(len(BASE_SPEC['aggregates']),15)
        self.assertEqual(len(BASE_SPEC['derived']),0)
        self.assertFalse(any('label' in e['sql'] for e in BASE_SPEC['aggregates']))

    def test_rowwise_program_and_drop(self):
        self.assertIn('def modify_features',check_program(FIXTURE))
        check_program('def modify_features(df_input):\n    return df_input.drop(columns=["raw_u_age"])')
        for code in ['X.groupby("raw_u_age").sum()','X.mean()','X.sample(2)','pd.read_csv("x")']:
            with self.assertRaises(ValueError):check_program('def modify_features(X):\n    return '+code)

    def test_notebook_sources_and_config(self):
        import nbformat
        notebook=nbformat.read(ROOT/'LLMFeatures/kaggle/llmfe_llama31_hm_flat_kaggle_t4.ipynb',as_version=4)
        nbformat.validate(notebook)
        configuration=None
        for cell in notebook.cells:
            if cell.cell_type!='code':continue
            for node in ast.parse(cell.source).body:
                if isinstance(node,ast.Assign):
                    if any(isinstance(t,ast.Name) and t.id=='MODULES' for t in node.targets):
                        for name,source in ast.literal_eval(node.value).items():self.assertEqual(source,(Path(__file__).parent/name).read_text())
                    if any(isinstance(t,ast.Name) and t.id=='CONFIG' for t in node.targets):
                        configuration={k.value:v for k,v in zip(node.value.keys,node.value.values)}
        for key,expected in [('train_pairs',803377),('target_successful_distinct',20),('max_llm_calls',300),('max_repairs_per_proposal',3),('abort_if_no_success_after_calls',6)]:
            self.assertEqual(ast.literal_eval(configuration[key]),expected)
        self.assertIn('duckdb==1.4.1',''.join(c.source for c in notebook.cells))

    def test_pilot_gate(self):
        import tempfile
        settings={'target_successful_distinct':20,'max_llm_calls':300,'max_repairs_per_proposal':3,'abort_if_no_success_after_calls':6}
        with tempfile.TemporaryDirectory() as tmp,patch('runtime.prompt',return_value='fixture'),patch('runtime.progress'),patch('runtime.evaluate',return_value={'map':.01}),contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError,'Pilot gate'):
                search('unused',tmp,settings,lambda *_:{'text':'{','truncated':False})
            trials=[json.loads(p.read_text()) for p in Path(tmp).glob('candidates/*/trial.json')]
            self.assertEqual(len(trials),6)
            self.assertTrue(all(t['status']=='rejected' for t in trials))


def integration():
    # Full data cache proves original pairs/labels order and all52 past-only snapshots are handled.
    data,manifest=prepare(SOURCE,OUT/'prepared')
    assert manifest['train_pairs']==803377 and len(manifest['base_fields'])==30
    original=pd.read_parquet(SOURCE/'train_pairs.parquet')
    tagged=pd.read_parquet(data/'train_pairs.parquet')
    pd.testing.assert_frame_equal(tagged[original.columns],original)
    dataset=Data(data)
    pairs=pd.read_parquet(data/'search_pairs.parquet').head(100)
    values,names=matrix(dataset,pairs,compile_program(FIXTURE))
    left,_=matrix(dataset,pairs.iloc[:50],compile_program(FIXTURE))
    right,_=matrix(dataset,pairs.iloc[50:],compile_program(FIXTURE))
    np.testing.assert_array_equal(values,np.concatenate([left,right]))
    changed=pairs.assign(label=999)
    alternate,_=matrix(dataset,changed,compile_program(FIXTURE))
    np.testing.assert_array_equal(values,alternate)
    # Check raw and seed on ALL803377 pairs with actual saved-model evaluation.
    configuration={'target_successful_distinct':2,'max_llm_calls':8,'max_repairs_per_proposal':3,
        'abort_if_no_success_after_calls':6,'cpu_threads':4,'search_backend':'lightgbm','train_pairs':803377,
        'evaluation_memory_gb':4,'evaluation_timeout_seconds':1800}
    bad=OUT/'batch_dependent';bad.mkdir(exist_ok=True)
    (bad/'program.py').write_text('def modify_features(X):\n    F=X.copy()\n    F["f_batch_size"]=len(X)\n    return F\n')
    try:
        evaluate(data,bad,'preflight',configuration)
        raise AssertionError('Batch-dependent feature must be rejected')
    except RuntimeError as error:
        assert 'depend on batch size' in str(error)
    for name,source in [('prepared30',RAW),('seeded32',SEED),('llm_fixture',FIXTURE),('raw15',RAW_ONLY)]:
        folder=OUT/'fulltrain'/name;folder.mkdir(parents=True,exist_ok=True)
        (folder/'program.py').write_text(source)
        preflight=evaluate(data,folder,'preflight',configuration) if source!=RAW else None
        result=evaluate(data,folder,'search',configuration)
        assert json.loads((folder/'schema.json').read_text())['train_pairs']==803377
        val=evaluate(data,folder,'val',configuration)
        replay=evaluate(data,folder,'replay_val',configuration)
        assert replay['passed'] and replay['map']==val['map']
        print('Full-pair fixture checked:',name,result['seconds'],flush=True)
    # Tiny test subset for search/repair/duplicate/confirmation/final controls and references.
    tiny=OUT/'tiny';tiny.mkdir(exist_ok=True)
    fm=dict(manifest)
    for split in ['train','search','confirm','val','test']:
        p=pd.read_parquet(data/f'{split}_pairs.parquet')
        if split=='train':p=p[p.timestamp==p.timestamp.max()].head(2000)
        else:
            truth=pd.read_parquet(data/f'{split}_targets.parquet').head(8)
            truth.to_parquet(tiny/f'{split}_targets.parquet',index=False)
            p=p[p.customer_id.isin(truth.customer_id)]
        f=pd.read_parquet(data/f'{split}_flat.parquet').iloc[p['_flat_row'].to_numpy()].reset_index(drop=True)
        p=p.copy().reset_index(drop=True);p['_flat_row']=np.arange(len(p))
        p.to_parquet(tiny/f'{split}_pairs.parquet',index=False);f.to_parquet(tiny/f'{split}_flat.parquet',index=False)
        if split in ['val','test']:
            for label in ['manual_lightgbm','gnn_lightgbm','idgnn']:
                np.save(tiny/f'{split}_{label}_reference.npy',np.load(data/f'{split}_{label}_reference.npy')[:8])
    shutil.copy2(data/'manifest.json',tiny/'manifest.json')
    write_json(tiny/'flat_manifest.json',fm)
    calls=[]
    second=FIXTURE.replace('+ 1)', '+ 2)')
    sequence=['not python',FIXTURE,FIXTURE,second]
    def fake(prompt,seed):
        calls.append(seed);return {'text':sequence[len(calls)-1],'truncated':False,'synthetic_not_llm':True}
    small={**configuration,'train_pairs':2000,'smoke':True}
    selected=search(tiny,OUT/'synthetic_run',small,fake)
    report=final(tiny,OUT/'synthetic_run',small)
    trials=json.loads((OUT/'synthetic_run/trials.json').read_text())
    assert [t['status'] for t in trials]==['rejected','valid','duplicate','valid']
    assert report['independent_full_replay'] and selected['search_budget']['target_met']
    def forbidden(*_):raise AssertionError('Resume must not generate')
    assert search(tiny,OUT/'synthetic_run',small,forbidden)==selected
    assert len(report['metrics'])>=6
    write_json(OUT/'verification.json',{'passed':True,'unit_tests':4,'fulltrain_pairs':803377,
        'same_original_pair_rows_and_labels':True,'fulltrain_control_and_fixture_replay':True,
        'synthetic_search_final':True,'real_llama_executed':False,'quality_result':False})
    print('Flat-table integration passed, not a real Llama result.')


if __name__=='__main__':
    result=unittest.main(exit=False)
    if not result.result.wasSuccessful():raise SystemExit(1)
    integration()
