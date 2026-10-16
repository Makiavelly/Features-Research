def modify_features(X, history):
    # Compute average customer age
    avg_customer_age = history.groupby('customer_id')['customer_age'].mean().to_frame('avg_customer_age')
    
    # Compute count of purchases in the last 7 days
    recent_purchases = history[history['days_ago'] <= 7].groupby('customer_id')['article_id'].nunique().to_frame('recent_purchases')
    
    # Compute count of different product types purchased in the last 7 days
    recent_product_types = history[history['days_ago'] <= 7].groupby('customer_id')['product_type_no'].nunique().to_frame('recent_product_types')
    
    # Merge aggregates with X
    F = pd.merge(X, avg_customer_age, on='customer_id', suffixes=('_x',''), validate='many_to_one')
    F = pd.merge(F, recent_purchases, on='customer_id', suffixes=('_x',''), validate='many_to_one')
    F = pd.merge(F, recent_product_types, on='customer_id', suffixes=('_x',''), validate='many_to_one')
    
    # Assign values positionally to F
    F[['f_avg_customer_age', 'f_recent_purchases', 'f_recent_product_types']] = F[['avg_customer_age','recent_purchases','recent_product_types']].to_numpy()
    
    return F
