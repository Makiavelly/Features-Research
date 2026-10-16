def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute average purchase price for each customer in the last 180 days
    avg_price = history.pivot_table(index='customer_id', values='price', aggfunc='mean', observed=False)
    F['f_avg_price'] = X['customer_id'].map(avg_price)
    
    # Compute the number of past purchases for each customer in the last 180 days
    past_purchases = history.pivot_table(index='customer_id', aggfunc='size', observed=False)
    F['f_past_purchases'] = X['customer_id'].map(past_purchases)
    
    # Compute the average age of customers who made purchases in the last 180 days
    avg_age = history.pivot_table(index='customer_id', values='customer_age', aggfunc='mean', observed=False)
    F['f_avg_age'] = X['customer_id'].map(avg_age)
    
    # Compute the average purchase price per day for each customer in the last 180 days
    avg_daily_price = history.pivot_table(index='customer_id', values='price', aggfunc='mean', observed=False, bins=[0, 30, 60, 90, 180], columns='days_ago')
    F[['f_avg_daily_price_0_30', 'f_avg_daily_price_30_60', 'f_avg_daily_price_60_90', 'f_avg_daily_price_90_180']] = X['customer_id'].map(avg_daily_price)
    
    # Compute the number of past purchases per day for each customer in the last 180 days
    past_daily_purchases = history.pivot_table(index='customer_id', aggfunc='size', observed=False, bins=[0, 30, 60, 90, 180], columns='days_ago')
    F[['f_past_daily_purchases_0_30', 'f_past_daily_purchases_30_60', 'f_past_daily_purchases_60_90', 'f_past_daily_purchases_90_180']] = X['customer_id'].map(past_daily_purchases)
    
    return F
