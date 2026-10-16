def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Compute average purchase price for each customer in the last 180 days
    avg_price = history.loc[history['days_ago'] <= 180, 'customer_id'].value_counts().index.get_level_values(0).unique()
    avg_price = history.loc[history['days_ago'] <= 180, 'price'].groupby(history['customer_id']).mean().reindex(avg_price).fillna(0)
    F['f_avg_price'] = pd.Series(index=X['customer_id'].unique(), data=avg_price).reindex(X['customer_id'], fill_value=0)
    
    # Compute number of past purchases for each customer in the last 180 days
    past_purchases = history.loc[history['days_ago'] <= 180, 'customer_id'].value_counts().index.get_level_values(0).unique()
    past_purchases = history.loc[history['days_ago'] <= 180, 'days_ago'].groupby(history['customer_id']).count().reindex(past_purchases).fillna(0)
    F['f_past_purchases'] = pd.Series(index=X['customer_id'].unique(), data=past_purchases).reindex(X['customer_id'], fill_value=0)
    
    # Compute average age of customers who made purchases in the last 180 days
    avg_age = history.loc[history['days_ago'] <= 180, 'customer_id'].value_counts().index.get_level_values(0).unique()
    avg_age = history.loc[history['days_ago'] <= 180, 'customer_age'].groupby(history['customer_id']).mean().reindex(avg_age).fillna(0)
    F['f_avg_age'] = pd.Series(index=X['customer_id'].unique(), data=avg_age).reindex(X['customer_id'], fill_value=0)
    
    # Compute average number of past purchases per day for each customer in the last 180 days
    past_purchases_per_day = history.loc[history['days_ago'] <= 180, 'customer_id'].value_counts().index.get_level_values(0).unique()
    past_purchases_per_day = history.loc[history['days_ago'] <= 180, 'days_ago'].groupby(history['customer_id']).count().reindex(past_purchases_per_day).fillna(0) / 180
    F['f_past_purchases_per_day'] = pd.Series(index=X['customer_id'].unique(), data=past_purchases_per_day).reindex(X['customer_id'], fill_value=0)
    
    return F
