def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    # Compute the average price for each customer within the last 180 days
    avg_price_customer = history[(history['days_ago'] <= 180)].groupby('customer_id')['price'].mean().reset_index()
    
    # Compute the count of purchases for each customer within the last 180 days
    purchases_customer = history[(history['days_ago'] <= 180)].groupby('customer_id')['article_id'].nunique().reset_index()
    
    # Compute the average customer age for each customer within the last 180 days
    avg_age_customer = history[(history['days_ago'] <= 180)].groupby('customer_id')['customer_age'].mean().reset_index()
    
    # Compute the max and min price for each article within the last 180 days
    price_max_article = history[(history['days_ago'] <= 180)].groupby('article_id')['price'].transform('max').reset_index()
    price_min_article = history[(history['days_ago'] <= 180)].groupby('article_id')['price'].transform('min').reset_index()
    
    # Compute the avg price and purchases for each article within the last 180 days
    avg_price_article = history[(history['days_ago'] <= 180)].groupby('article_id')['price'].mean().reset_index()
    purchases_article = history[(history['days_ago'] <= 180)].groupby('article_id')['customer_id'].nunique().reset_index()
    
    # Merge to create F with unchanged X.index
    F = pd.merge(avg_price_customer, purchases_customer, on='customer_id', how='left', validate='many_to_one')
    F = pd.merge(F, avg_age_customer, on='customer_id', how='left', validate='many_to_one')
    F = pd.merge(F, price_max_article, on='article_id', how='left', validate='many_to_one')
    F = pd.merge(F, price_min_article, on='article_id', how='left', validate='many_to_one')
    F = pd.merge(F, avg_price_article, on='article_id', how='left', validate='many_to_one')
    F = pd.merge(F, purchases_article, on='article_id', how='left', validate='many_to_one')
    
    # Rename columns
    F.columns = ['customer_id', 'article_id', 'f_avg_price_customer', 'f_count_purchases_customer', 
                 'f_avg_age_customer', 'f_price_max_article', 'f_price_min_article', 'f_avg_price_article', 
                 'f_count_purchases_article']
    
    # Assign values to F positionally
    F = F[['customer_id', 'article_id', 'f_avg_price_customer', 'f_count_purchases_customer', 
           'f_avg_age_customer', 'f_price_max_article', 'f_price_min_article', 'f_avg_price_article', 
           'f_count_purchases_article']]
    
    return F
