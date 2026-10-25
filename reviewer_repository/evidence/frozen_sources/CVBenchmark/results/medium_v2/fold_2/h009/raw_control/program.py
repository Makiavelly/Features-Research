def modify_features(X, history):
    return pd.DataFrame({"f_control": np.ones(len(X))}, index=X.index)
