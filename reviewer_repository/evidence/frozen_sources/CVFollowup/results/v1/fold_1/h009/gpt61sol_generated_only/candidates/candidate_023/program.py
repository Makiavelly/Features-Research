def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def cnt(frame, col):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        return frame.groupby(col, sort=False).size().astype("float64")

    def grp(frame, keys, col=None, agg="size"):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        g = frame.groupby(keys, sort=False)
        return g.size().astype("float64") if agg == "size" else g[col].agg(agg).astype("float64")

    def lookup(s, a, b):
        mi = pd.MultiIndex.from_arrays([X[a].to_numpy(), X[b].to_numpy()])
        return s.reindex(mi).fillna(0).to_numpy(dtype="float64")

    for w in (7, 30, 90):
        r = h.loc[h["days_ago"] <= w]
        out[f"f_item_count_{w}d"] = X["article_id"].map(cnt(r, "article_id")).fillna(0).to_numpy()

    out["f_item_count_all"] = X["article_id"].map(cnt(h, "article_id")).fillna(0).to_numpy()

    pair = ["customer_id", "article_id"]
    out["f_pair_count"] = lookup(grp(h, pair), *pair)
    out["f_pair_count_90d"] = lookup(grp(h.loc[h["days_ago"] <= 90], pair), *pair)
    out["f_pair_recency"] = lookup(grp(h, pair, "days_ago", "min"), *pair)

    if len(h):
        out["f_user_count"] = X["customer_id"].map(cnt(h, "customer_id")).fillna(0).to_numpy()
        out["f_user_count_30d"] = X["customer_id"].map(
            cnt(h.loc[h["days_ago"] <= 30], "customer_id")
        ).fillna(0).to_numpy()
        out["f_user_recency"] = X["customer_id"].map(
            h.groupby("customer_id", sort=False)["days_ago"].min()
        ).to_numpy(dtype="float64")
        out["f_item_users"] = X["article_id"].map(
            h.groupby("article_id", sort=False)["customer_id"].nunique()
        ).fillna(0).to_numpy()
    else:
        out["f_user_count"] = np.zeros(n)
        out["f_user_count_30d"] = np.zeros(n)
        out["f_user_recency"] = np.full(n, np.nan)
        out["f_item_users"] = np.zeros(n)

    for hc, rc, name in (
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
    ):
        s = grp(h, ["customer_id", hc])
        out[f"f_user_{name}_count"] = lookup(s, "customer_id", rc)

    return out.replace([np.inf, -np.inf], np.nan)
