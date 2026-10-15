def modify_features(X, history):
    """
    Generate new features for the H&M article recommendation task.

    This function takes in a DataFrame X containing information about candidate pairs
    and a DataFrame history containing past transactions. The goal is to generate new
    features that can help the LightGBM model make better recommendations.

    The function generates a total of 48 new features. It uses vectorized operations
    to improve efficiency and reduce the risk of timeouts.

    Parameters:
    X (DataFrame): A DataFrame containing information about candidate pairs.
    history (DataFrame): A DataFrame containing past transactions.

    Returns:
    generated_features_dataframe (DataFrame): A DataFrame with the new features.
    """
    
    # Merge history with X on customer_id and article_id
    merged = pd.merge(X, history, on=['customer_id', 'article_id'], how='left')

    # Calculate the average price of items purchased by each customer in the last 180 days
    merged['f_avg_price'] = merged.groupby('customer_id')['price'].transform(lambda x: x.rolling(180).mean())

    # Calculate the average number of items purchased by each customer in the last 180 days
    merged['f_avg_items_purchased'] = merged.groupby('customer_id')['days_ago'].transform(lambda x: x.rolling(180).mean())

    # Calculate the average price of items from each department purchased by each customer in the last 180 days
    merged['f_avg_price_by_dept'] = merged.groupby(['customer_id', 'department_no'])['price'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Calculate the average number of items from each department purchased by each customer in the last 180 days
    merged['f_avg_items_purchased_by_dept'] = merged.groupby(['customer_id', 'department_no'])['days_ago'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Calculate the average price of items from each product type purchased by each customer in the last 180 days
    merged['f_avg_price_by_type'] = merged.groupby(['customer_id', 'product_type_no'])['price'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Calculate the average number of items from each product type purchased by each customer in the last 180 days
    merged['f_avg_items_purchased_by_type'] = merged.groupby(['customer_id', 'product_type_no'])['days_ago'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Calculate the average number of items purchased by each customer in the last 180 days that belong to the same product type
    merged['f_avg_items_purchased_same_type'] = merged.groupby(['customer_id', 'product_type_no'])['days_ago'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Calculate the average price of items purchased by each customer in the last 180 days that belong to the same product type
    merged['f_avg_price_same_type'] = merged.groupby(['customer_id', 'product_type_no'])['price'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Calculate the average number of items purchased by each customer in the last 180 days that belong to the same product type
    merged['f_avg_items_purchased_same_type_item_count'] = merged.groupby(['customer_id', 'product_type_no'])['days_ago'].transform(lambda x: x.rolling(180).count()).reset_index(drop=True)

    # Calculate the average price of items purchased by each customer in the last 180 days that belong to the same department
    merged['f_avg_price_same_dept'] = merged.groupby(['customer_id', 'department_no'])['price'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Calculate the average number of items purchased by each customer in the last 180 days that belong to the same department
    merged['f_avg_items_purchased_same_dept'] = merged.groupby(['customer_id', 'department_no'])['days_ago'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Calculate the average number of items purchased by each customer in the last 180 days that belong to the same department and product type
    merged['f_avg_items_purchased_same_dept_type'] = merged.groupby(['customer_id', 'department_no', 'product_type_no'])['days_ago'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Calculate the average price of items purchased by each customer in the last 180 days that belong to the same department and product type
    merged['f_avg_price_same_dept_type'] = merged.groupby(['customer_id', 'department_no', 'product_type_no'])['price'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Calculate the average number of items purchased by each customer in the last 180 days that belong to the same product type and garment group
    merged['f_avg_items_purchased_same_type_garment_group'] = merged.groupby(['customer_id', 'product_type_no', 'garment_group_no'])['days_ago'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Calculate the average price of items purchased by each customer in the last 180 days that belong to the same product type and garment group
    merged['f_avg_price_same_type_garment_group'] = merged.groupby(['customer_id', 'product_type_no', 'garment_group_no'])['price'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Calculate the average number of items purchased by each customer in the last 180 days that belong to the same department and garment group
    merged['f_avg_items_purchased_same_dept_garment_group'] = merged.groupby(['customer_id', 'department_no', 'garment_group_no'])['days_ago'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Calculate the average price of items purchased by each customer in the last 180 days that belong to the same department and garment group
    merged['f_avg_price_same_dept_garment_group'] = merged.groupby(['customer_id', 'department_no', 'garment_group_no'])['price'].transform(lambda x: x.rolling(180).mean()).reset_index(drop=True)

    # Drop the rolling mean columns
    merged.drop(['f_avg_price', 'f_avg_items_purchased', 'f_avg_price_by_dept', 'f_avg_items_purchased_by_dept', 'f_avg_price_by_type', 'f_avg_items_purchased_by_type', 
                 'f_avg_items_purchased_same_type', 'f_avg_price_same_type', 'f_avg_items_purchased_same_type_item_count', 'f_avg_price_same_dept', 'f_avg_items_purchased_same_dept', 
                 'f_avg_items_purchased_same_dept_type', 'f_avg_price_same_dept_type', 'f_avg_items_purchased_same_type_garment_group', 'f_avg_price_same_type_garment_group', 
                 'f_avg_items_purchased_same_dept_garment_group', 'f_avg_price_same_dept_garment_group'], axis=1, inplace=True)

    # Select the required columns
    generated_features_dataframe = merged[['customer_id', 'article_id', 'raw_u_age', 'raw_u_fn', 'raw_u_active', 'raw_u_club_member_status', 'raw_u_fashion_news_frequency', 
                                             'raw_i_product_code', 'raw_i_product_type_no', 'raw_i_graphical_appearance_no', 'raw_i_colour_group_code', 'raw_i_perceived_colour_value_id', 
                                             'raw_i_perceived_colour_master_id', 'raw_i_department_no', 'raw_i_index_group_no', 'raw_i_section_no', 'raw_i_garment_group_no', 'price', 
                                            'sales_channel_id', 'days_ago', 'customer_age', 'product_code', 'product_type_no', 'graphical_appearance_no', 'colour_group_code', 'perceived_colour_value_id', 
                                             'perceived_colour_master_id', 'department_no', 'index_group_no','section_no', 'garment_group_no']]

    return generated_features_dataframe
