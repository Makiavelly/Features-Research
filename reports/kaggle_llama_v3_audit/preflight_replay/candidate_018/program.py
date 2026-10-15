def modify_features(X, history):
    """
    Generate useful nontrivial recommendation features using clothing/customer domain knowledge.
    
    Parameters:
    X (pd.DataFrame): Candidate pairs, with one row per pair.
    history (pd.DataFrame): Past transactions, with only past data.
    
    Returns:
    pd.DataFrame: New features, with exactly the same row order as X.index.
    """

    # Compute vector of customer ages at the cutoff day
    X['raw_u_age_at_cutoff'] = history.groupby('customer_id')['customer_age'].transform(lambda x: x.iloc[-1])

    # Compute average number of transactions per customer in the last 30 days
    X['f_avg_recent_transactions'] = history.groupby('customer_id')['days_ago'].transform(lambda x: (x <= 30).sum())

    # Compute average number of transactions per customer in the last 7 days
    X['f_avg_last_week_transactions'] = history.groupby('customer_id')['days_ago'].transform(lambda x: (x <= 7).sum())

    # Compute number of transactions per customer in the last 7 days where the article was in the top 3 sales channels
    X['f_recent_channel_3_transactions'] = history.groupby('customer_id')['sales_channel_id'].transform(
        lambda x: (x.shift(1) == 3).rolling(7).sum())

    # Compute number of transactions per customer where the article was purchased in the same department in the last 30 days
    X['f_recent_same_department_transactions'] = history.groupby('customer_id')['department_no'].transform(
        lambda x: (x.iloc[1:] == x.iloc[0]).rolling(30).sum())

    # Compute product category similarity between the two articles in a pair
    X['f_category_similarity'] = history.groupby('customer_id')['product_type_no'].transform(
        lambda x: (x.iloc[:-1] == x.iloc[-2]).sum())

    # Compute average article price per customer in the last 7 days
    X['f_avg_recent_price'] = history.groupby('customer_id')['price'].transform(lambda x: x.iloc[-7: -1].mean())

    # Compute average article price per customer in the last 30 days
    X['f_avg_last_month_price'] = history.groupby('customer_id')['price'].transform(lambda x: x.iloc[-30: -8].mean())

    # Compute number of transactions per customer where the article was purchased in the same department and index in the last 30 days
    X['f_recent_same_department_index_transactions'] = history.groupby('customer_id')['index_group_no'].transform(
        lambda x: (x.iloc[1:] == x.iloc[0]).rolling(30).sum())

    # Compute average article index per customer in the last 7 days
    X['f_avg_recent_index'] = history.groupby('customer_id')['index_group_no'].transform(lambda x: x.iloc[-7: -1].mean())

    # Compute average article index per customer in the last 30 days
    X['f_avg_last_month_index'] = history.groupby('customer_id')['index_group_no'].transform(lambda x: x.iloc[-30: -8].mean())

    # Compute article department similarity between the two articles in a pair
    X['f_department_similarity'] = history.groupby('customer_id')['department_no'].transform(
        lambda x: (x.iloc[:-1] == x.iloc[-2]).sum())

    # Compute article index similarity between the two articles in a pair
    X['f_index_similarity'] = history.groupby('customer_id')['index_group_no'].transform(
        lambda x: (x.iloc[:-1] == x.iloc[-2]).sum())

    # Compute article category similarity between the two articles in a pair
    X['f_category_similarity'] = history.groupby('customer_id')['product_type_no'].transform(
        lambda x: (x.iloc[:-1] == x.iloc[-2]).sum())

    # Compute article index similarity between the two articles in a pair
    X['f_index_similarity'] = history.groupby('customer_id')['index_group_no'].transform(
        lambda x: (x.iloc[:-1] == x.iloc[-2]).sum())

    # Compute average article price per customer in the last 7 days where the article was purchased in the same department
    X['f_avg_recent_price_in_same_department'] = history.groupby('customer_id')['price'].transform(
        lambda x: (x.iloc[-7: -1] == x.iloc[0]).rolling(7).mean())

    # Compute average article price per customer in the last 30 days where the article was purchased in the same department
    X['f_avg_last_month_price_in_same_department'] = history.groupby('customer_id')['price'].transform(
        lambda x: (x.iloc[-30: -8] == x.iloc[0]).rolling(30).mean())

    return X
