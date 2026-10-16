def modify_features(X):
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(F['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(F['h_article_count_30'].fillna(0))
    F['f_recent_purchase_ratio'] = F['h_user_article_count'] / F['h_user_count_180'].fillna(0)
    F['f_recent_purchase_ratio_article'] = F['h_user_article_count'] / F['h_article_count_180'].fillna(0)
    F['f_user_article_recency_diff'] = F['h_user_article_recency'] - F['h_article_recency']
    F['f_article_colour_ratio'] = F['h_user_colour_count'] / F['h_user_count_180'].fillna(0)
    return F
