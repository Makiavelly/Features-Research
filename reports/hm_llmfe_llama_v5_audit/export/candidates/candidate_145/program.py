def modify_features(X, history):
    # Compute aggregates and assign numeric f_* columns into F.
    F = pd.DataFrame(index=X.index)
    
    # Calculate average purchase price and number of past purchases for each customer
    avg_price_per_customer = history.pivot_table(index='customer_id', values='price', aggfunc='mean')
    past_purchases_count_per_customer = history.pivot_table(index='customer_id', values='customer_id', aggfunc='count', fill_value=0)
    
    # Calculate average purchase price and number of past purchases for each article
    avg_price_per_article = history.pivot_table(index='article_id', values='price', aggfunc='mean')
    past_purchases_count_per_article = history.pivot_table(index='article_id', values='customer_id', aggfunc='count', fill_value=0)
    
    # Calculate average customer age and count of articles purchased by each customer
    avg_age_per_customer = history.pivot_table(index='customer_id', values='customer_age', aggfunc='mean')
    articles_purchased_count_per_customer = history.pivot_table(index='customer_id', values='customer_id', aggfunc='count', fill_value=0)
    
    # Calculate the average age of customers who purchased an article and the count of articles purchased by each customer
    avg_age_articles_purchased_per_customer = history.pivot_table(index='customer_id', values='customer_age', aggfunc=['mean', 'count'], fill_value=0)
    
    # Merge the aggregates onto X
    F.loc[:, 'f_avg_price_per_customer'] = avg_price_per_customer[X.index].values
    F.loc[:, 'f_past_purchases_count_per_customer'] = past_purchases_count_per_customer[X.index].values
    F.loc[:, 'f_avg_price_per_article'] = avg_price_per_article[X.index].values
    F.loc[:, 'f_past_purchases_count_per_article'] = past_purchases_count_per_article[X.index].values
    F.loc[:, 'f_avg_age_per_customer'] = avg_age_per_customer[X.index].values
    F.loc[:, 'f_articles_purchased_count_per_customer'] = articles_purchased_count_per_customer[X.index].values
    F.loc[:, 'f_avg_age_articles_purchased_per_customer'] = avg_age_articles_purchased_per_customer[X.index].T.values
    
    return F
