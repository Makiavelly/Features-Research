def modify_features(X, history):
    # Filter days_ago for a 7-day history window, calculate past purchases and price mean for each customer
    history_7_days = history[history['days_ago'] <= 7]
    avg_price = history_7_days.groupby('customer_id')['price'].mean().reset_index()
    avg_price = avg_price[['customer_id', 'price']].rename(columns={'price': 'avg_price'})
    
    # Compute customer average age, count of each category, and most frequent article
    avg_age = history.groupby('customer_id')['customer_age'].mean().reset_index()
    avg_age = avg_age[['customer_id', 'customer_age']].rename(columns={'customer_age': 'avg_age'})
    
    # Count of each category for different categories: product_code, product_type_no, graphical_appearance_no, colour_group_code, perceived_colour_value_id, perceived_colour_master_id, department_no, index_group_no, section_no, garment_group_no
    category_counts = [
        history_7_days.groupby('customer_id')[col].nunique().reset_index().assign(col_name=col) 
        for col in ['product_code', 'product_type_no', 'graphical_appearance_no', 'colour_group_code', 'perceived_colour_value_id', 'perceived_colour_master_id', 'department_no', 'index_group_no','section_no', 'garment_group_no']
    ]
    
    # Merge the computed features into one DataFrame and assign numeric columns into F
    F = avg_price.merge(avg_age, on='customer_id', validate='many_to_one')
    F = F.merge(*category_counts, on='customer_id', validate='many_to_one')
    
    F = F[['customer_id', 'avg_price', 'avg_age'] + [col['col_name'] for col in category_counts[0]] + \
          [col['col_name'] for col in category_counts[1]] + [col['col_name'] for col in category_counts[2]] + \
          [col['col_name'] for col in category_counts[3]] + [col['col_name'] for col in category_counts[4]] + \
          [col['col_name'] for col in category_counts[5]] + [col['col_name'] for col in category_counts[6]] + \
          [col['col_name'] for col in category_counts[7]] + [col['col_name'] for col in category_counts[8]] + \
          [col['col_name'] for col in category_counts[9]]]
    
    return F
