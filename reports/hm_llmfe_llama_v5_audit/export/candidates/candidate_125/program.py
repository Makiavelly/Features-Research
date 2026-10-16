def modify_features(X, history):
    # Calculate the count of past purchases for each customer within the last 180 days
    past_purchases = history[history['days_ago'] <= 180]
    past_purchases = past_purchases.groupby('customer_id')['article_id'].nunique().reset_index()
    past_purchases = past_purchases.rename(columns={'article_id': 'f_past_purchases'})

    # Calculate the average purchase price for each customer within the last 180 days
    avg_price = history[history['days_ago'] <= 180].groupby('customer_id')['price'].mean().reset_index()
    avg_price = avg_price.rename(columns={'price': 'f_avg_price'})

    # Merge the aggregates with X on customer_id
    F = past_purchases.merge(X[['customer_id']], on='customer_id')
    F = F.merge(avg_price[['customer_id', 'f_avg_price']], on='customer_id', how='left', validate='many_to_one')
    
    return F
