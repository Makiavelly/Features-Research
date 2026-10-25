def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)
    h = history

    names = (
        "f_item_count_30d", "f_item_count_7d", "f_item_recency",
        "f_user_count_30d", "f_user_recency", "f_pair_count",
        "f_pair_recent_count", "f_pair_recency",
        "f_user_type_recent_count", "f_user_department_recent_count",
        "f_user_section_recent_count"
    )
    if h is None or len(h) == 0:
        for name in names:
            out[name] = np.zeros(n, dtype=float)
        return out

    def lookup(keys, values):
        left = pd.DataFrame({"_p": np.arange(n)})
        for i, key in enumerate(keys):
            left["_k" + str(i)] = X[key].to_numpy()
        right = values.rename("_v").reset_index()
        right.columns = ["_k" + str(i) for i in range(len(keys))] + ["_v"]
        merged = left.merge(right, on=["_k" + str(i) for i in range(len(keys))],
                            how="left", sort=False)
        return merged.sort_values("_p")["_v"].to_numpy()

    h30 = h.loc[h["days_ago"] <= 30]
    h7 = h.loc[h["days_ago"] <= 7]
    out["f_item_count_30d"] = X["article_id"].map(
        h30.groupby("article_id").size()).fillna(0).to_numpy()
    out["f_item_count_7d"] = X["article_id"].map(
        h7.groupby("article_id").size()).fillna(0).to_numpy()
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()).to_numpy()

    out["f_user_count_30d"] = X["customer_id"].map(
        h30.groupby("customer_id").size()).fillna(0).to_numpy()
    out["f_user_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()).to_numpy()

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(
        ["size", "min"])
    pair30 = h30.groupby(["customer_id", "article_id"]).size()
    out["f_pair_count"] = lookup(["customer_id", "article_id"], pair["size"])
    out["f_pair_recent_count"] = lookup(["customer_id", "article_id"], pair30)
    out["f_pair_recency"] = lookup(["customer_id", "article_id"], pair["min"])

    for col, raw, name in (
        ("product_type_no", "raw_i_product_type_no", "f_user_type_recent_count"),
        ("department_no", "raw_i_department_no", "f_user_department_recent_count"),
        ("section_no", "raw_i_section_no", "f_user_section_recent_count")
    ):
        counts = h30.groupby(["customer_id", col]).size()
        out[name] = lookup(["customer_id", raw], counts)

    return out.astype(float)
