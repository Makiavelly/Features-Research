def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def count_map(frame, column):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        return frame.groupby(column, sort=False).size().astype("float64")

    def pair_map(frame, keys, value, agg="size"):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        if agg == "size":
            return frame.groupby(keys, sort=False).size().astype("float64")
        return frame.groupby(keys, sort=False)[value].agg(agg).astype("float64")

    def pair_lookup(series, keys):
        mi = pd.MultiIndex.from_arrays([X[k].to_numpy() for k in keys])
        return series.reindex(mi).to_numpy(dtype="float64")

    for window in (7, 30, 90):
        r = h.loc[h["days_ago"] <= window]
        out[f"f_item_count_{window}d"] = X["article_id"].map(count_map(r, "article_id")).fillna(0).to_numpy()

    out["f_item_count_all"] = X["article_id"].map(count_map(h, "article_id")).fillna(0).to_numpy()

    keys = ["customer_id", "article_id"]
    out["f_pair_count"] = pair_lookup(pair_map(h, keys, None), keys)
    out["f_pair_count_90d"] = pair_lookup(pair_map(h.loc[h["days_ago"] <= 90], keys, None), keys)
    out["f_pair_recency"] = pair_lookup(pair_map(h, keys, "days_ago", "min"), keys)

    if len(h):
        out["f_user_count"] = X["customer_id"].map(count_map(h, "customer_id")).fillna(0).to_numpy()
        r30 = h.loc[h["days_ago"] <= 30]
        out["f_user_count_30d"] = X["customer_id"].map(count_map(r30, "customer_id")).fillna(0).to_numpy()
        out["f_user_recency"] = X["customer_id"].map(
            h.groupby("customer_id", sort=False)["days_ago"].min()
        ).to_numpy(dtype="float64")
    else:
        out["f_user_count"] = np.zeros(n)
        out["f_user_count_30d"] = np.zeros(n)
        out["f_user_recency"] = np.full(n, np.nan)

    for hist_col, raw_col, name in (
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
    ):
        keys2 = ["customer_id", hist_col]
        affinity = pair_map(h, keys2, None)
        mi = pd.MultiIndex.from_arrays([X["customer_id"].to_numpy(), X[raw_col].to_numpy()])
        out[f"f_user_{name}_affinity"] = affinity.reindex(mi).fillna(0).to_numpy(dtype="float64")

    return out.replace([np.inf, -np.inf], np.nan)
