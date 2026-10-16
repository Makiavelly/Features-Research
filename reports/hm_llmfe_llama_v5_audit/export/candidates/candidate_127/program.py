def modify_features(X, history):
    # Calculate the count of past purchases for each customer within the last 7 days
    past_purchases_7_days = history[(history['days_ago'] <= 7)].groupby('customer_id')['article_id'].nunique().reset_index()
    past_purchases_7_days = past_purchases_7_days.rename(columns={'article_id': 'f_past_purchases_7_days'})

    # Calculate the count of past purchases for each customer within the last 180 days
    past_purchases_180_days = history[(history['days_ago'] <= 180)].groupby('customer_id')['article_id'].nunique().reset_index()
    past_purchases_180_days = past_purchases_180_days.rename(columns={'article_id': 'f_past_purchases_180_days'})

    # Calculate the average purchase price for each customer within the last 180 days
    avg_price_180_days = history[(history['days_ago'] <= 180)].groupby('customer_id')['price'].mean().reset_index()
    avg_price_180_days = avg_price_180_days.rename(columns={'price': 'f_avg_price_180_days'})

    # Calculate the count of article categories for each customer within the last 180 days
    article_categories_180_days = history[(history['days_ago'] <= 180)].groupby('customer_id')['product_code'].nunique().reset_index()
    article_categories_180_days = article_categories_180_days.rename(columns={'product_code': 'f_article_categories_180_days'})

    # Merge the aggregates with X on customer_id
    F = X[['customer_id']]
    F = F.merge(past_purchases_7_days[['customer_id', 'f_past_purchases_7_days']], on='customer_id', how='left', validate='many_to_one')
    F = F.merge(past_purchases_180_days[['customer_id', 'f_past_purchases_180_days']], on='customer_id', how='left', validate='many_to_one')
    F = F.merge(avg_price_180_days[['customer_id', 'f_avg_price_180_days']], on='customer_id', how='left', validate='many_to_one')
    F = F.merge(article_categories_180_days[['customer_id', 'f_article_categories_180_days']], on='customer_id', how='left', validate='many_to_one')

    return F
