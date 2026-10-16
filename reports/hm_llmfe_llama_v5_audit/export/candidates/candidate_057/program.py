def modify_features(X, history):
    # Compute the average price and count of purchases for each customer within the last 180 days
    avg_price = history.pivot_table(index='customer_id', values='price', columns='article_id', aggfunc='mean', fill_value=0)
    
    # Compute the average customer age and count of purchases for each article within the last 180 days
    avg_age = history.pivot_table(index='article_id', values='customer_age', aggfunc='mean')
    
    # Compute the count of purchases for each article within the last 180 days
    purchases = history.pivot_table(index='article_id', values='customer_id', aggfunc='count')
    
    # Compute the average price and count of purchases for each article within the last 180 days
    avg_price_article = history.pivot_table(index='article_id', values='price', aggfunc='mean', fill_value=0)
    
    # Compute the average customer age and count of purchases for each customer within the last 180 days
    avg_age_customer = history.pivot_table(index='customer_id', values='customer_age', aggfunc='mean')
    
    # Join candidate keys LEFT to unique aggregates
    avg_price_article = pd.DataFrame(avg_price_article).index.rename('article_id')
    avg_price_article = avg_price_article.join(X[['customer_id']])
    avg_price_article = avg_price_article.set_index('customer_id', append=True)
    
    # Assign values to F (e.g. to_numpy) positionally, not by an unrelated index
    F = pd.DataFrame(index=X.index)
    F['f_avg_price_article'] = avg_price_article.unstack('article_id').iloc[:,0]
    F['f_count_purchases_article'] = purchases.unstack('article_id').iloc[:,0]
    F['f_avg_age_customer'] = avg_age_customer.unstack('article_id').iloc[:,0]
    
    return F
