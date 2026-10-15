def modify_features(X, history):
    """
    Non-trivial features for H&M's customer item recommendation.

    The goal is to rank fixed candidate articles per customer for purchases in the next 7 days, maximizing validation MAP@12.
    This function takes into account the customer's age, fashion news frequency, product codes, types, graphical appearances,
    colours, departments, index groups, sections, and garment groups.

    Parameters:
    X (pd.DataFrame): DataFrame containing candidate pairs.
    history (pd.DataFrame): DataFrame containing past transactions.

    Returns:
    pd.DataFrame: DataFrame with new features.
    """
    
    # Calculate average price of articles bought by each customer in the last 30 days
    avg_price_last_30 = history.pivot_table(index='customer_id', values='price', columns='article_id', aggfunc='mean', fill_value=0).reindex(X.index, fill_value=0). rename_axis('article_id')
    
    # Map article IDs to their corresponding product codes
    article_product_codes = history.groupby('article_id')['product_code'].nunique().reset_index().rename(columns={'product_code': 'num_product_codes'})
    
    # Calculate number of distinct products bought by each customer in the last 30 days
    distinct_product_codes_last_30 = history[history['days_ago'] <= 30].groupby('customer_id')['product_code'].nunique().reset_index().rename(columns={'product_code': 'num_distinct_product_codes_last_30'})
    
    # Calculate number of purchases made by each customer in the last 30 days
    num_purchases_last_30 = history[history['days_ago'] <= 30].groupby('customer_id')['customer_id'].count().reset_index().rename(columns={'customer_id': 'num_purchases_last_30'})
    
    # Count the number of article types bought by each customer in the last 30 days
    article_types_last_30 = history[history['days_ago'] <= 30].groupby('customer_id')['product_type_no'].nunique().reset_index().rename(columns={'product_type_no': 'num_article_types_last_30'})
    
    # Calculate average price of articles bought by each customer in the last 7 days
    avg_price_last_7 = history[history['days_ago'] <= 7].pivot_table(index='customer_id', values='price', columns='article_id', aggfunc='mean', fill_value=0).reindex(X.index, fill_value=0).rename_axis('article_id')
    
    # Calculate frequency of a customer buying an article
    freq_customer_article = history.pivot_table(index='customer_id', columns='article_id', aggfunc='size', fill_value=0).reindex(X.index, fill_value=0).rename_axis('article_id').apply(lambda x: x / x.sum(), axis=1)
    
    # Create feature dataframe
    features = pd.concat([
        pd.concat([X, avg_price_last_30], axis=1),
        pd.concat([X, avg_price_last_7], axis=1),
        pd.concat([X, article_product_codes], axis=1),
        pd.concat([X, distinct_product_codes_last_30], axis=1),
        pd.concat([X, num_purchases_last_30], axis=1),
        pd.concat([X, article_types_last_30], axis=1),
        pd.concat([X, freq_customer_article], axis=1)
    ], axis=1)
    
    return features
