def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def umap(col, series, default=0):
        return X[col].map(series).fillna(default).to_numpy()

    def pmap(series, default=0):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        return series.reindex(keys).fillna(default).to_numpy()

    def window(d):
        return h.loc[h["days_ago"] <= d]

    for d in (7, 30, 90):
        w = window(d)
        out["f_item_pop_%d" % d] = umap("article_id", w.groupby("article_id").size())
        out["f_user_activity_%d" % d] = umap("customer_id", w.groupby("customer_id").size())
    out["f_item_pop_all"] = umap("article_id", h.groupby("article_id").size())

    for d in (7, 30):
        out["f_pair_count_%d" % d] = pmap(
            window(d).groupby(["customer_id", "article_id"]).size()
        )
    out["f_pair_count_all"] = pmap(
        h.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_recency"] = pmap(
        h.groupby(["customer_id", "article_id"])["days_ago"].min(), np.nan
    )
    out["f_item_recency"] = umap(
        "article_id", h.groupby("article_id")["days_ago"].min(), np.nan
    )
    out["f_user_recency"] = umap(
        "customer_id", h.groupby("customer_id")["days_ago"].min(), np.nan
    )

    weight = np.exp(-h["days_ago"].to_numpy() / 21.0)
    weighted = pd.Series(weight, index=h.index)
    out["f_item_recent_weight"] = umap(
        "article_id", weighted.groupby(h["article_id"]).sum()
    )
    out["f_user_recent_weight"] = umap(
        "customer_id", weighted.groupby(h["customer_id"]).sum()
    )

    categories = (
        ("product_code", "raw_i_product_code", "product"),
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("section_no", "raw_i_section_no", "section"),
        ("department_no", "raw_i_department_no", "department"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
    )
    for hc, xc, name in categories:
        out["f_pop_" + name] = umap(xc, h.groupby(hc).size())
        out["f_user_" + name] = pmap(
            h.groupby(["customer_id", hc]).size()
        )

    ip = umap("article_id", h.groupby("article_id")["price"].mean(), np.nan)
    up = umap("customer_id", h.groupby("customer_id")["price"].mean(), np.nan)
    out["f_item_mean_price"] = ip
    out["f_user_mean_price"] = up
    out["f_price_vs_user"] = np.divide(
        ip, up, out=np.full(n, np.nan), where=np.asarray(up) != 0
    )

    out["f_item_channel2"] = umap(
        "article_id",
        h.assign(_c=(h["sales_channel_id"] == 2).astype(float))
         .groupby("article_id")["_c"].mean(),
        np.nan,
    )
    out["f_user_channel2"] = umap(
        "customer_id",
        h.assign(_c=(h["sales_channel_id"] == 2).astype(float))
         .groupby("customer_id")["_c"].mean(),
        np.nan,
    )

    for col, name in (
        ("raw_u_age", "age"),
        ("raw_u_active", "active"),
        ("raw_u_club_member_status", "club"),
        ("raw_i_product_type_no", "item_type"),
        ("raw_i_section_no", "item_section"),
    ):
        out["f_static_" + name] = X[col].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
