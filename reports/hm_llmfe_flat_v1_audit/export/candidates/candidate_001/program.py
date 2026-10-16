def modify_features(X):
    """
    Modify the input DataFrame X by creating new numeric features based on existing columns.

    Parameters:
    X (pd.DataFrame): Input DataFrame.

    Returns:
    F (pd.DataFrame): Modified DataFrame.
    """
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(X['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(X['h_article_count_30'].fillna(0))
    F['f_user_article_ratio'] = X['h_user_article_count'] / X['h_user_count_180'].fillna(0)
    F['f_user_colour_ratio'] = X['h_user_colour_count'] / X['h_user_count_180'].fillna(0)
    F['f_user_product_type_ratio_30'] = X['h_user_type_count_30'] / X['h_user_count_30'].fillna(0)
    F['f_article_recency_ratio'] = X['h_article_recency'] / X['h_article_count_180'].fillna(0)
    F['f_user_recency_ratio'] = X['h_user_recency'] / X['h_user_count_180'].fillna(0)
    return F
