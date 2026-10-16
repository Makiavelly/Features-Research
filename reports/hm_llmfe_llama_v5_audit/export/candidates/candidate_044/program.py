def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    # Mean customer age
    customer_age_mean = history.groupby('customer_id')['customer_age'].mean().reset_index()
    F = pd.merge(F, customer_age_mean[['customer_id','mean_customer_age']], left_index=True, right_on='customer_id', how='left', validate='many_to_one')
    
    # Count past purchases of same product type per customer
    customer_product_type_purchases = history.groupby(['customer_id', 'product_type_no'])['days_ago'].count().reset_index()
    F = pd.merge(F, customer_product_type_purchases[['customer_id', 'product_type_no', 'days_ago']], left_index=True, right_on=['customer_id', 'product_type_no'], how='left', validate='many_to_one')
    
    # Count transactions in the last 7 days per product type
    recent_purchases = history[(history['days_ago'] <= 7)]
    product_type_recent_purchases = recent_purchases.groupby('product_type_no')['days_ago'].count().reset_index()
    F = pd.merge(F, product_type_recent_purchases[['product_type_no', 'days_ago']], left_index=True, right_on='product_type_no', how='left', validate='many_to_one')
    
    # Count past purchases per product type
    product_type_purchases = history.groupby('product_type_no')['days_ago'].count().reset_index()
    F = pd.merge(F, product_type_purchases[['product_type_no', 'days_ago']], left_index=True, right_on='product_type_no', how='left', validate='many_to_one')
    
    # Count past purchases in the same department per customer
    customer_department_purchases = history.groupby(['customer_id', 'department_no'])['days_ago'].count().reset_index()
    F = pd.merge(F, customer_department_purchases[['customer_id', 'department_no', 'days_ago']], left_index=True, right_on=['customer_id', 'department_no'], how='left', validate='many_to_one')
    
    F = F.drop(columns=['customer_id', 'product_type_no', 'department_no'])
    
    return F
