def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def counts(frame, key):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        return frame.groupby(key, sort=False).size().astype("float64")

    def grouped(frame, keys, value=None, agg="size"):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        g = frame.groupby(keys, sort=False)
        if agg == "size":
            return g.size().astype("float64")
        return g[value].agg(agg).astype("float64")

    def lookup(series, left, right, fill=0.0):
        if len(series) == 0:
            return np.full(n, fill, dtype="float64")
        mi = pd.MultiIndex.from_arrays(
            [X[left].to_numpy(), X[right].to_numpy()]
        )
        return series.reindex(mi).fillna(fill).to_numpy(dtype="float64")

    for w in (7, 30, 90):
        r = h.loc[h["days_ago"] <= w]
        out[f"f_item_count_{w}d"] = X["article_id"].map(
            counts(r, "article_id")
        ).fillna(0).to_numpy(dtype="float64")

    out["f_item_count_all"] = X["article_id"].map(
        counts(h, "article_id")
    ).fillna(0).to_numpy(dtype="float64")

    pk = ["customer_id", "article_id"]
    out["f_pair_count"] = lookup(grouped(h, pk), "customer_id", "article_id")
    out["f_pair_count_90d"] = lookup(
        grouped(h.loc[h["days_ago"] <= 90], pk),
        "customer_id", "article_id"
    )
    out["f_pair_recency"] = lookup(
        grouped(h, pk, "days_ago", "min"),
        "customer_id", "article_id", np.nan
    )

    if len(h):
        out["f_user_count"] = X["customer_id"].map(
            counts(h, "customer_id")
        ).fillna(0).to_numpy(dtype="float64")
        out["f_user_count_30d"] = X["customer_id"].map(
            counts(h.loc[h["days_ago"] <= 30], "customer_id")
        ).fillna(0).to_numpy(dtype="float64")
        out["f_user_recency"] = X["customer_id"].map(
            h.groupby("customer_id", sort=False)["days_ago"].min()
        ).to_numpy(dtype="float64")
    else:
        out["f_user_count"] = np.zeros(n, dtype="float64")
        out["f_user_count_30d"] = np.zeros(n, dtype="float64")
        out["f_user_recency"] = np.full(n, np.nan, dtype="float64")

    for hist_col, raw_col, name in (
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
    ):
        s = grouped(h, ["customer_id", hist_col])
        out[f"f_user_{name}_affinity"] = lookup(
            s, "customer_id", raw_col
        )

    return out.replace([np.inf, -np.inf], np.nan)
