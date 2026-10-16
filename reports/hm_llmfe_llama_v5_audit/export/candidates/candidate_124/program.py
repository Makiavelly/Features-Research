def modify_features(X, history):
    # Calculate the count of past purchases for each customer within the last 180 days
    past_purchases = history.groupby('customer_id')['days_ago'].apply(lambda x: (x <= 180).sum()).reset_index()
    
    # Calculate the average purchase price for each customer within the last 180 days
    avg_price = history.groupby('customer_id')['price'].mean().reset_index()
    
    # Calculate the count of products purchased by each customer within the last 180 days
    product_counts = history.groupby('customer_id')['article_id'].nunique().reset_index()
    
    # Calculate the count of unique article categories purchased by each customer within the last 180 days
    category_counts = history.merge(past_purchases, on='customer_id').merge(avg_price, on='customer_id')
    category_counts = category_counts.merge(product_counts, on='customer_id')
    category_counts['f_category_counts'] = category_counts.groupby('customer_id')['product_code'].nunique()
    
    # Group by customer and aggregate the features
    aggregates = category_counts.groupby('customer_id')[['f_category_counts']].sum().reset_index()
    
    # Merge the aggregates with X on customer_id and article_id
    F = aggregates.merge(X, on='customer_id', how='left', validate='many_to_one')
    F = F.merge(past_purchases, on='customer_id', how='left', validate='many_to_one')
    F = F.merge(avg_price, on='customer_id', how='left', validate='many_to_one')
    F = F.merge(product_counts, on='customer_id', how='left', validate='many_to_one')
    
    # Return the resulting DataFrame
    return F[['customer_id', 'article_id', 'f_category_counts']]
