def modify_features(X, history):
    # Calculate average price per customer within the last 180 days
    avg_price_per_customer = history.pivot_table(index='customer_id', columns='article_id', values='price', aggfunc='mean', fill_value=0)
    F_avg_price_per_customer = pd.DataFrame(avg_price_per_customer)
    
    # Calculate number of purchases per customer within the last 180 days
    num_purchases_per_customer = history.pivot_table(index='customer_id', columns='article_id', values='customer_id', aggfunc='size', fill_value=0)
    F_num_purchases_per_customer = pd.DataFrame(num_purchases_per_customer)
    
    # Calculate average days ago per customer within the last 180 days
    avg_days_ago_per_customer = history.pivot_table(index='customer_id', columns='article_id', values='days_ago', aggfunc='mean', fill_value=0)
    F_avg_days_ago_per_customer = pd.DataFrame(avg_days_ago_per_customer)
    
    # Calculate average purchase frequency per customer within the last 180 days
    avg_purchase_frequency_per_customer = history.pivot_table(index='customer_id', columns='article_id', values='days_ago', aggfunc=lambda x: len(x) / x.max(), fill_value=0)
    F_avg_purchase_frequency_per_customer = pd.DataFrame(avg_purchase_frequency_per_customer)
    
    # Calculate average product type per customer within the last 180 days
    avg_product_type_per_customer = history.pivot_table(index='customer_id', columns='article_id', values='product_type_no', aggfunc='mean', fill_value=0)
    F_avg_product_type_per_customer = pd.DataFrame(avg_product_type_per_customer)
    
    # Calculate average purchase type per customer within the last 180 days
    avg_purchase_type_per_customer = history.pivot_table(index='customer_id', columns='article_id', values='product_code', aggfunc='mean', fill_value=0)
    F_avg_purchase_type_per_customer = pd.DataFrame(avg_purchase_type_per_customer)
    
    return pd.concat([F_avg_price_per_customer, F_num_purchases_per_customer, F_avg_days_ago_per_customer, F_avg_purchase_frequency_per_customer, F_avg_product_type_per_customer, F_avg_purchase_type_per_customer], axis=1)
