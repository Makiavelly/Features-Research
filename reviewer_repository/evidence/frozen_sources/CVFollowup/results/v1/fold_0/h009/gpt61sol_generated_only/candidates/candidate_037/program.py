def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    u = X["customer_id"]
    a = X["article_id"]

    out["f_u_age"] = X["raw_u_age"].to_numpy()
    out["f_u_active"] = X["raw_u_active"].to_numpy()
    out["f_u_club"] = X["raw_u_club_member_status"].to_numpy()
    out["f_i_department"] = X["raw_i_department_no"].to_numpy()
    out["f_i_section"] = X["raw_i_section_no"].to_numpy()
    out["f_i_type"] = X["raw_i_product_type_no"].to_numpy()

    names = [
        "f_item_7d", "f_item_30d", "f_item_90d", "f_item_recency",
        "f_customer_7d", "f_customer_30d", "f_customer_recency",
        "f_pair_count", "f_pair_recency", "f_department_affinity",
        "f_section_affinity", "f_type_affinity", "f_colour_affinity",
        "f_customer_department_30d", "f_department_30d", "f_item_total",
        "f_customer_total", "f_item_price", "f_item_channel2"
    ]

    if h.empty:
        for name in names:
            out[name] = np.nan if name.endswith(("recency", "price", "channel2")) else 0.0
        return out.replace([np.inf, -np.inf], np.nan)

    def amap(s):
        return a.map(s).to_numpy()

    def umap(s):
        return u.map(s).to_numpy()

    for w in (7, 30, 90):
        s = h.loc[h["days_ago"] <= w].groupby("article_id").size()
        out["f_item_" + str(w) + "d"] = a.map(s).fillna(0).to_numpy()

    out["f_item_recency"] = amap(h.groupby("article_id")["days_ago"].min())
    out["f_customer_recency"] = umap(h.groupby("customer_id")["days_ago"].min())

    for w in (7, 30):
        s = h.loc[h["days_ago"] <= w].groupby("customer_id").size()
        out["f_customer_" + str(w) + "d"] = u.map(s).fillna(0).to_numpy()

    pk = pd.MultiIndex.from_arrays([u.to_numpy(), a.to_numpy()])
    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(["size", "min"])
    out["f_pair_count"] = pair["size"].reindex(pk).fillna(0).to_numpy()
    out["f_pair_recency"] = pair["min"].reindex(pk).to_numpy()

    for col, label in (
        ("department_no", "department"),
        ("section_no", "section"),
        ("product_type_no", "type"),
        ("colour_group_code", "colour"),
    ):
        k = pd.MultiIndex.from_arrays([u.to_numpy(), X["raw_i_" + col].to_numpy()])
        out["f_" + label + "_affinity"] = h.groupby(
            ["customer_id", col]
        ).size().reindex(k).fillna(0).to_numpy()

    recent = h.loc[h["days_ago"] <= 30]
    k = pd.MultiIndex.from_arrays([u.to_numpy(), X["raw_i_department_no"].to_numpy()])
    out["f_customer_department_30d"] = recent.groupby(
        ["customer_id", "department_no"]
    ).size().reindex(k).fillna(0).to_numpy()
    out["f_department_30d"] = X["raw_i_department_no"].map(
        recent.groupby("department_no").size()
    ).fillna(0).to_numpy()
    out["f_item_total"] = amap(h.groupby("article_id").size())
    out["f_customer_total"] = umap(h.groupby("customer_id").size())
    out["f_item_price"] = amap(h.groupby("article_id")["price"].mean())
    out["f_item_channel2"] = amap(
        h.assign(_c=(h["sales_channel_id"] == 2).astype(float))
        .groupby("article_id")["_c"].mean()
    )
    return out.replace([np.inf, -np.inf], np.nan)
