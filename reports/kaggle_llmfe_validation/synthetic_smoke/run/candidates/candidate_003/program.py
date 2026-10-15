def modify_features(X, history):
    return pd.DataFrame({'f_fixture': X.raw_u_age.fillna(0) * 2}, index=X.index)
