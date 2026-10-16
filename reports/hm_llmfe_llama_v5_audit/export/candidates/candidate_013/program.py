def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Calculate average price per customer
    avg_price = history.loc[history['days_ago'] <= 180, ['customer_id', 'price']].groupby('customer_id')['price'].mean().reset_index()
    
    # Calculate average customer age
    avg_customer_age = history.loc[history['days_ago'] <= 180, ['customer_id', 'customer_age']].groupby('customer_id')['customer_age'].mean().reset_index()
    
    # Calculate days ago count for calendar-day windows
    days_ago_bin_counts = history['days_ago'].value_counts(sort=True, bins=10, normalize=True).sort_index().rename('days_ago_bin_count')
    
    # Merge aggregated history into F
    F = F.merge(avg_price[['customer_id', 'price']], on='customer_id', how='left').merge(avg_customer_age[['customer_id', 'customer_age']], on='customer_id', how='left').merge(days_ago_bin_counts.reset_index().rename(columns={'index': 'days_ago'}), on='', how='left', left_index=True, right_index=True)
    
    # Filter days ago count for calendar-day windows
    F = F[F['days_ago'] >= F['days_ago']].copy()
    
    # Assign values positionally to F
    F = F[['customer_id', 'article_id', 'price', 'customer_age', 'days_ago_bin_count', 'days_ago']]
    
    return F
