def modify_features(X):
    F = X.copy()
    F['f_log_user_purchases'] = np.log1p(X['h_user_count_180'].fillna(0))
    F['f_log_article_purchases'] = np.log1p(X['h_article_count_30'].fillna(0))
    return F
