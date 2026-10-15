"""Test structured compiler and real CPU evaluator; no Llama quality claim."""
import ast
import json
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
from structured_features import validate_program,to_sql,compile_structured

ROOT=Path(__file__).resolve().parents[3]
SPEC={'aggregates':[
    {'name':'f_recent','keys':['customer_id'],'op':'count','column':'*','window':30},
    {'name':'f_recency','keys':['customer_id'],'op':'min','column':'days_ago','window':180}],
    'derived':[
        {'name':'f_rate','expr':{'op':'divide','args':[{'ref':'f_recent'},{'op':'add','args':[{'ref':'f_recency'},1]}]}},
        {'name':'f_log_rate','expr':{'op':'log1p','args':[{'ref':'f_rate'}]}}]}


class Tests(unittest.TestCase):
    def test_compiled_values_and_row_order(self):
        X=pd.DataFrame({'customer_id':[2,1,3,2],'article_id':[5,6,7,8]},index=[4,7,1,8])
        H=pd.DataFrame({'customer_id':[1,2,2],'days_ago':[7,10,50]})
        result=compile_structured(json.dumps(SPEC))(X,H)
        np.testing.assert_allclose(result.f_recent,[1,1,np.nan,1],equal_nan=True)
        np.testing.assert_allclose(result.f_recency,[10,7,np.nan,10],equal_nan=True)
        np.testing.assert_allclose(result.f_rate,[1/11,1/8,np.nan,1/11],equal_nan=True)
        self.assertTrue(result.index.equals(X.index))

    def test_reports_multiple_errors_from_user_failure(self):
        broken={'aggregates':[
            {'name':'f_a','keys':['customer_id'],'op':'avg','column':'raw_u_active'},
            {'name':'f_b','keys':['sales_channel_id'],'op':'count'}],
            'derived':[{'name':'f_c','expr':{'ref':'f_nonexistent'}}]}
        with self.assertRaises(ValueError) as caught:validate_program(broken)
        for location in ['aggregates[0]','aggregates[1]','derived[0]']:
            self.assertIn(location,str(caught.exception))

    def test_forbid_sql_nested_aggregates_and_ids(self):
        for column in ['customer_id','product_type_no','AVG(price)','price); SELECT 1']:
            with self.subTest(column=column),self.assertRaises(ValueError):
                validate_program({'aggregates':[{'name':'f_bad','keys':['article_id'],'op':'avg','column':column}]})
        with self.assertRaises(ValueError):validate_program({'aggregates':[{'name':'f_bad','keys':['article_id'],'op':'count','sql':'COUNT(*)'}]})

    def test_math_missing_values_and_raw_fields(self):
        program={'derived':[
            {'name':'f_zero','expr':{'op':'divide','args':[1,0]}},
            {'name':'f_log','expr':{'op':'log1p','args':[-1]}},
            {'name':'f_age','expr':{'op':'multiply','args':[{'ref':'raw_u_age'},2]}}]}
        X=pd.DataFrame({'raw_u_age':[20,30]})
        F=compile_structured(json.dumps(program))(X,pd.DataFrame({'customer_id':[]}))
        self.assertTrue(F.f_zero.isna().all())
        np.testing.assert_array_equal(F.f_log,[0,0]);np.testing.assert_array_equal(F.f_age,[40,60])

    def test_canonicalization_limits_and_future_references(self):
        a=validate_program(SPEC);b=json.loads(json.dumps(SPEC));b['aggregates'].reverse()
        self.assertEqual(a,validate_program(b))
        with self.assertRaises(ValueError):validate_program({'derived':[{'name':'f_bad','expr':{'ref':'f_later'}}]})
        with self.assertRaises(ValueError):validate_program({'derived':[{'name':'f_bad','expr':float('inf')}]})
        with self.assertRaises(ValueError):validate_program({'aggregates':[{**SPEC['aggregates'][0],'window':181}]})

    def test_time_and_label_invariance(self):
        from worker import Data,matrix
        data=Data(ROOT/'data/kaggle_hm_llmfe_fulltrain_v2')
        pairs=pd.read_parquet(data.root/'search_pairs.parquet').head(128)
        function=compile_structured(json.dumps(SPEC));values,names=matrix(data,pairs,function)
        future=data.tx.head(10).copy();future['t_dat']=pairs.timestamp.max()+pd.Timedelta(days=1)
        data.tx=pd.concat([data.tx,future],ignore_index=True)
        pairs=pairs.assign(label=999)
        other,_=matrix(data,pairs,function)
        np.testing.assert_array_equal(values,other)

    def test_notebook_embedded_sources(self):
        import nbformat
        nb=nbformat.read(ROOT/'LLMFeatures/kaggle/llmfe_llama31_hm_structured_kaggle_t4.ipynb',as_version=4)
        nbformat.validate(nb)
        for cell in nb.cells:
            if cell.cell_type!='code':continue
            for node in ast.parse(cell.source).body:
                if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MODULES' for t in node.targets):
                    for name,source in ast.literal_eval(node.value).items():
                        self.assertEqual(source,(Path(__file__).parent/name).read_text())
        text=''.join(c.source for c in nb.cells)
        self.assertIn('structured_aggregates_and_expression_trees',text)
        self.assertIn('llmfe_structured_runtime',text)


if __name__=='__main__':unittest.main()
