def modify_features(X, history):
    # Compute mean of past purchase price and assign mean price column
    mean_price = history.groupby('customer_id')['price'].mean().reindex(X['customer_id']).fillna(0)
    F = pd.DataFrame(index=X.index)
    F['f_mean_price'] = mean_price.values
    
    # Compute number of past purchases within 90 days and assign past_purchases column
    past_purchases = history[(history['days_ago'] <= 90) & (history['customer_id'].isin(X['customer_id']))].groupby('customer_id')['customer_id'].count().reindex(X['customer_id']).fillna(0)
    F['f_past_purchases'] = past_purchases.values
    
    # Compute mean of past purchases' product Types and assign mean_product_type column
    mean_product_type = history.groupby('customer_id')['product_type_no'].mean().reindex(X['customer_id']).fillna(0)
    F['f_mean_product_type'] = mean_product_type.values
    
    # Compute count of past purchases' colors and assign past_colors column
    past_colors = history.groupby('customer_id')['colour_group_code'].nunique().reindex(X['customer_id']).fillna(0)
    F['f_past_colors'] = past_colors.values
    
    # Compute count of past purchases' departments and assign past_departments column
    past_departments = history.groupby('customer_id')['department_no'].nunique().reindex(X['customer_id']).fillna(0)
    F['f_past_departments'] = past_departments.values
    
    return F
