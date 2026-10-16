def modify_features(X, history):
    idx = history.set_index(['customer_id', 'article_id']).index
    F = pd.DataFrame(index=X.index)
    F['f_customer_age_in_180_days'] = history['customer_age'].loc[idx].fillna(0).rolling(180, min_periods=1).mean().reindex(idx)
    F['f_customer_avg_price'] = history['price'].loc[idx].fillna(0).groupby(idx).mean().reindex(idx)
    F['f_days_ago_avg_price'] = history['price'].loc[idx].fillna(0).rolling(7, min_periods=1).mean().reindex(idx)
    F['f_customer Avg_product_type_no'] = history['product_type_no'].loc[idx].fillna(0).groupby(idx).mean().reindex(idx)
    F['f_user_club_membership_avg'] = history['customer_age'].loc[idx].fillna(0).groupby(idx).mean().reindex(idx)
    return F
