def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def agg(frame, keys, column=None, func="size"):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        g = frame.groupby(keys, sort=False)
        if func == "size":
            return g.size().astype("float64")
        return g[column].agg(func).astype("float64")

    def one(s, key, fill=0.0):
        if len(s) == 0:
            return np.full(n, fill, dtype="float64")
        return X[key].map(s).fillna(fill).to_numpy(dtype="float64")

    def two(s, left, right, fill=0.0):
        if len(s) == 0:
            return np.full(n, fill, dtype="float64")
        idx = pd.MultiIndex.from_arrays(
            [X[left].to_numpy(), X[right].to_numpy()]
        )
        return s.reindex(idx).fillna(fill).to_numpy(dtype="float64")

    r7 = h.loc[h["days_ago"] <= 7]
    r60 = h.loc[h["days_ago"] <= 60]
    r365 = h.loc[h["days_ago"] <= 365]

    out["f_article_buyers_60d"] = one(
        agg(r60, "article_id", "customer_id", "nunique"), "article_id"
    )
    out["f_article_buyers_all"] = one(
        agg(h, "article_id", "customer_id", "nunique"), "article_id"
    )
    out["f_article_channel2_60d"] = one(
        agg(r60.assign(__v=(r60["sales_channel_id"] == 2).astype("float64")),
            "article_id", "__v", "sum"),
        "article_id"
    )
    out["f_article_last_seen"] = one(
        agg(h, "article_id", "days_ago", "min"), "article_id", np.nan
    )

    pair = ["customer_id", "article_id"]
    out["f_pair_count_7d"] = two(agg(r7, pair), "customer_id", "article_id")
    out["f_pair_count_365d"] = two(agg(r365, pair), "customer_id", "article_id")
    out["f_pair_last_seen"] = two(
        agg(h, pair, "days_ago", "min"),
        "customer_id", "article_id", np.nan
    )

    if len(h):
        q = h[pair + ["days_ago"]].copy()
        q["__weight"] = np.exp(-q["days_ago"].to_numpy(dtype="float64") / 7.0)
        out["f_pair_decay_7d"] = two(
            q.groupby(pair, sort=False)["__weight"].sum(),
            "customer_id", "article_id"
        )
        out["f_user_unique_articles"] = one(
            agg(h, "customer_id", "article_id", "nunique"), "customer_id"
        )
        out["f_user_unique_articles_30d"] = one(
            agg(h.loc[h["days_ago"] <= 30], "customer_id",
                "article_id", "nunique"),
            "customer_id"
        )
    else:
        out["f_pair_decay_7d"] = np.zeros(n, dtype="float64")
        out["f_user_unique_articles"] = np.zeros(n, dtype="float64")
        out["f_user_unique_articles_30d"] = np.zeros(n, dtype="float64")

    for hc, rc, name in (
        ("colour_group_code", "raw_i_colour_group_code", "colour"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
    ):
        keys = ["customer_id", hc]
        out[f"f_user_{name}_count_60d"] = two(
            agg(r60, keys), "customer_id", rc
        )
        out[f"f_user_{name}_recency"] = two(
            agg(h, keys, "days_ago", "min"),
            "customer_id", rc, np.nan
        )

    return out.replace([np.inf, -np.inf], np.nan)
