def modify_features(X, history):
    # Filter days_ago for a 7-day history window, calculate past purchases and price mean for each customer
    history_7_days = history[history['days_ago'] <= 7]
    avg_price = history_7_days.groupby('customer_id')['price'].mean().reset_index()
    avg_price = avg_price.rename(columns={'price': 'avg_price'})
    
    # Compute customer average age, count of each category, and most frequent article
    avg_age = history.groupby('customer_id')['customer_age'].mean().reset_index()
    avg_age = avg_age.rename(columns={'customer_age': 'avg_age'})
    
    # Count of each category for different categories
    category_counts = [
        history_7_days.groupby('customer_id')[col].nunique().reset_index() 
        for col in ['product_code', 'product_type_no', 'graphical_appearance_no', 'colour_group_code', 'perceived_colour_value_id', 'perceived_colour_master_id', 'department_no', 'index_group_no','section_no', 'garment_group_no']
    ]
    
    # Rename columns in category_counts to avoid conflicts
    for category in category_counts:
        category = category.rename(columns={col: f'f_{col}_count' for col in category.columns[1:]})
    
    # Merge the computed features into one DataFrame and assign numeric columns into F
    F = avg_price.merge(avg_age, on='customer_id', validate='many_to_one')
    F = F.merge(*category_counts, on='customer_id', validate='many_to_one')
    
    F = F[['customer_id', 'avg_price', 'avg_age', 'f_product_code_count', 'f_product_type_no_count', 
          'f_graphical_appearance_no_count', 'f_colour_group_code_count', 'f_perceived_colour_value_id_count', 
          'f_perceived_colour_master_id_count', 'f_department_no_count', 'f_index_group_no_count', 
          'f_section_no_count', 'f_garment_group_no_count']]
    
    return F
