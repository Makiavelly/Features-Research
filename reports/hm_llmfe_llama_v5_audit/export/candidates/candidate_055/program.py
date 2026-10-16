def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute mean purchase price over last 180 days for each customer
    cohort_price_mean = history[history['days_ago'] <= 180].groupby('customer_id')['price'].mean().reset_index()
    
    # Compute mean age of customers purchasing each article in last 180 days
    cohort_age_mean = history[history['days_ago'] <= 180].groupby('article_id')['customer_age'].mean().reset_index()
    
    # Compute purchases in last 180 days of customers for each article
    cohort_purchase_count = history[history['days_ago'] <= 180].groupby(['customer_id', 'article_id'])['price'].count().reset_index(name='purchase_count')
    
    # Merge cohorts with customer data on customer_id
    cohort_merge = pd.merge(cohort_price_mean, cohort_age_mean, on='customer_id')
    cohort_merge = pd.merge(cohort_merge, cohort_purchase_count, on=['customer_id', 'article_id'], how='left').fillna(0)
    
    # Merge cohorts with candidate articles
    F = pd.merge(X, cohort_merge, on=['customer_id', 'article_id'], how='left')
    
    # Compute mean purchase price and age for current candidate articles
    F['f_price_mean'] = F['price_y']
    F['f_age_mean'] = F['customer_age_y']
    
    # Compute purchases in last 180 days of customers for each article
    F['f_purchase_count'] = F['purchase_count_y']
    
    return F[['customer_id', 'article_id', 'f_price_mean', 'f_age_mean', 'f_purchase_count']]
