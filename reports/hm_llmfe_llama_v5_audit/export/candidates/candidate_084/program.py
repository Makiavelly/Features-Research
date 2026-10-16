def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    # Calculate aggregate statistics for customer buying history within last 180 days
    last180 = history[(history['customer_id'].isin(X['customer_id'])) & (history['days_ago'] <= 180)]
    days_ago_count = last180.groupby('customer_id')['days_ago'].count().reindex(X['customer_id']).fillna(0)
    days_ago_mean = last180.groupby('customer_id')['days_ago'].mean().reindex(X['customer_id']).fillna(0)
    days_ago_median = last180.groupby('customer_id')['days_ago'].median().reindex(X['customer_id']).fillna(0)
    price_mean = last180.groupby('customer_id')['price'].mean().reindex(X['customer_id']).fillna(0)
    price_median = last180.groupby('customer_id')['price'].median().reindex(X['customer_id']).fillna(0)
    
    # Create a new DataFrame F with the same index as X
    F['f_days_ago_count'] = days_ago_count
    F['f_days_ago_mean'] = days_ago_mean
    F['f_days_ago_median'] = days_ago_median
    F['f_price_mean'] = price_mean
    F['f_price_median'] = price_median
    
    # Calculate customer age within last 180 days
    last180_age = last180.groupby('customer_id')['customer_age'].mean().reindex(X['customer_id']).fillna(0)
    F['f_customer_age'] = last180_age
    
    # Calculate the average number of past purchases for each customer
    past_purchases_count = last180.groupby('customer_id')['days_ago'].count().reindex(X['customer_id']).fillna(0)
    F['f_past_purchases_count'] = past_purchases_count
    
    # Calculate the average price of past purchases for each customer
    past_purchases_price_mean = last180.groupby('customer_id')['price'].mean().reindex(X['customer_id']).fillna(0)
    F['f_past_purchases_price_mean'] = past_purchases_price_mean
    
    return F
