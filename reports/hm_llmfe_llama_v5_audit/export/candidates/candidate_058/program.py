def modify_features(X, history):
    # Filter history for the last 180 days
    history_last_180_days = history[(history['days_ago'] <= 180)]
    
    # Compute the average price for each article within the last 180 days
    avg_price_article = history_last_180_days.pivot_table(index='article_id', values='price', aggfunc='mean', fill_value=0)
    
    # Compute the count of purchases for each article within the last 180 days
    purchases_article = history_last_180_days.pivot_table(index='article_id', values='customer_id', aggfunc='count')
    
    # Compute the average customer age for each article within the last 180 days
    avg_age_article = history_last_180_days.pivot_table(index='article_id', values='customer_age', aggfunc='mean')
    
    # Join candidate keys LEFT to unique aggregates
    avg_price_article = avg_price_article.reset_index()
    purchases_article = purchases_article.reset_index()
    avg_age_article = avg_age_article.reset_index()
    
    # Merge the three aggregates on the article_id index
    F = avg_price_article.merge(purchases_article, on='article_id', how='left', suffixes=('', '_purchases'))
    F = F.merge(avg_age_article, on='article_id', how='left', suffixes=('', '_age'))
    
    # Assign values to F (e.g. to_numpy) positionally, not by an unrelated index
    F = F[['article_id', 'f_avg_price_article', 'f_count_purchases_article', 'f_avg_age_article']]
    
    return F
