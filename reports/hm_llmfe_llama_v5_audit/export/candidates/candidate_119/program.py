def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    # Compute mean of past purchase price and assign mean price column
    f_mean_price = history.groupby('customer_id')['price'].mean().reindex(X['customer_id']).fillna(0)
    F['f_mean_price'] = f_mean_price.values
    
    # Compute number of past purchases within 100 days and assign past_purchases column
    f_past_purchases = history[(history['days_ago'] <= 100) & (history['customer_id'].isin(X['customer_id']))].groupby('customer_id')['customer_id'].count().reindex(X['customer_id']).fillna(0)
    F['f_past_purchases'] = f_past_purchases.values
    
    # Compute mean of past purchases' product Types and assign mean_product_type column
    f_mean_product_type = history.groupby('customer_id')['product_type_no'].mean().reindex(X['customer_id']).fillna(0)
    F['f_mean_product_type'] = f_mean_product_type.values
    
    # Compute count of past purchases' colors and assign past_colors column
    f_past_colors = history.groupby('customer_id')['colour_group_code'].nunique().reindex(X['customer_id']).fillna(0)
    F['f_past_colors'] = f_past_colors.values
    
    return F
