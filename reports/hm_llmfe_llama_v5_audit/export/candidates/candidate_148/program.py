def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute aggregate values for each customer within a 7-day window
    history_7day = history[history['days_ago'] <= 7]
    customer_7day = history_7day.groupby(['customer_id']).agg({
        'price':'mean',
        'product_code':'mean',
        'product_type_no':'mean',
        'graphical_appearance_no':'mean',
        'colour_group_code':'mean',
        'perceived_colour_value_id':'mean',
        'perceived_colour_master_id':'mean',
        'department_no':'mean',
        'index_group_no':'mean',
       'section_no':'mean',
        'garment_group_no':'mean'
    }).reset_index()
    
    # Merge customer_7day with X to create new features
    F['f_customer_mean_price'] = customer_7day.merge(X, on='customer_id', how='left')['price'].values
    F['f_customer_avg_product_code'] = customer_7day.merge(X, on='customer_id', how='left')['product_code'].values
    F['f_customer_avg_product_type'] = customer_7day.merge(X, on='customer_id', how='left')['product_type_no'].values
    F['f_customer_avg_graphical_appearance'] = customer_7day.merge(X, on='customer_id', how='left')['graphical_appearance_no'].values
    F['f_customer_avg_colour_group'] = customer_7day.merge(X, on='customer_id', how='left')['colour_group_code'].values
    F['f_customer_avg_perceived_colour_value'] = customer_7day.merge(X, on='customer_id', how='left')['perceived_colour_value_id'].values
    F['f_customer_avg_perceived_colour_master'] = customer_7day.merge(X, on='customer_id', how='left')['perceived_colour_master_id'].values
    F['f_customer_avg_department'] = customer_7day.merge(X, on='customer_id', how='left')['department_no'].values
    F['f_customer_avg_index_group'] = customer_7day.merge(X, on='customer_id', how='left')['index_group_no'].values
    F['f_customer_avg_section'] = customer_7day.merge(X, on='customer_id', how='left')['section_no'].values
    F['f_customer_avg_garment_group'] = customer_7day.merge(X, on='customer_id', how='left')['garment_group_no'].values
    
    return F
