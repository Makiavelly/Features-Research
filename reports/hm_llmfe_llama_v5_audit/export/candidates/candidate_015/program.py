def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute average purchase price for each customer in the last 180 days
    avg_price = history.groupby('customer_id')[['price']].mean()
    F['f_avg_price'] = X['customer_id'].map(avg_price['price'])
    
    # Compute the number of past purchases for each customer in the last 180 days
    past_purchases = history.groupby('customer_id')[['days_ago']].count().reset_index()
    past_purchases.columns = ['customer_id', 'past_purchases']
    F['f_past_purchases'] = X['customer_id'].map(past_purchases.set_index('customer_id')['past_purchases'])
    
    # Compute the average age of customers who made purchases in the last 180 days
    avg_age = history.groupby('customer_id')[['customer_age']].mean()
    F['f_avg_age'] = X['customer_id'].map(avg_age['customer_age'])
    
    # Compute the average purchase price per day for each customer in the last 180 days
    avg_daily_price = history.pivot_table(index='customer_id', values='price', aggfunc='mean', columns='days_ago')
    avg_daily_price.columns = [f'f_avg_daily_price_{i}' for i in range(181)]
    F = pd.concat([F, avg_daily_price[X['customer_id'].reset_index().merge(avg_daily_price.index, left_on='customer_id', right_on='customer_id').sort_values('customer_id')]], axis=1)
    
    # Compute the number of past purchases per day for each customer in the last 180 days
    past_daily_purchases = history.pivot_table(index='customer_id', values='days_ago', aggfunc='size', columns='days_ago')
    past_daily_purchases.columns = [f'f_past_daily_purchases_{i}' for i in range(181)]
    F = pd.concat([F, past_daily_purchases[X['customer_id'].reset_index().merge(past_daily_purchases.index, left_on='customer_id', right_on='customer_id').sort_values('customer_id')]], axis=1)
    
    return F
