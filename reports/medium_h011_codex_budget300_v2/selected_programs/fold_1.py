import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h7 = history.loc[history['days_ago'] <= 7]
    h30 = history.loc[history['days_ago'] <= 30]
    h90 = history.loc[history['days_ago'] <= 90]

    item = history.groupby('article_id').agg(
        item_recency=('days_ago', 'min'),
        item_oldest=('days_ago', 'max'),
        item_buyers=('customer_id', 'nunique'),
        item_price=('price', 'mean'),
        item_price_std=('price', 'std'),
        item_channel=('sales_channel_id', 'mean')
    )
    i7 = h7.groupby('article_id').size()
    i30 = h30.groupby('article_id').size()
    i90 = h90.groupby('article_id').size()
    cat_item = h30.groupby(
        ['product_type_no', 'department_no', 'article_id']
    ).size()
    cat = cat_item.groupby(level=[0, 1]).agg(['sum', 'mean', 'size'])
    customer = history.groupby('customer_id').agg(
        customer_count=('article_id', 'size'),
        customer_types=('product_type_no', 'nunique'),
        customer_departments=('department_no', 'nunique'),
        customer_price=('price', 'mean'),
        customer_price_std=('price', 'std'),
        customer_channel=('sales_channel_id', 'mean'),
        customer_recency=('days_ago', 'min')
    )
    cc = history.groupby(
        ['customer_id', 'product_type_no', 'department_no']
    ).agg(
        cc_recency=('days_ago', 'min'),
        cc_count=('article_id', 'size'),
        cc_price=('price', 'mean'),
        cc_price_std=('price', 'std'),
        cc_channel=('sales_channel_id', 'mean')
    )
    cc30 = h30.groupby(['customer_id', 'product_type_no', 'department_no']).size()
    pair = history.groupby(['customer_id', 'article_id']).agg(pair_recency=('days_ago', 'min'), pair_count=('article_id', 'size'))
    product = history.groupby(['customer_id', 'product_code']).agg(product_recency=('days_ago', 'min'))

    cat_key = pd.MultiIndex.from_arrays([
        X['raw_i_product_type_no'].to_numpy(), X['raw_i_department_no'].to_numpy()
    ])
    cc_key = pd.MultiIndex.from_arrays([
        X['customer_id'].to_numpy(), X['raw_i_product_type_no'].to_numpy(),
        X['raw_i_department_no'].to_numpy()
    ])
    pair_key = pd.MultiIndex.from_arrays([X['customer_id'].to_numpy(), X['article_id'].to_numpy()])
    product_key = pd.MultiIndex.from_arrays([X['customer_id'].to_numpy(), X['raw_i_product_code'].to_numpy()])
    ci_key = pd.MultiIndex.from_arrays([
        X['raw_i_product_type_no'].to_numpy(), X['raw_i_department_no'].to_numpy(),
        X['article_id'].to_numpy()
    ])
    ci30 = cat_item.reindex(ci_key).fillna(0).to_numpy()
    cat_sum = cat['sum'].reindex(cat_key).fillna(0).to_numpy()
    cat_mean = cat['mean'].reindex(cat_key).fillna(0).to_numpy()
    ip = X['article_id'].map(item['item_price'])

    out['f_item_count_7'] = np.log1p(X['article_id'].map(i7).fillna(0))
    out['f_item_count_30'] = np.log1p(X['article_id'].map(i30).fillna(0))
    out['f_item_count_90'] = np.log1p(X['article_id'].map(i90).fillna(0))
    out['f_item_buyers'] = np.log1p(X['article_id'].map(item['item_buyers']).fillna(0))
    out['f_item_recency'] = X['article_id'].map(item['item_recency'])
    out['f_item_oldest'] = X['article_id'].map(item['item_oldest'])
    out['f_item_price'] = ip
    out['f_item_price_std'] = X['article_id'].map(item['item_price_std'])
    out['f_item_channel'] = X['article_id'].map(item['item_channel'])
    out['f_item_category_relative'] = ci30 / (cat_mean + 1.0)
    out['f_item_category_share'] = ci30 / (cat_sum + 1.0)
    out['f_category_count_30'] = np.log1p(cat_sum)
    out['f_category_items_30'] = np.log1p(cat['size'].reindex(cat_key).fillna(0).to_numpy())
    out['f_customer_category_recency'] = cc['cc_recency'].reindex(cc_key).to_numpy()
    out['f_customer_category_count'] = np.log1p(cc['cc_count'].reindex(cc_key).fillna(0).to_numpy())
    out['f_customer_category_count_30'] = np.log1p(cc30.reindex(cc_key).fillna(0).to_numpy())
    cp = cc['cc_price'].reindex(cc_key).to_numpy()
    cps = cc['cc_price_std'].reindex(cc_key).to_numpy()
    out['f_customer_category_price'] = cp
    out['f_customer_category_channel'] = cc['cc_channel'].reindex(cc_key).to_numpy()
    out['f_item_category_price_gap'] = np.abs(ip.to_numpy() - cp)
    out['f_item_category_price_z'] = np.abs(ip.to_numpy() - cp) / (cps + 0.005)
    out['f_customer_count'] = np.log1p(X['customer_id'].map(customer['customer_count']).fillna(0))
    out['f_customer_type_diversity'] = X['customer_id'].map(customer['customer_types'])
    out['f_customer_department_diversity'] = X['customer_id'].map(customer['customer_departments'])
    out['f_customer_price'] = X['customer_id'].map(customer['customer_price'])
    out['f_customer_price_std'] = X['customer_id'].map(customer['customer_price_std'])
    out['f_customer_channel'] = X['customer_id'].map(customer['customer_channel'])
    out['f_customer_recency'] = X['customer_id'].map(customer['customer_recency'])
    out['f_user_age'] = X['raw_u_age']
    out['f_user_active'] = X['raw_u_active']
    out['f_item_type'] = X['raw_i_product_type_no']
    out['f_item_department'] = X['raw_i_department_no']
    out['f_item_garment'] = X['raw_i_garment_group_no']
    out['f_pair_recency'] = pair['pair_recency'].reindex(pair_key).to_numpy()
    out['f_pair_count'] = np.log1p(pair['pair_count'].reindex(pair_key).fillna(0).to_numpy())
    out['f_product_code_recency'] = product['product_recency'].reindex(product_key).to_numpy()
    return out
