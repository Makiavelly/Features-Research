def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    # Compute the average price for each article over the last 180 days
    avg_price = history[history['days_ago'] <= 180].groupby('article_id')['price'].mean().to_frame('f_avg_price')
    
    # Compute the number of purchases for each customer over the last 180 days
    num_purchases = history[history['days_ago'] <= 180].groupby('customer_id')['article_id'].nunique().to_frame('f_num_purchases')
    
    # Compute the average age of customers who purchased each article over the last 180 days
    avg_customer_age = history[history['days_ago'] <= 180].groupby('article_id')['customer_age'].mean().to_frame('f_avg_customer_age')
    
    # Merge the results into a single DataFrame
    F = pd.merge(avg_price, num_purchases, on='article_id', how='left')
    F = pd.merge(F, avg_customer_age, on='article_id', how='left')
    
    # Drop non-key columns and assign the results to the positionally indexed F
    F = F[['customer_id', 'article_id', 'f_avg_price', 'f_num_purchases', 'f_avg_customer_age']]
    F = F.reindex(columns=F.columns.tolist() + X.columns.tolist())
    
    return F
