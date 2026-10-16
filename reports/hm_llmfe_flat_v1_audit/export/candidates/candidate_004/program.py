def modify_features(X):
    """
    Modify features for H&M clothing recommendations.

    Parameters:
    X (pd.DataFrame): A numeric pandas DataFrame with one row per customer-article pair.

    Returns:
    pd.DataFrame: A modified numeric pandas DataFrame with additional transformations.
    """
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(X['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(X['h_article_count_30'].fillna(0))
    F['f_user_purchase_ratio'] = np.log1p(X['h_user_count_180'].fillna(0) / X['h_article_count_30'].fillna(0))
    F['f_age_band'] = np.floor(X['raw_u_age'] / 10) * 10
    F['f_article_recency_ratio'] = np.log1p(X['h_article_recency'] / 180)
    F['f_user_colour_purchase_ratio'] = np.log1p(X['h_user_colour_count'] / X['h_article_count_180'].fillna(0))
    F['f_log_article_price_mean'] = np.log1p(X['h_article_price_mean'].fillna(0))
    return F
