def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)
    h = history

    names = (
        "f_article_buyers_30d", "f_article_channel2_30d",
        "f_article_mean_price", "f_customer_items_30d",
        "f_pair_count_365d", "f_pair_recency",
        "f_user_type_count_90d", "f_user_garment_count_90d",
        "f_user_colour_count_90d", "f_department_popularity_30d"
    )

    if h is None or len(h) == 0:
        for name in names:
            out[name] = np.zeros(n, dtype=float)
        return out

    def lookup(keys, values):
        left = pd.DataFrame({"_position": np.arange(n)})
        for i, key in enumerate(keys):
            left["_key" + str(i)] = X[key].to_numpy()
        right = values.rename("_value").reset_index()
        right.columns = ["_key" + str(i) for i in range(len(keys))] + ["_value"]
        z = left.merge(
            right,
            on=["_key" + str(i) for i in range(len(keys))],
            how="left",
            sort=False
        )
        return z.sort_values("_position")["_value"].to_numpy()

    h30 = h.loc[h["days_ago"] <= 30]
    h90 = h.loc[h["days_ago"] <= 90]

    out["f_article_buyers_30d"] = X["article_id"].map(
        h30.groupby("article_id")["customer_id"].nunique()
    ).fillna(0).to_numpy()

    out["f_article_channel2_30d"] = X["article_id"].map(
        h30.loc[h30["sales_channel_id"] == 2].groupby("article_id").size()
    ).fillna(0).to_numpy()

    out["f_article_mean_price"] = X["article_id"].map(
        h.groupby("article_id")["price"].mean()
    ).fillna(0).to_numpy()

    out["f_customer_items_30d"] = X["customer_id"].map(
        h30.groupby("customer_id")["article_id"].nunique()
    ).fillna(0).to_numpy()

    pair = h.groupby(["customer_id", "article_id"]).agg(
        _count=("days_ago", "size"),
        _recent=("days_ago", "min")
    )
    out["f_pair_count_365d"] = lookup(
        ["customer_id", "article_id"], pair["_count"]
    )
    out["f_pair_recency"] = lookup(
        ["customer_id", "article_id"], pair["_recent"]
    )

    for hist_col, raw_col, name in (
        ("product_type_no", "raw_i_product_type_no",
         "f_user_type_count_90d"),
        ("garment_group_no", "raw_i_garment_group_no",
         "f_user_garment_count_90d"),
        ("colour_group_code", "raw_i_colour_group_code",
         "f_user_colour_count_90d")
    ):
        values = h90.groupby(["customer_id", hist_col]).size()
        out[name] = lookup(["customer_id", raw_col], values)

    dept = h30.groupby("department_no").size()
    out["f_department_popularity_30d"] = X["raw_i_department_no"].map(
        dept).fillna(0).to_numpy()

    return out.astype(float)
