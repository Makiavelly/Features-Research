def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    names = (
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_count_all", "f_item_recency", "f_customer_count_30d",
        "f_customer_count_all", "f_pair_count", "f_pair_recency",
        "f_user_product_type_count", "f_user_department_count"
    )

    if history is None or len(history) == 0:
        for name in names:
            out[name] = np.zeros(n, dtype=float)
        return out

    h = history

    for days, name in ((7, "f_item_count_7d"),
                       (30, "f_item_count_30d"),
                       (90, "f_item_count_90d")):
        counts = h.loc[h["days_ago"] <= days].groupby("article_id").size()
        out[name] = X["article_id"].map(counts).fillna(0).to_numpy()

    item_counts = h.groupby("article_id").size()
    out["f_item_count_all"] = X["article_id"].map(item_counts).fillna(0).to_numpy()
    item_recency = h.groupby("article_id")["days_ago"].min()
    out["f_item_recency"] = X["article_id"].map(item_recency).to_numpy()

    recent = h.loc[h["days_ago"] <= 30]
    user_recent = recent.groupby("customer_id").size()
    user_all = h.groupby("customer_id").size()
    out["f_customer_count_30d"] = X["customer_id"].map(user_recent).fillna(0).to_numpy()
    out["f_customer_count_all"] = X["customer_id"].map(user_all).fillna(0).to_numpy()

    def lookup(keys, grouped):
        left = pd.DataFrame({"_pos": np.arange(n)})
        for i, key in enumerate(keys):
            left[f"_k{i}"] = X[key].to_numpy()
        right = grouped.rename("_value").reset_index()
        right.columns = [f"_k{i}" for i in range(len(keys))] + ["_value"]
        merged = left.merge(right, on=[f"_k{i}" for i in range(len(keys))],
                            how="left", sort=False)
        return merged.sort_values("_pos")["_value"].to_numpy()

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(
        ["size", "min"])
    out["f_pair_count"] = lookup(
        ["customer_id", "article_id"], pair["size"])
    out["f_pair_recency"] = lookup(
        ["customer_id", "article_id"], pair["min"])

    user_type = h.groupby(["customer_id", "product_type_no"]).size()
    user_department = h.groupby(["customer_id", "department_no"]).size()
    out["f_user_product_type_count"] = lookup(
        ["customer_id", "raw_i_product_type_no"], user_type)
    out["f_user_department_count"] = lookup(
        ["customer_id", "raw_i_department_no"], user_department)

    return out.astype(float)
