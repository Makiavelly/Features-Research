def modify_features(X, history):
    """
    H&M recommendation engine feature engineering.

    Produce a DataFrame with numeric feature columns to enhance candidate article ranking.
    Hypothesis: incorporate time-varying customer-article interactions and static attributes
    to improve the selection of likely purchases per customer within the next week.

    Args:
        X (DataFrame): Input DataFrame with customer-article pair data.
        history (DataFrame): Transaction history for the selected customer cohort.

    Returns:
        DataFrame: Enhanced input DataFrame with additional numeric feature columns.
    """
    # Groupby customer and compute average transaction price and count purchases
    avg_price = history.groupby('customer_id')['price'].mean().reset_index()
    avg_price.columns = ['customer_id', 'avg_price']
    count_purchases = history.groupby('customer_id')['price'].count().reset_index()
    count_purchases.columns = ['customer_id', 'count_purchases']

    # Merge average price and purchase count with X
    X = pd.merge(X, avg_price, on='customer_id', how='left')
    X = pd.merge(X, count_purchases, on='customer_id', how='left')

    # Compute time-varying interactions (average price in last 7, 30, 180 days)
    interactions = history.groupby('customer_id')['price'].rolling(window=7).mean().reset_index()
    interactions.columns = ['customer_id', 'avg_price_7_days']
    interactions = history.groupby('customer_id')['price'].rolling(window=30).mean().reset_index()
    interactions.columns = ['customer_id', 'avg_price_30_days']
    interactions = history.groupby('customer_id')['price'].rolling(window=180).mean().reset_index()
    interactions.columns = ['customer_id', 'avg_price_180_days']

    # Merge interactions with X
    X = pd.merge(X, interactions, on='customer_id', how='left')

    # Compute affinity between customers based on purchases
    affinity = history.groupby('customer_id')['article_id'].nunique().reset_index()
    affinity.columns = ['customer_id', 'num_articles']

    # Merge affinity with X
    X = pd.merge(X, affinity, on='customer_id', how='left')

    # Compute static customer features (average age, active, and fashion news frequency)
    static_features = history[['customer_id', 'raw_u_age', 'raw_u_active', 'raw_u_fashion_news_frequency']].groupby('customer_id').mean().reset_index()
    static_features.columns = ['customer_id', 'avg_age', 'avg_active', 'avg_fashion_news_frequency']

    # Merge static features with X
    X = pd.merge(X, static_features, on='customer_id', how='left')

    # Compute feature interactions (price * avg_age, etc.)
    X[['price', 'avg_age']] = X[['price', 'avg_age']].fillna(0)  # replace NaN with 0
    X['price_avg_age'] = X['price'] * X['avg_age']
    X['price_avg_active'] = X['price'] * X['avg_active']
    X['price_avg_fashion_news_frequency'] = X['price'] * X['avg_fashion_news_frequency']

    # Return the DataFrame with new numeric feature columns
    return X
