def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    n = len(X)
    c = X["customer_id"]
    a = X["article_id"]
    h = history

    static = (
        ("raw_u_age", "f_user_age"),
        ("raw_u_fn", "f_user_fn"),
        ("raw_u_active", "f_user_active"),
        ("raw_u_club_member_status", "f_user_club_status"),
        ("raw_u_fashion_news_frequency", "f_user_news_frequency"),
        ("raw_i_product_code", "f_item_product_code"),
        ("raw_i_product_type_no", "f_item_product_type"),
        ("raw_i_graphical_appearance_no", "f_item_graphical_appearance"),
        ("raw_i_colour_group_code", "f_item_colour_group"),
        ("raw_i_perceived_colour_value_id", "f_item_colour_value"),
        ("raw_i_perceived_colour_master_id", "f_item_colour_master"),
        ("raw_i_department_no", "f_item_department"),
        ("raw_i_index_group_no", "f_item_index_group"),
        ("raw_i_section_no", "f_item_section"),
        ("raw_i_garment_group_no", "f_item_garment_group"),
    )
    for source, name in static:
        out[name] = X[source].to_numpy()

    def mapped(series, key):
        return key.map(series).fillna(0).to_numpy()

    def pair_values(grouped, columns):
        keys = pd.MultiIndex.from_arrays(
            [c.to_numpy(), a.to_numpy()],
            names=["customer_id", "article_id"],
        )
        return grouped.reindex(keys).fillna(0).to_numpy()

    if h.empty:
        zeros = (
            "f_item_purchases_7d f_item_purchases_30d "
            "f_item_purchases_90d f_item_purchases_all "
            "f_item_recency f_item_mean_price "
            "f_user_purchases_7d f_user_purchases_30d "
            "f_user_purchases_90d f_user_purchases_all "
            "f_user_mean_price f_user_item_purchases_7d "
            "f_user_item_purchases_30d f_user_item_purchases_90d "
            "f_user_item_purchases_all f_user_item_recency "
            "f_user_department_purchases f_user_product_type_purchases "
            "f_user_section_purchases f_user_garment_group_purchases"
        ).split()
        for name in zeros:
            out[name] = np.nan if "recency" in name or "price" in name else 0.0
        return out.reindex(X.index)

    d = h["days_ago"]

    for w in (7, 30, 90):
        q = h.loc[d <= w].groupby("article_id").size()
        out[f"f_item_purchases_{w}d"] = mapped(q, a)

    ig = h.groupby("article_id")
    out["f_item_purchases_all"] = mapped(ig.size(), a)
    out["f_item_recency"] = a.map(ig["days_ago"].min()).to_numpy()
    out["f_item_mean_price"] = a.map(ig["price"].mean()).to_numpy()

    for w in (7, 30, 90):
        q = h.loc[d <= w].groupby("customer_id").size()
        out[f"f_user_purchases_{w}d"] = mapped(q, c)
    ug = h.groupby("customer_id")
    out["f_user_purchases_all"] = mapped(ug.size(), c)
    out["f_user_mean_price"] = c.map(ug["price"].mean()).to_numpy()

    pg = h.groupby(["customer_id", "article_id"])
    out["f_user_item_purchases_all"] = pair_values(pg.size(), None)
    out["f_user_item_recency"] = pair_values(pg["days_ago"].min(), None)
    for w in (7, 30, 90):
        pw = h.loc[d <= w].groupby(["customer_id", "article_id"]).size()
        out[f"f_user_item_purchases_{w}d"] = pair_values(pw, None)

    for hc, xc, name in (
        ("department_no", "raw_i_department_no", "f_user_department_purchases"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_type_purchases"),
        ("section_no", "raw_i_section_no", "f_user_section_purchases"),
        ("garment_group_no", "raw_i_garment_group_no", "f_user_garment_group_purchases"),
    ):
        q = h.groupby(["customer_id", hc]).size()
        keys = pd.MultiIndex.from_arrays(
            [c.to_numpy(), X[xc].to_numpy()],
            names=["customer_id", hc],
        )
        out[name] = q.reindex(keys).fillna(0).to_numpy()

    return out.reindex(X.index)
