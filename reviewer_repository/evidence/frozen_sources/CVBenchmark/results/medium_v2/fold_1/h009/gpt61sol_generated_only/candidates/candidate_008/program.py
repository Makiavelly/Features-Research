def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def counts(frame, key):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        return frame.groupby(key, sort=False).size().astype("float64")

    def pair_values(frame, keys, value, agg="sum"):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        return frame.groupby(keys, sort=False)[value].agg(agg).astype("float64")

    def lookup(series, keys):
        if len(series) == 0:
            return np.zeros(n, dtype="float64")
        mi = pd.MultiIndex.from_arrays([X[k].to_numpy() for k in keys])
        return series.reindex(mi).fillna(0).to_numpy(dtype="float64")

    for w in (7, 30, 90):
        r = h.loc[h["days_ago"] <= w]
        out["f_item_count_" + str(w) + "d"] = X["article_id"].map(
            counts(r, "article_id")
        ).fillna(0).to_numpy()

    out["f_item_count_all"] = X["article_id"].map(counts(h, "article_id")).fillna(0).to_numpy()
    out["f_product_count_30d"] = X["raw_i_product_code"].map(
        counts(h.loc[h["days_ago"] <= 30], "product_code")
    ).fillna(0).to_numpy()

    keys = ["customer_id", "article_id"]
    out["f_user_item_count"] = lookup(pair_values(h, keys, "days_ago", "count"), keys)
    out["f_user_item_count_30d"] = lookup(
        pair_values(h.loc[h["days_ago"] <= 30], keys, "days_ago", "count"), keys
    )
    out["f_user_item_count_90d"] = lookup(
        pair_values(h.loc[h["days_ago"] <= 90], keys, "days_ago", "count"), keys
    )
    out["f_user_item_recency"] = lookup(pair_values(h, keys, "days_ago", "min"), keys)

    if len(h):
        decay = np.exp(-h["days_ago"].to_numpy(dtype="float64") / 30.0)
        hh = h.copy()
        hh["__decay"] = decay
        out["f_item_decay"] = X["article_id"].map(
            hh.groupby("article_id", sort=False)["__decay"].sum()
        ).fillna(0).to_numpy()
        out["f_user_decay"] = X["customer_id"].map(
            hh.groupby("customer_id", sort=False)["__decay"].sum()
        ).fillna(0).to_numpy()
        out["f_user_item_decay"] = lookup(
            hh.groupby(keys, sort=False)["__decay"].sum(), keys
        )
        out["f_user_history_count"] = X["customer_id"].map(
            counts(h, "customer_id")
        ).fillna(0).to_numpy()
        out["f_user_recency"] = X["customer_id"].map(
            h.groupby("customer_id", sort=False)["days_ago"].min()
        ).to_numpy()
    else:
        for c in ("f_item_decay", "f_user_decay", "f_user_item_decay",
                  "f_user_history_count"):
            out[c] = np.zeros(n)
        out["f_user_recency"] = np.full(n, np.nan)

    for hc, rc, name in (
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
        ("section_no", "raw_i_section_no", "section"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
    ):
        k = ["customer_id", hc]
        mi = pd.MultiIndex.from_arrays([X["customer_id"].to_numpy(), X[rc].to_numpy()])
        s = h.groupby(k, sort=False).size() if len(h) else pd.Series(dtype="float64")
        out["f_user_" + name + "_count"] = s.reindex(mi).fillna(0).to_numpy(dtype="float64")

    out["f_raw_item_code"] = X["raw_i_product_code"].fillna(-1).to_numpy(dtype="float64")
    out["f_raw_item_type"] = X["raw_i_product_type_no"].fillna(-1).to_numpy(dtype="float64")
    return out.replace([np.inf, -np.inf], np.nan)
