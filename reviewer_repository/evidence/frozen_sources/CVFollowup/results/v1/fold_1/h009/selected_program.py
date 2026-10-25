def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def mapped(grouped, key):
        return X[key].map(grouped)

    def joined(keys, grouped, name):
        left = pd.DataFrame({"_pos": np.arange(n)})
        for i, key in enumerate(keys):
            left[f"_k{i}"] = X[key].to_numpy()
        right = grouped.reset_index()
        right.columns = [f"_k{i}" for i in range(len(keys))] + [name]
        merged = left.merge(right, on=[f"_k{i}" for i in range(len(keys))],
                            how="left", sort=False)
        return merged.sort_values("_pos")[name].to_numpy()

    if h is None or len(h) == 0:
        for name in ("f_item_count_7d", "f_item_count_30d",
                     "f_item_count_90d", "f_item_recency",
                     "f_customer_count_30d", "f_customer_count_all",
                     "f_pair_count", "f_pair_recency",
                     "f_user_product_type_count", "f_user_department_count"):
            out[name] = np.zeros(n, dtype=float)
        return out

    for days, name in ((7, "f_item_count_7d"),
                       (30, "f_item_count_30d"),
                       (90, "f_item_count_90d")):
        counts = h.loc[h["days_ago"] <= days].groupby("article_id").size()
        out[name] = mapped(counts, "article_id").fillna(0).to_numpy()

    item_recency = h.groupby("article_id")["days_ago"].min()
    out["f_item_recency"] = mapped(item_recency, "article_id").to_numpy()

    recent_users = h.loc[h["days_ago"] <= 30].groupby("customer_id").size()
    all_users = h.groupby("customer_id").size()
    out["f_customer_count_30d"] = mapped(recent_users, "customer_id").fillna(0).to_numpy()
    out["f_customer_count_all"] = mapped(all_users, "customer_id").fillna(0).to_numpy()

    pair = h.groupby(["customer_id", "article_id"]).agg(
        _pair_count=("days_ago", "size"), _pair_recency=("days_ago", "min"))
    out["f_pair_count"] = joined(
        ["customer_id", "article_id"], pair["_pair_count"], "v").astype(float)
    out["f_pair_recency"] = joined(
        ["customer_id", "article_id"], pair["_pair_recency"], "v").astype(float)

    user_type = h.groupby(["customer_id", "product_type_no"]).size()
    out["f_user_product_type_count"] = joined(
        ["customer_id", "raw_i_product_type_no"], user_type, "v").astype(float)

    user_dept = h.groupby(["customer_id", "department_no"]).size()
    out["f_user_department_count"] = joined(
        ["customer_id", "raw_i_department_no"], user_dept, "v").astype(float)

    return out.astype(float)
