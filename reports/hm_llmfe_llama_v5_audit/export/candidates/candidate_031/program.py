def modify_features(X, history):
    # Compute aggregates
    customer_age_in_180_days = history.set_index(['customer_id', 'article_id'])['customer_age'].fillna(0).rolling(180, min_periods=1).mean().reset_index()
    customer_avg_price = history.set_index(['customer_id', 'article_id'])['price'].fillna(0).groupby(['customer_id']).mean().reset_index()
    days_ago_avg_price = history.set_index(['customer_id', 'article_id'])['price'].fillna(0).rolling(7, min_periods=1).mean().reset_index()
    customer_category_average = history.set_index(['customer_id', 'article_id'])['product_type_no'].fillna(0).groupby(['customer_id']).mean().reset_index()
    days_ago_count = history.set_index(['customer_id', 'article_id'])['customer_id'].value_counts().reset_index(name='days_ago_count')

    # Merge results and assign to F
    F = pd.merge(customer_age_in_180_days, customer_avg_price, on=['customer_id'], suffixes=('_x',''), validate='many_to_one')
    F = pd.merge(F, days_ago_avg_price, on=['customer_id'], suffixes=('_x',''), validate='many_to_one')
    F = pd.merge(F, customer_category_average, on=['customer_id'], suffixes=('_x',''), validate='many_to_one')
    F = pd.merge(F, days_ago_count, on=['customer_id'], suffixes=('_x',''), validate='many_to_one')

    # Remove non-key columns and reorder to desired columns
    F = F[['customer_id', 'article_id', 'f_customer_age_in_180_days', 'f_customer_avg_price', 'f_days_ago_avg_price', 'f_customer_category_average', 'f_days_ago_count']]
    F = F.set_index(['customer_id', 'article_id'])

    return F
