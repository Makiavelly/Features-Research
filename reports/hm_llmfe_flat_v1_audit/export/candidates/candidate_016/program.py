def modify_features(X):
    """
    Create meaningful interactions, ratios, recency/popularity transforms,
    and affinities between customer preferences and candidate attributes.
    """
    F = X.copy()
    F['f_article_purchase_ratio'] = X['h_article_count_30'].fillna(0) / X['h_article_count_180'].fillna(0)
    F['f_log_product_type_purchases'] = np.log1p(X['h_user_type_count_180'].fillna(0))
    F['f_log_article_purchases_times_product_type'] = np.log1p(X['h_article_count_7'].fillna(0)) * F['f_log_product_type_purchases']
    F['f_colour_group_likelihood'] = X['h_user_colour_count'].fillna(0) / (X['h_user_count_180'].fillna(0) + 1)
    return F
