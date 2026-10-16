def modify_features(X, history):
    # Aggregate past transactions per customer
    history_unique = history[["customer_id", "days_ago", "price"]].groupby('customer_id').apply(
        lambda x: x[x['days_ago'] < 180].mean()).reset_index()

    # Compute count of article types per customer in time window
    article_type_count = history[["customer_id", "product_type_no"]].groupby('customer_id').apply(
        lambda x: x["product_type_no"].value_counts().sort_index()).reset_index()

    # Merge the features into F
    F = pd.DataFrame(index=X.index)
    F['f_avg_price'] = history_unique['price']
    F['f_article_type_count'] = article_type_count['product_type_no']

    # Compute average fashion news frequency of customers who purchased
    hist_cluster = history.groupby('customer_id')['raw_u_fashion_news_frequency'].mean().reset_index()
    F['f_avg_fashion_news_frequency'] = history_unique['customer_id'].map(hist_cluster['raw_u_fashion_news_frequency'])

    return F
