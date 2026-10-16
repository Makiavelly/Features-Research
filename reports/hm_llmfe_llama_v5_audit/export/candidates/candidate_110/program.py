def modify_features(X, history):
    # Calculate average price per customer
    avg_price_per_customer = history.groupby('customer_id')['price'].mean().to_frame('f_avg_price')
    
    # Calculate average sales channel per customer
    avg_sales_channel_per_customer = history.groupby('customer_id')['sales_channel_id'].mean().to_frame('f_avg_sales_channel')
    
    # Calculate most recent product type per customer
    recent_product_type_per_customer = history.groupby('customer_id')['product_type_no'].last().to_frame('f_recent_product_type')
    
    # Calculate most recent perceived color value per customer
    recent_perceived_color_value_per_customer = history.groupby('customer_id')['perceived_colour_value_id'].last().to_frame('f_recent_perceived_color_value')
    
    # Compute the number of past purchases per customer
    past_purchases_per_customer = history.groupby('customer_id')['article_id'].count().to_frame('f_past_purchases')
    
    # Compute the average price per purchase per customer
    avg_price_per_purchase = history.groupby('customer_id')['price'].mean().to_frame('f_avg_price_per_purchase')
    
    # Perform left merge on history with aggregates
    F = pd.merge(history, avg_price_per_customer, on='customer_id', how='left')
    
    F = pd.merge(F, avg_sales_channel_per_customer, on='customer_id', how='left')
    
    F = pd.merge(F, recent_product_type_per_customer, on='customer_id', how='left')
    
    F = pd.merge(F, recent_perceived_color_value_per_customer, on='customer_id', how='left')
    
    F = pd.merge(F, past_purchases_per_customer, on='customer_id', how='left')
    
    F = pd.merge(F, avg_price_per_purchase, on='customer_id', how='left')
    
    # Compute the number of past purchases per customer in the last 180 days
    recent_past_purchases_per_customer = history[history['days_ago'] <= 180].groupby('customer_id')['article_id'].count().to_frame('f_recent_past_purchases')
    
    # Perform left merge on F with recent past purchases
    F = pd.merge(F, recent_past_purchases_per_customer, on='customer_id', how='left')
    
    # Perform left merge on X with F, drop unnecessary columns, and reindex to match X's index
    F = pd.merge(F, X[['customer_id', 'article_id']], on=['customer_id'], how='left')
    F = F.drop(['customer_id'], axis=1)
    
    return F[['article_id'] + list(F.columns)[-6:]]  # Return only f_* features in unchanged X order
