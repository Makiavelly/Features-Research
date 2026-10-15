def modify_features(X, history):
    """
    Generate non-trivial recommendation features for clothing customers.
    
    Hypothesis: Features that capture customer buying behavior, article attributes,
    and their interactions will be useful for recommending articles.
    """
    
    # Calculate the mean and count of articles purchased by each customer in the past 7 days
    customer_article_mean = history.groupby('customer_id')['article_id'].apply(lambda x: x.nlargest(7).mean())
    customer_article_count = history.groupby('customer_id')['article_id'].apply(lambda x: x.nlargest(7).count())
    
    # Merge the results into the original DataFrame
    X['customer_article_mean'] = X['customer_id'].map(customer_article_mean)
    X['customer_article_count'] = X['customer_id'].map(customer_article_count)
    
    # Calculate the popularity of each article (number of customers who purchased it in the past 7 days)
    article_popularity = history.groupby('article_id')['customer_id'].nunique().reset_index(name='popularity')
    
    # Merge the results into the original DataFrame
    X = X.merge(article_popularity, on='article_id', how='left')
    
    # Calculate the similarity between each article and the articles purchased by the customer in the past 7 days
    article_similarity = history.groupby('customer_id')['article_id'].apply(lambda x: x.nlargest(7).map(lambda y: x.nlargest(7).isin(x['article_id']).sum()))
    
    # Merge the results into the original DataFrame
    X['article_similarity'] = X['customer_id'].map(article_similarity)
    
    # Calculate the average price of articles purchased by each customer in the past 7 days
    customer_average_price = history.groupby('customer_id')['price'].apply(lambda x: x.nlargest(7).mean())
    
    # Merge the results into the original DataFrame
    X['customer_average_price'] = X['customer_id'].map(customer_average_price)
    
    # Calculate the number of different departments purchased by each customer in the past 7 days
    customer_department_count = history.groupby('customer_id')['department_no'].apply(lambda x: x.nlargest(7).nunique())
    
    # Merge the results into the original DataFrame
    X['customer_department_count'] = X['customer_id'].map(customer_department_count)
    
    # Return the updated DataFrame
    return X
