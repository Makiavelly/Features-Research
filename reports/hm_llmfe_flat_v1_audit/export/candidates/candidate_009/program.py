def modify_features(X):
    """
    Generate new features for H&M clothing recommendations.

    Parameters:
    X (DataFrame): A numeric pandas DataFrame containing customer-article pairs.

    Returns:
    F (DataFrame): A numeric pandas DataFrame with new features.
    """
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(X['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(X['h_article_count_30'].fillna(0))
    F['f_article_purchases_ratio'] = np.log1p(X['h_article_count_30'].fillna(0)) / np.log1p(X['h_article_count_7'].fillna(0))
    F['f_article_price_mean_ratio'] = np.log1p(X['h_article_price_mean'].fillna(0))
    F['f_age_colour_product_affinity'] = np.log1p(X['raw_u_age'] * X['raw_i_colour_group_code'])
    return F
