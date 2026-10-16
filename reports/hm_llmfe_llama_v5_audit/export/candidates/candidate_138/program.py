def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute average purchase price for each customer in the last 180 days
    avg_price = history.loc[history['days_ago'] <= 180, 'customer_id'].value_counts().index.unique()
    avg_price_series = history.loc[history['days_ago'] <= 180, 'price'].groupby(history['customer_id']).mean()
    F['f_avg_price'] = avg_price_series.reindex(avg_price).fillna(0).values
    
    # Compute number of past purchases for each customer in the last 180 days
    past_purchases = history.loc[history['days_ago'] <= 180, 'customer_id'].value_counts().index.unique()
    past_purchases_series = history.loc[history['days_ago'] <= 180, 'days_ago'].groupby(history['customer_id']).count()
    F['f_past_purchases'] = past_purchases_series.reindex(past_purchases).fillna(0).values
    
    # Compute average age of customers who made purchases in the last 180 days
    avg_age = history.loc[history['days_ago'] <= 180, 'customer_id'].value_counts().index.unique()
    avg_age_series = history.loc[history['days_ago'] <= 180, 'customer_age'].groupby(history['customer_id']).mean()
    F['f_avg_age'] = avg_age_series.reindex(avg_age).fillna(0).values
    
    # Compute average number of past purchases per day for each customer in the last 180 days
    past_purchases_per_day = history.loc[history['days_ago'] <= 180, 'customer_id'].value_counts().index.unique()
    past_purchases_per_day_series = history.loc[history['days_ago'] <= 180, 'days_ago'].groupby(history['customer_id']).count() / 180
    F['f_past_purchases_per_day'] = past_purchases_per_day_series.reindex(past_purchases_per_day).fillna(0).values
    
    return F
