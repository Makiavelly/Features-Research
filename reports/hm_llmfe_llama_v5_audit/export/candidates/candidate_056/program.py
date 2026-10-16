def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Calculate past purchases within a 7-day window
    history_7day = history[history['days_ago'] <= 7]
    F['f_past_purchases_7day'] = history_7day.groupby('customer_id')['article_id'].count().reindex(F.index) / 7
    
    # Calculate the number of articles purchased in total
    F['f_total_past_purchases'] = history.groupby('customer_id')['article_id'].count().reindex(F.index)
    
    # Calculate the average price of past purchases
    F['f_avg_price'] = history.groupby('customer_id')['price'].mean().reindex(F.index)
    
    # Calculate the number of different product codes purchased
    F['f_unique_product_codes'] = history.groupby('customer_id')['product_code'].nunique().reindex(F.index)
    
    # Calculate the number of articles purchased in the same department
    F['f_same_department_purchases'] = history.groupby('customer_id')['department_no'].apply(lambda x: x.value_counts().max()).reindex(F.index)
    
    return F
