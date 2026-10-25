def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def one(frame, col):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        return frame.groupby(col, sort=False).size().astype("float64")

    def two(frame, keys, col=None, agg="size"):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        g = frame.groupby(keys, sort=False)
        if agg == "size":
            return g.size().astype("float64")
        return g[col].agg(agg).astype("float64")

    def get_pair(s, a, b, fill=0.0):
        if len(s) == 0:
            return np.full(n, fill, dtype="float64")
        m = pd.MultiIndex.from_arrays([X[a].to_numpy(), X[b].to_numpy()])
        return s.reindex(m).fillna(fill).to_numpy(dtype="float64")

    for w in (7, 30, 90):
        r = h.loc[h["days_ago"] <= w]
        out[f"f_item_count_{w}d"] = X["article_id"].map(
            one(r, "article_id")
        ).fillna(0).to_numpy(dtype="float64")

    out["f_item_count_all"] = X["article_id"].map(
        one(h, "article_id")
    ).fillna(0).to_numpy(dtype="float64")

    pk = ["customer_id", "article_id"]
    out["f_pair_count"] = get_pair(two(h, pk), "customer_id", "article_id")
    out["f_pair_count_30d"] = get_pair(
        two(h.loc[h["days_ago"] <= 30], pk), "customer_id", "article_id"
    )
    out["f_pair_count_90d"] = get_pair(
        two(h.loc[h["days_ago"] <= 90], pk), "customer_id", "article_id"
    )
    out["f_pair_recency"] = get_pair(
        two(h, pk, "days_ago", "min"), "customer_id", "article_id", np.nan
    )

    if len(h):
        out["f_user_count"] = X["customer_id"].map(
            one(h, "customer_id")
        ).fillna(0).to_numpy(dtype="float64")
        out["f_user_count_30d"] = X["customer_id"].map(
            one(h.loc[h["days_ago"] <= 30], "customer_id")
        ).fillna(0).to_numpy(dtype="float64")
        out["f_user_recency"] = X["customer_id"].map(
            h.groupby("customer_id", sort=False)["days_ago"].min()
        ).to_numpy(dtype="float64")
        out["f_item_users"] = X["article_id"].map(
            h.groupby("article_id", sort=False)["customer_id"].nunique()
        ).fillna(0).to_numpy(dtype="float64")
        z = h[["customer_id", "article_id", "days_ago"]].copy()
        z["__w"] = np.exp(-z["days_ago"].to_numpy(dtype="float64") / 30.0)
        out["f_pair_decay"] = get_pair(
            z.groupby(pk, sort=False)["__w"].sum(),
            "customer_id", "article_id"
        )
        out["f_item_decay"] = X["article_id"].map(
            z.groupby("article_id", sort=False)["__w"].sum()
        ).fillna(0).to_numpy(dtype="float64")
    else:
        out["f_user_count"] = np.zeros(n)
        out["f_user_count_30d"] = np.zeros(n)
        out["f_user_recency"] = np.full(n, np.nan)
        out["f_item_users"] = np.zeros(n)
        out["f_pair_decay"] = np.zeros(n)
        out["f_item_decay"] = np.zeros(n)

    for hc, rc, name in (
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
        ("section_no", "raw_i_section_no", "section"),
    ):
        s = two(h, ["customer_id", hc])
        out[f"f_user_{name}_count"] = get_pair(
            s, "customer_id", rc
        )

    return out.replace([np.inf, -np.inf], np.nan)
