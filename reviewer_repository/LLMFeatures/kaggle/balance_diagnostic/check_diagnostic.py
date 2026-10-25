"""CPU checks and explicitly synthetic six-call integration, no actual Llama."""
import ast
import hashlib
import json
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
from worker import extract,transform
from host import initial_source,build_prompt,controls,run_diagnostic,report,write_json,pack_results

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=HERE/'upstream'
SPEC=initial_source(SOURCE)
TORQUE='''def modify_features(df_input):
    result=df_input.copy()
    result['torque_diff']=df_input['Left-Weight']*df_input['Left-Distance']-df_input['Right-Weight']*df_input['Right-Distance']
    return result
'''


class Tests(unittest.TestCase):
    def test_dataset_and_source_hashes(self):
        manifest=json.loads((HERE/'upstream_manifest.json').read_text())
        for name,entry in manifest['files'].items():
            self.assertEqual(hashlib.sha256((SOURCE/name).read_bytes()).hexdigest(),entry['sha256'])
        frame=pd.read_csv(SOURCE/'data/balance-scale.csv');self.assertEqual(frame.shape,(625,5))
        delta=frame['Left-Weight']*frame['Left-Distance']-frame['Right-Weight']*frame['Right-Distance']
        np.testing.assert_array_equal(frame.iloc[:,-1],np.where(delta==0,'balanced',np.where(delta>0,'left','right')))

    def test_authors_seed_and_continuation(self):
        X=pd.read_csv(SOURCE/'data/balance-scale.csv').iloc[:10,:-1]
        output=transform(extract(SPEC),X)
        np.testing.assert_array_equal(output.weight_difference,abs(X['Left-Weight']-X['Right-Weight']))
        continuation="df_output = df_input.copy()\ndf_output['new'] = df_input['Left-Weight'] + 1\nreturn df_output"
        self.assertIn('new',transform(extract(continuation),X))

    def test_bad_programs(self):
        for text in ['def modify_features(x):\n    return open("secret")',
                     'def modify_features(x):\n    import os\n    return x',
                     'def modify_features(x):\n    return pd.read_csv("file")']:
            with self.assertRaises(ValueError):extract(text)

    def test_prompt_and_notebook(self):
        import nbformat
        prompt=build_prompt(SOURCE)
        self.assertIn('weight_difference',prompt)
        self.assertIn('modify_features_v1',prompt)
        self.assertNotIn('[EXAMPLES]',prompt)
        self.assertNotIn('[PREFIX]',prompt)
        nb=nbformat.read(ROOT/'LLMFeatures/kaggle/llmfe_llama31_balance_scale_diagnostic_t4.ipynb',as_version=4)
        nbformat.validate(nb)
        for cell in nb.cells:
            if cell.cell_type!='code':continue
            for node in ast.parse(cell.source).body:
                if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MODULES' for t in node.targets):
                    for name,source in ast.literal_eval(node.value).items():self.assertEqual(source,(HERE/name).read_text())
                if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='INPUT_FILES' for t in node.targets):
                    manifest=json.loads((HERE/'upstream_manifest.json').read_text())
                    for name,source in ast.literal_eval(node.value).items():
                        self.assertEqual(hashlib.sha256(source.encode()).hexdigest(),manifest['files'][name]['sha256'])
        text=''.join(c.source for c in nb.cells)
        self.assertIn("'max_calls':6",text)
        self.assertIn("'bitsandbytes','xgboost-cpu'",text)
        self.assertIn('xgboost-cpu==3.0.5',text)
        self.assertIn("'uninstall','-y','xgboost','xgboost-cpu'",text)
        self.assertIn('balance_scale_llama31_diagnostic_v2_cpu',text)
        self.assertIn("'rendered_prompt':text",text)

    def test_failure_zip_before_generation(self):
        import tempfile
        import zipfile
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'run';out.mkdir()
            write_json(out/'run_config.json',{'fixture':True})
            archive=pack_results(out,RuntimeError('fixture: no CUDA device'),stage='controls')
            with zipfile.ZipFile(archive) as zipped:
                failure=json.loads(zipped.read('failure.json'))
                self.assertEqual(failure['stage'],'controls')
                self.assertEqual(failure['llm_calls_started'],0)
                self.assertIn('run_config.json',zipped.namelist())


def integration():
    OUT=ROOT/'reports/kaggle_llmfe_validation/balance_diagnostic_v2_cpu_synthetic'
    OUT.mkdir(parents=True,exist_ok=True)
    control=controls(SOURCE,OUT)
    configuration={'formats':['chat','completion'],'seeds':[42,43,44],'max_calls':6}
    calls=[]
    def fake(prompt,seed,mode):
        calls.append((mode,seed))
        return {'text':'not python' if seed==42 else SPEC if seed==43 else TORQUE,
                'truncated':False,'synthetic_not_llm':True,'rendered_prompt':prompt}
    trials=run_diagnostic(SOURCE,OUT,configuration,fake)
    assert [t['status'] for t in trials]==['rejected','valid','valid']*2
    assert all(t['train_rows']==500 and t['heldout_rows_not_evaluated']==125 for t in trials if t['status']=='valid')
    def forbidden(*_):raise AssertionError('Resume must not generate')
    assert run_diagnostic(SOURCE,OUT,configuration,forbidden)==trials
    report(OUT,configuration,trials,control)
    assert all(t['xgboost_build_info']['USE_CUDA'] is False for t in trials if t['status']=='valid')
    write_json(OUT/'verification.json',{'passed':True,'unit_tests':5,'synthetic_calls':len(calls),
        'heldout_evaluated':False,'real_llama_executed':False,'quality_result':False,'cpu_xgboost_cv_checked':True})
    print('Synthetic diagnostic pipeline passed; not a Llama result.')


if __name__=='__main__':
    result=unittest.main(exit=False)
    if not result.result.wasSuccessful():raise SystemExit(1)
    integration()
