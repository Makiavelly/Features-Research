def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute average purchase price for each customer in the last 180 days
    avg_price = history.groupby('customer_id')['price'].mean().reindex(X['customer_id'].unique()).fillna(0)
    F['f_avg_price'] = X['customer_id'].map(avg_price)
    
    # Compute number of past purchases for each customer in the last 180 days
    past_purchases = history[history['days_ago'] <= 180].groupby('customer_id')['days_ago'].nunique().reindex(X['customer_id'].unique()).fillna(0)
    F['f_past_purchases'] = X['customer_id'].map(past_purchases)
    
    # Compute average age of customers who made purchases in the last 180 days
    avg_age = history[history['days_ago'] <= 180].groupby('customer_id')['customer_age'].mean().reindex(X['customer_id'].unique()).fillna(0)
    F['f_avg_age'] = X['customer_id'].map(avg_age)
    
    # Compute average purchase value of each item type for each customer in the last 180 days
    avg_item_value = history[history['days_ago'] <= 180].groupby(['customer_id', 'article_id'])['price'].mean().groupby('customer_id').mean().reindex(X['customer_id'].unique()).fillna(0)
    F['f_avg_item_value'] = X['customer_id'].map(avg_item_value)
    
    # Compute ratio of past purchases to customer age for each customer in the last 180 days
    purchase_ratio = history[history['days_ago'] <= 180].groupby('customer_id')['days_ago'].nunique().div(history[history['days_ago'] <= 180].groupby('customer_id')['customer_age'].mean()).reindex(X['customer_id'].unique()).fillna(0)
    F['f_purchase_ratio'] = X['customer_id'].map(purchase_ratio)
    
    return F
