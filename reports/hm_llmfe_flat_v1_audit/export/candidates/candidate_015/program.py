def modify_features(X):
    """
    Modifies the input DataFrame X to create meaningful interactions, ratios, 
    recency/popularity transforms, and affinities between customer preferences 
    and candidate attributes.

    Parameters:
    X (pd.DataFrame): Input DataFrame with numeric values

    Returns:
    F (pd.DataFrame): Modified DataFrame with additional features
    """
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(X['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(X['h_article_count_30'].fillna(0))
    F['f_article_purchase_ratio'] = X['h_article_count_30'].fillna(0) / (X['h_user_count_180'].fillna(0) + 1)
    F['f_age_discount'] = np.minimum(F['raw_u_age'], 50) / 100
    F['f_user_article_popularity'] = np.log1p(X['h_user_article_count'].fillna(0)) + np.log1p(X['h_article_count_30'].fillna(0))
    F['f_color_similarity'] = np.minimum(X['raw_i_colour_group_code'], X['raw_i_perceived_colour_value_id']) / 100
    return F
