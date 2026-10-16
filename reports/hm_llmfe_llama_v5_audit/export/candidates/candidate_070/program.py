def modify_features(X, history):
    # Aggregate past transactions per customer
    history_unique = history.groupby('customer_id').apply(lambda x: x[x['days_ago'] < 180].max()).reset_index()

    # Compute average purchase price per customer in time window
    F = pd.DataFrame({'f_avg_price': history_unique.groupby('customer_id')['price'].mean().values})

    # Compute average fashion news frequency of customers who purchased
    fashion_news_freq = history_unique.groupby('customer_id')['raw_u_fashion_news_frequency'].mean().reset_index()
    F = pd.merge(F, fashion_news_freq, how='left', on='customer_id', validate='many_to_one')

    # Compute count of article types per customer in time window
    article_type_count = history_unique['product_type_no'].value_counts().sort_index().to_frame('article_type_count').reset_index()
    F = pd.merge(F, article_type_count, how='left', on='product_type_no', validate='many_to_one')

    return F.iloc[X.index]
