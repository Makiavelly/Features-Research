def modify_features(X):
    """
    Modify the input features to rank each customer's fixed candidate articles for purchases in the next 7 days.
    
    Parameters:
    X (pd.DataFrame): A numeric pandas DataFrame with one row per customer-article pair.
    
    Returns:
    pd.DataFrame: A modified numeric pandas DataFrame with the same index and row order as the input.
    """
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(X['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(X['h_article_count_30'].fillna(0))
    F['f_article_purchase_ratio'] = np.divide(X['h_article_count_7'].fillna(0), X['h_article_count_30'].fillna(0))
    F['f_user_purchase_ratio'] = np.divide(X['h_user_count_7'].fillna(0), X['h_user_count_30'].fillna(0))
    F['f_user_age_article_recency_diff'] = X['raw_u_age'].fillna(0) - X['h_article_recency'].fillna(0)
    F['f_user_product_type_purchase_ratio'] = np.divide(X['h_user_type_count_180'].fillna(0), X['h_user_article_count'].fillna(0))
    return F
