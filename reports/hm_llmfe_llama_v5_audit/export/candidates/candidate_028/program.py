def modify_features(X, history):
    # Compute f_average_price_180_days, f_count_product_codes_180_days, f_count_transactions_180_days, f_mean_color_group_180_days
    # Merge all aggregates into a new DataFrame F with a left join
    F = pd.DataFrame(index=X.index)
    
    # Compute average price of past 180 days for each customer
    average_price_180_days = history[history['days_ago'] <= 180].groupby('customer_id')['price'].mean().reset_index()
    average_price_180_days.columns = ['customer_id', 'f_average_price_180_days']
    
    # Compute count of different product codes in past 180 days for each customer
    product_code_counts_180_days = history[history['days_ago'] <= 180].groupby('customer_id')['product_code'].nunique().reset_index()
    product_code_counts_180_days.columns = ['customer_id', 'f_count_product_codes_180_days']
    
    # Compute count of transactions for each customer
    count_transactions_180_days = history[history['days_ago'] <= 180].groupby('customer_id')['article_id'].nunique().reset_index()
    count_transactions_180_days.columns = ['customer_id', 'f_count_transactions_180_days']
    
    # Compute mean of color group code in past 180 days for each customer
    color_group_means_180_days = history[history['days_ago'] <= 180].groupby('customer_id')['colour_group_code'].mean().reset_index()
    color_group_means_180_days.columns = ['customer_id', 'f_mean_color_group_180_days']
    
    # Merge all aggregates into a new DataFrame F with a left join
    F = pd.merge(F, average_price_180_days[['customer_id', 'f_average_price_180_days']], on='customer_id', how='left')
    F = pd.merge(F, product_code_counts_180_days[['customer_id', 'f_count_product_codes_180_days']], on='customer_id', how='left')
    F = pd.merge(F, count_transactions_180_days[['customer_id', 'f_count_transactions_180_days']], on='customer_id', how='left')
    F = pd.merge(F, color_group_means_180_days[['customer_id', 'f_mean_color_group_180_days']], on='customer_id', how='left')
    
    # Return F with X.index and row order
    F = F.drop(columns=['customer_id'])
    return F
