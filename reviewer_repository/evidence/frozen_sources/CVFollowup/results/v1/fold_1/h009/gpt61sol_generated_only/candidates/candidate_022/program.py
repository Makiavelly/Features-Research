def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)
    h = history

    feature_names = (
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_count_all", "f_item_recency", "f_customer_count_30d",
        "f_customer_count_all", "f_customer_recency", "f_pair_count",
        "f_pair_recency", "f_user_product_type_count",
        "f_user_department_count"
    )

    if h is None or len(h) == 0:
        for name in feature_names:
            out[name] = np.zeros(n, dtype=float)
        return out

    def lookup(keys, values):
        left = pd.DataFrame({"_pos": np.arange(n)})
        for i, key in enumerate(keys):
            left["_k" + str(i)] = X[key].to_numpy()
        right = values.rename("_value").reset_index()
        right.columns = ["_k" + str(i) for i in range(len(keys))] + ["_value"]
        merged = left.merge(
            right,
            on=["_k" + str(i) for i in range(len(keys))],
            how="left",
            sort=False
        )
        return merged.sort_values("_pos")["_value"].to_numpy()

    for days, name in (
        (7, "f_item_count_7d"),
        (30, "f_item_count_30d"),
        (90, "f_item_count_90d")
    ):
        counts = h.loc[h["days_ago"] <= days].groupby("article_id").size()
        out[name] = X["article_id"].map(counts).fillna(0).to_numpy()

    out["f_item_count_all"] = X["article_id"].map(
        h.groupby("article_id").size()).fillna(0).to_numpy()
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()).to_numpy()

    recent = h.loc[h["days_ago"] <= 30]
    out["f_customer_count_30d"] = X["customer_id"].map(
        recent.groupby("customer_id").size()).fillna(0).to_numpy()
    out["f_customer_count_all"] = X["customer_id"].map(
        h.groupby("customer_id").size()).fillna(0).to_numpy()
    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()).to_numpy()

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(
        ["size", "min"])
    out["f_pair_count"] = lookup(
        ["customer_id", "article_id"], pair["size"])
    out["f_pair_recency"] = lookup(
        ["customer_id", "article_id"], pair["min"])

    for hist_col, raw_col, name in (
        ("product_type_no", "raw_i_product_type_no",
         "f_user_product_type_count"),
        ("department_no", "raw_i_department_no",
         "f_user_department_count")
    ):
        values = h.groupby(["customer_id", hist_col]).size()
        out[name] = lookup(["customer_id", raw_col], values)

    return out.astype(float)
