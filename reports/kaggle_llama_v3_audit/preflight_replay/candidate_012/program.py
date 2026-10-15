def modify_features(X, history):
    """
    Generate up to 48 numeric columns named f_* using customer and clothing domain knowledge.
    
    Parameters:
    X (DataFrame): Candidate pairs with one row per pair.
    history (DataFrame): Past transactions without future data or labels.
    
    Returns:
    DataFrame: New features with exactly X.index and row order, plus 15 raw static features.
    """
    
    # Append the same 15 raw static features to the output
    X = pd.concat([X, history[['price','sales_channel_id', 'days_ago', 'customer_age', 'product_code', 'product_type_no', 
                               'graphical_appearance_no', 'colour_group_code', 'perceived_colour_value_id', 
                               'perceived_colour_master_id', 'department_no', 'index_group_no','section_no', 'garment_group_no']]], axis=1)
    
    # Calculate average age of customer
    X['f_avg_age'] = history.groupby('customer_id')['customer_age'].mean().reindex(X['customer_id']).fillna(0)
    
    # Calculate average customer account flags
    X['f_avg_fn'] = history.groupby('customer_id')['raw_u_fn'].mean().reindex(X['customer_id']).fillna(0)
    X['f_avg_active'] = history.groupby('customer_id')['raw_u_active'].mean().reindex(X['customer_id']).fillna(0)
    
    # Calculate average membership status
    X['f_avg_club_member_status'] = history.groupby('customer_id')['raw_u_club_member_status'].mean().reindex(X['customer_id']).fillna(0)
    
    # Calculate average fashion news frequency
    X['f_avg_fashion_news_frequency'] = history.groupby('customer_id')['raw_u_fashion_news_frequency'].mean().reindex(X['customer_id']).fillna(0)
    
    # Calculate average price of past purchases by customer
    X['f_avg_price'] = history.groupby('customer_id')['price'].mean().reindex(X['customer_id']).fillna(0)
    
    # Calculate average number of past purchases by customer
    X['f_avg_num_purchases'] = history.groupby('customer_id')['customer_id'].count().reindex(X['customer_id']).fillna(0)
    
    # Calculate average number of past purchases by article
    X['f_avg_num_article_purchases'] = history.groupby('article_id')['article_id'].count().reindex(X['article_id']).fillna(0)
    
    # Calculate average time since last purchase by customer
    X['f_avg_time_since_last_purchase'] = history.sort_values('days_ago').groupby('customer_id')['days_ago'].mean().reindex(X['customer_id']).fillna(0)
    
    # Calculate average time since last purchase by article
    X['f_avg_time_since_last_article_purchase'] = history.sort_values('days_ago').groupby('article_id')['days_ago'].mean().reindex(X['article_id']).fillna(0)
    
    # Calculate average sales channel for customer
    X['f_avg_sales_channel'] = history.groupby('customer_id')['sales_channel_id'].mean().reindex(X['customer_id']).fillna(0)
    
    # Calculate average product type for customer
    X['f_avg_product_type'] = history.groupby('customer_id')['product_type_no'].mean().reindex(X['customer_id']).fillna(0)
    
    # Calculate average number of purchased product types by customer
    X['f_avg_num_product_types'] = history.groupby('customer_id')['product_type_no'].nunique().reindex(X['customer_id']).fillna(0)
    
    return X
