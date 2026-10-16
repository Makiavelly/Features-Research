def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute the number of purchases in the last 180 days for each customer-article pair
    last_180_days = history[history['days_ago'] <= 180][['customer_id', 'article_id']]
    last_180_days = last_180_days.merge(X[['customer_id', 'article_id']], on=['customer_id', 'article_id'], how='left')
    F['f_last_180_days'] = last_180_days.groupby(['customer_id', 'article_id'])['customer_id'].count()
    
    # Compute the average price of purchases in the last 180 days for each customer-article pair
    F['f_avg_price_last_180_days'] = last_180_days.groupby(['customer_id', 'article_id'])['price'].transform('mean')
    
    # Compute the number of purchases in the last 7 days for each customer-article pair
    last_7_days = history[history['days_ago'] <= 7][['customer_id', 'article_id']]
    last_7_days = last_7_days.merge(X[['customer_id', 'article_id']], on=['customer_id', 'article_id'], how='left')
    F['f_last_7_days'] = last_7_days.groupby(['customer_id', 'article_id'])['customer_id'].count()
    
    # Compute the average age of customers who made purchases in the last 180 days for each article
    F['f_avg_customer_age_article_last_180_days'] = history[history['days_ago'] <= 180].groupby('article_id')['customer_age'].transform('mean')
    
    return F
