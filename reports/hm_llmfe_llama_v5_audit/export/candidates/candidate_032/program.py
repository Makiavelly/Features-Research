def modify_features(X, history):
    F = pd.DataFrame(index=X.index)

    # Compute customer age in the last 180 days
    customer_age_in_180_days = history.groupby(['customer_id'])['customer_age'].apply(lambda x: x[x > 0].rolling(180, min_periods=1).mean()).reset_index()

    # Compute average price per customer
    customer_avg_price = history.groupby(['customer_id'])['price'].apply(lambda x: x[x > 0].mean()).reset_index()

    # Compute average price per customer in the last 7 days
    days_ago_avg_price = history[history['days_ago'] <= 7].groupby(['customer_id'])['price'].apply(lambda x: x[x > 0].mean()).reset_index()

    # Compute average product type per customer
    customer_category_average = history.groupby(['customer_id'])['product_type_no'].apply(lambda x: x[x > 0].mean()).reset_index()

    # Compute the count of customers who purchased in the last 7 days
    days_ago_count = history[history['days_ago'] <= 7].groupby(['customer_id'])['customer_id'].count().reset_index(name='days_ago_count')

    # Merge results and assign to F
    F = pd.merge(F, customer_age_in_180_days, on='customer_id', suffixes=('', '_180_days'), validate='many_to_one')
    F = pd.merge(F, customer_avg_price, on='customer_id', suffixes=('', '_avg_price'), validate='many_to_one')
    F = pd.merge(F, days_ago_avg_price, on='customer_id', suffixes=('', '_days_avg_price'), validate='many_to_one')
    F = pd.merge(F, customer_category_average, on='customer_id', suffixes=('', '_category_average'), validate='many_to_one')
    F = pd.merge(F, days_ago_count, on='customer_id', suffixes=('', '_days_ago_count'), validate='many_to_one')

    # Select desired columns
    F = F[['customer_id', 'article_id', 'f_customer_age_in_180_days', 'f_customer_avg_price', 'f_days_ago_avg_price', 'f_customer_category_average', 'f_days_ago_count']]

    return F
