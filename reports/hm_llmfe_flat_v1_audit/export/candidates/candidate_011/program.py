def modify_features(X):
    """
    Modify the input DataFrame to include new features that can help in ranking customer-article pairs.

    The new features include:
    - f_log_user_purchases: log of the number of user purchases in the last 180 days
    - f_log_article_purchases: log of the number of article purchases in the last 30 days
    - f_user_article_recency_ratio: ratio of article recency to user recency
    - f_user_colour_count_ratio: ratio of user colour count to article colour count
    - f_price_similarity: similarity between user average price and article average price

    Parameters:
    X (pd.DataFrame): Input DataFrame

    Returns:
    pd.DataFrame: Modified DataFrame with new features
    """
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(F['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(F['h_article_count_30'].fillna(0))
    F['f_user_article_recency_ratio'] = F['h_user_article_recency'] / F['h_article_recency']
    F['f_user_colour_count_ratio'] = F['h_user_colour_count'] / F['h_article_count_7']
    F['f_price_similarity'] = np.abs(F['h_user_price_mean'] - F['h_article_price_mean'])
    return F
