def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Mean past purchases per customer
    customer_purchases = history.groupby('customer_id')['days_ago'].mean().to_frame('mean_days_ago')
    customer_purchases = customer_purchases.join(history.groupby('customer_id', observed=True)['article_id'].size().to_frame('total_purchases'), lsuffix='_customer', rsuffix='_customer', how='left')
    F = pd.merge(F, customer_purchases, left_index=True, right_index=True, validate='many_to_one', how='left')
    
    # Count past purchases of same product type per customer
    customer_product_type_purchases = history.groupby(['customer_id', 'product_type_no'])['days_ago'].count().to_frame('count_product_type_purchases')
    F = pd.merge(F, customer_product_type_purchases, left_index=True, right_index=True, validate='many_to_one', how='left')
    
    # Mean days ago for products in same department per customer
    customer_department_purchases = history.groupby(['customer_id', 'department_no'])['days_ago'].mean().to_frame('mean_days_ago_department')
    F = pd.merge(F, customer_department_purchases, left_index=True, right_index=True, validate='many_to_one', how='left')
    
    # Count transactions in the last 7 days per customer
    recent_purchases = history[(history['days_ago'] <= 7)]
    customer_recent_purchases = recent_purchases.groupby('customer_id')['days_ago'].count().to_frame('count_recent_purchases')
    F = pd.merge(F, customer_recent_purchases, left_index=True, right_index=True, validate='many_to_one', how='left')
    
    return F
