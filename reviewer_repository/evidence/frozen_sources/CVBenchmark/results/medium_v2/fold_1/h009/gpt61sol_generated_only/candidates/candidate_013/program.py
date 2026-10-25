def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    names = (
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_recency", "f_customer_count_30d", "f_customer_count_all",
        "f_pair_count", "f_pair_recency", "f_user_product_type_count",
        "f_user_department_count"
    )

    if h is None or len(h) == 0:
        for name in names:
            out[name] = np.zeros(n, dtype=float)
        return out

    for days, name in ((7, "f_item_count_7d"),
                       (30, "f_item_count_30d"),
                       (90, "f_item_count_90d")):
        counts = h.loc[h["days_ago"] <= days].groupby("article_id").size()
        out[name] = X["article_id"].map(counts).fillna(0).to_numpy()

    item_recency = h.groupby("article_id")["days_ago"].min()
    out["f_item_recency"] = X["article_id"].map(item_recency).to_numpy()

    recent_users = h.loc[h["days_ago"] <= 30].groupby("customer_id").size()
    all_users = h.groupby("customer_id").size()
    out["f_customer_count_30d"] = X["customer_id"].map(
        recent_users).fillna(0).to_numpy()
    out["f_customer_count_all"] = X["customer_id"].map(
        all_users).fillna(0).to_numpy()

    def joined(keys, grouped, name):
        left = pd.DataFrame({"_pos": np.arange(n)})
        for i, key in enumerate(keys):
            left["_k" + str(i)] = X[key].to_numpy()
        right = grouped.reset_index()
        right.columns = ["_k" + str(i) for i in range(len(keys))] + [name]
        merged = left.merge(
            right, on=["_k" + str(i) for i in range(len(keys))],
            how="left", sort=False
        )
        return merged.sort_values("_pos")[name].to_numpy()

    pair = h.groupby(["customer_id", "article_id"]).agg(
        _pair_count=("days_ago", "size"),
        _pair_recency=("days_ago", "min")
    )
    out["f_pair_count"] = joined(
        ["customer_id", "article_id"], pair["_pair_count"], "v")
    out["f_pair_recency"] = joined(
        ["customer_id", "article_id"], pair["_pair_recency"], "v")

    user_type = h.groupby(["customer_id", "product_type_no"]).size()
    out["f_user_product_type_count"] = joined(
        ["customer_id", "raw_i_product_type_no"], user_type, "v")

    user_department = h.groupby(["customer_id", "department_no"]).size()
    out["f_user_department_count"] = joined(
        ["customer_id", "raw_i_department_no"], user_department, "v")

    return out.astype(float)
