"""CPU-only SQL interface tests and synthetic end-to-end verification, no real Llama."""
import ast
import hashlib
import json
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
from sql_features import compile_sql,validate_program
from runtime import source_from_response,source_key

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
SPEC={'aggregates':[
    {'name':'f_count','keys':['customer_id'],'sql':'COUNT(*)'},
    {'name':'f_price','keys':['customer_id','product_type_no'],'sql':'AVG(price)'}],
    'derived':[{'name':'f_log_count','sql':'LN(1 + COALESCE(f_count, 0))'},
               {'name':'f_interaction','sql':'f_log_count * raw_u_age'}]}


class Checks(unittest.TestCase):
    def test_join_order_and_missing_groups(self):
        X=pd.DataFrame({'customer_id':[2,1,2,3],'article_id':[11,12,13,14],
                        'raw_i_product_type_no':[4,4,5,4],'raw_u_age':[20,30,40,50]},index=[8,2,7,6])
        H=pd.DataFrame({'customer_id':[1,2,2],'article_id':[9,10,11],
                        'product_type_no':[4,4,4],'price':[.2,.4,.6]})
        F=compile_sql(json.dumps(SPEC))(X,H)
        np.testing.assert_allclose(F.f_count,[2,1,2,np.nan],equal_nan=True)
        np.testing.assert_allclose(F.f_price,[.5,.2,np.nan,np.nan],equal_nan=True)
        np.testing.assert_allclose(F.f_log_count,np.log1p([2,1,2,0]))
        np.testing.assert_allclose(F.f_interaction,np.log1p([2,1,2,0])*[20,30,40,50])
        self.assertTrue(F.index.equals(X.index))

    def test_reject_external_access_and_labels(self):
        for sql in ['(SELECT 1)','read_csv(1)','AVG(label)','SUM(price); DROP TABLE history_input',
                    'AVG(customer_id)',"COUNT(*) --comment",'random()','COUNT(*) OVER ()']:
            with self.subTest(sql=sql),self.assertRaises(ValueError):
                validate_program({'aggregates':[SPEC['aggregates'][0],{'name':'f_bad','keys':['article_id'],'sql':sql}]})

    def test_json_dedup_and_output_contract(self):
        a=source_from_response('```json\n'+json.dumps(SPEC)+'\n```')
        b=json.loads(a);b['aggregates'].reverse();b['rationale']='irrelevant'
        self.assertEqual(source_key(a),source_key(json.dumps(b)))
        with self.assertRaises(ValueError): source_from_response('{"aggregates":[]}')
        with self.assertRaises(ValueError): source_from_response('def modify_features(X, history): pass')

    def test_derived_namespace_and_local_qwen_limits(self):
        for sql in ['price + 1','customer_id + 1','f_not_yet_defined + 1','AVG(label)']:
            with self.subTest(sql=sql),self.assertRaises(ValueError):
                validate_program({'derived':[{'name':'f_bad','sql':sql}]})
        self.assertEqual(len(validate_program({'aggregates':[
            {'name':'f_test'+str(i),'keys':['customer_id'],'sql':'COUNT(*)'} for i in range(24)]})['aggregates']),24)
        with self.assertRaises(ValueError):
            validate_program({'derived':[{'name':'f_test'+str(i),'sql':'raw_u_age + 1'} for i in range(13)]})

    def test_time_boundaries_and_label_invariance(self):
        from worker import Data,matrix
        data=Data(ROOT/'data/kaggle_hm_llmfe_fulltrain_v2')
        pairs=pd.read_parquet(data.root/'search_pairs.parquet').head(100)
        function=compile_sql(json.dumps(SPEC))
        values,names=matrix(data,pairs,function)
        cutoff=pairs.timestamp.max()
        future=data.tx.head(10).copy();future['t_dat']=cutoff+pd.Timedelta(days=1)
        data.tx=pd.concat([data.tx,future],ignore_index=True)
        changed=pairs.copy();changed['label']=999
        other,other_names=matrix(data,changed,function)
        np.testing.assert_array_equal(values,other)
        self.assertEqual(names,other_names)

    def test_embedded_sources_and_notebook(self):
        import nbformat
        notebook=nbformat.read(ROOT/'LLMFeatures/kaggle/llmfe_llama31_hm_sql_kaggle_t4.ipynb',as_version=4)
        nbformat.validate(notebook)
        modules=None;config=None
        for cell in notebook.cells:
            if cell.cell_type!='code': continue
            for node in ast.parse(cell.source).body:
                if isinstance(node,ast.Assign):
                    if any(isinstance(t,ast.Name) and t.id=='MODULES' for t in node.targets): modules=ast.literal_eval(node.value)
                    if any(isinstance(t,ast.Name) and t.id=='CONFIG' for t in node.targets):
                        config={k.value:v for k,v in zip(node.value.keys,node.value.values)}
        for name,source in modules.items():
            self.assertEqual(source,(HERE/name).read_text())
        self.assertEqual(ast.literal_eval(config['feature_interface']),'qwen_sql_aggregates_and_derived')
        self.assertEqual(ast.literal_eval(config['target_successful_distinct']),20)
        self.assertEqual(ast.literal_eval(config['max_llm_calls']),300)
        self.assertEqual(ast.literal_eval(config['max_repairs_per_proposal']),3)
        self.assertEqual(ast.literal_eval(config['search_backend']),'lightgbm')


if __name__=='__main__':
    unittest.main()
