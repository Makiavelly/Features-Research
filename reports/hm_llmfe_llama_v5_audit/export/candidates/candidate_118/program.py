def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    # Compute the number of purchases in the last 7 days
    last_7_days_purchases = history[(history['days_ago'] <= 7)].groupby(['customer_id', 'article_id'])['price'].count().reset_index(name='last_7_days_purchases')
    
    # Compute the number of purchases in the last 180 days
    last_180_days_purchases = history[(history['days_ago'] <= 180)].groupby(['customer_id', 'article_id'])['price'].count().reset_index(name='last_180_days_purchases')
    
    # Compute the average price of purchases
    avg_price = history.groupby(['customer_id', 'article_id'])['price'].mean().reset_index(name='avg_price')
    
    # Merge the last 7 days purchases with F
    F = pd.merge(F, last_7_days_purchases, on=['customer_id', 'article_id'], how='left', validate='many_to_one')
    F['f_last_7_days_purchases'] = (F['last_7_days_purchases'].fillna(0) / (F['days_ago'] + 1)).astype(float)
    
    # Merge the last 180 days purchases with F
    F = pd.merge(F, last_180_days_purchases, on=['customer_id', 'article_id'], how='left', validate='many_to_one')
    F['f_last_180_days_purchases'] = (F['last_180_days_purchases'].fillna(0) / (F['days_ago'] + 1)).astype(float)
    
    # Merge the average price with F
    F = pd.merge(F, avg_price, on=['customer_id', 'article_id'], how='left', validate='many_to_one')
    F['f_avg_price'] = F['avg_price'].fillna(0)
    
    # Filter the history to get the customers and articles in X
    filtered_history = history[history['customer_id'].isin(X['customer_id']) & history['article_id'].isin(X['article_id'])]
    
    # Compute the average customer age for the customers in X
    avg_customer_age = filtered_history.groupby(['customer_id'])['customer_age'].mean().reset_index(name='avg_customer_age')
    
    # Merge the average customer age with F
    F = pd.merge(F, avg_customer_age, on='customer_id', how='left', validate='many_to_one')
    
    return F
