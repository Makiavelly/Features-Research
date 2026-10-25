def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)
    h = history

    feature_names = (
        "f_item_sales_14d", "f_item_sales_60d", "f_item_sales_180d",
        "f_item_buyers_60d", "f_item_weighted_activity",
        "f_customer_sales_14d", "f_customer_sales_60d",
        "f_pair_sales_14d", "f_pair_sales_60d",
        "f_user_section_sales_60d", "f_user_colour_sales_60d"
    )

    if h is None or len(h) == 0:
        for name in feature_names:
            out[name] = np.zeros(n, dtype=float)
        return out

    def lookup(keys, values):
        left = pd.DataFrame({"_position": np.arange(n)})
        for i, key in enumerate(keys):
            left["_key" + str(i)] = X[key].to_numpy()
        right = values.rename("_value").reset_index()
        right.columns = ["_key" + str(i) for i in range(len(keys))] + ["_value"]
        merged = left.merge(
            right,
            on=["_key" + str(i) for i in range(len(keys))],
            how="left",
            sort=False
        )
        return merged.sort_values("_position")["_value"].to_numpy()

    for days, name in (
        (14, "f_item_sales_14d"),
        (60, "f_item_sales_60d"),
        (180, "f_item_sales_180d")
    ):
        part = h.loc[h["days_ago"] <= days]
        values = part.groupby("article_id").size()
        out[name] = X["article_id"].map(values).fillna(0).to_numpy()

    recent = h.loc[h["days_ago"] <= 60]
    buyers = recent.groupby("article_id")["customer_id"].nunique()
    out["f_item_buyers_60d"] = X["article_id"].map(buyers).fillna(0).to_numpy()

    weighted = h.assign(
        _weight=np.exp(-h["days_ago"].astype(float) / 28.0)
    ).groupby("article_id")["_weight"].sum()
    out["f_item_weighted_activity"] = X["article_id"].map(
        weighted).fillna(0).to_numpy()

    for days, name in (
        (14, "f_customer_sales_14d"),
        (60, "f_customer_sales_60d")
    ):
        part = h.loc[h["days_ago"] <= days]
        values = part.groupby("customer_id").size()
        out[name] = X["customer_id"].map(values).fillna(0).to_numpy()

    pair14 = h.loc[h["days_ago"] <= 14].groupby(
        ["customer_id", "article_id"]).size()
    pair60 = h.loc[h["days_ago"] <= 60].groupby(
        ["customer_id", "article_id"]).size()
    out["f_pair_sales_14d"] = lookup(
        ["customer_id", "article_id"], pair14)
    out["f_pair_sales_60d"] = lookup(
        ["customer_id", "article_id"], pair60)

    section = h.loc[h["days_ago"] <= 60].groupby(
        ["customer_id", "section_no"]).size()
    out["f_user_section_sales_60d"] = lookup(
        ["customer_id", "raw_i_section_no"], section)

    colour = h.loc[h["days_ago"] <= 60].groupby(
        ["customer_id", "colour_group_code"]).size()
    out["f_user_colour_sales_60d"] = lookup(
        ["customer_id", "raw_i_colour_group_code"], colour)

    return out.astype(float)
