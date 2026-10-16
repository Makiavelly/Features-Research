def modify_features(X, history):
    # Compute the average age of customers who bought each product type
    avg_age_product_type = history.groupby('product_type_no')['customer_age'].mean().reset_index()
    avg_age_product_type = avg_age_product_type.rename(columns={'customer_age': 'f_avg_age_product_type'})
    
    # Compute the total number of past purchases for each customer-article-product type combination in the past 7 days
    history_7days = history[history['days_ago'] <= 7]
    customer_purchases_7days = history_7days.groupby(['customer_id', 'article_id', 'product_type_no'])['price'].sum().reset_index()
    customer_purchases_7days = customer_purchases_7days.rename(columns={'price': 'f_total_purchases_7days'})
    
    # Compute the count of customers aged 25-34 who bought each product type
    young_customers = history[history['customer_age'].between(25, 34)]
    product_type_young_customers = young_customers.groupby('product_type_no')['customer_age'].count().reset_index()
    product_type_young_customers = product_type_young_customers.rename(columns={'customer_age': 'f_young_customers'})
    
    # Compute the total number of past purchases for each customer-product type
    history_customer_product_type = history.groupby(['customer_id', 'product_type_no'])['price'].sum().reset_index()
    history_customer_product_type = history_customer_product_type.rename(columns={'price': 'f_total_purchases_customer_product_type'})
    
    # Merge the created features into the original DataFrame
    F = pd.merge(X, avg_age_product_type[['product_type_no', 'f_avg_age_product_type']], on='product_type_no', how='left')
    F = pd.merge(F, customer_purchases_7days[['customer_id', 'article_id', 'product_type_no', 'f_total_purchases_7days']], on=['customer_id', 'article_id', 'product_type_no'], how='left')
    F = pd.merge(F, product_type_young_customers[['product_type_no', 'f_young_customers']], on='product_type_no', how='left')
    F = pd.merge(F, history_customer_product_type[['customer_id', 'product_type_no', 'f_total_purchases_customer_product_type']], on=['customer_id', 'product_type_no'], how='left')
    
    return F
