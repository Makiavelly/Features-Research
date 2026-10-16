def modify_features(X, history):
    idx = history.set_index(['customer_id', 'article_id']).index
    F = pd.DataFrame(index=X.index, columns=['f_customer_age_in_180_days', 'f_customer_avg_price', 'f_days_ago_avg_price', 'f_customer_category_average', 'f_days_ago_count'])
    
    F['f_customer_age_in_180_days'] = history['customer_age'].loc[idx].fillna(0).rolling(180, min_periods=1).mean().reindex(idx)
    F['f_customer_avg_price'] = history['price'].loc[idx].fillna(0).groupby(idx).mean().reindex(idx)['price']
    F['f_days_ago_avg_price'] = history['price'].loc[idx].fillna(0).rolling(7, min_periods=1).mean().reindex(idx)['price']
    F['f_customer_category_average'] = history['product_type_no'].loc[idx].fillna(0).groupby(idx).mean().reindex(idx)['product_type_no']
    F['f_days_ago_count'] = history['customer_id'].loc[idx].value_counts().reindex(idx).fillna(0)
    
    return F
