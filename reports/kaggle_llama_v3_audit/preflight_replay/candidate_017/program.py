def modify_features(X, history):
    """
    Generate new features for customer-article pairs.
    
    This function generates up to 48 numeric columns named f_*. 
    The host always appends the same 15 raw static features.
    
    Parameters:
    X (DataFrame): DataFrame with one row per candidate pair.
    history (DataFrame): DataFrame containing only past transactions.
    
    Returns:
    DataFrame: DataFrame with exactly X.index and row order, containing new features.
    """
    
    # Merge history and X on customer_id and article_id
    merged_history = pd.merge(X, history, on=['customer_id', 'article_id'], how='left')
    
    # Generate new features
    merged_history['f_days_since_last_purchase'] = merged_history.groupby('customer_id')['days_ago'].transform('min')
    merged_history['f_last_purchase_article_type'] = merged_history.groupby('customer_id')['raw_i_product_type_no'].transform('first')
    merged_history['f_last_purchase_price'] = merged_history.groupby('customer_id')['price'].transform('first')
    merged_history['f_last_purchase_department'] = merged_history.groupby('customer_id')['raw_i_department_no'].transform('first')
    merged_history['f_average_purchase_price'] = merged_history.groupby('customer_id')['price'].transform('mean')
    merged_history['f_average_purchase_article_type'] = merged_history.groupby('customer_id')['raw_i_product_type_no'].transform('mean')
    merged_history['f_average_purchase_department'] = merged_history.groupby('customer_id')['raw_i_department_no'].transform('mean')
    merged_history['f_number_of_purchases'] = merged_history.groupby('customer_id')['days_ago'].count()
    merged_history['f_recent_purchase'] = merged_history.groupby('customer_id')['days_ago'].transform('min') < 30
    merged_history['f_last_purchase_in_same_department'] = merged_history['raw_i_department_no'].eq(merged_history['raw_i_department_no'].shift())
    merged_history['f_last_purchase_in_same_type'] = merged_history['raw_i_product_type_no'].eq(merged_history['raw_i_product_type_no'].shift())
    merged_history['f_same_article_purchased_before'] = merged_history['article_id'].duplicated()
    merged_history['f_same_article_bought_before'] = merged_history['article_id'].duplicated(keep=False)
    merged_history['f_last_purchase_price_in_same_department'] = merged_history.groupby('customer_id')['raw_i_department_no'].transform('first') == merged_history['raw_i_department_no']
    merged_history['f_last_purchase_price_in_same_type'] = merged_history.groupby('customer_id')['raw_i_product_type_no'].transform('first') == merged_history['raw_i_product_type_no']
    merged_history['f_average_purchase_price_in_same_department'] = merged_history.groupby('customer_id')['raw_i_department_no'].transform('first') == merged_history['raw_i_department_no']
    merged_history['f_average_purchase_price_in_same_type'] = merged_history.groupby('customer_id')['raw_i_product_type_no'].transform('first') == merged_history['raw_i_product_type_no']
    merged_history['f_same_price_level_last_purchase'] = merged_history.groupby('customer_id')['price'].transform('first') == merged_history['price']
    merged_history['f_same_price_level_last_purchase_in_same_department'] = merged_history.groupby('customer_id')['raw_i_department_no'].transform('first') == merged_history['raw_i_department_no']
    merged_history['f_same_price_level_last_purchase_in_same_type'] = merged_history.groupby('customer_id')['raw_i_product_type_no'].transform('first') == merged_history['raw_i_product_type_no']
    
    # Select new features
    new_features = merged_history.loc[:, ['f_days_since_last_purchase', 'f_last_purchase_article_type',
                                           'f_last_purchase_price', 'f_last_purchase_department',
                                           'f_average_purchase_price', 'f_average_purchase_article_type',
                                           'f_average_purchase_department',
                                           'f_number_of_purchases', 'f_recent_purchase',
                                           'f_last_purchase_in_same_department', 'f_last_purchase_in_same_type',
                                           'f_same_article_purchased_before', 'f_same_article_bought_before',
                                           'f_last_purchase_price_in_same_department',
                                           'f_last_purchase_price_in_same_type',
                                           'f_average_purchase_price_in_same_department',
                                           'f_average_purchase_price_in_same_type',
                                           'f_same_price_level_last_purchase',
                                           'f_same_price_level_last_purchase_in_same_department',
                                           'f_same_price_level_last_purchase_in_same_type']]
    
    # Return new features with the same order as X
    return new_features.reset_index(drop=True)
