def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Filter history within a 7-day window and calculate customer-specific aggregates
    history_7day = history[history['days_ago'] <= 7]
    customer_7day = history_7day.groupby('customer_id').agg({
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
    }).reset_index(drop=True)
    
    # Merge customer_7day with X to create new features
    F['f_customer_mean_price'] = customer_7day['price'].values
    
    # Create new features by expanding customer_7day to match the number of rows in X
    F['f_customer_avg_product_code'] = customer_7day['product_code'].values.repeat(len(X))
    F['f_customer_avg_product_type'] = customer_7day['product_type_no'].values.repeat(len(X))
    F['f_customer_avg_graphical_appearance'] = customer_7day['graphical_appearance_no'].values.repeat(len(X))
    F['f_customer_avg_colour_group'] = customer_7day['colour_group_code'].values.repeat(len(X))
    F['f_customer_avg_perceived_colour_value'] = customer_7day['perceived_colour_value_id'].values.repeat(len(X))
    F['f_customer_avg_perceived_colour_master'] = customer_7day['perceived_colour_master_id'].values.repeat(len(X))
    F['f_customer_avg_department'] = customer_7day['department_no'].values.repeat(len(X))
    F['f_customer_avg_index_group'] = customer_7day['index_group_no'].values.repeat(len(X))
    F['f_customer_avg_section'] = customer_7day['section_no'].values.repeat(len(X))
    F['f_customer_avg_garment_group'] = customer_7day['garment_group_no'].values.repeat(len(X))
    
    return F
