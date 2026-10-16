def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    # Compute average age of customers who purchased each article type in the last 180 days
    article_avg_age = history.groupby('article_id')['customer_age'].mean().reindex(X['article_id'], fill_value=0).to_frame('f_article_avg_age')
    
    # Compute the number of times each article was purchased in the last 180 days
    article_purchases = history.groupby('article_id')['customer_id'].count().reindex(X['article_id'], fill_value=0).to_frame('f_article_purchases')
    
    # Compute average purchase amount per article in the last 180 days
    article_avg_price = history.groupby('article_id')['price'].mean().reindex(X['article_id'], fill_value=0).to_frame('f_article_avg_price')
    
    # Compute number of unique customers who purchased each article in the last 180 days
    article_unique_customers = history.groupby('article_id')['customer_id'].nunique().reindex(X['article_id'], fill_value=0).to_frame('f_article_unique_customers')
    
    # Compute number of articles purchased by each customer in the last 180 days
    customer_purchases = history.groupby('customer_id')['article_id'].count().to_frame('f_customer_purchases')
    
    # Filter days ago for calendar-day windows
    F_days_ago = history['days_ago'].apply(lambda x: x if 1 <= x <= 180 else 0)
    
    # Create a new DataFrame with the filtered days ago values
    F_days_ago_df = pd.DataFrame(F_days_ago, columns=['f_days_ago'])
    
    # Reorder the columns to match the desired output order
    F = pd.concat([article_avg_age, article_purchases, article_avg_price, article_unique_customers, F_days_ago_df, customer_purchases], axis=1)
    
    # Reorder the columns
    F = F[['f_article_avg_age', 'f_article_purchases', 'f_article_avg_price', 'f_article_unique_customers', 'f_days_ago', 'f_customer_purchases']]
    
    return F
