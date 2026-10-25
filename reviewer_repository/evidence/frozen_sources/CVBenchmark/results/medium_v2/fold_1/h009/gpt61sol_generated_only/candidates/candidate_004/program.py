def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    names = (
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_count_all", "f_item_recency", "f_customer_count_30d",
        "f_customer_count_all", "f_customer_recency", "f_pair_count",
        "f_pair_recency", "f_user_product_type_count",
        "f_user_department_count", "f_user_section_count",
        "f_user_colour_count", "f_user_product_code_count"
    )
    if h is None or len(h) == 0:
        for name in names:
            out[name] = np.zeros(n, dtype=float)
        return out

    def mapped(series, key):
        return X[key].map(series).fillna(0).to_numpy()

    def joined(keys, series, name):
        left = pd.DataFrame({"_pos": np.arange(n)})
        for i, key in enumerate(keys):
            left[f"_k{i}"] = X[key].to_numpy()
        right = series.rename(name).reset_index()
        right.columns = [f"_k{i}" for i in range(len(keys))] + [name]
        merged = left.merge(right, on=[f"_k{i}" for i in range(len(keys))],
                            how="left", sort=False)
        return merged.sort_values("_pos")[name].fillna(0).to_numpy()

    for days, name in ((7, "f_item_count_7d"),
                       (30, "f_item_count_30d"),
                       (90, "f_item_count_90d")):
        counts = h.loc[h["days_ago"] <= days].groupby("article_id").size()
        out[name] = mapped(counts, "article_id")

    out["f_item_count_all"] = mapped(h.groupby("article_id").size(), "article_id")
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()).to_numpy()

    recent = h.loc[h["days_ago"] <= 30]
    out["f_customer_count_30d"] = mapped(
        recent.groupby("customer_id").size(), "customer_id")
    out["f_customer_count_all"] = mapped(
        h.groupby("customer_id").size(), "customer_id")
    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()).to_numpy()

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(
        ["size", "min"])
    out["f_pair_count"] = joined(
        ["customer_id", "article_id"], pair["size"], "v")
    out["f_pair_recency"] = joined(
        ["customer_id", "article_id"], pair["min"], "v")

    for hist_col, x_col, name in (
        ("product_type_no", "raw_i_product_type_no", "f_user_product_type_count"),
        ("department_no", "raw_i_department_no", "f_user_department_count"),
        ("section_no", "raw_i_section_no", "f_user_section_count"),
        ("colour_group_code", "raw_i_colour_group_code", "f_user_colour_count"),
        ("product_code", "raw_i_product_code", "f_user_product_code_count")
    ):
        counts = h.groupby(["customer_id", hist_col]).size()
        out[name] = joined(["customer_id", x_col], counts, "v")

    return out.astype(float)
