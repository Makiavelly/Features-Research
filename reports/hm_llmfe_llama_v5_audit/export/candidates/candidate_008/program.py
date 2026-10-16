def modify_features(X, history):
    F = pd.DataFrame(index=X.index)

    # Calculate the average purchase price of each customer in the last 180 days
    avg_price_filter = (history['customer_id'] == X['customer_id']) & (history['days_ago'] <= 180)
    avg_price = history[avg_price_filter][['customer_id', 'price']].groupby('customer_id')['price'].mean().to_frame('avg_price')
    F['f_avg_price'] = avg_price['avg_price'].reindex(X['customer_id']).fillna(0).astype(float)

    # Calculate the count of past purchases for each customer in the last 180 days
    past_purchases_filter = (history['customer_id'] == X['customer_id']) & (history['days_ago'] <= 180)
    past_purchases = history[past_purchases_filter][['customer_id']].groupby('customer_id').size().to_frame('past_purchases')
    F['f_past_purchases'] = past_purchases['past_purchases'].reindex(X['customer_id']).fillna(0).astype(float)

    # Calculate the average age of customers who purchased each article in the last 180 days
    avg_age_filter = (history['article_id'] == X['article_id']) & (history['days_ago'] <= 180)
    avg_age = history[avg_age_filter][['article_id', 'customer_age']].groupby('article_id')['customer_age'].mean().to_frame('avg_age')
    F['f_avg_age'] = avg_age['avg_age'].reindex(X['article_id']).fillna(0).astype(float)

    # Calculate the count of customers who purchased each article in the last 180 days
    customer_count_filter = (history['article_id'] == X['article_id']) & (history['days_ago'] <= 180)
    customer_count = history[customer_count_filter]['customer_id'].groupby('article_id').nunique().to_frame('customer_count')
    F['f_customer_count'] = customer_count['customer_count'].reindex(X['article_id']).fillna(0).astype(float)

    return F[['f_avg_price', 'f_past_purchases', 'f_avg_age', 'f_customer_count']]
