def modify_features(X, history):
    # Calculate moving averages and modes of past purchases
    avg_price_180 = history[(history['days_ago'] <= 180) & (history['days_ago'] >= 0)].groupby(['customer_id', 'article_id'])['price'].mean().mean().reset_index(name='f_avg_price_180')
    mode_product_type_180 = history[(history['days_ago'] <= 180) & (history['days_ago'] >= 0)].groupby(['customer_id', 'article_id'])['product_type_no'].apply(lambda x: x.mode().iloc[0]).reset_index(name='f_mode_product_type_180')
    avg_age_180 = history[(history['days_ago'] <= 180) & (history['days_ago'] >= 0)].groupby('customer_id')['customer_age'].mean().mean().reset_index(name='f_avg_age_180')
    
    # Filter and merge history for each candidate pair
    filtered_history = history[(history['days_ago'] <= 180) & (history['days_ago'] >= 0)]
    merged_history = filtered_history.merge(avg_price_180, on='customer_id', how='left', validate='many_to_one')
    merged_history = merged_history.merge(mode_product_type_180, on='customer_id', how='left', validate='many_to_one')
    merged_history = merged_history.merge(avg_age_180, on='customer_id', how='left', validate='many_to_one')
    
    # Select required columns and assign to F
    F = merged_history[['customer_id', 'article_id', 'f_avg_price_180', 'f_mode_product_type_180', 'f_avg_age_180']].copy()
    
    return F
