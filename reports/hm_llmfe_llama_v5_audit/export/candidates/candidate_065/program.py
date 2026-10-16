def modify_features(X, history):
    # Compute the average price for each article over the last 180 days
    avg_price = history.groupby('article_id')['price'].mean().to_frame('avg_price')
    
    # Compute the number of purchases for each customer over the last 180 days
    num_purchases = history.groupby('customer_id').size().to_frame('num_purchases')
    
    # Compute the average age of customers who purchased each article over the last 180 days
    avg_customer_age = history.merge(avg_price, on='article_id', how='left').groupby('article_id')['customer_age'].mean().to_frame('avg_customer_age')
    
    # Compute the number of articles purchased by each customer over the last 180 days
    unique_articles = history.groupby('customer_id')['article_id'].nunique().to_frame('unique_articles')
    
    # Merge the results into a single DataFrame
    result = pd.concat([num_purchases, avg_price, avg_customer_age, unique_articles], axis=1)
    
    # Assign the results to the positionally indexed F
    F = pd.DataFrame(index=X.index)
    F['f_avg_price'] = result['avg_price'].reindex(X['article_id']).fillna(0)
    F['f_num_purchases'] = result['num_purchases'].reindex(X['customer_id']).fillna(0)
    F['f_avg_customer_age'] = result['avg_customer_age'].reindex(X['article_id']).fillna(0)
    F['f_unique_articles'] = result['unique_articles'].reindex(X['customer_id']).fillna(0)
    
    return F
