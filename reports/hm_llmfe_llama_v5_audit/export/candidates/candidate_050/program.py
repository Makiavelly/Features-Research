def modify_features(X, history):
    # Compute average customer age
    avg_customer_age = history.groupby('customer_id')['customer_age'].mean().to_frame('f_avg_customer_age')
    
    # Compute count of purchases in the last 7 days
    recent_purchases = history[history['days_ago'] <= 7].groupby('customer_id')['article_id'].nunique().to_frame('f_recent_purchases')
    
    # Compute count of different product types purchased in the last 7 days
    recent_product_types = history[history['days_ago'] <= 7].groupby('customer_id')['product_type_no'].nunique().to_frame('f_recent_product_types')
    
    # Merge aggregates with X using left join
    F = pd.merge(X, avg_customer_age, on='customer_id', how='left', suffixes=('', '_avg_customer_age'), validate='many_to_one')
    F = pd.merge(F, recent_purchases, on='customer_id', how='left', suffixes=('_avg_customer_age', '_recent_purchases'), validate='many_to_one')
    F = pd.merge(F, recent_product_types, on='customer_id', how='left', suffixes=('_recent_purchases', '_recent_product_types'), validate='many_to_one')
    
    # Remove NaN values from aggregated columns
    F[['f_avg_customer_age', 'f_recent_purchases', 'f_recent_product_types']] = F[['f_avg_customer_age', 'f_recent_purchases', 'f_recent_product_types']].fillna(0)
    
    return F
