def modify_features(X):
    """
    Modify the provided DataFrame to create new features for ranking customer-article pairs.
    
    Parameters:
    X (numeric pandas DataFrame): Input data with customer-article pairs.
    
    Returns:
    numeric pandas DataFrame: Modified data with new features.
    """
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(X['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(X['h_article_count_30'].fillna(0))
    F['f_user_recency_ratio'] = X['h_user_recency'] / X['h_user_count_180'].fillna(0)
    F['f_article_recency_ratio'] = X['h_article_recency'] / X['h_article_count_30'].fillna(0)
    F['f_user_age_article_colour_group'] = X['raw_u_age'] * X['raw_i_colour_group_code']
    F['f_user_type_count_article_colour_group_ratio'] = X['h_user_type_count_180'].fillna(0) / (X['h_user_colour_count'] + 1)
    return F
