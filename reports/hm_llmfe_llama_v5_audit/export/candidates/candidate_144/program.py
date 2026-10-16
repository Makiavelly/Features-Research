def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # 1. Average purchase price of past products
    avg_price = history.groupby('customer_id')['price'].mean().to_frame('avg_price')
    F['f_avg_price'] = avg_price['avg_price'].reindex(X['customer_id']).fillna(0).astype(float)
    
    # 2. Count of unique product types purchased in past 180 days
    unique_types = history[(history['days_ago'] <= 180)].groupby('customer_id')['product_type_no'].nunique().to_frame('unique_types')
    F['f_unique_types'] = unique_types['unique_types'].reindex(X['customer_id']).fillna(0).astype(float)
    
    # 3. Count of recently purchased products in the same department
    recent_dept_count = history[(history['days_ago'] <= 30)].groupby(['customer_id', 'article_id'])['customer_id'].count().groupby('customer_id')['customer_id'].sum().to_frame('recent_dept_count')
    F['f_recent_dept_count'] = recent_dept_count['recent_dept_count'].reindex(X['customer_id']).fillna(0).astype(float)
    
    # 4. Average customer age
    avg_age = history.groupby('customer_id')['customer_age'].mean().to_frame('avg_age')
    F['f_avg_age'] = avg_age['avg_age'].reindex(X['customer_id']).fillna(0).astype(float)
    
    # 5. Number of unique articles purchased by each customer in the past 180 days
    unique_articles = history[(history['days_ago'] <= 180)].groupby('customer_id')['article_id'].nunique().to_frame('unique_articles')
    F['f_unique_articles'] = unique_articles['unique_articles'].reindex(X['customer_id']).fillna(0).astype(float)
    
    return F
