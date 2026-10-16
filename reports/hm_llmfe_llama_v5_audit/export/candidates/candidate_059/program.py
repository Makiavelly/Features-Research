def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Filter history for the last 180 days
    history_last_180_days = history[(history['days_ago'] <= 180)]
    
    # Compute the average price for each article within the last 180 days
    avg_price_article = history_last_180_days.groupby('article_id')['price'].mean().reset_index()
    
    # Compute the count of purchases for each article within the last 180 days
    purchases_article = history_last_180_days.groupby('article_id')['customer_id'].nunique().reset_index()
    
    # Compute the average customer age for each article within the last 180 days
    avg_age_article = history_last_180_days.groupby('article_id')['customer_age'].mean().reset_index()
    
    # Assign values to F (e.g. to_numpy) positionally, not by an unrelated index
    F = pd.merge(avg_price_article, purchases_article, on='article_id', how='left', suffixes=('', '_purchases'))
    F = pd.merge(F, avg_age_article, on='article_id', how='left', suffixes=('', '_age'))
    
    # Rename columns
    F.columns = ['article_id', 'f_avg_price_article', 'f_count_purchases_article', 'f_avg_age_article']
    
    # Assign values to F positionally
    F = F[['article_id', 'f_avg_price_article', 'f_count_purchases_article', 'f_avg_age_article']]
    
    # Add new features
    F['f_price_max'] = history_last_180_days.groupby('article_id')['price'].transform('max')
    F['f_price_min'] = history_last_180_days.groupby('article_id')['price'].transform('min')
    
    return F
