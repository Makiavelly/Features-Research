def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute average purchase price for each customer in the last 180 days
    avg_price = history.groupby('customer_id')['price'].mean().reindex(X['customer_id'].unique()).fillna(0)
    F['f_avg_price'] = X['customer_id'].map(avg_price)
    
    # Compute average number of past purchases for each customer in the last 180 days
    past_purchases = history.groupby('customer_id')['days_ago'].count().reindex(X['customer_id'].unique()).fillna(0)
    F['f_past_purchases'] = X['customer_id'].map(past_purchases)
    
    # Compute average age of customers who made purchases in the last 180 days
    avg_age = history.groupby('customer_id')['customer_age'].mean().reindex(X['customer_id'].unique()).fillna(0)
    F['f_avg_age'] = X['customer_id'].map(avg_age)
    
    # Compute average purchase price per product category for each customer in the last 180 days
    avg_price_product_category = history.groupby(['customer_id', 'product_code'])['price'].mean().reindex(X['customer_id'].unique(), level=0).unstack('product_code').fillna(0)
    F[['f_avg_price_product_category_1', 'f_avg_price_product_category_2']] = F['customer_id'].map(avg_price_product_category)
    
    return F
