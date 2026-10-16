def modify_features(X, history):
    # Compute purchase count and average price for each customer in the past 180 days
    customer_history = history[history['days_ago'] <= 180].pivot_table(index='customer_id', values='price', columns='article_id', aggfunc=['sum','mean'], fill_value=0)
    customer_history.columns = [f'customer_{col}_purchase_count', f'customer_{col}_average_price']
    
    # Compute purchase count for each customer in the past 180 days
    customer_history = customer_history.groupby(customer_history.index)['customer_article_id_purchase_count'].sum().to_frame('customer_purchase_count').reset_index()
    
    # Merge purchased articles into customer purchase count
    customer_history = pd.merge(customer_history, history[history['days_ago'] <= 180].groupby('customer_id')['article_id'].nunique().to_frame('customer_purchased_articles'), left_on='customer_id', right_index=True, how='left')
    
    # Compute article frequency for each customer in the past 180 days
    article_frequency = history[history['days_ago'] <= 180].groupby('customer_id')['article_id'].count().to_frame('article_frequency').reset_index()
    article_frequency.columns = ['customer_id', 'article_frequency']
    
    # Merge article frequency into customer history
    customer_history = pd.merge(customer_history, article_frequency, on='customer_id', how='left')
    
    # Compute max purchase count for each customer in the past 180 days
    max_purchase_count = customer_history.groupby('customer_id')['customer_purchase_count'].max().to_frame('max_customer_purchase_count').reset_index()
    
    # Merge max purchase count into customer history
    customer_history = pd.merge(customer_history, max_purchase_count, on='customer_id', how='left')
    
    # Compute average age for each customer in the past 180 days
    customer_age = history[history['days_ago'] <= 180].groupby('customer_id')['customer_age'].mean().to_frame('customer_average_age').reset_index()
    
    # Merge average age into customer history
    customer_history = pd.merge(customer_history, customer_age, on='customer_id', how='left')
    
    # Replace NaN values with 0
    customer_history = customer_history.replace({np.nan: 0})
    
    # Compute mean and std of article frequency for each customer in the past 180 days
    article_frequency_mean = customer_history.groupby('customer_id')['article_frequency'].mean().to_frame('article_frequency_mean').reset_index()
    article_frequency_std = customer_history.groupby('customer_id')['article_frequency'].std().to_frame('article_frequency_std').reset_index()
    
    # Merge article frequency mean and std into customer history
    customer_history = pd.merge(customer_history, article_frequency_mean, on='customer_id', how='left')
    customer_history = pd.merge(customer_history, article_frequency_std, on='customer_id', how='left')
    
    # Compute mean and std of article average price for each customer in the past 180 days
    article_average_price_mean = customer_history.groupby('customer_id')['customer_article_id_average_price'].mean().to_frame('article_average_price_mean').reset_index()
    article_average_price_std = customer_history.groupby('customer_id')['customer_article_id_average_price'].std().to_frame('article_average_price_std').reset_index()
    
    # Merge article average price mean and std into customer history
    customer_history = pd.merge(customer_history, article_average_price_mean, on='customer_id', how='left')
    customer_history = pd.merge(customer_history, article_average_price_std, on='customer_id', how='left')
    
    # Compute mean and std of max purchase count for each customer in the past 180 days
    max_purchase_count_mean = customer_history.groupby('customer_id')['max_customer_purchase_count'].mean().to_frame('max_customer_purchase_count_mean').reset_index()
    max_purchase_count_std = customer_history.groupby('customer_id')['max_customer_purchase_count'].std().to_frame('max_customer_purchase_count_std').reset_index()
    
    # Merge max purchase count mean and std into customer history
    customer_history = pd.merge(customer_history, max_purchase_count_mean, on='customer_id', how='left')
    customer_history = pd.merge(customer_history, max_purchase_count_std, on='customer_id', how='left')
    
    # Merge customer history into original X DataFrame
    F = customer_history[['customer_id', 'article_id']].copy().set_index(['customer_id', 'article_id'])
    F = F.merge(customer_history[['customer_purchase_count', 'customer_average_age', 'article_frequency', 'article_frequency_mean', 'article_frequency_std', 'article_average_price', 'article_average_price_mean', 'article_average_price_std','max_customer_purchase_count','max_customer_purchase_count_mean','max_customer_purchase_count_std']].reset_index(), left_index=True, right_index=True, how='left')
    
    # Compute aggregates
    F['f_customer_purchase_count'] = F['customer_purchase_count']
    F['f_article_frequency'] = F['article_frequency']
    F['f_article_average_price'] = F['article_average_price']
    F['f_customer_average_age'] = F['customer_average_age']
    F['f_max_customer_purchase_count'] = F['max_customer_purchase_count']
    F['f_article_frequency_mean'] = F['article_frequency_mean']
    F['f_article_frequency_std'] = F['article_frequency_std']
    F['f_article_average_price_mean'] = F['article_average_price_mean']
    F['f_article_average_price_std'] = F['article_average_price_std']
    F['f_max_customer_purchase_count_mean'] = F['max_customer_purchase_count_mean']
    F['f_max_customer_purchase_count_std'] = F['max_customer_purchase_count_std']
    
    # Filter out rows where customer_id and article_id are not present in X
    F = F[F['customer_id'].isin(X['customer_id']) & F['article_id'].isin(X['article_id'])].reset_index(drop=True)
    
    return F
