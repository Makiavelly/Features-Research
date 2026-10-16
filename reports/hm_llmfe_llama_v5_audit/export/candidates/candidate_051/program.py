def modify_features(X, history):
    # Compute average customer age
    avg_customer_age = history.groupby('customer_id')['customer_age'].mean().to_frame('f_avg_customer_age')
    
    # Compute count of purchases in the last 7 days
    recent_purchases = history[history['days_ago'] <= 7].groupby('customer_id')['article_id'].nunique().to_frame('f_recent_purchases')
    
    # Compute count of different product types purchased in the last 7 days
    recent_product_types = history[history['days_ago'] <= 7].groupby('customer_id')['product_type_no'].nunique().to_frame('f_recent_product_types')
    
    # Compute average price of purchases in the last 7 days
    recent_prices = history[history['days_ago'] <= 7].groupby('customer_id')['price'].mean().to_frame('f_recent_average_price')
    
    # Compute count of purchases from different sales channels in the last 7 days
    recent_sales_channels = history[history['days_ago'] <= 7].groupby('customer_id')['sales_channel_id'].nunique().to_frame('f_recent_sales_channels')
    
    # Merge aggregates with X using left join
    F = pd.merge(avg_customer_age, recent_purchases, on='customer_id', how='left', validate='many_to_one')
    F = pd.merge(F, recent_product_types, on='customer_id', how='left', validate='many_to_one')
    F = pd.merge(F, recent_prices, on='customer_id', how='left', validate='many_to_one')
    F = pd.merge(F, recent_sales_channels, on='customer_id', how='left', validate='many_to_one')
    
    # Remove NaN values from aggregated columns and assign values positionally to F
    F[['f_avg_customer_age', 'f_recent_purchases', 'f_recent_product_types', 'f_recent_average_price', 'f_recent_sales_channels']] = F[['f_avg_customer_age', 'f_recent_purchases', 'f_recent_product_types', 'f_recent_average_price', 'f_recent_sales_channels']].fillna(0)
    
    return F
