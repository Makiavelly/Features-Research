def modify_features(X, history):
    # Compute time-safe past180 days statistic: average price for each customer
    avg_price_history = history.groupby('customer_id')['price'].mean().to_frame('avg_price')
    # Compute time-safe past180 days statistic: count of article categories for each customer
    article_count_history = history.groupby('customer_id')['article_id'].nunique().to_frame('article_count')
    # Compute time-safe past180 days statistic: count of past purchases for each customer
    past_purchase_count_history = history.groupby('customer_id')['days_ago'].count().to_frame('past_purchase_count')
    # Compute time-safe past180 days statistic: average age for each customer
    avg_age_history = history.groupby('customer_id')['customer_age'].mean().to_frame('avg_age')
    
    # Merge past 180 days history statistics with the candidate pairs on customer ID
    F = pd.DataFrame(index=X.index)
    F['avg_price'] = history.merge(avg_price_history, left_on='customer_id', right_index=True, validate='many_to_one', how='left')['avg_price']
    F['article_count'] = history.merge(article_count_history, left_on='customer_id', right_index=True, validate='many_to_one', how='left')['article_count']
    F['past_purchase_count'] = history.merge(past_purchase_count_history, left_on='customer_id', right_index=True, validate='many_to_one', how='left')['past_purchase_count']
    F['avg_age'] = history.merge(avg_age_history, left_on='customer_id', right_index=True, validate='many_to_one', how='left')['avg_age']
    
    # Filter days_ago for calendar-day windows
    days_ago_filter = history['days_ago'] <= 180
    
    # Compute feature: proportion of past 180 days articles that belong to the same product category
    same_category_proportion = history.groupby('customer_id')['product_code'].apply(lambda x: len(x) / len(history['customer_id'][days_ago_filter])).to_frame('same_category_proportion')
    
    # Compute feature: average number of days between purchases of the same article
    avg_days_same_article = history.groupby('article_id')['days_ago'].apply(lambda x: (x.max() - x.min()) if len(x) > 1 else 0).mean().to_frame('avg_days_same_article')
    
    # Compute feature: number of consecutive days the customer purchased from the same product category
    consecutive_days_same_category = history.groupby('customer_id')['days_ago'].apply(lambda x: x.max() - x.min()).mean().to_frame('consecutive_days_same_category')
    
    # Merge computed features with the candidate pairs on customer ID
    F = pd.concat([F, same_category_proportion, avg_days_same_article, consecutive_days_same_category], axis=1)
    
    return F
