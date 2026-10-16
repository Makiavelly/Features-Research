def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute average number of purchases per week for each customer.
    avg_purchases_per_week = history.groupby('customer_id')['days_ago'].apply(lambda x: x[x <= 180].count() / 4).reset_index()[['customer_id']]
    F['f_avg_purchases_per_week'] = history.merge(avg_purchases_per_week, on='customer_id')['days_ago']

    # Compute average price per customer who purchased in last 2 weeks.
    recent_purchases = history[history['days_ago'] <= 14]
    avg_price_recent = recent_purchases.groupby('customer_id')['price'].mean().reset_index()[['customer_id']]
    F = F.merge(avg_price_recent, on='customer_id')[['customer_id', 'f_avg_price_recent']]

    # Compute maximum number of purchases in a week for each customer.
    max_purchases_in_week = history.groupby('customer_id')['days_ago'].apply(lambda x: x[x <= 180].value_counts().idxmax()).reset_index()[['customer_id']]
    F['f_max_purchases_in_week'] = history.merge(max_purchases_in_week, on='customer_id')['days_ago']

    # Compute average age of customers who purchased the most popular products.
    popular_products = history.groupby('article_id')['customer_id'].count().reset_index()[['article_id', 'customer_id']]
    popular_products = popular_products[popular_products['customer_id'] > 100]
    avg_age_popular = history.merge(popular_products, on='article_id')[['customer_id', 'customer_age']].groupby('customer_id')['customer_age'].mean().reset_index()[['customer_id']]
    F = F.merge(avg_age_popular, on='customer_id')[['customer_id', 'f_avg_age_popular']]

    # Compute average days ago for the most frequently purchased department.
    freq_departments = history['department_no'].value_counts().reset_index()
    max_freq_department = freq_departments.idxmax()
    avg_days_recent = history[history['department_no'] == max_freq_department][['customer_id', 'days_ago']]
    avg_days_recent = avg_days_recent.groupby('customer_id')['days_ago'].mean().reset_index()[['customer_id']]
    F = F.merge(avg_days_recent, on='customer_id')[['customer_id', 'f_avg_days_recent']]

    return F[['customer_id', 'f_avg_purchases_per_week', 'f_avg_price_recent', 'f_max_purchases_in_week', 'f_avg_age_popular', 'f_avg_days_recent']]
