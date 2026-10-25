def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def counts(frame, col):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        return frame.groupby(col, sort=False).size().astype("float64")

    def pair_count(frame, keys):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        return frame.groupby(keys, sort=False).size().astype("float64")

    def pair_lookup(series, left, right):
        mi = pd.MultiIndex.from_arrays([X[left].to_numpy(), X[right].to_numpy()])
        return series.reindex(mi).to_numpy(dtype="float64")

    for w in (7, 30, 90):
        r = h.loc[h["days_ago"] <= w]
        out[f"f_item_count_{w}d"] = X["article_id"].map(counts(r, "article_id")).fillna(0).to_numpy()

    out["f_item_count_all"] = X["article_id"].map(counts(h, "article_id")).fillna(0).to_numpy()

    pair = ["customer_id", "article_id"]
    out["f_pair_count"] = pair_lookup(pair_count(h, pair), *pair)
    out["f_pair_count_90d"] = pair_lookup(
        pair_count(h.loc[h["days_ago"] <= 90], pair), *pair
    )
    if len(h):
        rec = h.groupby(pair, sort=False)["days_ago"].min()
        out["f_pair_recency"] = pair_lookup(rec, *pair)
        out["f_user_count"] = X["customer_id"].map(counts(h, "customer_id")).fillna(0).to_numpy()
        r30 = h.loc[h["days_ago"] <= 30]
        out["f_user_count_30d"] = X["customer_id"].map(counts(r30, "customer_id")).fillna(0).to_numpy()
        out["f_user_recency"] = X["customer_id"].map(
            h.groupby("customer_id", sort=False)["days_ago"].min()
        ).to_numpy(dtype="float64")
        decay = np.exp(-h["days_ago"].to_numpy(dtype="float64") / 30.0)
        temp = h[["customer_id", "article_id"]].copy()
        temp["__d"] = decay
        out["f_item_decay"] = X["article_id"].map(
            temp.groupby("article_id", sort=False)["__d"].sum()
        ).fillna(0).to_numpy()
    else:
        out["f_pair_recency"] = np.full(n, np.nan)
        out["f_user_count"] = np.zeros(n)
        out["f_user_count_30d"] = np.zeros(n)
        out["f_user_recency"] = np.full(n, np.nan)
        out["f_item_decay"] = np.zeros(n)

    for hist_col, raw_col, name in (
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
    ):
        affinity = pair_count(h, ["customer_id", hist_col])
        out[f"f_user_{name}_affinity"] = pair_lookup(
            affinity, "customer_id", raw_col
        ).astype("float64")

    return out.replace([np.inf, -np.inf], np.nan)
