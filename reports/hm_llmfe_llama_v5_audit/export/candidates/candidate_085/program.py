def modify_features(X, history):
    # Aggregate the history to compute the average days_ago for each customer_id/article_id pair
    avg_days_ago = history.groupby(['customer_id', 'article_id'])['days_ago'].mean().reset_index()
    
    # Aggregate the history to compute the average customer_age for each customer_id/article_id pair
    avg_customer_age = history.groupby(['customer_id', 'article_id'])['customer_age'].mean().reset_index()
    
    # Merge the aggregates with X to preserve the left order
    merged_avg_days_ago = X.merge(avg_days_ago, on=['customer_id', 'article_id'], how='left')
    merged_avg_days_ago = merged_avg_days_ago.merge(avg_customer_age, on=['customer_id', 'article_id'], how='left')
    
    # Compute the number of past purchases for each customer_id/article_id pair
    past_purchases = history.groupby(['customer_id', 'article_id']).size().reset_index(name='past_purchases')
    
    # Merge past_purchases with X to preserve the left order
    merged_past_purchases = merged_avg_days_ago.merge(past_purchases, on=['customer_id', 'article_id'], how='left')
    
    # Compute the frequency of purchases for each customer_id/article_id pair
    purchase_frequency = history.groupby(['customer_id', 'article_id'])['days_ago'].nunique().reset_index(name='purchase_frequency')
    
    # Merge purchase_frequency with merged_past_purchases to preserve the left order
    merged_purchase_frequency = merged_past_purchases.merge(purchase_frequency, on=['customer_id', 'article_id'], how='left')
    
    # Compute the average price for each customer_id/article_id pair
    avg_price = history.groupby(['customer_id', 'article_id'])['price'].mean().reset_index(name='avg_price')
    
    # Merge avg_price with merged_purchase_frequency to preserve the left order
    merged_avg_price = merged_purchase_frequency.merge(avg_price, on=['customer_id', 'article_id'], how='left')
    
    # Assign the average days_ago, average customer_age, number of past purchases, purchase frequency and average price to F
    F = pd.DataFrame(merged_avg_price[['customer_id', 'article_id', 'avg_days_ago', 'avg_customer_age', 'past_purchases', 'purchase_frequency', 'avg_price']].values, index=X.index)
    
    # Replace NaN with 0 for numeric features
    F = F.fillna(0)
    
    # Return F with exactly X.index and row order
    return F
