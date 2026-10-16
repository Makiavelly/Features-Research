def modify_features(X, history):
    # Compute total past purchases for each customer
    customer_purchases = history.groupby('customer_id')['price'].sum().to_frame('total_purchases')
    
    # Compute average past purchases per day for each customer
    customer_avg_purchases = history.groupby('customer_id')['price'].mean().to_frame('avg_purchases_per_day')
    
    # Compute the total number of past purchases for each customer-article pair in the past 7 days
    history_7days = history[history['days_ago'] <= 7]
    customer_purchases_7days = history_7days.groupby(['customer_id', 'article_id'])['price'].sum().to_frame('total_purchases_7days')
    
    # Compute the average price of past purchases for each customer-article pair
    avg_price = history.groupby(['customer_id', 'article_id'])['price'].mean().to_frame('avg_price')
    
    # Compute the average age of customers who bought each article
    article_avg_age = history.groupby('article_id')['customer_age'].mean().to_frame('avg_age_customer')
    
    # Merge the features into a single DataFrame
    F = pd.merge(X[['customer_id', 'article_id']], customer_purchases, on='customer_id', how='left')
    F = pd.merge(F, customer_avg_purchases, on='customer_id', how='left')
    F = pd.merge(F, customer_purchases_7days, on=['customer_id', 'article_id'], how='left')
    F = pd.merge(F, avg_price, on=['customer_id', 'article_id'], how='left')
    F = pd.merge(F, article_avg_age, on='article_id', how='left')
    
    return F
