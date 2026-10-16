def modify_features(X, history):
    # Compute the number of past purchases of each customer within the last 180 days
    past_purchases = history[history['days_ago'] <= 180].groupby('customer_id')['article_id'].nunique().reset_index()
    
    # Compute the average age of customers
    avg_age = history.groupby('customer_id')['customer_age'].mean().reset_index()
    
    # Compute the average price of articles bought by customers within the last 180 days
    avg_price_last_180_days = history[history['days_ago'] <= 180].groupby(['customer_id', 'article_id'])['price'].mean().reset_index()
    
    # Compute the count of each article type bought by customers within the last 180 days
    article_type_count = history[history['days_ago'] <= 180].groupby(['customer_id', 'product_type_no'])['article_id'].count().reset_index()
    
    # Compute the count of each article color bought by customers within the last 180 days
    article_color_count = history[history['days_ago'] <= 180].groupby(['customer_id', 'colour_group_code'])['article_id'].count().reset_index()
    
    # Merge the dataframes based on the customer id and article id
    F = pd.merge(past_purchases, avg_age, on='customer_id', validate='many_to_one')
    F = pd.merge(F, avg_price_last_180_days, on=['customer_id', 'article_id'], validate='many_to_one')
    F = pd.merge(F, article_type_count, on=['customer_id', 'product_type_no'], validate='many_to_one')
    F = pd.merge(F, article_color_count, on=['customer_id', 'colour_group_code'], validate='many_to_one')
    
    # Preserve the order of X when merging
    F = F.loc[X.index]
    
    # Rename the columns
    F.columns = ['f_past_purchases', 'f_avg_age', 'f_avg_price_last_180_days', 'f_article_type_count', 'f_article_color_count']
    
    return F
