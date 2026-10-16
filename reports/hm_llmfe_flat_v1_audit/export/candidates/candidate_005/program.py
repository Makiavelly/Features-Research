def modify_features(X):
    """
    Modify features for H&M clothing recommendations.
    
    Parameters:
    X (DataFrame): A flat numeric table with one row per customer-article pair.
    
    Returns:
    F (DataFrame): A numeric pandas DataFrame with modified features.
    """
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(X['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(X['h_article_count_30'].fillna(0))
    F['f_user_article_ratio'] = np.log1p(X['h_user_article_count'] / (X['h_user_count_180'] + 1))
    F['f_article_recency_transform'] = np.log1p(1 / (X['h_article_recency'] + 1))
    F['f_colour_group_similarity'] = X['raw_i_colour_group_code'] == X['raw_i_perceived_colour_value_id']
    F = F[['raw_u_age', 'raw_u_fn', 'raw_u_active', 'raw_u_club_member_status', 'raw_u_fashion_news_frequency', 'raw_i_product_code', 'raw_i_product_type_no', 'raw_i_graphical_appearance_no', 'raw_i_colour_group_code', 'raw_i_perceived_colour_value_id', 'raw_i_perceived_colour_master_id', 'raw_i_department_no', 'raw_i_index_group_no', 'raw_i_section_no', 'raw_i_garment_group_no', 'h_user_count_180', 'h_article_count_30', 'h_article_price_mean', 'h_article_recency', 'h_user_article_count', 'h_user_article_recency', 'h_user_colour_count', 'h_user_price_mean', 'h_user_recency', 'h_user_type_count_180', 'f_log_user_purchases', 'f_log_article_purchases', 'f_user_article_ratio', 'f_article_recency_transform', 'f_colour_group_similarity']]
    return F
