def modify_features(X, history):
    # Compute statistics and aggregates
    F = pd.DataFrame(index=X.index)
    # 1. Average purchase price of past products
    avg_price = history.groupby('customer_id')['price'].mean().to_frame('avg_price')
    F['f_avg_price'] = avg_price.loc[X['customer_id']].values

    # 2. Count of unique product types purchased in past 180 days
    unique_types = history[(history['days_ago'] <= 180)].groupby('customer_id')['product_type_no'].nunique().to_frame('unique_types')
    F['f_unique_types'] = unique_types.loc[X['customer_id']].values

    # 3. Count of recently purchased products in the same department
    recent_dept_count = history[(history['days_ago'] <= 30)].merge(X, on='customer_id').groupby(['customer_id', 'article_id'])['article_id'].count().groupby('customer_id').sum().to_frame('recent_dept_count')
    F['f_recent_dept_count'] = recent_dept_count.loc[X['customer_id']].values

    # 4. Average customer age
    avg_age = history.groupby('customer_id')['customer_age'].mean().to_frame('avg_age')
    F['f_avg_age'] = avg_age.loc[X['customer_id']].values

    return F
