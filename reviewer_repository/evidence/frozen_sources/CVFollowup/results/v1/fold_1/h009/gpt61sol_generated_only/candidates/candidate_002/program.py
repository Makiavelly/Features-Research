def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def grouped_count(frame, keys):
        if len(frame) == 0:
            return pd.Series(dtype="float64", index=pd.MultiIndex.from_arrays([[] for _ in keys]))
        return frame.groupby(keys, sort=False).size().astype("float64")

    def lookup(series, keys):
        if len(series) == 0:
            return np.zeros(n, dtype="float64")
        mi = pd.MultiIndex.from_arrays([X[k].to_numpy() for k in keys])
        return series.reindex(mi).fillna(0).to_numpy(dtype="float64")

    for window in (7, 30, 90):
        recent = h.loc[h["days_ago"] <= window]
        item_counts = recent.groupby("article_id", sort=False).size().astype("float64")
        out[f"f_item_count_{window}d"] = X["article_id"].map(item_counts).fillna(0).to_numpy()

    pair_keys = ["customer_id", "article_id"]
    pair_counts = grouped_count(h, pair_keys)
    out["f_user_item_count"] = lookup(pair_counts, pair_keys)

    pair_recent = h.loc[h["days_ago"] <= 90]
    out["f_user_item_count_90d"] = lookup(grouped_count(pair_recent, pair_keys), pair_keys)

    if len(h):
        rec = h.groupby(pair_keys, sort=False)["days_ago"].min()
        mi = pd.MultiIndex.from_arrays([X[k].to_numpy() for k in pair_keys])
        out["f_user_item_recency"] = rec.reindex(mi).to_numpy(dtype="float64")
        user_counts = h.groupby("customer_id", sort=False).size().astype("float64")
        out["f_user_history_count"] = X["customer_id"].map(user_counts).fillna(0).to_numpy()
        user_recent = h.loc[h["days_ago"] <= 30].groupby("customer_id", sort=False).size().astype("float64")
        out["f_user_history_count_30d"] = X["customer_id"].map(user_recent).fillna(0).to_numpy()
    else:
        out["f_user_item_recency"] = np.full(n, np.nan)
        out["f_user_history_count"] = np.zeros(n)
        out["f_user_history_count_30d"] = np.zeros(n)

    for hist_col, raw_col, name in (
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
    ):
        keys = ["customer_id", hist_col]
        affinity = grouped_count(h, keys)
        mi = pd.MultiIndex.from_arrays([X["customer_id"].to_numpy(), X[raw_col].to_numpy()])
        out[f"f_user_{name}_purchases"] = affinity.reindex(mi).fillna(0).to_numpy(dtype="float64")

    return out.replace([np.inf, -np.inf], np.nan)
