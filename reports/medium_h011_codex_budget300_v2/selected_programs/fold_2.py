import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    # temporal purchase counts for customers and articles
    for w, tag in [(7,'7d'), (30,'30d'), (90,'90d'), (365,'365d')]:
        hw = h.loc[h['days_ago'] <= w]
        cu = hw.groupby('customer_id').size()
        it = hw.groupby('article_id').size()
        out['f_customer_count_'+tag] = X['customer_id'].map(cu).fillna(0).astype(float)
        out['f_article_count_'+tag] = X['article_id'].map(it).fillna(0).astype(float)
    # direct pair repetition and recency
    pair_n = h.groupby(['customer_id','article_id']).size()
    pair_last = h.groupby(['customer_id','article_id'])['days_ago'].min()
    keys = list(zip(X['customer_id'].to_numpy(), X['article_id'].to_numpy()))
    out['f_pair_count'] = pair_n.reindex(keys).to_numpy()
    out['f_pair_recency'] = pair_last.reindex(keys).to_numpy()
    # recent pair counts
    for w, tag in [(7,'7d'), (30,'30d'), (90,'90d')]:
        hw = h.loc[h['days_ago'] <= w]
        s = hw.groupby(['customer_id','article_id']).size()
        out['f_pair_count_'+tag] = s.reindex(keys).fillna(0).to_numpy()
    # category affinity: customer purchases in candidate product/type/section
    for col, raw, tag in [('product_code','raw_i_product_code','prod'),
                          ('product_type_no','raw_i_product_type_no','type'),
                          ('section_no','raw_i_section_no','section'),
                          ('department_no','raw_i_department_no','dept'),
                          ('garment_group_no','raw_i_garment_group_no','garment')]:
        g = h.groupby(['customer_id', col]).size()
        k = list(zip(X['customer_id'].to_numpy(), X[raw].to_numpy()))
        out['f_customer_'+tag+'_count'] = g.reindex(k).fillna(0).to_numpy()
        # category popularity, useful for cold customers
        pop = h.groupby(col).size()
        out['f_article_'+tag+'_pop'] = X[raw].map(pop).fillna(0).astype(float)
    # customer and item recency, plus channel propensity
    out['f_customer_recency'] = X['customer_id'].map(h.groupby('customer_id')['days_ago'].min())
    out['f_article_recency'] = X['article_id'].map(h.groupby('article_id')['days_ago'].min())
    ch = h.groupby('customer_id')['sales_channel_id'].mean()
    out['f_customer_channel'] = X['customer_id'].map(ch)
    # price affinity versus customer historical average and article average
    cprice = h.groupby('customer_id')['price'].mean()
    iprice = h.groupby('article_id')['price'].mean()
    out['f_customer_price_mean'] = X['customer_id'].map(cprice)
    out['f_article_price_mean'] = X['article_id'].map(iprice)
    return out
