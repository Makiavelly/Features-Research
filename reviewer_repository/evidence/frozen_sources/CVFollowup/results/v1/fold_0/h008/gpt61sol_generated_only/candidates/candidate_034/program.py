def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def one_map(col, s, default=0.0):
        return X[col].map(s).fillna(default).to_numpy()

    def pair_map(s, default=0.0):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        return s.reindex(keys).fillna(default).to_numpy()

    def category_map(hcol, xcol, default=0.0):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[xcol].to_numpy()]
        )
        s = h.groupby(["customer_id", hcol]).size()
        return s.reindex(keys).fillna(default).to_numpy()

    d = h["days_ago"]
    h7 = h.loc[d <= 7]
    h30 = h.loc[d <= 30]
    h90 = h.loc[d <= 90]

    out["f_item_pop_7d"] = one_map("article_id", h7.groupby("article_id").size())
    out["f_item_pop_30d"] = one_map("article_id", h30.groupby("article_id").size())
    out["f_item_pop_90d"] = one_map("article_id", h90.groupby("article_id").size())
    out["f_user_activity_7d"] = one_map("customer_id", h7.groupby("customer_id").size())
    out["f_user_activity_30d"] = one_map("customer_id", h30.groupby("customer_id").size())
    out["f_user_activity_90d"] = one_map("customer_id", h90.groupby("customer_id").size())

    weighted = h.assign(_w=np.exp(-h["days_ago"].to_numpy() / 21.0))
    out["f_item_pop_decay"] = one_map(
        "article_id", weighted.groupby("article_id")["_w"].sum()
    )

    out["f_pair_count"] = pair_map(
        h.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_count_30d"] = pair_map(
        h30.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_recency"] = pair_map(
        h.groupby(["customer_id", "article_id"])["days_ago"].min(), np.nan
    )
    out["f_customer_recency"] = one_map(
        "customer_id", h.groupby("customer_id")["days_ago"].min(), np.nan
    )
    out["f_item_recency"] = one_map(
        "article_id", h.groupby("article_id")["days_ago"].min(), np.nan
    )

    for hc, xc, name in (
        ("product_code", "raw_i_product_code", "product"),
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("section_no", "raw_i_section_no", "section"),
        ("department_no", "raw_i_department_no", "department"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
        ("colour_group_code", "raw_i_colour_group_code", "colour"),
    ):
        a = category_map(hc, xc)
        out["f_user_" + name] = a
        out["f_user_" + name + "_share"] = np.divide(
            a,
            out["f_user_activity_90d"].to_numpy(),
            out=np.zeros(n, dtype=float),
            where=out["f_user_activity_90d"].to_numpy() > 0,
        )

    item_price = h.groupby("article_id")["price"].mean()
    user_price = h.groupby("customer_id")["price"].mean()
    ip = one_map("article_id", item_price, np.nan)
    up = one_map("customer_id", user_price, np.nan)
    out["f_item_mean_price"] = ip
    out["f_price_vs_user"] = np.divide(
        ip, up, out=np.full(n, np.nan), where=np.isfinite(up) & (up != 0)
    )

    for c in (
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
    ):
        out["f_static_" + c[4:]] = X[c].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
