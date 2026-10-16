def modify_features(X):
    """
    Modify input DataFrame X to rank each customer's fixed candidate articles for purchases in the next 7 days.
    
    Parameters:
    X (pd.DataFrame): A numeric pandas DataFrame with one row per customer-article pair.
    
    Returns:
    F (pd.DataFrame): A numeric pandas DataFrame with the same index and row order as X.
    """
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(X['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(X['h_article_count_30'].fillna(0))
    F['f_user_article_interaction'] = X['h_user_count_180'].fillna(0) / X['h_article_count_30'].fillna(0)
    F['f_log_user_purchases'] = np.log1p(F['f_log_user_purchases'])
    F['f_log_article_purchases'] = np.log1p(F['f_log_article_purchases'])
    F['f_age_priority'] = 1 / (X['raw_u_age'] + 1)
    F['f_recency_interaction'] = np.abs(X['h_user_recency'] - X['h_article_recency'])
    return F
