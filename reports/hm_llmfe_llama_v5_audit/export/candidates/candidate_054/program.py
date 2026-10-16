def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute mean purchase price over last 180 days for each customer
    cohort_price_mean = history[history['days_ago'] <= 180].pivot_table(index='customer_id', values='price', aggfunc='mean', fill_value=0)
    
    # Compute mean age of customers purchasing each article in last 180 days
    cohort_age_mean = history[history['days_ago'] <= 180].pivot_table(index='article_id', values='customer_age', aggfunc='mean', fill_value=0)
    
    # Compute purchases in last 180 days of customers for each article
    cohort_purchase_count = history[history['days_ago'] <= 180].pivot_table(index='article_id', columns='customer_id', aggfunc='size', fill_value=0).fillna(0).astype(int)
    
    # Merge cohorts with customer data
    cohort_merge = pd.concat([cohort_price_mean, cohort_age_mean, cohort_purchase_count], axis=1).fillna(0)
    
    # Extract customer IDs from merge
    cohort_merge.index = cohort_merge.index.rename('customer_id')
    
    # Merge cohorts with candidate articles for mean purchase price, age, and purchases
    F = pd.merge(X, cohort_merge, left_on='customer_id', right_index=True, how='left', validate='many_to_one')
    
    # Compute mean purchase price and age for current candidate articles
    F['f_price_mean'] = F['price_y']
    F['f_age_mean'] = F['customer_age_y']
    
    # Compute purchases in last 180 days of customers for each article
    F['f_purchase_count'] = F['purchase_count_y']
    
    return F
