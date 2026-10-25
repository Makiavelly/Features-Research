def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def gm(frame, keys, value=None, agg="size"):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        g = frame.groupby(keys, sort=False)
        if agg == "size":
            return g.size().astype("float64")
        return g[value].agg(agg).astype("float64")

    def map_one(series, key, fill=0.0):
        if len(series) == 0:
            return np.full(n, fill, dtype="float64")
        return X[key].map(series).fillna(fill).to_numpy(dtype="float64")

    def map_two(series, a, b, fill=0.0):
        if len(series) == 0:
            return np.full(n, fill, dtype="float64")
        idx = pd.MultiIndex.from_arrays([X[a].to_numpy(), X[b].to_numpy()])
        return series.reindex(idx).fillna(fill).to_numpy(dtype="float64")

    recent14 = h.loc[h["days_ago"] <= 14]
    recent180 = h.loc[h["days_ago"] <= 180]

    out["f_item_count_14d"] = map_one(gm(recent14, "article_id"), "article_id")
    out["f_item_count_180d"] = map_one(gm(recent180, "article_id"), "article_id")
    out["f_item_recency"] = map_one(
        gm(h, "article_id", "days_ago", "min"), "article_id", np.nan
    )
    out["f_item_distinct_users"] = map_one(
        gm(h, "article_id", "customer_id", "nunique"), "article_id"
    )

    pair = ["customer_id", "article_id"]
    out["f_pair_count_14d"] = map_two(
        gm(recent14, pair), "customer_id", "article_id"
    )
    out["f_pair_count_365d"] = map_two(
        gm(h.loc[h["days_ago"] <= 365], pair),
        "customer_id", "article_id"
    )
    out["f_pair_last_gap"] = map_two(
        gm(h, pair, "days_ago", "min"),
        "customer_id", "article_id", np.nan
    )

    if len(h):
        z = h[pair + ["days_ago"]].copy()
        z["__w"] = np.exp(-z["days_ago"].to_numpy(dtype="float64") / 14.0)
        out["f_pair_recent_weight"] = map_two(
            z.groupby(pair, sort=False)["__w"].sum(),
            "customer_id", "article_id"
        )
        user_last = h.groupby("customer_id", sort=False)["days_ago"].min()
        out["f_user_active_14d"] = map_one(
            gm(recent14, "customer_id"), "customer_id"
        )
        out["f_user_days_since_last"] = map_one(user_last, "customer_id", np.nan)
    else:
        out["f_pair_recent_weight"] = np.zeros(n)
        out["f_user_active_14d"] = np.zeros(n)
        out["f_user_days_since_last"] = np.full(n, np.nan)

    for hc, rc, name in (
        ("section_no", "raw_i_section_no", "section"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
    ):
        out[f"f_user_{name}_recent"] = map_two(
            gm(recent180, ["customer_id", hc]),
            "customer_id", rc
        )
        out[f"f_item_{name}_recent"] = map_one(
            gm(recent14, hc), rc
        )

    return out.replace([np.inf, -np.inf], np.nan)
