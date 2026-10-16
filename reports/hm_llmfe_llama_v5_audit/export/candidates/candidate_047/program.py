def modify_features(X, history):
    # Compute average purchase price for each customer in the last 180 days
    avg_price = history.groupby('customer_id')['price'].mean()
    
    # Compute average age of customers who made purchases in the last 180 days
    avg_age = history.groupby('customer_id')['customer_age'].mean()
    
    # Compute total number of past purchases for each customer in the last 30 days
    total_past_purchases = history[history['days_ago'] <= 180].groupby('customer_id')['days_ago'].count().to_dict()
    
    # Compute number of days since the last purchase for each customer
    days_since_last_purchase = history.groupby('customer_id')['days_ago'].max().to_dict()
    
    F = pd.DataFrame(index=X.index)
    F['f_avg_price'] = X['customer_id'].map(avg_price)
    F['f_avg_age'] = X['customer_id'].map(avg_age)
    F['f_total_past_purchases'] = X['customer_id'].map(total_past_purchases)
    F['f_days_since_last_purchase'] = X['customer_id'].map(days_since_last_purchase)
    
    return F
