def modify_features(X, history):
    # Aggregate history by customer_id to compute mean and count
    customer_history = history.groupby('customer_id').agg({
        'customer_age': ['mean', 'count']
    })['mean', 'count'].reset_index()
    customer_history.columns = ['customer_id','mean_customer_age', 'count_transactions']

    # Merge customer history into X with a left join
    merged_X = X.merge(customer_history[['customer_id','mean_customer_age', 'count_transactions']],
                       on='customer_id', validate='many_to_one', how='left')

    # Compute average price of past 30, 60, and 180 days
    price_averages = history.groupby('customer_id')['price'].agg({
       'mean_price_30_days': lambda x: x[x['days_ago'] <= 30].mean(),
       'mean_price_60_days': lambda x: x[(x['days_ago'] > 30) & (x['days_ago'] <= 60)].mean(),
       'mean_price_180_days': lambda x: x[x['days_ago'] <= 180].mean()
    }).reset_index()

    # Merge price averages into X with a left join
    merged_X = merged_X.merge(price_averages,
                              on='customer_id', validate='many_to_one', how='left')

    # Compute count of different product codes in past 180 days
    product_code_counts = history.groupby('customer_id')['product_code'].nunique().reset_index(name='count_product_codes')
    merged_X = merged_X.merge(product_code_counts,
                              on='customer_id', validate='many_to_one', how='left')

    # Compute mean of color group code in past 180 days
    color_group_mean = history[history['days_ago'] <= 180].groupby('customer_id')['colour_group_code'].mean().reset_index(name='mean_color_group')
    merged_X = merged_X.merge(color_group_mean,
                              on='customer_id', validate='many_to_one', how='left')

    # Extract relevant columns into a new DataFrame F and return it
    F = merged_X[['customer_id', 'article_id', 'f_mean_customer_age', 'f_count_transactions', 'f_mean_price_30_days', 'f_mean_price_60_days', 'f_mean_price_180_days', 'f_count_product_codes', 'f_mean_color_group']]
    F.columns = ['f_mean_customer_age', 'f_count_transactions', 'f_mean_price_30_days', 'f_mean_price_60_days', 'f_mean_price_180_days', 'f_count_product_codes', 'f_mean_color_group', 'customer_id', 'article_id']
    return F
