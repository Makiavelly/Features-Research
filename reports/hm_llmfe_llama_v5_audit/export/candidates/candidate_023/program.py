def modify_features(X, history):
    # Calculate moving averages and modes of past purchases
    avg_price_180 = history[(history['days_ago'] <= 180) & (history['days_ago'] >= 0)].groupby(['customer_id', 'article_id'])['price'].mean().reset_index()
    mode_product_type_180 = history[(history['days_ago'] <= 180) & (history['days_ago'] >= 0)].groupby(['customer_id', 'article_id'])['product_type_no'].apply(lambda x: x.mode().iloc[0]).reset_index()
    avg_age_180 = history[(history['days_ago'] <= 180) & (history['days_ago'] >= 0)].groupby('customer_id')['customer_age'].mean().reset_index()
    
    # Filter and merge history for each candidate pair
    filtered_history = history[(history['days_ago'] <= 180) & (history['days_ago'] >= 0)]
    merged_history = filtered_history.merge(avg_price_180[['customer_id', 'article_id', 'price']], on=['customer_id', 'article_id'], how='left', validate='many_to_one')
    merged_history = merged_history.merge(mode_product_type_180[['customer_id', 'article_id', 'product_type_no']], on=['customer_id', 'article_id'], how='left', validate='many_to_one')
    merged_history = merged_history.merge(avg_age_180[['customer_id', 'customer_age']], on='customer_id', how='left', validate='many_to_one')
    
    # Calculate new features
    merged_history['f_avg_price_180'] = merged_history['price_y']
    merged_history['f_mode_product_type_180'] = merged_history['product_type_no_y']
    merged_history['f_avg_age_180'] = merged_history['customer_age_y']
    
    # Select required columns and assign to F
    F = merged_history[['customer_id', 'article_id', 'f_avg_price_180', 'f_mode_product_type_180', 'f_avg_age_180']].copy()
    
    return F
