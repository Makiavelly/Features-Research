def modify_features(X):
    """
    Modify the input DataFrame to extract meaningful features for H&M clothing recommendations.
    
    Parameters:
    X (pandas DataFrame): Input DataFrame containing customer-article pair information.
    
    Returns:
    F (pandas DataFrame): Modified DataFrame with new features.
    """
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(F['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(F['h_article_count_30'].fillna(0))
    F['f_purchase_rate_7'] = F['h_user_count_7'] / F['h_user_count_30'].fillna(0)
    F['f_article_purchase_rate_7'] = F['h_article_count_7'] / F['h_article_count_30'].fillna(0)
    F['f_recent_purchase_rate_7'] = F['h_user_count_7'] / F['h_user_recency'].fillna(0)
    F['f_article_recent_purchase_rate_7'] = F['h_article_count_7'] / F['h_article_recency'].fillna(0)
    return F
