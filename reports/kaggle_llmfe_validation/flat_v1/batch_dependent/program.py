def modify_features(X):
    F=X.copy()
    F["f_batch_size"]=len(X)
    return F
