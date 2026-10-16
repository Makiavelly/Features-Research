def modify_features(X, history):
    # Calculate average price per customer
    avg_price_per_customer = history.groupby('customer_id')['price'].mean().to_frame('avg_price')
    
    # Calculate average sales channel per customer
    avg_sales_channel_per_customer = history.groupby('customer_id')['sales_channel_id'].mean().to_frame('avg_sales_channel')
    
    # Calculate most recent product type per customer
    recent_product_type_per_customer = history.groupby('customer_id')['product_type_no'].last().to_frame('recent_product_type')
    
    # Calculate most recent perceived color value per customer
    recent_perceived_color_value_per_customer = history.groupby('customer_id')['perceived_colour_value_id'].last().to_frame('recent_perceived_color_value')
    
    # Groupby customer_id and assign the required columns
    F = history.groupby('customer_id')[['avg_price', 'avg_sales_channel','recent_product_type','recent_perceived_color_value']].mean()
    
    # Perform left merge on X with F, drop unnecessary columns, and reindex to match X's index
    F = pd.merge(X, F, on='customer_id', how='left', validate='many_to_one')
    F = F.drop(['avg_price', 'avg_sales_channel','recent_product_type','recent_perceived_color_value'], axis=1)
    F = F.reindex(columns=X.columns.tolist() + ['f_avg_price', 'f_avg_sales_channel', 'f_recent_product_type', 'f_recent_perceived_color_value'])
    
    # Positional assignment of numeric features from F to the result
    F['f_avg_price'] = F.pop('avg_price')
    F['f_avg_sales_channel'] = F.pop('avg_sales_channel')
    F['f_recent_product_type'] = F.pop('recent_product_type')
    F['f_recent_perceived_color_value'] = F.pop('recent_perceived_color_value')
    
    return F
