def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Calculate average price per customer
    avg_price_per_customer = history.groupby('customer_id')['price'].mean().reset_index()
    F['f_avg_price_per_customer'] = avg_price_per_customer.set_index('customer_id')['price'].reindex(X['customer_id']).fillna(0)
    
    # Calculate average days ago per customer
    avg_days_ago_per_customer = history.groupby('customer_id')['days_ago'].mean().reset_index()
    F['f_avg_days_ago_per_customer'] = avg_days_ago_per_customer.set_index('customer_id')['days_ago'].reindex(X['customer_id']).fillna(0)
    
    # Calculate average purchase frequency per customer
    avg_purchase_frequency_per_customer = history.groupby('customer_id')['days_ago'].mean().reset_index()
    F['f_avg_purchase_frequency_per_customer'] = avg_purchase_frequency_per_customer.set_index('customer_id')['days_ago'].reindex(X['customer_id']).fillna(0)
    
    # Calculate number of purchases per customer
    num_purchases_per_customer = history.groupby('customer_id')['days_ago'].count().reset_index()
    F['f_num_purchases_per_customer'] = num_purchases_per_customer.set_index('customer_id')['days_ago'].reindex(X['customer_id']).fillna(0)
    
    # Calculate average product type no per article
    avg_product_type_no_per_article = history.groupby('article_id')['product_type_no'].mean().reset_index()
    F['f_avg_product_type_no_per_article'] = avg_product_type_no_per_article.set_index('article_id')['product_type_no'].reindex(X['article_id']).fillna(0)
    
    return F
