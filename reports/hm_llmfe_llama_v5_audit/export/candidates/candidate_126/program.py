def modify_features(X, history):
    # Calculate the count of past purchases for each customer within the last 180 days
    past_purchases = history[(history['days_ago'] <= 180)].groupby('customer_id')['article_id'].nunique().reset_index()
    past_purchases = past_purchases.rename(columns={'article_id': 'f_past_purchases'})

    # Calculate the count of past purchases for each customer within the last 180 days by article type
    past_purchase_types = history[(history['days_ago'] <= 180)].merge(history[['customer_id', 'article_id', 'product_type_no']], on=['customer_id', 'article_id'])
    past_purchase_types = past_purchase_types.groupby('customer_id')['product_type_no'].nunique().reset_index()
    past_purchase_types = past_purchase_types.rename(columns={'product_type_no': 'f_past_purchase_types'})

    # Calculate the average purchase price for each customer within the last 180 days
    avg_price = history[(history['days_ago'] <= 180)].groupby('customer_id')['price'].mean().reset_index()
    avg_price = avg_price.rename(columns={'price': 'f_avg_price'})

    # Merge the aggregates with X on customer_id
    F = X[['customer_id']]
    F = F.merge(past_purchases[['customer_id', 'f_past_purchases']], on='customer_id', how='left', validate='many_to_one')
    F = F.merge(avg_price[['customer_id', 'f_avg_price']], on='customer_id', how='left', validate='many_to_one')
    F = F.merge(past_purchase_types[['customer_id', 'f_past_purchase_types']], on='customer_id', how='left', validate='many_to_one')

    # Calculate the percentage of past purchases by article type for each customer within the last 180 days
    past_purchase_type_percentages = history[(history['days_ago'] <= 180)].merge(history[['customer_id', 'article_id', 'product_type_no']], on=['customer_id', 'article_id'])
    past_purchase_type_percentages = past_purchase_type_percentages.groupby('customer_id')['product_type_no'].value_counts().unstack('product_type_no')
    past_purchase_type_percentages = past_purchase_type_percentages.fillna(0).reset_index()
    past_purchase_type_percentages = past_purchase_type_percentages.add_prefix('f_past_purchase_type_percentages_')
    F = F.merge(past_purchase_type_percentages[['customer_id', 'f_past_purchase_type_percentages_product_type_no']], on='customer_id', how='left', validate='many_to_one')

    return F
