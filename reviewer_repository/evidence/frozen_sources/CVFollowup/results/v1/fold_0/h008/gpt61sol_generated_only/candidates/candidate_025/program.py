def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def mapped(column, values, default=0):
        return X[column].map(values).fillna(default).to_numpy()

    def paired(values, default=0):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        return values.reindex(keys).fillna(default).to_numpy()

    days = h["days_ago"]

    for w in (7, 30, 90):
        hw = h.loc[days <= w]
        out["f_item_count_%dd" % w] = mapped(
            "article_id", hw.groupby("article_id").size()
        )
        out["f_user_count_%dd" % w] = mapped(
            "customer_id", hw.groupby("customer_id").size()
        )

    out["f_item_count_all"] = mapped(
        "article_id", h.groupby("article_id").size()
    )

    pairs = h.groupby(["customer_id", "article_id"])
    out["f_pair_count"] = paired(pairs.size())
    out["f_pair_count_30d"] = paired(
        h.loc[days <= 30].groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_recency"] = paired(pairs["days_ago"].min(), np.nan)

    out["f_customer_recency"] = mapped(
        "customer_id", h.groupby("customer_id")["days_ago"].min(), np.nan
    )
    out["f_item_recency"] = mapped(
        "article_id", h.groupby("article_id")["days_ago"].min(), np.nan
    )

    decay = np.exp(-days.to_numpy(dtype=float) / 30.0)
    weighted = h.assign(_w=decay)

    out["f_item_weighted"] = mapped(
        "article_id", weighted.groupby("article_id")["_w"].sum()
    )
    out["f_user_weighted"] = mapped(
        "customer_id", weighted.groupby("customer_id")["_w"].sum()
    )

    dimensions = (
        ("product_code", "raw_i_product_code", "product"),
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("section_no", "raw_i_section_no", "section"),
        ("department_no", "raw_i_department_no", "department"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
    )

    for hc, xc, name in dimensions:
        out["f_user_" + name] = paired(
            h.groupby(["customer_id", hc]).size()
        )
        out["f_pop_" + name] = mapped(
            xc, h.groupby(hc).size()
        )

    item_mean = h.groupby("article_id")["price"].mean()
    user_mean = h.groupby("customer_id")["price"].mean()
    item_price = mapped("article_id", item_mean, np.nan)
    user_price = mapped("customer_id", user_mean, np.nan)

    out["f_item_mean_price"] = item_price
    out["f_user_mean_price"] = user_price
    out["f_price_vs_user"] = np.divide(
        item_price,
        user_price,
        out=np.full(n, np.nan, dtype=float),
        where=np.isfinite(user_price) & (user_price != 0),
    )

    for col in (
        "raw_u_age",
        "raw_u_fn",
        "raw_u_active",
        "raw_u_club_member_status",
        "raw_u_fashion_news_frequency",
        "raw_i_product_code",
        "raw_i_product_type_no",
    ):
        out["f_static_" + col[4:]] = X[col].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
