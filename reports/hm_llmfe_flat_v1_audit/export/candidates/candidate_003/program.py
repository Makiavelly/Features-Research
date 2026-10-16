def modify_features(X):
    """
    Modify numeric features to rank customer-article pairs for purchases in the next 7 days.
    
    Parameters:
    X (pd.DataFrame): Flat numeric table with one row per customer-article pair.
    
    Returns:
    F (pd.DataFrame): Modified numeric DataFrame with same index and row order as X.
    """
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(X['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(X['h_article_count_30'].fillna(0))
    F['f_user_article_purchases_ratio'] = np.where(X['h_user_count_180'] > 0, X['h_user_article_count'] / X['h_user_count_180'], 0)
    F['f_article_user_purchases_ratio'] = np.where(X['h_article_count_30'] > 0, X['h_user_article_count'] / X['h_article_count_30'], 0)
    F['f_user_article_recency_ratio'] = np.where(X['h_user_count_180'] > 0, X['h_user_article_recency'] / X['h_user_recency'], 0)
    F['f_article_user_recency_ratio'] = np.where(X['h_article_count_30'] > 0, X['h_user_article_recency'] / X['h_article_recency'], 0)
    return F
