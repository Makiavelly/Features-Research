def modify_features(X, history):
    # Compute average purchase price for each customer in the last 180 days
    avg_price_series = history.loc[history['days_ago'] <= 180, 'price'].groupby(history['customer_id']).mean().mean()
    F = pd.DataFrame(index=X.index)
    F['f_avg_price'] = avg_price_series.values
    
    # Compute number of past purchases for each customer in the last 180 days
    past_purchases_series = history.loc[history['days_ago'] <= 180, 'customer_id'].value_counts().sort_index().sort_index().reindex(X['customer_id']).fillna(0)
    F['f_past_purchases'] = past_purchases_series[X.index].values
    
    # Compute average age of customers who made purchases in the last 180 days
    avg_age_series = history.loc[history['days_ago'] <= 180, 'customer_age'].groupby(history['customer_id']).mean().mean()
    F['f_avg_age'] = avg_age_series.values
    
    # Compute average number of past purchases per day for each customer in the last 180 days
    past_purchases_per_day_series = history.loc[history['days_ago'] <= 180, 'days_ago'].groupby(history['customer_id']).count().mean()
    F['f_past_purchases_per_day'] = past_purchases_per_day_series.values
    
    return F
