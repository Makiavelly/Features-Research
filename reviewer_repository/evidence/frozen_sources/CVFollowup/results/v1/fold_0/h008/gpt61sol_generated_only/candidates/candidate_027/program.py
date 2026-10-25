def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)
    c = X["customer_id"]
    a = X["article_id"]

    def mapped(series, key):
        return key.map(series).fillna(0).to_numpy()

    def pair_values(series, fill=0):
        keys = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return series.reindex(keys).fillna(fill).to_numpy()

    if h.empty:
        for w in (7, 30, 90):
            out["f_item_purchases_%dd" % w] = 0.0
            out["f_user_purchases_%dd" % w] = 0.0
            out["f_user_item_purchases_%dd" % w] = 0.0
        for name in (
            "f_item_purchases_all", "f_item_recency", "f_item_mean_price",
            "f_item_decay", "f_user_item_purchases_all",
            "f_user_item_recency", "f_user_item_decay",
            "f_user_total_purchases", "f_user_mean_price",
            "f_user_department_purchases", "f_user_product_type_purchases",
            "f_user_product_code_purchases", "f_user_section_purchases",
        ):
            out[name] = np.nan if ("recency" in name or "price" in name) else 0.0
    else:
        d = h["days_ago"]
        hg = h.groupby("article_id")
        ug = h.groupby("customer_id")
        pg = h.groupby(["customer_id", "article_id"])

        for w in (7, 30, 90):
            r = h.loc[d <= w]
            out["f_item_purchases_%dd" % w] = mapped(
                r.groupby("article_id").size(), a)
            out["f_user_purchases_%dd" % w] = mapped(
                r.groupby("customer_id").size(), c)
            out["f_user_item_purchases_%dd" % w] = pair_values(
                r.groupby(["customer_id", "article_id"]).size())

        out["f_item_purchases_all"] = mapped(hg.size(), a)
        out["f_item_recency"] = a.map(hg["days_ago"].min())
        out["f_item_mean_price"] = a.map(hg["price"].mean())
        out["f_item_decay"] = mapped(
            np.exp(-d / 30.0).groupby(h["article_id"]).sum(), a)

        out["f_user_item_purchases_all"] = pair_values(pg.size())
        out["f_user_item_recency"] = pair_values(pg["days_ago"].min(), np.nan)
        out["f_user_item_decay"] = pair_values(
            np.exp(-d / 30.0).groupby(
                [h["customer_id"], h["article_id"]]).sum())
        out["f_user_total_purchases"] = mapped(ug.size(), c)
        out["f_user_mean_price"] = c.map(ug["price"].mean())

        for hc, rc, name in (
            ("department_no", "raw_i_department_no",
             "f_user_department_purchases"),
            ("product_type_no", "raw_i_product_type_no",
             "f_user_product_type_purchases"),
            ("product_code", "raw_i_product_code",
             "f_user_product_code_purchases"),
            ("section_no", "raw_i_section_no",
             "f_user_section_purchases"),
        ):
            keys = pd.MultiIndex.from_arrays([c.to_numpy(), X[rc].to_numpy()])
            s = h.groupby(["customer_id", hc]).size()
            out[name] = s.reindex(keys).fillna(0).to_numpy()

    static = (
        ("raw_u_age", "f_user_age"),
        ("raw_u_fn", "f_user_fashion_news"),
        ("raw_u_active", "f_user_active"),
        ("raw_u_club_member_status", "f_user_club_status"),
        ("raw_u_fashion_news_frequency", "f_user_news_frequency"),
        ("raw_i_product_code", "f_article_product_code"),
        ("raw_i_product_type_no", "f_article_product_type"),
        ("raw_i_graphical_appearance_no", "f_article_graphical"),
        ("raw_i_colour_group_code", "f_article_colour"),
        ("raw_i_perceived_colour_value_id", "f_article_colour_value"),
        ("raw_i_perceived_colour_master_id", "f_article_colour_master"),
        ("raw_i_department_no", "f_article_department"),
        ("raw_i_index_group_no", "f_article_index_group"),
        ("raw_i_section_no", "f_article_section"),
        ("raw_i_garment_group_no", "f_article_garment_group"),
    )
    for src, dst in static:
        out[dst] = X[src].to_numpy()

    out["f_item_user_ratio"] = (
        out["f_item_purchases_all"] /
        (out["f_item_purchases_all"] + out["f_user_total_purchases"] + 1.0)
    )
    out["f_pair_user_ratio"] = (
        out["f_user_item_purchases_all"] /
        (out["f_user_total_purchases"] + 1.0)
    )
    return out.reindex(X.index)
