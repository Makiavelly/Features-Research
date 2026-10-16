def modify_features(X, history):
    # Calculate average price within the last 90 days, weighted by the number of days since the purchase
    avg_price_90_weighted_last = (history.pivot_table(index='customer_id', columns='article_id', values='price', aggfunc='mean', fill_value=0) *
                                  history.pivot_table(index='customer_id', columns='article_id', values='days_ago', aggfunc='mean', fill_value=0)).mean(axis=1)

    # Calculate average price and the number of past purchases within the last 180 days
    avg_price_last_180 = history.pivot_table(index='customer_id', columns='article_id', values='price', aggfunc='mean', fill_value=0)
    num_past_purchases_last_180 = history.pivot_table(index='customer_id', columns='article_id', values='days_ago', aggfunc='count', fill_value=0)

    # Calculate the average age of customers who purchased the article in the last 180 days
    avg_customer_age_last_180 = history.pivot_table(index='customer_id', columns='article_id', values='customer_age', aggfunc='mean', fill_value=0)

    # Create a new DataFrame with the calculated features
    F = pd.DataFrame(index=X.index)

    # Assign the calculated features to the new DataFrame
    F['f_avg_price_90_weighted_last'] = avg_price_90_weighted_last[X['article_id']].values
    F['f_avg_price_last_180'] = avg_price_last_180[X['article_id']].values
    F['f_num_past_purchases_last_180'] = num_past_purchases_last_180[X['article_id']].values
    F['f_avg_customer_age_last_180'] = avg_customer_age_last_180[X['article_id']].values

    return F
