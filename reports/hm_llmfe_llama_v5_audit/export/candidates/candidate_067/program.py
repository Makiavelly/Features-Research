def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute the average price for each article over the last 180 days
    avg_price = history[history['days_ago'] <= 180].groupby('article_id')['price'].mean().to_frame('avg_price')
    avg_price.columns = ['f_avg_price']
    
    # Compute the number of purchases for each customer over the last 180 days
    num_purchases = history[history['days_ago'] <= 180].groupby('customer_id')['article_id'].nunique().to_frame('num_purchases')
    num_purchases.columns = ['f_num_purchases']
    
    # Compute the average age of customers who purchased each article over the last 180 days
    avg_customer_age = history[history['days_ago'] <= 180].merge(avg_price, on='article_id', how='left').groupby('article_id')['customer_age'].mean().to_frame('f_avg_customer_age')
    
    # Merge the results into a single DataFrame
    result = pd.concat([num_purchases, avg_price, avg_customer_age], axis=1)
    
    # Reindex and assign the results to the positionally indexed F
    F = result.reindex(index=X['article_id']).reindex(columns=X.columns.tolist() + ['f_avg_price', 'f_num_purchases', 'f_avg_customer_age'])
    
    return F
