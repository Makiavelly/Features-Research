def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    # Calculate average purchase price for each customer
    avg_price_per_customer = history.pivot_table(index='customer_id', values='price', aggfunc='mean')
    avg_price_per_customer = avg_price_per_customer.reindex(index=X.index).fillna(0)
    F.loc[:, 'f_avg_price_per_customer'] = avg_price_per_customer[X.index].values

    # Calculate number of past purchases for each customer
    past_purchases_count_per_customer = history.groupby('customer_id')['article_id'].nunique().reindex(index=X.index).fillna(0)
    F.loc[:, 'f_past_purchases_count_per_customer'] = past_purchases_count_per_customer[X.index].values

    # Calculate average customer age for each customer
    avg_age_per_customer = history.pivot_table(index='customer_id', values='customer_age', aggfunc='mean')
    avg_age_per_customer = avg_age_per_customer.reindex(index=X.index).fillna(0)
    F.loc[:, 'f_avg_age_per_customer'] = avg_age_per_customer[X.index].values

    # Calculate number of articles purchased by each customer in the last 7 days
    past_purchases_count_last_7_days = history[history['days_ago'] <= 7].groupby('customer_id')['article_id'].nunique().reindex(index=X.index).fillna(0)
    F.loc[:, 'f_past_purchases_count_last_7_days'] = past_purchases_count_last_7_days[X.index].values

    # Calculate average purchase value for each article
    avg_purchase_value_per_article = history.pivot_table(index='article_id', values='price', aggfunc='mean')
    avg_purchase_value_per_article = avg_purchase_value_per_article.reindex(index=X.index).fillna(0)
    F.loc[:, 'f_avg_purchase_value_per_article'] = avg_purchase_value_per_article[X.index].values

    return F
