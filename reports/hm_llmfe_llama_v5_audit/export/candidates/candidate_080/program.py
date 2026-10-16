def modify_features(X, history):
    # Merge customer_id and article_id from X with history
    merged = history.merge(X[['customer_id', 'article_id']], on='customer_id', validate='many_to_one')

    # Calculate average price within the last 90 days
    avg_price_90_weighted_last = merged.groupby('article_id')['price'].apply(lambda x: x[x['days_ago'] <= 90].sum() / (x['days_ago'].loc[x['days_ago'] <= 90] + 1)).reset_index()

    # Merge avg_price_90_weighted_last with X on article_id
    avg_price_90_weighted_last = avg_price_90_weighted_last.merge(X[['article_id']], on='article_id', how='left')

    # Create a new DataFrame with the calculated features
    F = pd.DataFrame(index=X.index)

    # Assign the calculated features to the new DataFrame
    F['f_avg_price_90_weighted_last'] = avg_price_90_weighted_last['price'].values
    F['f_avg_price_last_180'] = merged.groupby('article_id')['price'].apply(lambda x: x[x['days_ago'] <= 180].mean()).reset_index()['price'].values
    F['f_num_past_purchases_last_180'] = merged[merged['days_ago'] <= 180].groupby('article_id')['days_ago'].count().reset_index()['days_ago'].values

    return F
