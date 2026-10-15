def modify_features(X, history):
    """
    Generate new features for the ranking of fixed candidate articles per customer
    for purchases in the next 7 days, maximizing validation MAP@12.

    Hypothesis: Customers who have purchased similar products in the past are more
    likely to buy similar products in the future.
    """
    
    # Calculate the number of past purchases for each customer
    num_past_purchases = history.groupby('customer_id')['article_id'].count().reset_index(name='num_past_purchases')
    
    # Merge the number of past purchases into X
    X = X.merge(num_past_purchases, on='customer_id', how='left')
    
    # Calculate the number of past purchases for each article
    num_past_purchases_article = history.groupby('article_id')['customer_id'].count().reset_index(name='num_past_purchases_article')
    
    # Merge the number of past purchases for each article into X
    X = X.merge(num_past_purchases_article, on='article_id', how='left')
    
    # Calculate the average price of past purchases for each customer
    avg_past_price_customer = history.groupby('customer_id')['price'].mean().reset_index(name='avg_past_price_customer')
    
    # Merge the average price of past purchases for each customer into X
    X = X.merge(avg_past_price_customer, on='customer_id', how='left')
    
    # Calculate the average price of past purchases for each article
    avg_past_price_article = history.groupby('article_id')['price'].mean().reset_index(name='avg_past_price_article')
    
    # Merge the average price of past purchases for each article into X
    X = X.merge(avg_past_price_article, on='article_id', how='left')
    
    # Calculate the number of past purchases in each clothing product family/type
    num_past_purchases_family = history.groupby('raw_i_product_type_no')['article_id'].count().reset_index(name='num_past_purchases_family')
    
    # Merge the number of past purchases in each clothing product family/type into X
    X = X.merge(num_past_purchases_family, on='raw_i_product_type_no', how='left')
    
    # Calculate the average price of past purchases in each clothing product family/type
    avg_past_price_family = history.groupby('raw_i_product_type_no')['price'].mean().reset_index(name='avg_past_price_family')
    
    # Merge the average price of past purchases in each clothing product family/type into X
    X = X.merge(avg_past_price_family, on='raw_i_product_type_no', how='left')
    
    # Calculate the number of past purchases in each clothing product type
    num_past_purchases_type = history.groupby('raw_i_product_code')['article_id'].count().reset_index(name='num_past_purchases_type')
    
    # Merge the number of past purchases in each clothing product type into X
    X = X.merge(num_past_purchases_type, on='raw_i_product_code', how='left')
    
    # Calculate the average price of past purchases in each clothing product type
    avg_past_price_type = history.groupby('raw_i_product_code')['price'].mean().reset_index(name='avg_past_price_type')
    
    # Merge the average price of past purchases in each clothing product type into X
    X = X.merge(avg_past_price_type, on='raw_i_product_code', how='left')
    
    # Calculate the difference between the number of past purchases and the average price of past purchases
    X['f_num_past_purchases_diff_avg_past_price'] = X['num_past_purchases'] - X['avg_past_price_customer']
    
    # Calculate the average of the difference between the number of past purchases and the average price of past purchases
    X['f_avg_num_past_purchases_diff_avg_past_price'] = X.groupby('customer_id')['num_past_purchases_diff_avg_past_price'].transform('mean')
    
    # Calculate the difference between the number of past purchases in each product type and the average price of past purchases
    X['f_num_past_purchases_type_diff_avg_past_price_type'] = X['num_past_purchases_type'] - X['avg_past_price_type']
    
    # Calculate the average of the difference between the number of past purchases in each product type and the average price of past purchases
    X['f_avg_num_past_purchases_type_diff_avg_past_price_type'] = X.groupby('raw_i_product_code')['num_past_purchases_type_diff_avg_past_price_type'].transform('mean')
    
    # Remove index before returning
    #X.index=x.index
    
    return X
