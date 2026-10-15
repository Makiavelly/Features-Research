def modify_features(X, history):
    """
    Generate new features for ranking fixed candidate articles per customer for purchases in the next 7 days.

    Parameters:
    X (DataFrame): Candidate pairs with customer and article information.
    history (DataFrame): Past transactions of customers.

    Returns:
    DataFrame: A DataFrame with new features for each candidate pair.
    """
    
    # Calculate the number of transactions in the past 7 days
    X['f_recent_transactions'] = history.groupby('customer_id')['price'].transform(lambda x: x[x > 0].shape[0] if not x.empty else 0)
    
    # Calculate the average age of customers who have purchased the article in the past 7 days
    X['f_recent_article_age'] = history.groupby(['customer_id', 'article_id'])['raw_u_age'].transform('mean')
    
    # Calculate the average frequency of fashion news for customers who have purchased the article in the past 7 days
    X['f_recent_article_fn_frequency'] = history.groupby(['customer_id', 'article_id'])['raw_u_fashion_news_frequency'].transform('mean')
    
    # Calculate the average price paid by customers who have purchased the article in the past 7 days
    X['f_recent_article_avg_price'] = history.groupby(['customer_id', 'article_id'])['price'].transform('mean')
    
    # Calculate the average number of transactions per customer in the past 7 days
    X['f_recent_transactions_per_customer'] = history.groupby('customer_id')['price'].transform(lambda x: x[x > 0].shape[0] if not x.empty else 0) / X.groupby('customer_id')['customer_id'].transform('count') if X.shape[0]!= 0 else 0
    
    # Calculate the average age of customers who have purchased any article in the past 7 days
    X['f_recent_customer_age'] = history.groupby('customer_id')['raw_u_age'].transform('mean')
    
    # Calculate the average frequency of fashion news for customers who have purchased any article in the past 7 days
    X['f_recent_customer_fn_frequency'] = history.groupby('customer_id')['raw_u_fashion_news_frequency'].transform('mean')
    
    # Calculate the average price paid by customers who have purchased any article in the past 7 days
    X['f_recent_customer_avg_price'] = history.groupby('customer_id')['price'].transform('mean')
    
    return X
