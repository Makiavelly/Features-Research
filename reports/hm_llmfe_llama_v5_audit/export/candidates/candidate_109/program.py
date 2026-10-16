def modify_features(X, history):
    # Calculate average price per customer
    avg_price_per_customer = history.groupby('customer_id')['price'].mean().to_frame('avg_price')
    
    # Calculate average sales channel per customer
    avg_sales_channel_per_customer = history.groupby('customer_id')['sales_channel_id'].map(lambda x: x.mean()).to_frame('avg_sales_channel')
    
    # Calculate most recent product type per customer
    recent_product_type_per_customer = history.groupby('customer_id')['product_type_no'].last().to_frame('recent_product_type')
    
    # Calculate most recent perceived color value per customer
    recent_perceived_color_value_per_customer = history.groupby('customer_id')['perceived_colour_value_id'].last().to_frame('recent_perceived_color_value')
    
    # Compute the number of past purchases per customer
    past_purchases_per_customer = history.groupby('customer_id')['article_id'].count().to_frame('past_purchases')
    
    # Compute the average price per purchase per customer
    avg_price_per_purchase = history.groupby('customer_id')['price'].mean().to_frame('avg_price_per_purchase')
    
    # Perform left merge on history with aggregates, drop unnecessary columns, and reindex to match history's index
    F = pd.merge(history, avg_price_per_customer, on='customer_id', how='left')
    F = F.drop(['customer_id'], axis=1)
    F = F.rename(columns={'avg_price': 'f_avg_price'})
    
    F = pd.merge(F, avg_sales_channel_per_customer, on='customer_id', how='left')
    F = F.drop(['customer_id'], axis=1)
    F = F.rename(columns={'avg_sales_channel': 'f_avg_sales_channel'})
    
    F = pd.merge(F, recent_product_type_per_customer, on='customer_id', how='left')
    F = F.drop(['customer_id'], axis=1)
    F = F.rename(columns={'recent_product_type': 'f_recent_product_type'})
    
    F = pd.merge(F, recent_perceived_color_value_per_customer, on='customer_id', how='left')
    F = F.drop(['customer_id'], axis=1)
    F = F.rename(columns={'recent_perceived_color_value': 'f_recent_perceived_color_value'})
    
    F = pd.merge(F, past_purchases_per_customer, on='customer_id', how='left')
    F = F.drop(['customer_id'], axis=1)
    F = F.rename(columns={'past_purchases': 'f_past_purchases'})
    
    F = pd.merge(F, avg_price_per_purchase, on='customer_id', how='left')
    F = F.drop(['customer_id'], axis=1)
    F = F.rename(columns={'avg_price_per_purchase': 'f_avg_price_per_purchase'})
    
    # Perform left merge on X with F, drop unnecessary columns, and reindex to match X's index
    F = pd.merge(F, X, on=['article_id'], how='left')
    F = F.drop(['article_id'], axis=1)
    F = F.rename(columns={'f_avg_price': 'f_avg_price', 'f_avg_sales_channel': 'f_avg_sales_channel',
                         'f_recent_product_type': 'f_recent_product_type', 'f_recent_perceived_color_value': 'f_recent_perceived_color_value',
                         'f_past_purchases': 'f_past_purchases', 'f_avg_price_per_purchase': 'f_avg_price_per_purchase'})
    
    return F
