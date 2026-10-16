def modify_features(X):
    F = X.copy()
    F['f_user_type_share'] = X['h_user_type_count_30'].fillna(0) / (X['h_user_count_30'].fillna(0) + 2)
    return F
