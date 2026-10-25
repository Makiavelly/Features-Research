def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    customer = X["customer_id"]
    article = X["article_id"]

    def mapped(series, keys):
        idx = pd.MultiIndex.from_arrays(
            [key.to_numpy() for key in keys]
        )
        return pd.Series(series.reindex(idx).to_numpy(), index=X.index)

    names = (
        "f_item_count_7d", "f_item_count_30d", "f_item_count_all",
        "f_customer_count_30d", "f_customer_count_all",
        "f_pair_count_all", "f_pair_count_30d", "f_pair_recency",
        "f_customer_product_count", "f_customer_type_count",
        "f_customer_department_count", "f_customer_colour_count",
    )
    if history is None or len(history) == 0:
        for name in names:
            out[name] = 0.0
        return out

    h = history
    d = h["days_ago"]
    recent7 = h.loc[d <= 7]
    recent30 = h.loc[d <= 30]

    for name, frame in (
        ("f_item_count_7d", recent7),
        ("f_item_count_30d", recent30),
        ("f_item_count_all", h),
    ):
        out[name] = article.map(frame.groupby("article_id").size()).fillna(0).to_numpy()

    out["f_customer_count_30d"] = (
        customer.map(recent30.groupby("customer_id").size()).fillna(0).to_numpy()
    )
    out["f_customer_count_all"] = (
        customer.map(h.groupby("customer_id").size()).fillna(0).to_numpy()
    )

    pair = h.groupby(["customer_id", "article_id"]).agg(
        count=("days_ago", "size"),
        recency=("days_ago", "min"),
    )
    out["f_pair_count_all"] = mapped(pair["count"], [customer, article]).fillna(0).to_numpy()
    out["f_pair_recency"] = mapped(pair["recency"], [customer, article]).fillna(3650).to_numpy()
    pair30 = recent30.groupby(["customer_id", "article_id"]).size()
    out["f_pair_count_30d"] = mapped(pair30, [customer, article]).fillna(0).to_numpy()

    for field, raw, name in (
        ("product_code", "raw_i_product_code", "f_customer_product_count"),
        ("product_type_no", "raw_i_product_type_no", "f_customer_type_count"),
        ("department_no", "raw_i_department_no", "f_customer_department_count"),
        ("colour_group_code", "raw_i_colour_group_code", "f_customer_colour_count"),
    ):
        if field in h.columns and raw in X.columns:
            counts = h.groupby(["customer_id", field]).size()
            out[name] = mapped(counts, [customer, X[raw]]).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    return out.replace([np.inf, -np.inf], np.nan)
