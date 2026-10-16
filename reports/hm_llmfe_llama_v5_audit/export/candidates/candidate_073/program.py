def modify_features(X, history):
    # Compute time-safe past180 days statistic: average price for each customer cohort
    avg_price_history = history.groupby(['customer_id'])['price'].mean()
    # Compute time-safe past180 days statistic: count of article categories for each customer cohort
    article_count_history = history.groupby(['customer_id'])['article_id'].count()
    # Compute time-safe past180 days statistic: average age for each customer cohort
    avg_age_history = history.groupby(['customer_id'])['customer_age'].mean()
    # Compute time-safe past180 days statistic: average product type for each customer cohort
    avg_product_type_history = history.groupby(['customer_id'])['product_type_no'].mean()
    
    # Merge past 180 days history statistics with the candidate pairs on customer ID
    F = pd.merge(X, avg_price_history.to_frame('avg_price'), on='customer_id', validate='many_to_one', how='left')
    F = pd.merge(F, article_count_history.to_frame('article_count'), on='customer_id', validate='many_to_one', how='left')
    F = pd.merge(F, avg_age_history.to_frame('avg_age'), on='customer_id', validate='many_to_one', how='left')
    F = pd.merge(F, avg_product_type_history.to_frame('avg_product_type'), on='customer_id', validate='many_to_one', how='left')
    
    # Compute time-safe past180 days statistic: average price for each product category
    avg_price_category_history = history.groupby(['article_id'])['price'].mean()
    # Compute time-safe past180 days statistic: count of customer cohort for each product category
    customer_count_category_history = history.groupby(['article_id'])['customer_id'].nunique()
    # Compute time-safe past180 days statistic: average age for each product category
    avg_age_category_history = history.groupby(['article_id'])['customer_age'].mean()
    # Compute time-safe past180 days statistic: average product type for each product category
    avg_product_type_category_history = history.groupby(['article_id'])['product_type_no'].mean()
    
    # Merge past 180 days history statistics with the candidate pairs on article ID
    F = pd.merge(F, avg_price_category_history.to_frame('avg_price_category'), on='article_id', validate='many_to_one', how='left')
    F = pd.merge(F, customer_count_category_history.to_frame('customer_count_category'), on='article_id', validate='many_to_one', how='left')
    F = pd.merge(F, avg_age_category_history.to_frame('avg_age_category'), on='article_id', validate='many_to_one', how='left')
    F = pd.merge(F, avg_product_type_category_history.to_frame('avg_product_type_category'), on='article_id', validate='many_to_one', how='left')
    
    # Compute feature: proportion of past 180 days articles that belong to the same product category
    F['same_category_proportion'] = F.apply(lambda x: np.mean(history['article_id'] == x['article_id']) if (x['customer_id'] in history['customer_id']) and (x['article_id'] in history['article_id']) else 0, axis=1)
    
    # Compute feature: proportion of past 180 days customers that purchased the same article
    F['same_article_proportion'] = F.apply(lambda x: np.mean(history['customer_id'] == x['customer_id']) if (x['article_id'] in history['article_id']) and (x['customer_id'] in history['customer_id']) else 0, axis=1)
    
    # Compute feature: number of consecutive days the customer purchased from the same product category
    F['consecutive_days_same_category'] = history.groupby('customer_id')['days_ago'].max() - history.groupby('customer_id')['days_ago'].min()
    
    # Compute feature: average number of days between purchases of the same article
    F['avg_days_same_article'] = (history.groupby('article_id')['days_ago'].max() - history.groupby('article_id')['days_ago'].min()).mean()
    
    # Drop rows with all missing values
    F.dropna(axis=1, how='all', inplace=True)
    
    return F
