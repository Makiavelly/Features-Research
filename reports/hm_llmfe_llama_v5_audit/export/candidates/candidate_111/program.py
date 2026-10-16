def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute the number of purchases in the last 180 days for each customer-article pair
    F['f_last_180_days'] = (
        history[history['days_ago'] <= 180]
        [['customer_id', 'article_id']]
       .merge(X[['customer_id', 'article_id']], on=['customer_id', 'article_id'], how='left')
       .groupby(['customer_id', 'article_id'])['price']
       .count()
       .reindex(F.index)
       .fillna(0)
       .astype(int)
    )
    
    # Compute the average price of purchases in the last 180 days for each customer-article pair
    F['f_avg_price'] = (
        history[history['days_ago'] <= 180]
        [['customer_id', 'article_id']]
       .merge(X[['customer_id', 'article_id']], on=['customer_id', 'article_id'], how='left')
       .groupby(['customer_id', 'article_id'])['price']
       .mean()
       .reindex(F.index)
       .fillna(0)
    )
    
    # Compute the number of purchases in the last 7 days for each customer-article pair
    F['f_last_7_days'] = (
        history[history['days_ago'] <= 7]
        [['customer_id', 'article_id']]
       .merge(X[['customer_id', 'article_id']], on=['customer_id', 'article_id'], how='left')
       .groupby(['customer_id', 'article_id'])['price']
       .count()
       .reindex(F.index)
       .fillna(0)
       .astype(int)
    )
    
    # Compute the average age of customers who made purchases in the last 180 days for each article
    F['f_avg_customer_age_article'] = (
        history[history['days_ago'] <= 180]
        [['article_id']]
       .merge(X[['article_id']], on=['article_id'], how='left')
       .groupby('article_id')['customer_age']
       .mean()
       .reindex(F.index)
       .fillna(0)
    )
    
    # Compute the average age of customers who made purchases in the last 7 days for each article
    F['f_avg_customer_age_article_last_7_days'] = (
        history[history['days_ago'] <= 7]
        [['article_id']]
       .merge(X[['article_id']], on=['article_id'], how='left')
       .groupby('article_id')['customer_age']
       .mean()
       .reindex(F.index)
       .fillna(0)
    )
    
    return F
