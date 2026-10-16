def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Calculate past purchases count
    purchases_count = history.groupby('customer_id')['article_id'].count().add_suffix('_count').reset_index()
    
    # Calculate average price per customer
    avg_price_per_customer = history.loc[history['days_ago'] <= 180, ['customer_id']].merge(history[['price']], left_on='customer_id', right_on='customer_id').groupby('customer_id')['price'].mean().reset_index().rename(columns={'price': 'avg_price'})
    
    # Merge aggregated history into F
    F = F.merge(purchases_count[['customer_id', 'article_id_count']], on='customer_id', how='left').merge(avg_price_per_customer[['customer_id', 'avg_price']], on='customer_id', how='left')
    
    # Calculate days_ago histogram
    days_ago_bin_counts = history['days_ago'].value_counts(bins=10, sort=False).sort_index().rename('days_ago_count')
    
    # Merge days_ago bin counts into F
    F = F.merge(days_ago_bin_counts.reset_index().rename(columns={'index': 'days_ago_bin', 0: 'days_ago_count'}), on='', how='left', left_index=True, right_index=True)
    
    # Filter days_ago_count for calendar-day windows (assuming days_ago>=0)
    F = F[F['days_ago'] >= F['days_ago_bin']].copy()
    
    # Create a new column with the result of a map operation on days_ago_count
    F['days_ago_count'] = F['days_ago_count'].map(lambda x: x if x > 0 else 0)
    
    # Drop unneeded columns
    F = F[['customer_id', 'article_id', 'article_id_count', 'avg_price', 'days_ago_bin', 'days_ago_count']]
    
    return F
