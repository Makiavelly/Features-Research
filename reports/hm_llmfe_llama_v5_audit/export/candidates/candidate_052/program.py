def modify_features(X, history):
    # Compute customer cohort statistics over time-safe past 180 days
    F = pd.DataFrame(index=X.index)

    # Compute mean purchase price over last 180 days for each customer
    cohort_price_mean = history.pivot_table(index='customer_id', aggfunc='mean', values='price', fill_value=0)

    # Compute number of distinct article categories purchased by each customer in last 180 days
    cohort_article_distinct_count = history.pivot_table(index='customer_id', aggfunc='nunique', columns='article_id', values='customer_id')

    # Merge cohorts with customer data for mean purchase price and distinct article counts
    cohort_merge = pd.merge(cohort_price_mean, cohort_article_distinct_count, left_index=True, right_index=True, how='left')

    # Compute mean purchase price and distinct article counts for current candidate articles
    # using customer cohort statistics
    F['f_price_mean'] = cohort_merge['price'].loc[X['customer_id']]

    # Filter days_ago for calendar-day windows and compute mean number of past purchases
    history_filtered = history[(history['days_ago'] <= 180) & (history['days_ago'] >= 0)]

    # Compute mean number of past purchases for each customer
    cohort_purchase_count_mean = history_filtered.pivot_table(index='customer_id', aggfunc='mean', values='days_ago', fill_value=0)

    F['f_purchase_count_mean'] = cohort_purchase_count_mean.loc[X['customer_id']]

    # Compute mean age of customers purchasing each article in last 180 days
    cohort_age_mean = history.pivot_table(index='article_id', aggfunc='mean', values='customer_age', fill_value=0)

    F['f_age_mean'] = cohort_age_mean.loc[X['article_id']]

    return F
