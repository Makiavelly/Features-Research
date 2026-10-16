def modify_features(X, history):
    # Compute time-safe past180 days statistic: average price for each customer cohort
    avg_price_history = history.groupby('customer_id')['price'].mean().to_frame('avg_price')
    # Compute time-safe past180 days statistic: count of article categories for each customer cohort
    article_count_history = history.groupby('customer_id')['article_id'].nunique().to_frame('article_count')
    # Compute time-safe past180 days statistic: average age for each customer cohort
    avg_age_history = history.groupby('customer_id')['customer_age'].mean().to_frame('avg_age')
    
    # Merge past 180 days history statistics with the candidate pairs on customer ID
    F = pd.DataFrame(index=X.index)
    F['avg_price'] = pd.merge(X, avg_price_history, left_on='customer_id', right_index=True, validate='many_to_one', how='left')['avg_price']
    F['article_count'] = pd.merge(X, article_count_history, left_on='customer_id', right_index=True, validate='many_to_one', how='left')['article_count']
    F['avg_age'] = pd.merge(X, avg_age_history, left_on='customer_id', right_index=True, validate='many_to_one', how='left')['avg_age']
    
    # Filter days_ago for calendar-day windows
    days_ago_filter = (history['days_ago'] <= 180)
    
    # Compute feature: proportion of past 180 days articles that belong to the same product category
    same_category_proportion = history.groupby('customer_id')['product_code'].apply(lambda x: len(x) / len(history['customer_id']))
    F['same_category_proportion'] = same_category_proportion
    
    # Compute feature: average number of days between purchases of the same article
    avg_days_same_article = history.groupby('article_id')['days_ago'].max() - history.groupby('article_id')['days_ago'].min()
    F['avg_days_same_article'] = avg_days_same_article.mean()
    
    # Compute feature: number of consecutive days the customer purchased from the same product category
    consecutive_days_same_category = history.groupby('customer_id')['days_ago'].max() - history.groupby('customer_id')['days_ago'].min()
    F['consecutive_days_same_category'] = consecutive_days_same_category
    
    # Filter days_ago for calendar-day windows
    F = F[F['customer_id'].isin(history['customer_id'][days_ago_filter])]
    
    return F
