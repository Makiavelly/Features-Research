def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Calculate past purchases count
    purchases_count = history.groupby('customer_id')['article_id'].count().add_suffix('_count').reset_index()
    
    # Calculate average price per customer
    avg_price_per_customer = history.loc[history['days_ago'] <= 180, ['customer_id', 'price']].groupby('customer_id')['price'].mean().reset_index().rename(columns={'price': 'avg_price'})
    
    # Merge aggregated history into F
    F = F.merge(purchases_count[['customer_id', 'article_id_count']], on='customer_id', how='left').merge(avg_price_per_customer[['customer_id', 'avg_price']], on='customer_id', how='left')
    
    # Calculate days ago histogram
    days_ago_bin_counts = history['days_ago'].value_counts(sort=False, bins=10).sort_index().rename('days_ago_count')
    
    # Merge days ago bin counts into F
    F = F.merge(days_ago_bin_counts.reset_index().rename(columns={'index': 'days_ago_bin'}), on='', how='left', left_index=True, right_index=True)
    
    # Filter days ago count for calendar-day windows
    F = F[F['days_ago_bin'] >= F['days_ago']].copy()
    
    # Drop unneeded columns
    F = F[['customer_id', 'article_id', 'article_id_count', 'avg_price', 'days_ago_bin', 'days_ago_count']]
    
    # Calculate average customer age
    avg_customer_age = history.loc[history['days_ago'] <= 180, ['customer_id', 'customer_age']].groupby('customer_id')['customer_age'].mean().reset_index().rename(columns={'customer_age': 'avg_customer_age'})
    
    # Merge average customer age into F
    F = F.merge(avg_customer_age[['customer_id', 'avg_customer_age']], on='customer_id', how='left')
    
    return F
