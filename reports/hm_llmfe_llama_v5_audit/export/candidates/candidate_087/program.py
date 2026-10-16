def modify_features(X, history):
    # Compute the average days_ago for each customer_id/article_id pair
    avg_days_ago = history.groupby(['customer_id', 'article_id'])['days_ago'].mean().reset_index(name='avg_days_ago')
    
    # Compute the average customer_age for each customer_id/article_id pair
    avg_customer_age = history.groupby(['customer_id', 'article_id'])['customer_age'].mean().reset_index(name='avg_customer_age')
    
    # Compute the number of past purchases for each customer_id/article_id pair
    past_purchases = history.groupby(['customer_id', 'article_id'])['price'].count().reset_index(name='past_purchases')
    
    # Merge the aggregates with X to preserve the left order
    merged_features = pd.merge(X, avg_days_ago[['customer_id', 'article_id', 'avg_days_ago']], on=['customer_id', 'article_id'], how='left')
    merged_features = pd.merge(merged_features, avg_customer_age[['customer_id', 'article_id', 'avg_customer_age']], on=['customer_id', 'article_id'], how='left')
    merged_features = pd.merge(merged_features, past_purchases[['customer_id', 'article_id', 'past_purchases']], on=['customer_id', 'article_id'], how='left')
    
    # Assign the average days_ago, average customer_age and number of past purchases to F
    F = merged_features[['customer_id', 'article_id', 'avg_days_ago', 'avg_customer_age', 'past_purchases']]
    
    # Replace NaN with 0 for numeric features
    F = F.fillna(0)
    
    return F
