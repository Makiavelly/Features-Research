def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    # Mean past purchases per customer
    customer_purchases = history.groupby('customer_id')['days_ago'].mean().to_frame('mean_days_ago')
    F = pd.merge(F, customer_purchases, left_index=True, right_index=True, validate='many_to_one', how='left')
    
    # Count past purchases of same product type per customer
    customer_product_type_purchases = history.groupby(['customer_id', 'product_type_no'])['days_ago'].count().to_frame('count_product_type_purchases')
    F = pd.merge(F, customer_product_type_purchases, left_index=True, right_index=True, validate='many_to_one', how='left')
    
    # Count transactions in the last 7 days per product type
    recent_purchases = history[(history['days_ago'] <= 7)]
    product_type_recent_purchases = recent_purchases.groupby('product_type_no')['days_ago'].count().to_frame('count_recent_purchases_product_type')
    F = pd.merge(F, product_type_recent_purchases, left_index=True, right_index=True, validate='many_to_one', how='left')
    
    # Count past purchases per product type
    product_type_purchases = history.groupby('product_type_no')['days_ago'].count().to_frame('total_purchases_product_type')
    F = pd.merge(F, product_type_purchases, left_index=True, right_index=True, validate='many_to_one', how='left')
    
    # Count past purchases in the same department per customer
    customer_department_purchases = history.groupby(['customer_id', 'department_no'])['days_ago'].count().to_frame('count_department_purchases')
    F = pd.merge(F, customer_department_purchases, left_index=True, right_index=True, validate='many_to_one', how='left')
    
    # Mean days ago for products in the same department per product type
    department_product_mean_days_ago = history.groupby(['department_no', 'product_type_no'])['days_ago'].mean().to_frame('mean_days_ago_department_product_type')
    F = pd.merge(F, department_product_mean_days_ago, left_index=True, right_index=True, validate='many_to_one', how='left')
    
    return F.iloc[:, :-15]
