"""Synthetic correctness checks only: no LightGBM fit and no ranking fitness."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
info=json.loads((ROOT/'reports/authored20_v1/current_run.json').read_text())
source=Path(info['directory'])
sys.path.insert(0,str(source/'runtime_sources'))
from authored20_design import program
from python_features import validate_program,compile_function,construct


def main():
    h=pd.DataFrame({'customer_id':[0,0,1,1],'article_id':[0,1,1,2],
                    'product_type_no':[0,1,1,2],'days_ago':[1,10,2,3],
                    'price':[10.,30.,20.,40.],'sales_channel_id':[1,2,2,1],
                    'customer_age':[20.,20.,40.,40.]})
    X=pd.DataFrame({'customer_id':[0,0,1,99],'article_id':[0,2,0,99],
                    'raw_i_product_type_no':[0,2,0,99],'raw_u_age':[20.,20.,40.,50.]},index=[8,3,7,4])
    names=['u_n0','i_n7','p_n0','p_r','u_r','i_price','u_price','u_std','u_q25','u_q75',
           'i_age','u_ch2','i_ch2','i_dec14','t_share','t_lift','price_gap','price_z',
           'age_gap','channel_match','u_uniq','i_uniq','graph_t90','graph_t365']
    func=compile_function(validate_program({'code':program(names)}))
    values=construct(func,X,h)
    np.testing.assert_array_equal(values.f_u_n0,[2,2,2,0])
    np.testing.assert_array_equal(values.f_i_n7,[1,1,1,0])
    np.testing.assert_array_equal(values.f_p_n0,[1,0,0,0])
    np.testing.assert_allclose(values.f_p_r,[1,np.nan,np.nan,np.nan],equal_nan=True)
    np.testing.assert_allclose(values.f_price_gap,[10,20,20,np.nan],equal_nan=True)
    np.testing.assert_allclose(values.f_u_std,[10,10,10,np.nan],equal_nan=True)
    np.testing.assert_allclose(values.f_u_q25,[15,15,25,np.nan],equal_nan=True)
    np.testing.assert_allclose(values.f_u_q75,[25,25,35,np.nan],equal_nan=True)
    np.testing.assert_allclose(values.f_t_share,[.2,0,0,0],equal_nan=True)
    np.testing.assert_allclose(values.f_age_gap,[0,20,20,np.nan],equal_nan=True)
    np.testing.assert_allclose(values.f_graph_t90,[.5/np.sqrt(2),.5/np.sqrt(2),.5/np.sqrt(2),0])
    np.testing.assert_allclose(values.f_i_dec14,[np.exp(-1/14),np.exp(-3/14),np.exp(-1/14),0])
    np.testing.assert_allclose(values.f_u_ch2,[.5,.5,.5,np.nan],equal_nan=True)
    construct(func,X,h.iloc[:0],expected=list(values))
    perm=[2,0,3,1]
    changed=construct(func,X.iloc[perm],h,expected=list(values))
    np.testing.assert_allclose(changed.to_numpy()[np.argsort(perm)],values,equal_nan=True)
    chunks=pd.concat([construct(func,X.iloc[:2],h),construct(func,X.iloc[2:],h)])
    np.testing.assert_allclose(chunks,values,equal_nan=True)
    result={'status':'passed','checks':['independent_counts','pair_recency','price_and_quantiles',
            'age_difference','channel_statistics','decay_weight','smoothed_preference','cosine_category_graph',
            'empty_history','nondefault_row_index','row_permutation','batch_invariance'],
            'lightgbm_training_runs':0,'search_evaluations':0,'api_requests':0,
            'design_sha256':hashlib.sha256((source/'runtime_sources/authored20_design.py').read_bytes()).hexdigest()}
    out=ROOT/'reports/authored20_v1/kernel_verification.json'
    out.write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
