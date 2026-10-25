def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    days = h["days_ago"]

    def one_map(col, values, default=0):
        return X[col].map(values).fillna(default).to_numpy()

    def pair_map(xcol, values, default=0):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[xcol].to_numpy()]
        )
        return values.reindex(keys).fillna(default).to_numpy()

    for window in (7, 30, 90):
        hw = h.loc[days <= window]
        out["f_item_pop_%d" % window] = one_map(
            "article_id", hw.groupby("article_id").size()
        )
        out["f_user_activity_%d" % window] = one_map(
            "customer_id", hw.groupby("customer_id").size()
        )

    out["f_item_pop_all"] = one_map(
        "article_id", h.groupby("article_id").size()
    )
    out["f_pair_count"] = pair_map(
        "article_id", h.groupby(["customer_id", "article_id"]).size()
    )
    for window in (7, 30):
        out["f_pair_count_%dd" % window] = pair_map(
            "article_id",
            h.loc[days <= window].groupby(["customer_id", "article_id"]).size()
        )
    out["f_pair_recency"] = pair_map(
        "article_id",
        h.groupby(["customer_id", "article_id"])["days_ago"].min(),
        np.nan,
    )
    out["f_customer_recency"] = one_map(
        "customer_id", h.groupby("customer_id")["days_ago"].min(), np.nan
    )
    out["f_item_recency"] = one_map(
        "article_id", h.groupby("article_id")["days_ago"].min(), np.nan
    )

    categories = (
        ("product_code", "raw_i_product_code", "product"),
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("section_no", "raw_i_section_no", "section"),
        ("department_no", "raw_i_department_no", "department"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
        ("index_group_no", "raw_i_index_group_no", "index"),
    )
    for hc, xc, name in categories:
        out["f_user_" + name] = pair_map(
            xc, h.groupby(["customer_id", hc]).size()
        )

    recent = h.loc[days <= 30]
    for hc, xc, name in categories[:5]:
        out["f_user_" + name + "_30d"] = pair_map(
            xc, recent.groupby(["customer_id", hc]).size()
        )
    for hc, xc, name in categories[2:5]:
        out["f_pop_" + name + "_30d"] = one_map(
            xc, recent.groupby(hc).size()
        )

    out["f_item_mean_price"] = one_map(
        "article_id", h.groupby("article_id")["price"].mean(), np.nan
    )
    user_price = one_map(
        "customer_id", h.groupby("customer_id")["price"].mean(), np.nan
    )
    out["f_user_mean_price"] = user_price
    item_price = out["f_item_mean_price"].to_numpy()
    out["f_price_vs_user"] = np.divide(
        item_price,
        user_price,
        out=np.full(len(X), np.nan),
        where=np.isfinite(user_price) & (user_price != 0),
    )
    channel2 = h["sales_channel_id"].eq(2).astype(float)
    out["f_item_channel2_rate"] = one_map(
        "article_id", channel2.groupby(h["article_id"]).mean(), np.nan
    )
    out["f_user_channel2_rate"] = one_map(
        "customer_id", channel2.groupby(h["customer_id"]).mean(), np.nan
    )

    for col in (
        "raw_u_age",
        "raw_u_fn",
        "raw_u_active",
        "raw_u_club_member_status",
    ):
        out["f_static_" + col[4:]] = X[col].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
