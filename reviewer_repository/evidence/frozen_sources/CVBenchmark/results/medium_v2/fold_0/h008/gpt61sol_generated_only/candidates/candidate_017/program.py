def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    d = h["days_ago"]

    def mapped(col, series, default=0):
        return X[col].map(series).fillna(default).to_numpy()

    def pair_values(series, default=0):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        return series.reindex(keys).fillna(default).to_numpy()

    for w in (7, 30, 90):
        hw = h.loc[d <= w]
        out["f_item_pop_%d" % w] = mapped(
            "article_id", hw.groupby("article_id").size()
        )
        out["f_user_activity_%d" % w] = mapped(
            "customer_id", hw.groupby("customer_id").size()
        )

    out["f_item_pop_all"] = mapped(
        "article_id", h.groupby("article_id").size()
    )

    out["f_pair_count_7d"] = pair_values(
        h.loc[d <= 7].groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_count_30d"] = pair_values(
        h.loc[d <= 30].groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_count_all"] = pair_values(
        h.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_recency"] = pair_values(
        h.groupby(["customer_id", "article_id"])["days_ago"].min(),
        np.nan
    )

    out["f_customer_recency"] = mapped(
        "customer_id", h.groupby("customer_id")["days_ago"].min(), np.nan
    )
    out["f_item_recency"] = mapped(
        "article_id", h.groupby("article_id")["days_ago"].min(), np.nan
    )

    for hc, xc, name in (
        ("product_code", "raw_i_product_code", "product"),
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("section_no", "raw_i_section_no", "section"),
        ("department_no", "raw_i_department_no", "department"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
    ):
        out["f_user_" + name] = pair_values(
            h.groupby(["customer_id", hc]).size()
        ) if False else h.groupby(["customer_id", hc]).size().reindex(
            pd.MultiIndex.from_arrays(
                [X["customer_id"].to_numpy(), X[xc].to_numpy()]
            )
        ).fillna(0).to_numpy()

    item_price = h.groupby("article_id")["price"].mean()
    user_price = h.groupby("customer_id")["price"].mean()
    ip = mapped("article_id", item_price, np.nan)
    up = mapped("customer_id", user_price, np.nan)

    out["f_item_mean_price"] = ip
    out["f_user_mean_price"] = up
    out["f_price_vs_user"] = np.divide(
        ip,
        up,
        out=np.full(len(X), np.nan, dtype=float),
        where=np.asarray(up) != 0
    )

    static = (
        "raw_u_age",
        "raw_u_fn",
        "raw_u_active",
        "raw_u_club_member_status",
        "raw_u_fashion_news_frequency",
        "raw_i_product_code",
        "raw_i_product_type_no",
        "raw_i_graphical_appearance_no",
        "raw_i_colour_group_code",
        "raw_i_perceived_colour_value_id",
        "raw_i_perceived_colour_master_id",
        "raw_i_department_no",
        "raw_i_index_group_no",
        "raw_i_section_no",
        "raw_i_garment_group_no",
    )
    for col in static:
        out["f_static_" + col[4:]] = X[col].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
