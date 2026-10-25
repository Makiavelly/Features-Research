def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def map_one(series, key, fill=np.nan):
        if h.empty or series.empty:
            return np.full(n, fill, dtype=float)
        return X[key].map(series).to_numpy(dtype=float)

    def map_pair(series, key1, key2, raw_col=None, fill=0.0):
        if h.empty or series.empty:
            return np.full(n, fill, dtype=float)
        if raw_col is None:
            idx = pd.MultiIndex.from_arrays([X[key1].to_numpy(), X[key2].to_numpy()])
        else:
            idx = pd.MultiIndex.from_arrays([X[key1].to_numpy(), X[raw_col].to_numpy()])
        return series.reindex(idx).fillna(fill).to_numpy(dtype=float)

    if h.empty:
        out["f_user_item_count"] = 0.0
        out["f_user_item_recency"] = np.nan
        for days in (7, 30, 90):
            out["f_item_pop_%dd" % days] = 0.0
        for days in (30, 90):
            out["f_user_activity_%dd" % days] = 0.0
        out["f_item_recency"] = np.nan
    else:
        out["f_user_item_count"] = map_pair(
            h.groupby(["customer_id", "article_id"], sort=False).size(),
            "customer_id", "article_id"
        )
        out["f_user_item_recency"] = map_pair(
            h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min(),
            "customer_id", "article_id", fill=np.nan
        )
        for days in (7, 30, 90):
            counts = h.loc[h["days_ago"] <= days].groupby("article_id", sort=False).size()
            out["f_item_pop_%dd" % days] = map_one(counts, "article_id", 0.0)
        for days in (30, 90):
            counts = h.loc[h["days_ago"] <= days].groupby("customer_id", sort=False).size()
            out["f_user_activity_%dd" % days] = map_one(counts, "customer_id", 0.0)
        out["f_item_recency"] = map_one(
            h.groupby("article_id", sort=False)["days_ago"].min(), "article_id"
        )

    for col, raw in (
        ("department_no", "raw_i_department_no"),
        ("product_type_no", "raw_i_product_type_no"),
        ("colour_group_code", "raw_i_colour_group_code"),
    ):
        if h.empty:
            vals = np.zeros(n)
        else:
            counts = h.groupby(["customer_id", col], sort=False).size()
            vals = map_pair(counts, "customer_id", col, raw, 0.0)
        out["f_user_%s_count" % col.replace("_no", "").replace("_code", "")] = vals

    if h.empty:
        out["f_user_department_30d"] = 0.0
        out["f_item_buyers"] = 0.0
        out["f_item_mean_price"] = np.nan
    else:
        recent = h.loc[h["days_ago"] <= 30]
        counts = recent.groupby(["customer_id", "department_no"], sort=False).size()
        out["f_user_department_30d"] = map_pair(
            counts, "customer_id", "department_no", "raw_i_department_no", 0.0
        )
        buyers = h.groupby("article_id", sort=False)["customer_id"].nunique()
        out["f_item_buyers"] = map_one(buyers, "article_id", 0.0)
        prices = h.groupby("article_id", sort=False)["price"].mean()
        out["f_item_mean_price"] = map_one(prices, "article_id")

    out["f_raw_age"] = X["raw_u_age"].to_numpy(dtype=float)
    out["f_raw_product_type"] = X["raw_i_product_type_no"].to_numpy(dtype=float)
    out["f_raw_department"] = X["raw_i_department_no"].to_numpy(dtype=float)
    return out.replace([np.inf, -np.inf], np.nan)
