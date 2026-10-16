def modify_features(X, history):
    # Compute the total number of past purchases for each customer
    customer_purchases = history.groupby('customer_id')['price'].sum().to_frame('f_total_purchases')
    
    # Compute the average age of customers who bought each article
    article_avg_age = history.groupby('article_id')['customer_age'].mean().to_frame('f_avg_age_customer')
    
    # Compute the total number of past purchases for each customer-article pair in the past 7 days
    history_7days = history[history['days_ago'] <= 7]
    customer_purchases_7days = history_7days.groupby(['customer_id', 'article_id'])['price'].sum().to_frame('f_total_purchases_7days')
    
    # Compute the count of customers aged 25-34 who bought each article
    young_customers = history[history['customer_age'].between(25, 34)]
    article_young_customers = young_customers.groupby('article_id').size().to_frame('f_young_customers')
    
    F = pd.DataFrame(index=X.index)
    F = pd.merge(F, customer_purchases[['customer_id', 'f_total_purchases']], on='customer_id', how='left', validate='many_to_one')
    F = pd.merge(F, article_avg_age[['article_id', 'f_avg_age_customer']], on='article_id', how='left', validate='many_to_one')
    F = pd.merge(F, customer_purchases_7days[['customer_id', 'article_id', 'f_total_purchases_7days']], on=['customer_id', 'article_id'], how='left', validate='many_to_one')
    F = pd.merge(F, article_young_customers[['article_id', 'f_young_customers']], on='article_id', how='left', validate='many_to_one')
    
    return F
