"""Local CPU checks; none of these results are Llama feature-search results."""
import ast
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import contextlib
import io
import numpy as np
import pandas as pd
from worker import Data,compile_program,check_program,map_at_12,rank,RAW
from runtime import locate_bundle,source_from_response,source_key,evaluate,search

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
DATA=ROOT/'data/kaggle_hm_llmfe_fulltrain_v2'


class NotebookTests(unittest.TestCase):
    def test_search_backend_and_cache_isolation(self):
        notebook=json.loads((HERE/'llmfe_llama31_hm_kaggle_t4.ipynb').read_text())
        config=None
        for cell in notebook['cells']:
            if cell['cell_type']!='code':
                continue
            for node in ast.parse(''.join(cell['source'])).body:
                if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CONFIG' for t in node.targets):
                    config={k.value:v for k,v in zip(node.value.keys,node.value.values)}
        self.assertEqual(ast.literal_eval(config['search_backend']),'lightgbm')
        self.assertIn('preflight_fulltrain_v5',ast.literal_eval(config['protocol']))
        self.assertEqual(ast.literal_eval(config['target_successful_distinct']),20)
        self.assertEqual(ast.literal_eval(config['max_llm_calls']),300)
        self.assertEqual(ast.literal_eval(config['max_repairs_per_proposal']),3)
        import sys
        self.assertNotIn('xgboost',sys.modules)
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            (folder/'search_metrics.json').write_text(json.dumps({'backend':'xgboost'}))
            with self.assertRaisesRegex(RuntimeError,'another evaluator'):
                evaluate(DATA,folder,'search',{'search_backend':'lightgbm'})

    def test_budget_stops_at_twenty_successful_sets(self):
        calls=[]
        def generator(prompt,seed):
            calls.append(seed)
            return {'text':f'def modify_features(X, history):\n    return pd.DataFrame({{"f_fixture": X.raw_u_age * {len(calls)}}}, index=X.index)\n'}
        settings={'target_successful_distinct':20,'max_llm_calls':300,'max_repairs_per_proposal':3}
        with tempfile.TemporaryDirectory() as tmp, patch('runtime.prompt',return_value='test prompt'), patch('runtime.progress'), patch('runtime.evaluate',return_value={'map':.01}), contextlib.redirect_stdout(io.StringIO()):
            selected=search(DATA,Path(tmp),settings,generator)
        self.assertEqual(len(calls),20)
        self.assertTrue(selected['search_budget']['target_met'])
        self.assertEqual(selected['search_budget']['evaluated_distinct'],20)

    def test_failed_preflight_never_counts_or_trains_candidate(self):
        stages=[]
        def evaluator(data,directory,stage,config):
            stages.append((Path(directory).name,stage))
            if stage=='preflight':
                raise ValueError('fixture: missing column before training')
            return {'map':.01}
        code='def modify_features(X, history):\n    return pd.DataFrame({"f_fixture": X.raw_u_age}, index=X.index)\n'
        settings={'target_successful_distinct':1,'max_llm_calls':4,'max_repairs_per_proposal':3}
        with tempfile.TemporaryDirectory() as tmp, patch('runtime.prompt',return_value='test prompt'), patch('runtime.progress'), patch('runtime.evaluate',side_effect=evaluator), contextlib.redirect_stdout(io.StringIO()):
            selected=search(DATA,Path(tmp),settings,lambda *_:{'text':code})
        self.assertEqual(selected['search_budget']['evaluated_distinct'],0)
        self.assertEqual(sum(stage=='preflight' for _,stage in stages),4)
        self.assertFalse(any(name.startswith('candidate_') and stage=='search' for name,stage in stages))

    def test_feature_error_reports_real_program_line_and_schema(self):
        from worker import feature_error
        function=compile_program('def modify_features(X, history):\n    return history.groupby("missing_column").size()\n')
        X=pd.DataFrame({'customer_id':[1],'article_id':[2]})
        history=pd.DataFrame({'customer_id':[1],'article_id':[2],'price':[.1]})
        try:
            function(X,history)
        except KeyError as error:
            message=feature_error(error,function,X,history)
        self.assertIn('missing_column',message)
        self.assertIn('Your code near line 2',message)
        self.assertIn('Available INPUT history columns',message)

    def test_300_request_ceiling_and_three_repairs(self):
        calls=[]
        def invalid(prompt,seed):
            calls.append(seed)
            return {'text':'invalid Python'}
        settings={'target_successful_distinct':20,'max_llm_calls':300,'max_repairs_per_proposal':3}
        with tempfile.TemporaryDirectory() as tmp, patch('runtime.prompt',return_value='test prompt'), patch('runtime.progress'), patch('runtime.evaluate',return_value={'map':.01}), contextlib.redirect_stdout(io.StringIO()):
            selected=search(DATA,Path(tmp),settings,invalid)
            trials=[json.loads(p.read_text()) for p in sorted(Path(tmp).glob('candidates/*/trial.json'))]
            # Selection already frozen: a resume cannot issue additional calls.
            search(DATA,Path(tmp),settings,lambda *_:self.fail('Unexpected resume generation'))
        self.assertEqual(len(calls),300)
        self.assertEqual([t['repair'] for t in trials],[0,1,2,3]*75)
        self.assertFalse(selected['search_budget']['target_met'])
        self.assertTrue(selected['search_budget']['budget_exhausted'])
        self.assertEqual(selected['search_budget']['evaluated_distinct'],0)
        self.assertEqual(selected['search_budget']['repair_calls'],225)
        self.assertEqual(selected['search_budget']['new_proposals'],75)
        for start in range(0,300,4):
            self.assertEqual(len({t['island'] for t in trials[start:start+4]}),1)
            self.assertEqual([t['parent_call'] for t in trials[start:start+4]],[None,start+1,start+2,start+3])

    def test_interrupted_request_consumes_budget_on_resume(self):
        settings={'target_successful_distinct':1,'max_llm_calls':300,'max_repairs_per_proposal':3}
        with tempfile.TemporaryDirectory() as tmp, patch('runtime.prompt',return_value='test prompt'), patch('runtime.progress'), patch('runtime.evaluate',return_value={'map':.01}), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(KeyboardInterrupt):
                search(DATA,Path(tmp),settings,lambda *_:(_ for _ in ()).throw(KeyboardInterrupt()))
            calls=[]
            def corrected(prompt,seed):
                calls.append(seed)
                return {'text':'def modify_features(X, history):\n    return pd.DataFrame({"f_fixture": X.raw_u_age}, index=X.index)\n'}
            selected=search(DATA,Path(tmp),settings,corrected)
            first=json.loads((Path(tmp)/'candidates/candidate_001/trial.json').read_text())
        self.assertEqual(len(calls),1)
        self.assertIn('interrupted',first['error'])
        self.assertEqual(selected['search_budget']['llm_calls'],2)
        self.assertEqual(selected['search_budget']['repair_calls'],1)

    def test_model_source_authentication(self):
        notebook=json.loads((HERE/'llmfe_llama31_hm_kaggle_t4.ipynb').read_text())
        nodes=[]
        for cell in notebook['cells']:
            if cell['cell_type']!='code':
                continue
            for node in ast.parse(''.join(cell['source'])).body:
                if isinstance(node,ast.FunctionDef) and node.name=='resolve_auth':
                    nodes.append(node)
                elif isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MODEL_SOURCES' for t in node.targets):
                    nodes.append(node)
        scope={}
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'<notebook-auth>','exec'),scope)
        resolve=scope['resolve_auth']
        def forbidden():
            raise AssertionError('Public source must not read Kaggle Secrets')
        self.assertIs(resolve('unsloth',{'HF_TOKEN':'invalid-existing-token'},forbidden),False)
        self.assertIs(resolve('unsloth',{},forbidden),False)
        self.assertEqual(resolve('hf',{'HF_TOKEN':'test-env'},forbidden),'test-env')
        self.assertEqual(resolve('hf',{},lambda:'test-secret'),'test-secret')
        with self.assertRaises(RuntimeError):
            resolve('hf',{},lambda:None)
        with self.assertRaises(ValueError):
            resolve('typo',{},forbidden)
        self.assertNotEqual(scope['MODEL_SOURCES']['hf']['repo_id'],scope['MODEL_SOURCES']['unsloth']['repo_id'])

    def test_notebook_schema_and_python_cells(self):
        import nbformat
        notebook=nbformat.read(HERE/'llmfe_llama31_hm_kaggle_t4.ipynb',as_version=4)
        nbformat.validate(notebook)
        for cell in notebook.cells:
            if cell.cell_type=='code':
                ast.parse(cell.source)
                self.assertEqual(cell.outputs,[])

    def test_function_restrictions(self):
        compile_program(RAW)
        bad=['import os\ndef modify_features(X, history): return X',
             'def modify_features(X, history):\n    return pd.read_parquet("targets.parquet")',
             'def modify_features(X, history):\n    return X.__class__',
             'def modify_features(X, history):\n    return open("targets.parquet")']
        for source in bad:
            with self.assertRaises(ValueError):
                check_program(source)

    def test_source_extract_and_dedup(self):
        self.assertEqual(source_from_response('```python\n'+RAW+'```'),RAW)
        self.assertEqual(source_key(RAW),source_key('# same function\n'+RAW))

    def test_exact_ranking_and_ap(self):
        ids=np.arange(24)
        pairs=pd.DataFrame({'customer_id':np.repeat([5,8],12),'article_id':ids})
        targets=pd.DataFrame({'customer_id':[5,8],'article_id':[[0,1],[23]]})
        predictions=rank(np.zeros(24),pairs,targets)
        np.testing.assert_array_equal(predictions,[np.arange(12),np.arange(12,24)])
        mean,ap=map_at_12(predictions,targets.article_id)
        np.testing.assert_allclose(ap,[1,1/12])
        self.assertAlmostEqual(mean,(1+1/12)/2)

    def test_bundle_and_original_training_identity(self):
        import hashlib
        expected=hashlib.sha256((DATA/'manifest.json').read_bytes()).hexdigest()
        root,manifest=locate_bundle(DATA,ROOT/'reports/kaggle_llmfe_validation',expected)
        self.assertEqual(manifest['train_pairs'],803377)
        self.assertEqual(manifest['files']['train_pairs.parquet']['sha256'],manifest['train_source_sha256'])
        indices=[set(manifest['splits'][s]['original_row_indices']) for s in ['search','confirm','val']]
        self.assertFalse(indices[0]&indices[1] or indices[0]&indices[2] or indices[1]&indices[2])

    def test_future_and_label_exclusion(self):
        data=Data(DATA)
        pairs=pd.read_parquet(DATA/'train_pairs.parquet').head(32)
        cutoff=pairs.timestamp.iloc[0]
        original_X,original_history=data.inputs(pairs,cutoff)
        for banned in ['label','timestamp','t_dat','target']:
            self.assertNotIn(banned,original_X)
            self.assertNotIn(banned,original_history)
        changed=pairs.copy();changed['label']=1-changed.label
        extra=data.tx.head(100).copy();extra['t_dat']=pd.Timestamp(cutoff)+pd.Timedelta(days=1000)
        data.tx=pd.concat([data.tx,extra],ignore_index=True)
        X,history=data.inputs(changed,cutoff)
        pd.testing.assert_frame_equal(X,original_X)
        pd.testing.assert_frame_equal(history,original_history)
        self.assertTrue((history.days_ago>=0).all())


if __name__=='__main__':
    unittest.main()
