def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    # Compute average age of customers who purchased each article type in the last 180 days
    article_avg_age = history.groupby('article_id')['customer_age'].mean().reindex(X['article_id'], fill_value=0).to_frame('f_article_avg_age')
    F = pd.merge(F, article_avg_age, left_index=True, right_index=True, how='left')
    
    # Compute the number of times each article was purchased in the last 180 days
    article_purchases = history.groupby('article_id')['customer_id'].count().reindex(X['article_id'], fill_value=0).to_frame('f_article_purchases')
    F = pd.merge(F, article_purchases, left_index=True, right_index=True, how='left')
    
    # Compute average purchase amount per article in the last 180 days
    article_avg_price = history.groupby('article_id')['price'].mean().reindex(X['article_id'], fill_value=0).to_frame('f_article_avg_price')
    F = pd.merge(F, article_avg_price, left_index=True, right_index=True, how='left')
    
    # Compute number of unique customers who purchased each article in the last 180 days
    article_unique_customers = history.groupby('article_id')['customer_id'].nunique().reindex(X['article_id'], fill_value=0).to_frame('f_article_unique_customers')
    F = pd.merge(F, article_unique_customers, left_index=True, right_index=True, how='left')
    
    # Filter days ago for calendar-day windows
    F['f_days_ago'] = F['days_ago'].apply(lambda x: x if 1 <= x <= 180 else 0)
    
    # Compute number of articles purchased by each customer in the last 180 days
    customer_purchases = history.groupby('customer_id')['article_id'].count().to_frame('f_customer_purchases')
    F = pd.merge(F, customer_purchases, left_index=True, right_index=True, how='left')
    
    return F[['f_article_avg_age', 'f_article_purchases', 'f_article_avg_price', 'f_article_unique_customers', 'f_days_ago', 'f_customer_purchases']]
