import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h7 = history.loc[history['days_ago'] <= 7]
    h30 = history.loc[history['days_ago'] <= 30]
    h90 = history.loc[history['days_ago'] <= 90]
    n7 = h7.groupby('article_id').size()
    n30 = h30.groupby('article_id').size()
    n90 = h90.groupby('article_id').size()
    x7 = X['article_id'].map(n7).fillna(0)
    x30 = X['article_id'].map(n30).fillna(0)
    x90 = X['article_id'].map(n90).fillna(0)
    out['f_item_sales_7'] = x7
    out['f_item_sales_30'] = x30
    out['f_item_sales_90'] = x90
    out['f_item_share_7_30'] = x7 / (x30 + 1.0)
    out['f_item_trend_7_vs_old'] = x7 - (x30 - x7) / 3.0
    out['f_item_recency'] = X['article_id'].map(history.groupby('article_id')['days_ago'].min())

    age_hist = h30.copy()
    age_hist['_age_bin'] = np.floor(age_hist['customer_age'].fillna(-10) / 10.0)
    age_x = np.floor(X['raw_u_age'].fillna(-10) / 10.0)
    age_item = age_hist.groupby(['article_id', '_age_bin']).size()
    age_keys = pd.MultiIndex.from_arrays([X['article_id'].to_numpy(), age_x.to_numpy()])
    out['f_item_agebin_sales_30'] = age_item.reindex(age_keys).fillna(0).to_numpy()

    age_hist7 = h7.copy()
    age_hist7['_age_bin'] = np.floor(age_hist7['customer_age'].fillna(-10) / 10.0)
    age_item7 = age_hist7.groupby(['article_id', '_age_bin']).size()
    out['f_item_agebin_sales_7'] = age_item7.reindex(age_keys).fillna(0).to_numpy()

    for raw, hist, tag in [
        ('raw_i_product_type_no', 'product_type_no', 'type'),
        ('raw_i_department_no', 'department_no', 'department')
    ]:
        out['f_' + tag + '_sales_7'] = X[raw].map(h7.groupby(hist).size()).fillna(0)
        out['f_' + tag + '_sales_30'] = X[raw].map(h30.groupby(hist).size()).fillna(0)

    out['f_customer_sales_7'] = X['customer_id'].map(h7.groupby('customer_id').size()).fillna(0)
    out['f_customer_sales_30'] = X['customer_id'].map(h30.groupby('customer_id').size()).fillna(0)
    out['f_customer_recency'] = X['customer_id'].map(history.groupby('customer_id')['days_ago'].min())
    out['f_raw_age'] = X['raw_u_age']
    return out
