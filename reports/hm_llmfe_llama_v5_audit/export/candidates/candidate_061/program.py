def modify_features(X, history):
    """
    Compute useful numeric aggregates from clothing/customer domain knowledge.
    
    Parameters:
    X (DataFrame): Candidate articles per customer for purchases in next 7 days.
    history (DataFrame): Past transactions; no future data/labels.
    
    Returns:
    F (DataFrame): Features with exactly X.index and row order.
    """
    # Compute target variable, which is the average past purchases of customers within the last 180 days
    # who purchased the article before
    past_purchases = history.groupby('customer_id')[['days_ago', 'article_id']].apply(lambda x: (x[x['days_ago'] <= 180].groupby('article_id')['days_ago'].count() / 180) if not x.empty else 0).reset_index()
    
    # Compute the average age of customers
    avg_age = history.groupby('customer_id')['customer_age'].mean().reset_index()
    
    # Compute the average price of articles bought by customers
    avg_price = history.groupby('article_id')['price'].mean().reset_index()
    
    # Compute the average number of past purchases of customers
    avg_past_purchases_num = history.groupby('customer_id')['article_id'].nunique().reset_index()
    
    # Compute the unique values within the last 180 days for each article
    unique_articles_last_180_days = history.groupby('article_id')['days_ago'].nunique().reset_index()
    
    # Compute the average price of articles bought by customers within the last 180 days
    avg_price_last_180_days = history.groupby(['article_id', 'customer_id'])['price'].mean().reset_index()
    
    # Compute the average number of past purchases of each customer within the last 180 days
    avg_past_purchases_num_last_180_days = history.groupby(['customer_id', 'article_id'])['days_ago'].nunique().reset_index()
    
    # Merge the dataframes based on the customer id and article id
    F = pd.merge(past_purchases, avg_age, on='customer_id', validate='many_to_one')
    F = pd.merge(F, avg_price, on='article_id', validate='many_to_one')
    F = pd.merge(F, avg_past_purchases_num, on='customer_id', validate='many_to_one')
    F = pd.merge(F, unique_articles_last_180_days, on='article_id', validate='many_to_one')
    F = pd.merge(F, avg_price_last_180_days, on=['article_id', 'customer_id'], validate='many_to_one')
    F = pd.merge(F, avg_past_purchases_num_last_180_days, on=['article_id', 'customer_id'], validate='many_to_one')
    
    # Group by article id and calculate the average values
    F = F.groupby('article_id')[['past_purchases', 'avg_age', 'avg_price', 'avg_past_purchases_num',
                                   'unique_articles_last_180_days', 'avg_price_last_180_days',
                                   'avg_past_purchases_num_last_180_days']].mean().reset_index()
    
    # Rename the columns
    F.columns = ['f_past_purchases', 'f_avg_age', 'f_avg_price', 'f_avg_past_purchases_num',
                 'f_unique_articles_last_180_days', 'f_avg_price_last_180_days',
                 'f_avg_past_purchases_num_last_180_days']
    
    return F
