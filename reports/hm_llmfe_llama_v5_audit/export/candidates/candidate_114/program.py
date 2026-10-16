def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute the number of purchases in the last 7 days for each customer-article pair
    last_7_days = history[history['days_ago'] <= 7][['customer_id', 'article_id']]
    F['f_last_7_days'] = (
        last_7_days.groupby(['customer_id', 'article_id'])['customer_id']
       .apply(lambda x: x.nunique())
       .reset_index(level=0, drop=True)
    )
    
    # Compute the number of purchases in the last 180 days for each customer-article pair
    last_180_days = history[history['days_ago'] <= 180][['customer_id', 'article_id']]
    F['f_last_180_days'] = (
        last_180_days.groupby(['customer_id', 'article_id'])['customer_id']
       .apply(lambda x: x.nunique())
       .reset_index(level=0, drop=True)
    )
    
    # Compute the average price of purchases in the last 7 days for each customer-article pair
    last_7_days_price = last_7_days.merge(history[['customer_id', 'article_id', 'price']], on=['customer_id', 'article_id'], how='left')
    F['f_avg_price_last_7_days'] = (
        last_7_days_price.groupby(['customer_id', 'article_id'])['price']
       .mean()
       .reset_index(level=0, drop=True)
    )
    
    # Compute the average price of purchases in the last 180 days for each customer-article pair
    last_180_days_price = last_180_days.merge(history[['customer_id', 'article_id', 'price']], on=['customer_id', 'article_id'], how='left')
    F['f_avg_price_last_180_days'] = (
        last_180_days_price.groupby(['customer_id', 'article_id'])['price']
       .mean()
       .reset_index(level=0, drop=True)
    )
    
    # Compute the average age of customers who made purchases in the last 7 days for each article
    last_7_days_age = last_7_days.merge(history[['customer_id', 'article_id', 'customer_age']], on=['customer_id', 'article_id'], how='left')
    F['f_avg_customer_age_article_last_7_days'] = (
        last_7_days_age.groupby(['article_id'])['customer_age']
       .mean()
       .reset_index(level=0, drop=True)
    )
    
    # Compute the average age of customers who made purchases in the last 180 days for each article
    last_180_days_age = last_180_days.merge(history[['customer_id', 'article_id', 'customer_age']], on=['customer_id', 'article_id'], how='left')
    F['f_avg_customer_age_article_last_180_days'] = (
        last_180_days_age.groupby(['article_id'])['customer_age']
       .mean()
       .reset_index(level=0, drop=True)
    )
    
    return F
