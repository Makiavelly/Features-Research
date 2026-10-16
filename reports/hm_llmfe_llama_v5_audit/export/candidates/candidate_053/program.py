def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute mean purchase price over last 180 days for each customer
    cohort_price_mean = history[history['days_ago'] <= 180].pivot_table(index='customer_id', aggfunc='mean', values='price', fill_value=0)
    
    # Compute mean age of customers purchasing each article in last 180 days
    cohort_age_mean = history[history['days_ago'] <= 180].pivot_table(index='article_id', aggfunc='mean', values='customer_age', fill_value=0)
    
    # Compute mean number of past purchases for each customer
    cohort_purchase_count_mean = history[history['days_ago'] <= 180].pivot_table(index='customer_id', aggfunc='mean', values='days_ago', fill_value=0)
    
    # Merge cohorts with customer data for mean purchase price, distinct article counts, age, and purchase counts
    cohort_merge = pd.merge(cohort_price_mean, cohort_age_mean, left_index=True, right_index=True, how='left')
    cohort_merge = pd.merge(cohort_merge, cohort_purchase_count_mean, left_index=True, right_index=True, how='left')
    
    # Compute mean purchase price and distinct article counts for current candidate articles
    # using customer cohort statistics
    F['f_price_mean'] = cohort_merge['price'].loc[X['customer_id']]
    
    # Compute mean age of customers purchasing each article in last 180 days
    F['f_age_mean'] = cohort_age_mean.loc[X['article_id']]
    
    # Compute mean number of past purchases for each customer
    F['f_purchase_count_mean'] = cohort_purchase_count_mean.loc[X['customer_id']]
    
    return F
