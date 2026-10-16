def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute average price for each article in the last 180 days
    avg_price_article = history.loc[history['days_ago'] <= 180].groupby('article_id')['price'].mean().reset_index()
    
    # Compute number of purchases for each customer in the last 180 days
    num_purchases = history.loc[history['days_ago'] <= 180].groupby('customer_id')['article_id'].nunique().reset_index()
    
    # Compute average customer age for each customer in the last 180 days
    avg_customer_age = history.loc[history['days_ago'] <= 180].groupby('customer_id')['customer_age'].mean().reset_index()
    
    # Compute average article purchase count for each customer in the last 180 days
    avg_article_purchase_count = history.loc[history['days_ago'] <= 180].groupby('customer_id')['article_id'].nunique().reset_index()
    
    # Compute days ago for each customer-article pair in the last 90 days
    days_ago_90 = history.loc[(history['days_ago'] >= 0) & (history['days_ago'] <= 90)].groupby(['customer_id', 'article_id'])['days_ago'].max().reset_index()
    
    # Merge the result
    F = pd.merge(F, avg_price_article, on='article_id', how='left')
    F = pd.merge(F, num_purchases, on='customer_id', how='left')
    F = pd.merge(F, avg_customer_age, on='customer_id', how='left')
    F = pd.merge(F, avg_article_purchase_count, on='customer_id', how='left')
    F = pd.merge(F, days_ago_90, on=['customer_id', 'article_id'], how='left')
    
    # Compute new features
    F['f_avg_price_article'] = F['price_x'].fillna(0)
    F['f_num_purchases'] = F['article_id_y'].fillna(0)
    F['f_avg_customer_age'] = F['customer_age_y'].fillna(0)
    F['f_avg_article_purchase_count'] = F['article_id_x'].fillna(0)
    F['f_days_ago_90'] = F['days_ago_y'].fillna(0)
    
    # Drop unnecessary columns
    F.drop(['price_x', 'price_y', 'article_id_x', 'article_id_y', 'customer_age_y', 'article_id_y', 'days_ago_y'], axis=1, inplace=True)
    
    return F
