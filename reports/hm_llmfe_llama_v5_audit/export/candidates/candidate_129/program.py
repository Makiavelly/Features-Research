def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    # Calculate average price per customer within the same article type
    avg_price_per_customer_per_article = history.merge(X, on='article_id')[['customer_id', 'price']].groupby('customer_id')['price'].mean().reset_index()
    F['f_avg_price_per_customer_per_article'] = avg_price_per_customer_per_article.set_index('customer_id')['price'].reindex(X['customer_id']).fillna(0)
    
    # Calculate number of purchases per customer within the same article type
    num_purchases_per_customer_per_article = history.merge(X, on='article_id')[['customer_id', 'customer_id']].groupby('customer_id')['customer_id'].count().reset_index()
    F['f_num_purchases_per_customer_per_article'] = num_purchases_per_customer_per_article.set_index('customer_id')['customer_id'].reindex(X['customer_id']).fillna(0)
    
    # Calculate average days ago per customer within the same article type
    avg_days_ago_per_customer_per_article = history.merge(X, on='article_id')[['customer_id', 'days_ago']].groupby('customer_id')['days_ago'].mean().reset_index()
    F['f_avg_days_ago_per_customer_per_article'] = avg_days_ago_per_customer_per_article.set_index('customer_id')['days_ago'].reindex(X['customer_id']).fillna(0)
    
    # Calculate average purchase frequency per customer within the same article type
    avg_purchase_frequency_per_customer_per_article = history.merge(X, on='article_id')[['customer_id', 'days_ago']].groupby('customer_id')['days_ago'].mean().reset_index()
    F['f_avg_purchase_frequency_per_customer_per_article'] = avg_purchase_frequency_per_customer_per_article.set_index('customer_id')['days_ago'].reindex(X['customer_id']).fillna(0)
    
    return F
