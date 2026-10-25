def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def counts(frame, key):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        return frame.groupby(key, sort=False).size().astype("float64")

    def pairs(frame, keys):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        return frame.groupby(keys, sort=False).size().astype("float64")

    def pair_lookup(series, left, right):
        mi = pd.MultiIndex.from_arrays([X[left].to_numpy(), X[right].to_numpy()])
        return series.reindex(mi).to_numpy(dtype="float64")

    for window in (7, 30, 90):
        r = h.loc[h["days_ago"] <= window]
        out[f"f_item_count_{window}d"] = X["article_id"].map(counts(r, "article_id")).fillna(0).to_numpy()

    out["f_item_count_all"] = X["article_id"].map(counts(h, "article_id")).fillna(0).to_numpy()

    pair_keys = ["customer_id", "article_id"]
    out["f_pair_count"] = pair_lookup(pairs(h, pair_keys), *pair_keys)
    out["f_pair_count_90d"] = pair_lookup(
        pairs(h.loc[h["days_ago"] <= 90], pair_keys), *pair_keys
    )

    if len(h):
        out["f_pair_recency"] = pair_lookup(
            h.groupby(pair_keys, sort=False)["days_ago"].min(), *pair_keys
        )
        out["f_user_count"] = X["customer_id"].map(counts(h, "customer_id")).fillna(0).to_numpy()
        recent = h.loc[h["days_ago"] <= 30]
        out["f_user_count_30d"] = X["customer_id"].map(counts(recent, "customer_id")).fillna(0).to_numpy()
        out["f_user_recency"] = X["customer_id"].map(
            h.groupby("customer_id", sort=False)["days_ago"].min()
        ).to_numpy(dtype="float64")
    else:
        out["f_pair_recency"] = np.full(n, np.nan)
        out["f_user_count"] = np.zeros(n)
        out["f_user_count_30d"] = np.zeros(n)
        out["f_user_recency"] = np.full(n, np.nan)

    for hist_col, raw_col, name in (
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
        ("section_no", "raw_i_section_no", "section"),
    ):
        mi = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[raw_col].to_numpy()]
        )
        affinity = pairs(h, ["customer_id", hist_col])
        out[f"f_user_{name}_affinity"] = affinity.reindex(mi).fillna(0).to_numpy(dtype="float64")

    return out.replace([np.inf, -np.inf], np.nan)
