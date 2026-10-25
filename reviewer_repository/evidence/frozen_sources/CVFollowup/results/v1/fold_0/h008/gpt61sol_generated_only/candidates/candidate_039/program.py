def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def one_map(xcol, vals, default=0):
        return X[xcol].map(vals).fillna(default).to_numpy()

    def pair_map(vals, default=0):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        return vals.reindex(keys).fillna(default).to_numpy()

    def cat_map(hist_col, raw_col, default=0):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[raw_col].to_numpy()]
        )
        vals = h.groupby(["customer_id", hist_col]).size()
        return vals.reindex(keys).fillna(default).to_numpy()

    d = h["days_ago"]
    for w in (7, 30, 90):
        hw = h.loc[d <= w]
        out["f_item_pop_%d" % w] = one_map(
            "article_id", hw.groupby("article_id").size()
        )
        out["f_user_activity_%d" % w] = one_map(
            "customer_id", hw.groupby("customer_id").size()
        )

    out["f_item_pop_all"] = one_map("article_id", h.groupby("article_id").size())
    out["f_pair_count"] = pair_map(
        h.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_count_30d"] = pair_map(
        h.loc[d <= 30].groupby(["customer_id", "article_id"]).size()
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

    item_price = h.groupby("article_id")["price"].mean()
    user_price = h.groupby("customer_id")["price"].mean()
    ip = one_map("article_id", item_price, np.nan)
    up = one_map("customer_id", user_price, np.nan)
    out["f_item_mean_price"] = ip
    out["f_price_vs_user"] = np.divide(
        ip, up, out=np.full(n, np.nan), where=np.asarray(up) != 0
    )

    cats = (
        ("product_code", "raw_i_product_code", "product"),
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("section_no", "raw_i_section_no", "section"),
        ("department_no", "raw_i_department_no", "department"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
    )
    for hc, xc, name in cats:
        out["f_user_" + name] = cat_map(hc, xc)
        out["f_cat_pop_" + name] = one_map(xc, h.groupby(hc).size())
        out["f_cat_pop30_" + name] = one_map(
            xc, h.loc[d <= 30].groupby(hc).size()
        )

    static = (
        "raw_u_age",
        "raw_u_fn",
        "raw_u_active",
        "raw_u_club_member_status",
        "raw_u_fashion_news_frequency",
        "raw_i_product_type_no",
        "raw_i_section_no",
    )
    for col in static:
        out["f_static_" + col[4:]] = X[col].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
