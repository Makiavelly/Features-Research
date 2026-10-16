def modify_features(X, history):
    # Compute count of transactions for each customer
    customer_history = history.groupby('customer_id')['article_id'].count().reset_index(name='f_count_transactions')
    
    # Compute average price of past 180 days for each customer
    price_averages = history[history['days_ago'] <= 180].groupby('customer_id')['price'].mean().reset_index(name='f_mean_price_180_days')
    
    # Compute count of different product codes in past 180 days for each customer
    product_code_counts = history[history['days_ago'] <= 180].groupby('customer_id')['product_code'].nunique().reset_index(name='f_count_product_codes')
    
    # Compute mean of color group code in past 180 days for each customer
    color_group_means = history[history['days_ago'] <= 180].groupby('customer_id')['colour_group_code'].mean().reset_index(name='f_mean_color_group')
    
    # Merge all aggregates into X with a left join
    merged_X = X.merge(customer_history, on='customer_id', validate='many_to_one', how='left')
    merged_X = merged_X.merge(price_averages, on='customer_id', validate='many_to_one', how='left')
    merged_X = merged_X.merge(product_code_counts, on='customer_id', validate='many_to_one', how='left')
    merged_X = merged_X.merge(color_group_means, on='customer_id', validate='many_to_one', how='left')
    
    # Extract relevant columns into a new DataFrame F and return it
    F = merged_X[['customer_id', 'article_id', 'f_count_transactions', 'f_mean_price_180_days', 'f_count_product_codes', 'f_mean_color_group']]
    return F
