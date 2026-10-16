def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Calculate average purchase price for each customer in the last 180 days
    avg_price = history[history['days_ago'] <= 180].groupby('customer_id')['price'].mean()
    F['f_avg_price'] = X['customer_id'].map(avg_price)
    
    # Calculate average age of customers who made purchases in the last 180 days
    avg_age = history[history['days_ago'] <= 180].groupby('customer_id')['customer_age'].mean()
    F['f_avg_age'] = X['customer_id'].map(avg_age)
    
    # Calculate average number of past purchases for each customer in the last 180 days
    past_purchases = history[history['days_ago'] <= 180].groupby('customer_id')['days_ago'].count()
    F['f_past_purchases'] = X['customer_id'].map(past_purchases)
    
    # Calculate average purchase price per day for each customer in the last 30 days
    avg_price_30_days = history[history['days_ago'] <= 30].groupby('customer_id')['price'].mean()
    F['f_avg_price_30_days'] = X['customer_id'].map(avg_price_30_days)
    
    # Calculate average number of past purchases per day for each customer in the last 30 days
    past_purchases_30_days = history[history['days_ago'] <= 30].groupby('customer_id')['days_ago'].count()
    F['f_past_purchases_30_days'] = X['customer_id'].map(past_purchases_30_days)
    
    # Calculate the number of different product categories each customer has purchased in the last 180 days
    product_categories = history[history['days_ago'] <= 180].groupby('customer_id')['product_code'].nunique()
    F['f_product_categories'] = X['customer_id'].map(product_categories)
    
    return F
