def modify_features(X, history):
    # Compute mean of past purchase price and assign mean price column
    f_mean_price = history.groupby('customer_id')['price'].mean().reindex(X['customer_id']).fillna(0)
    F = pd.DataFrame(index=X.index)
    F['f_mean_price'] = f_mean_price.values

    # Compute number of past purchases within 100 days and assign past_purchases column
    f_past_purchases = history[(history['days_ago'] <= 100) & (history['customer_id'].isin(X['customer_id']))].groupby('customer_id')['customer_id'].count().reindex(X['customer_id']).fillna(0)
    F['f_past_purchases'] = f_past_purchases.values

    # Compute mean of past purchases' product types and assign mean_product_type column
    f_mean_product_type = history.groupby('customer_id')['product_type_no'].mean().reindex(X['customer_id']).fillna(0)
    F['f_mean_product_type'] = f_mean_product_type.values

    # Compute count of past purchases' colors and assign past_colors column
    f_past_colors = history.groupby('customer_id')['colour_group_code'].nunique().reindex(X['customer_id']).fillna(0)
    F['f_past_colors'] = f_past_colors.values

    # Compute count of past purchases' garment groups and assign past_garment_groups column
    f_past_garment_groups = history.groupby('customer_id')['garment_group_no'].nunique().reindex(X['customer_id']).fillna(0)
    F['f_past_garment_groups'] = f_past_garment_groups.values

    # Compute mean of past purchases' sales channels and assign mean_sales_channel column
    f_mean_sales_channel = history.groupby('customer_id')['sales_channel_id'].mean().reindex(X['customer_id']).fillna(0)
    F['f_mean_sales_channel'] = f_mean_sales_channel.values

    return F
