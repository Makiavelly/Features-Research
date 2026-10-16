def modify_features(X, history):
    # Compute the average days_ago for each customer_id/article_id pair
    avg_days_ago = history.groupby(['customer_id', 'article_id'])['days_ago'].mean().reset_index()
    
    # Compute the average customer_age for each customer_id/article_id pair
    avg_customer_age = history.groupby(['customer_id', 'article_id'])['customer_age'].mean().reset_index()
    
    # Compute the number of past purchases for each customer_id/article_id pair
    past_purchases = history.groupby(['customer_id', 'article_id'])['price'].count().reset_index(name='past_purchases')
    
    # Compute the frequency of purchases for each customer_id/article_id pair
    purchase_frequency = history.groupby(['customer_id', 'article_id'])['days_ago'].unique().apply(lambda x: len(x)).reset_index(name='purchase_frequency')
    
    # Compute the average price for each customer_id/article_id pair
    avg_price = history.groupby(['customer_id', 'article_id'])['price'].mean().reset_index(name='avg_price')
    
    # Merge the aggregates with X to preserve the left order
    merged_avg_days_ago = X.merge(avg_days_ago[['customer_id', 'article_id', 'days_ago']], on=['customer_id', 'article_id'], how='left')
    merged_avg_days_ago = merged_avg_days_ago.merge(avg_customer_age[['customer_id', 'article_id', 'customer_age']], on=['customer_id', 'article_id'], how='left')
    merged_avg_days_ago = merged_avg_days_ago.merge(past_purchases[['customer_id', 'article_id', 'past_purchases']], on=['customer_id', 'article_id'], how='left')
    merged_avg_days_ago = merged_avg_days_ago.merge(purchase_frequency[['customer_id', 'article_id', 'purchase_frequency']], on=['customer_id', 'article_id'], how='left')
    merged_avg_days_ago = merged_avg_days_ago.merge(avg_price[['customer_id', 'article_id', 'avg_price']], on=['customer_id', 'article_id'], how='left')
    
    # Assign the average days_ago, average customer_age, number of past purchases, purchase frequency and average price to F
    F = pd.DataFrame(merged_avg_days_ago[['customer_id', 'article_id', 'days_ago', 'customer_age', 'past_purchases', 'purchase_frequency', 'avg_price']].values, index=X.index)
    
    # Replace NaN with 0 for numeric features
    F = F.fillna(0)
    
    return F
