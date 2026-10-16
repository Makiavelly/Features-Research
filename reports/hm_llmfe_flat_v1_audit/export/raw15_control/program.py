def modify_features(X):
    return X[[c for c in X.columns if c.startswith("raw_")]].copy()
