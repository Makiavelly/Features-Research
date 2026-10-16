def modify_features(X, history):
    # Compute the average days_ago for each customer_id/article_id pair
    avg_days_ago = history.groupby(['customer_id', 'article_id'])['days_ago'].mean().reset_index(name='avg_days_ago')
    
    # Compute the average customer_age for each customer_id/article_id pair
    avg_customer_age = history.groupby(['customer_id', 'article_id'])['customer_age'].mean().reset_index(name='avg_customer_age')
    
    # Compute the average price for each customer_id/article_id pair
    avg_price = history.groupby(['customer_id', 'article_id'])['price'].mean().reset_index(name='avg_price')
    
    # Compute the number of article_ids each customer_id has purchased within the last 180 days
    count_article_ids = history.groupby(['customer_id'])['article_id'].nunique().reset_index(name='count_article_ids')
    
    # Merge the aggregates with X to preserve the left order
    merged_features = pd.merge(X, avg_days_ago[['customer_id', 'article_id', 'avg_days_ago']], on='customer_id', how='left')
    merged_features = pd.merge(merged_features, avg_customer_age[['customer_id', 'article_id', 'avg_customer_age']], on='customer_id', how='left')
    merged_features = pd.merge(merged_features, avg_price[['customer_id', 'article_id', 'avg_price']], on='customer_id', how='left')
    merged_features = pd.merge(merged_features, count_article_ids[['customer_id', 'count_article_ids']], on='customer_id', how='left')
    
    # Assign the average days_ago, average customer_age, average price and number of article_ids purchased within the last 180 days to F
    F = merged_features[['customer_id', 'article_id', 'avg_days_ago', 'avg_customer_age', 'avg_price', 'count_article_ids']]
    
    # Replace NaN with 0 for numeric features
    F = F.fillna(0)
    
    return F
