def modify_features(X, history):
    # Calculate aggregate statistics for customer buying history within last 180 days
    days_ago_count = history[history['customer_id'].isin(X['customer_id'])].groupby('customer_id')['days_ago'].apply(lambda x: (x <= 180).sum())
    days_ago_mean = history[history['customer_id'].isin(X['customer_id'])].groupby('customer_id')['days_ago'].apply(lambda x: x[x <= 180].mean())
    days_ago_median = history[history['customer_id'].isin(X['customer_id'])].groupby('customer_id')['days_ago'].apply(lambda x: x[x <= 180].median())
    price_mean = history[history['customer_id'].isin(X['customer_id'])].groupby('customer_id')['price'].apply(lambda x: x[x <= 180].mean())
    price_median = history[history['customer_id'].isin(X['customer_id'])].groupby('customer_id')['price'].apply(lambda x: x[x <= 180].median())
    
    # Calculate customer age within last 180 days
    customer_age = history[history['customer_id'].isin(X['customer_id'])].groupby('customer_id')['customer_age'].apply(lambda x: x[x <= 180].mean())
    
    # Create a new DataFrame F with the same index as X
    F = pd.DataFrame(index=X.index)
    
    # Add the aggregate statistics as columns to F
    F['f_days_ago_count'] = days_ago_count[X.index]
    F['f_days_ago_mean'] = days_ago_mean[X.index]
    F['f_days_ago_median'] = days_ago_median[X.index]
    F['f_price_mean'] = price_mean[X.index]
    F['f_price_median'] = price_median[X.index]
    F['f_customer_age'] = customer_age[X.index]
    
    # Calculate the average number of past purchases for each customer
    past_purchases_count = history[history['customer_id'].isin(X['customer_id'])].groupby('customer_id')['days_ago'].apply(lambda x: x[x <= 180].count())
    F['f_past_purchases_count'] = past_purchases_count[X.index]
    
    # Calculate the average price of past purchases for each customer
    past_purchases_price_mean = history[history['customer_id'].isin(X['customer_id'])].groupby('customer_id')['price'].apply(lambda x: x[x <= 180].mean())
    F['f_past_purchases_price_mean'] = past_purchases_price_mean[X.index]
    
    return F
