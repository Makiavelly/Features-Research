def modify_features(X):
    """
    Modify the input DataFrame X by adding new features and transformations to rank each customer's fixed candidate articles for purchases in the next 7 days.
    
    Parameters:
    X (pd.DataFrame): A numeric pandas DataFrame with one row per customer-article pair.
    
    Returns:
    F (pd.DataFrame): A modified numeric pandas DataFrame with the same index and row order as X, and exactly X.index and row order.
    """
    F = X.copy()
    F['f_log_user_purchases_7'] = np.log1p(X['h_user_count_7'].fillna(0))
    F['f_log_article_purchases_7'] = np.log1p(X['h_article_count_7'].fillna(0))
    F['f_article_recency_ratio'] = np.log1p(X['h_article_recency']) - np.log1p(X['h_user_recency'])
    F['f_article_price_ratio'] = np.log1p(X['h_article_price_mean']) - np.log1p(X['h_user_price_mean'])
    F['f_age_article_type_interaction'] = X['raw_u_age'] * X['raw_i_product_type_no']
    F['f_recency_popularity_user_purchases_7'] = np.log1p(X['h_user_count_7'].fillna(0)) / np.log1p(X['h_user_recency'])
    return F
