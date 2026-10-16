def modify_features(X, history):
    # Compute count of transactions for each customer
    customer_history = history[history['days_ago'] <= 180].groupby('customer_id')['article_id'].nunique().reset_index(name='f_count_transactions')
    
    # Compute average price of past 180 days for each customer
    price_averages = history[history['days_ago'] <= 180].groupby('customer_id')['price'].mean().reset_index(name='f_mean_price_180_days')
    
    # Compute count of different product codes in past 180 days for each customer
    product_code_counts = history[history['days_ago'] <= 180].groupby('customer_id')['product_code'].nunique().reset_index(name='f_count_product_codes')
    
    # Compute mean of color group code in past 180 days for each customer
    color_group_means = history[history['days_ago'] <= 180].groupby('customer_id')['colour_group_code'].mean().reset_index(name='f_mean_color_group')
    
    # Merge all aggregates into a new DataFrame F with a left join
    F = pd.merge(customer_history, price_averages, on='customer_id', validate='many_to_one', how='left')
    F = pd.merge(F, product_code_counts, on='customer_id', validate='many_to_one', how='left')
    F = pd.merge(F, color_group_means, on='customer_id', validate='many_to_one', how='left')
    
    # Return F with X.index and row order
    F = F.reindex(columns=F.columns.tolist() + X.columns[X.columns!= 'customer_id'].tolist())
    F = F.reindex(index=X.index)
    return F
