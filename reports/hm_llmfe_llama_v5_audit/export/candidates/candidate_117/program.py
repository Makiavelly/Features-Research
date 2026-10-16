def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute the number of purchases in the last 7 days
    last_7_days_purchases = history[(history['days_ago'] <= 7)].groupby(['customer_id', 'article_id'])['price'].count().reset_index(name='last_7_days_purchases')
    
    # Compute the number of purchases in the last 180 days
    last_180_days_purchases = history[(history['days_ago'] <= 180)].groupby(['customer_id', 'article_id'])['price'].count().reset_index(name='last_180_days_purchases')
    
    # Compute the average price of purchases
    avg_price = history.groupby(['customer_id', 'article_id'])['price'].mean().reset_index(name='avg_price')
    
    # Compute the average customer age
    avg_customer_age = history.groupby(['customer_id'])['customer_age'].mean().reset_index(name='avg_customer_age')
    
    # Compute the average number of days ago purchases were made
    avg_days_ago = history.groupby(['customer_id', 'article_id'])['days_ago'].mean().reset_index(name='avg_days_ago')
    
    # Merge the last 7 days purchases with F
    F = pd.merge(F, last_7_days_purchases[['customer_id', 'article_id', 'last_7_days_purchases']], on=['customer_id', 'article_id'], how='left', validate='many_to_one')
    F['f_last_7_days_purchases'] = F['last_7_days_purchases'].fillna(0)
    
    # Merge the last 180 days purchases with F
    F = pd.merge(F, last_180_days_purchases[['customer_id', 'article_id', 'last_180_days_purchases']], on=['customer_id', 'article_id'], how='left', validate='many_to_one')
    F['f_last_180_days_purchases'] = F['last_180_days_purchases'].fillna(0)
    
    # Merge the average price with F
    F = pd.merge(F, avg_price[['customer_id', 'article_id', 'avg_price']], on=['customer_id', 'article_id'], how='left', validate='many_to_one')
    F['f_avg_price'] = F['avg_price'].fillna(0)
    
    # Merge the average customer age with F
    F = pd.merge(F, avg_customer_age[['customer_id', 'avg_customer_age']], on='customer_id', how='left', validate='many_to_one')
    F['f_avg_customer_age'] = F['avg_customer_age'].fillna(0)
    
    # Merge the average days ago with F
    F = pd.merge(F, avg_days_ago[['customer_id', 'article_id', 'avg_days_ago']], on=['customer_id', 'article_id'], how='left', validate='many_to_one')
    F['f_avg_days_ago'] = F['avg_days_ago'].fillna(0)
    
    return F
