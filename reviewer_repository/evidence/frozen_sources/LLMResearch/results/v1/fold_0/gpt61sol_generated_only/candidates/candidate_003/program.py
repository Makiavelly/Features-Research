import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    def vals(s, keys):
        return s.reindex(pd.MultiIndex.from_frame(keys)).to_numpy()

    # Customer activity and recency
    cust_rec = h.groupby('customer_id')['days_ago'].min()
    out['f_customer_recency'] = X['customer_id'].map(cust_rec)
    for w in (7, 30, 90):
        c = h.loc[h['days_ago'] <= w].groupby('customer_id').size()
        out['f_customer_purchases_%dd' % w] = X['customer_id'].map(c).fillna(0)

    # Overall article popularity and recency
    item_rec = h.groupby('article_id')['days_ago'].min()
    out['f_item_recency'] = X['article_id'].map(item_rec)
    for w in (7, 30, 90):
        c = h.loc[h['days_ago'] <= w].groupby('article_id').size()
        out['f_item_sales_%dd' % w] = X['article_id'].map(c).fillna(0)

    # Repeat purchase signals for exact customer/article pairs
    pair = h.groupby(['customer_id', 'article_id'])
    out['f_pair_count'] = vals(pair.size(), X[['customer_id', 'article_id']]).astype(float)
    out['f_pair_recency'] = vals(pair['days_ago'].min(), X[['customer_id', 'article_id']]).astype(float)

    def category_features(hist_col, raw_col, prefix):
        keys = X[['customer_id', raw_col]].copy()
        keys.columns = ['customer_id', hist_col]
        g = h.groupby(['customer_id', hist_col])
        out['f_%s_count' % prefix] = vals(g.size(), keys).astype(float)
        out['f_%s_recency' % prefix] = vals(g['days_ago'].min(), keys).astype(float)
        r = h.loc[h['days_ago'] <= 30].groupby(['customer_id', hist_col]).size()
        out['f_%s_count_30d' % prefix] = vals(r, keys).astype(float)

    category_features('product_code', 'raw_i_product_code', 'product_code')
    category_features('product_type_no', 'raw_i_product_type_no', 'product_type')
    category_features('department_no', 'raw_i_department_no', 'department')
    category_features('section_no', 'raw_i_section_no', 'section')
    category_features('perceived_colour_master_id',
                      'raw_i_perceived_colour_master_id', 'colour_master')

    # Selected static information is useful because raw fields are not appended by host.
    out['f_user_age'] = X['raw_u_age']
    out['f_user_active'] = X['raw_u_active']
    out['f_user_fn'] = X['raw_u_fn']
    out['f_user_club'] = X['raw_u_club_member_status']
    out['f_item_product_type'] = X['raw_i_product_type_no']
    out['f_item_department'] = X['raw_i_department_no']
    out['f_item_section'] = X['raw_i_section_no']
    out['f_item_garment_group'] = X['raw_i_garment_group_no']

    return out
