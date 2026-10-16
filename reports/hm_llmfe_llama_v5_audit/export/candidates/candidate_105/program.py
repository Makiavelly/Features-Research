def modify_features(X, history):
    # Compute average age of customers who purchased each article type in the last 180 days
    article_avg_age = history.loc[history['days_ago'] <= 180].groupby('article_id')['customer_age'].mean().reindex(X['article_id'], fill_value=0).to_frame('f_article_avg_age')
    
    # Compute average purchase amount per article in the last 180 days
    article_avg_price = history.loc[history['days_ago'] <= 180].groupby('article_id')['price'].mean().reindex(X['article_id'], fill_value=0).to_frame('f_article_avg_price')
    
    # Compute number of times each article was purchased in the last 180 days
    article_purchases = history.loc[history['days_ago'] <= 180].groupby('article_id')['customer_id'].count().reindex(X['article_id'], fill_value=0).to_frame('f_article_purchases')
    
    # Compute number of unique customers who purchased each article in the last 180 days
    article_unique_customers = history.loc[history['days_ago'] <= 180].groupby('article_id')['customer_id'].nunique().reindex(X['article_id'], fill_value=0).to_frame('f_article_unique_customers')
    
    # Compute number of articles purchased by each customer in the last 180 days
    customer_purchases = history.loc[history['days_ago'] <= 180].groupby('customer_id')['article_id'].count().to_frame('f_customer_purchases')
    
    # Create a new DataFrame with the above features
    F = pd.concat([article_avg_age, article_avg_price, article_purchases, article_unique_customers, customer_purchases], axis=1)
    
    # Reorder the columns
    F = F[['f_article_avg_age', 'f_article_avg_price', 'f_article_purchases', 'f_article_unique_customers', 'f_customer_purchases']]
    
    return F
