def modify_features(X, history):
    # Compute average number of purchases per week for each customer
    avg_purchases_per_week = history.groupby('customer_id')[
        (history['days_ago'] <= 180)]['days_ago'].count().reset_index()
    avg_purchases_per_week = avg_purchases_per_week.rename(
        columns={'days_ago': 'f_avg_purchases_per_week'})

    # Compute average price per customer who purchased in last 2 weeks
    recent_purchases = history[history['days_ago'] <= 14]
    avg_price_recent = recent_purchases.groupby('customer_id')['price'].mean().reset_index()
    avg_price_recent = avg_price_recent.rename(columns={'price': 'f_avg_price_recent'})

    # Compute maximum number of purchases in a week for each customer
    max_purchases_in_week = history.groupby('customer_id')['days_ago'].apply(lambda x: (x[x <= 180].value_counts().idxmax() - 1) / 3).reset_index()
    max_purchases_in_week = max_purchases_in_week.rename(columns={'days_ago': 'f_max_purchases_in_week'})

    # Compute average age of customers who purchased the most popular products
    popular_products = history.groupby('article_id')['customer_id'].count().reset_index()
    popular_products = popular_products[popular_products['customer_id'] > 100]
    avg_age_popular = history.merge(popular_products, on='article_id')[['customer_id', 'customer_age']].groupby('customer_id')['customer_age'].mean().reset_index()
    avg_age_popular = avg_age_popular.rename(columns={'customer_age': 'f_avg_age_popular'})

    # Compute average days ago for the most frequently purchased department
    freq_departments = history['department_no'].value_counts().reset_index()
    max_freq_department = freq_departments['department_no'].max()
    avg_days_recent = history[history['department_no'] == max_freq_department][['customer_id', 'days_ago']]
    avg_days_recent = avg_days_recent.groupby('customer_id')['days_ago'].mean().reset_index()
    avg_days_recent = avg_days_recent.rename(columns={'days_ago': 'f_avg_days_recent'})

    # Merge all features
    F = pd.concat([avg_purchases_per_week, avg_price_recent, max_purchases_in_week,
                   avg_age_popular, avg_days_recent], ignore_index=True)
    return F
