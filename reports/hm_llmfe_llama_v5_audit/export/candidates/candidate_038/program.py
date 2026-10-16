def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute average price for each customer in the last 180 days
    avg_price = history.loc[history['days_ago'] <= 180].groupby('customer_id')['price'].mean().reset_index()
    
    # Compute number of purchases for each customer in the last 180 days
    num_purchases = history.loc[history['days_ago'] <= 180].groupby('customer_id')['customer_id'].nunique().reset_index()
    
    # Compute average customer age for each customer in the last 180 days
    avg_customer_age = history.loc[history['days_ago'] <= 180].groupby('customer_id')['customer_age'].mean().reset_index()
    
    # Compute average price for each article in the last 180 days
    avg_price_article = history.loc[history['days_ago'] <= 180].groupby('article_id')['price'].mean().reset_index()
    
    # Compute number of purchases for each article in the last 180 days
    num_purchases_article = history.loc[history['days_ago'] <= 180].groupby('article_id')['customer_id'].nunique().reset_index()
    
    # Compute number of days ago for each customer-article pair in the last 90 and 180 days
    days_ago_90 = history.loc[(history['days_ago'] >= 0) & (history['days_ago'] <= 90)].groupby(['customer_id', 'article_id'])['days_ago'].max().reset_index()
    days_ago_180 = history.loc[history['days_ago'] <= 180].groupby(['customer_id', 'article_id'])['days_ago'].max().reset_index()
    
    # Merge the average price, number of purchases, average customer age, average price article and number of purchases article into the result
    F['f_avg_price'] = pd.merge(X, avg_price, on='customer_id')['price']
    F['f_num_purchases'] = pd.merge(X, num_purchases, on='customer_id')['customer_id']
    F['f_avg_customer_age'] = pd.merge(X, avg_customer_age, on='customer_id')['customer_age']
    F['f_avg_price_article'] = pd.merge(X, avg_price_article, on='article_id')['price']
    F['f_num_purchases_article'] = pd.merge(X, num_purchases_article, on='article_id')['customer_id']
    F['f_days_ago_90'] = pd.merge(X, days_ago_90, on=['customer_id', 'article_id'])['days_ago']
    F['f_days_ago_180'] = pd.merge(X, days_ago_180, on=['customer_id', 'article_id'])['days_ago']
    
    return F
