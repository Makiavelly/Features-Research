def modify_features(X, history):
    # Compute the number of past purchases of each customer within the last 180 days
    past_purchases = history.groupby('customer_id')['article_id'].nunique().reset_index()
    
    # Compute the average age of customers
    avg_age = history.groupby('customer_id')['customer_age'].mean().reset_index()
    
    # Compute the average price of articles bought by customers within the last 180 days
    avg_price_last_180_days = history.groupby(['customer_id', 'article_id'])['price'].mean().reset_index()
    
    # Merge the dataframes based on the customer id and article id
    F = pd.merge(past_purchases, avg_age, on='customer_id', validate='many_to_one')
    F = pd.merge(F, avg_price_last_180_days, on=['customer_id', 'article_id'], validate='many_to_one')
    
    # Group by article id and calculate the average values
    F = F.groupby('article_id')[['past_purchases', 'avg_age', 'avg_price_last_180_days']].mean().reset_index()
    
    # Rename the columns
    F.columns = ['f_past_purchases', 'f_avg_age', 'f_avg_price_last_180_days']
    
    return F
