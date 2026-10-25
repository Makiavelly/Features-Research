def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def one_map(col, vals, default=0):
        return X[col].map(vals).fillna(default).to_numpy()

    def pair_map(a, b, vals, default=0):
        keys = pd.MultiIndex.from_arrays(
            [X[a].to_numpy(), X[b].to_numpy()]
        )
        return vals.reindex(keys).fillna(default).to_numpy()

    def add_pair(name, hcol, xcol, frame, default=0):
        vals = frame.groupby(["customer_id", hcol]).size()
        out[name] = pair_map("customer_id", xcol, vals, default)

    d = h["days_ago"]

    for w in (7, 30, 90):
        hw = h.loc[d <= w]
        out["f_item_pop_%d" % w] = one_map(
            "article_id", hw.groupby("article_id").size()
        )
        out["f_user_activity_%d" % w] = one_map(
            "customer_id", hw.groupby("customer_id").size()
        )

    out["f_item_pop_all"] = one_map(
        "article_id", h.groupby("article_id").size()
    )
    out["f_pair_count"] = pair_map(
        "customer_id", "article_id",
        h.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_count_7d"] = pair_map(
        "customer_id", "article_id",
        h.loc[d <= 7].groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_count_30d"] = pair_map(
        "customer_id", "article_id",
        h.loc[d <= 30].groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_recency"] = pair_map(
        "customer_id", "article_id",
        h.groupby(["customer_id", "article_id"])["days_ago"].min(),
        np.nan
    )
    out["f_customer_recency"] = one_map(
        "customer_id", h.groupby("customer_id")["days_ago"].min(), np.nan
    )
    out["f_item_recency"] = one_map(
        "article_id", h.groupby("article_id")["days_ago"].min(), np.nan
    )

    cats = (
        ("product_code", "raw_i_product_code", "product"),
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("section_no", "raw_i_section_no", "section"),
        ("department_no", "raw_i_department_no", "department"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
        ("index_group_no", "raw_i_index_group_no", "index"),
    )
    for hc, xc, name in cats:
        out["f_user_%s" % name] = pair_map(
            "customer_id", xc, h.groupby(["customer_id", hc]).size()
        )
        out["f_user_%s_30d" % name] = pair_map(
            "customer_id", xc,
            h.loc[d <= 30].groupby(["customer_id", hc]).size()
        )
        out["f_pop_%s_30d" % name] = one_map(
            xc, h.loc[d <= 30].groupby(hc).size()
        )

    out["f_item_mean_price"] = one_map(
        "article_id", h.groupby("article_id")["price"].mean(), np.nan
    )
    up = one_map("customer_id", h.groupby("customer_id")["price"].mean(), np.nan)
    out["f_user_mean_price"] = up
    out["f_price_vs_user"] = np.divide(
        out["f_item_mean_price"].to_numpy(), up,
        out=np.full(n, np.nan), where=np.isfinite(up) & (up != 0)
    )
    out["f_item_channel2_rate"] = one_map(
        "article_id",
        h.assign(_c=(h["sales_channel_id"] == 2).astype(float))
         .groupby("article_id")["_c"].mean(),
        np.nan
    )
    out["f_user_channel2_rate"] = one_map(
        "customer_id",
        h.assign(_c=(h["sales_channel_id"] == 2).astype(float))
         .groupby("customer_id")["_c"].mean(),
        np.nan
    )

    for col in (
        "raw_u_age", "raw_u_fn", "raw_u_active",
        "raw_u_club_member_status", "raw_u_fashion_news_frequency",
        "raw_i_product_code", "raw_i_product_type_no",
        "raw_i_index_group_no", "raw_i_section_no",
        "raw_i_garment_group_no"
    ):
        out["f_static_" + col[4:]] = X[col].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
