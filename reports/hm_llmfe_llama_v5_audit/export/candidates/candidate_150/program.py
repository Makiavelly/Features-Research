def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Filter history within a 7-day window
    history_7day = history[history['days_ago'] <= 7]
    
    # Merge history_7day with X based on customer_id and article_id
    X_7day = pd.merge(X, history_7day, on=['customer_id', 'article_id'], validate='many_to_one')
    
    # Create new features by calculating customer-specific aggregates
    F['f_customer_mean_price'] = X_7day.groupby('customer_id')['price'].mean()
    F['f_customer_mean_product_code'] = X_7day.groupby('customer_id')['product_code'].mean()
    F['f_customer_mean_product_type'] = X_7day.groupby('customer_id')['product_type_no'].mean()
    F['f_customer_mean_graphical_appearance'] = X_7day.groupby('customer_id')['graphical_appearance_no'].mean()
    F['f_customer_mean_colour_group'] = X_7day.groupby('customer_id')['colour_group_code'].mean()
    F['f_customer_mean_perceived_colour_value'] = X_7day.groupby('customer_id')['perceived_colour_value_id'].mean()
    F['f_customer_mean_perceived_colour_master'] = X_7day.groupby('customer_id')['perceived_colour_master_id'].mean()
    F['f_customer_mean_department'] = X_7day.groupby('customer_id')['department_no'].mean()
    F['f_customer_mean_index_group'] = X_7day.groupby('customer_id')['index_group_no'].mean()
    F['f_customer_mean_section'] = X_7day.groupby('customer_id')['section_no'].mean()
    F['f_customer_mean_garment_group'] = X_7day.groupby('customer_id')['garment_group_no'].mean()
    
    return F
