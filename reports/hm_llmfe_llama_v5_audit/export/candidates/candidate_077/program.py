def modify_features(X, history):
    # Calculate average price and the number of past purchases within the last 30 and 90 days
    avg_price_30_last = history.pivot_table(index='customer_id', columns='article_id', values='price', aggfunc='mean', fill_value=0)
    num_past_purchases_30_last = history.pivot_table(index='customer_id', columns='article_id', values='days_ago', aggfunc='sum', fill_value=0)
    avg_price_90_last = history.pivot_table(index='customer_id', columns='article_id', values='price', aggfunc='mean', fill_value=0, weighted=True, weights='days_ago')
    num_past_purchases_90_last = history.pivot_table(index='customer_id', columns='article_id', values='days_ago', aggfunc='sum', fill_value=0)

    # Calculate the average age of customers who purchased the article in the last 180 days
    avg_customer_age_last_180 = history[history['days_ago'] <= 180].pivot_table(index='customer_id', columns='article_id', values='customer_age', aggfunc='mean')

    # Create a new DataFrame with the calculated features
    F = pd.DataFrame(index=X.index)

    # Assign the calculated features to the new DataFrame
    F['f_avg_price_30_last'] = avg_price_30_last[X['article_id']].values
    F['f_num_past_purchases_30_last'] = num_past_purchases_30_last[X['article_id']].values
    F['f_avg_price_90_last'] = avg_price_90_last[X['article_id']].values
    F['f_num_past_purchases_90_last'] = num_past_purchases_90_last[X['article_id']].values
    F['f_avg_customer_age_last_180'] = avg_customer_age_last_180[X['article_id']].values

    return F
