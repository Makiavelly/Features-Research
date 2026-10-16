def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    # Compute the count of each product type purchased by each customer in the last 7 days
    history_7_days = history[history['days_ago'] <= 7]
    product_type_count = history_7_days.groupby('customer_id')['product_type_no'].nunique().reset_index()
    product_type_count = product_type_count.rename(columns={'product_type_no': 'f_product_type_count'})
    # Compute the count of each color group purchased by each customer in the last 7 days
    color_group_count = history_7_days.groupby('customer_id')['colour_group_code'].nunique().reset_index()
    color_group_count = color_group_count.rename(columns={'colour_group_code': 'f_colour_group_count'})
    # Compute the past purchases of each customer
    past_purchases = history.groupby('customer_id')['days_ago'].max().reset_index()
    past_purchases = past_purchases.rename(columns={'days_ago': 'f_past_purchases'})
    # Compute the average age of each customer
    avg_age = history.groupby('customer_id')['customer_age'].mean().reset_index()
    avg_age = avg_age.rename(columns={'customer_age': 'f_avg_age'})
    # Compute the average price of each customer
    avg_price = history_7_days.groupby('customer_id')['price'].mean().reset_index()
    avg_price = avg_price.rename(columns={'price': 'f_avg_price'})
    # Merge the computed features into one DataFrame and assign numeric columns into F
    F = product_type_count.merge(avg_age, on='customer_id', validate='many_to_one')
    F = F.merge(avg_price, on='customer_id', validate='many_to_one')
    F = F.merge(color_group_count, on='customer_id', validate='many_to_one')
    F = F.merge(past_purchases, on='customer_id', validate='many_to_one')
    F = F.drop(columns=['customer_id'])  # Remove customer_id column as it is not a feature
    return F
