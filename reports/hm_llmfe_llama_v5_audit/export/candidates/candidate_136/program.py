def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute average purchase price for each customer in the last 180 days
    avg_price = history[history['days_ago'] <= 180].groupby('customer_id')['price'].mean().reindex(X['customer_id'].unique()).fillna(0)
    F['f_avg_price'] = X['customer_id'].map(avg_price)
    
    # Compute average age of customers who made purchases in the last 180 days
    avg_age = history[history['days_ago'] <= 180].groupby('customer_id')['customer_age'].mean().reindex(X['customer_id'].unique()).fillna(0)
    F['f_avg_age'] = X['customer_id'].map(avg_age)
    
    # Compute average number of past purchases per day for each customer in the last 30 days
    past_purchases_30_days = history[history['days_ago'] <= 30].groupby('customer_id')['days_ago'].count().reindex(X['customer_id'].unique()).fillna(0)
    F['f_past_purchases_30_days'] = X['customer_id'].map(past_purchases_30_days)
    
    # Compute number of past purchases for each customer in the last 180 days
    past_purchases = history[history['days_ago'] <= 180].groupby('customer_id')['days_ago'].count().reindex(X['customer_id'].unique()).fillna(0)
    F['f_past_purchases'] = X['customer_id'].map(past_purchases)
    
    # Compute average purchase price per day for each customer in the last 30 days
    avg_price_30_days = history[history['days_ago'] <= 30].groupby('customer_id')['price'].mean().reindex(X['customer_id'].unique()).fillna(0)
    F['f_avg_price_30_days'] = X['customer_id'].map(avg_price_30_days)
    
    # Compute number of different article types purchased by each customer in the last 180 days
    article_types = history[history['days_ago'] <= 180].groupby('customer_id')['article_id'].nunique().reindex(X['customer_id'].unique()).fillna(0)
    F['f_article_types'] = X['customer_id'].map(article_types)
    
    return F
