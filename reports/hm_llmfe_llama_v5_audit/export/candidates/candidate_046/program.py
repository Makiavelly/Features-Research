def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute average purchase price for each customer in the last 180 days
    avg_price = history.groupby('customer_id')['price'].mean()
    F['f_avg_price'] = X['customer_id'].map(avg_price)
    
    # Compute average age of customers who made purchases in the last 180 days
    avg_age = history.groupby('customer_id')['customer_age'].mean()
    F['f_avg_age'] = X['customer_id'].map(avg_age)
    
    # Compute average number of past purchases for each customer in the last 180 days
    past_purchases = history.groupby('customer_id')['days_ago'].count()
    F['f_past_purchases'] = X['customer_id'].map(past_purchases)
    
    # Compute average product type for each customer in the last 180 days
    avg_product_type = history.groupby('customer_id')['product_type_no'].mean()
    F['f_avg_product_type'] = X['customer_id'].map(avg_product_type)
    
    return F
