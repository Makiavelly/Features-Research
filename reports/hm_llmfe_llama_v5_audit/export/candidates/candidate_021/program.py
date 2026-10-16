def modify_features(X, history):
    # Calculate moving averages and modes of past purchases
    avg_price = history.groupby(['customer_id', 'article_id'])['price'].mean().reset_index()
    mode_product_type = history.groupby(['customer_id', 'article_id'])['product_type_no'].apply(lambda x: x.mode().iloc[0]).reset_index()
    avg_age = history.groupby('customer_id')['customer_age'].mean().reset_index()
    
    # Filter and merge history for each candidate pair
    filtered_history = history[(history['days_ago'] <= 180) & (history['days_ago'] >= 0)]
    merged_history = filtered_history.merge(avg_price, on=['customer_id', 'article_id'], how='left')
    merged_history = merged_history.merge(mode_product_type, on=['customer_id', 'article_id'], how='left')
    merged_history = merged_history.merge(avg_age, on='customer_id', how='left')
    
    # Calculate new features
    merged_history['f_avg_price_180'] = merged_history['avg_price']
    merged_history['f_mode_product_type_180'] = merged_history['mode_product_type']
    merged_history['f_avg_age_180'] = merged_history['avg_age']
    
    # Select required columns and assign to F
    F = merged_history[['customer_id', 'article_id', 'f_avg_price_180', 'f_mode_product_type_180', 'f_avg_age_180']].copy()
    
    return F
