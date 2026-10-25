def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def one_map(column, values, default=0.0):
        return X[column].map(values).fillna(default).to_numpy()

    def pair_map(values, default=0.0):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        return values.reindex(keys).fillna(default).to_numpy()

    def add_pair(name, frame, default=0.0):
        out[name] = pair_map(
            frame.groupby(["customer_id", "article_id"]).size(),
            default
        )

    d = h["days_ago"]

    for w in (7, 30, 90):
        hw = h.loc[d <= w]
        out["f_item_count_%d" % w] = one_map(
            "article_id", hw.groupby("article_id").size()
        )
        out["f_user_count_%d" % w] = one_map(
            "customer_id", hw.groupby("customer_id").size()
        )

    out["f_item_count_all"] = one_map(
        "article_id", h.groupby("article_id").size()
    )
    out["f_user_count_all"] = one_map(
        "customer_id", h.groupby("customer_id").size()
    )

    add_pair("f_pair_count_7", h.loc[d <= 7])
    add_pair("f_pair_count_30", h.loc[d <= 30])
    add_pair("f_pair_count_all", h)

    out["f_pair_recency"] = pair_map(
        h.groupby(["customer_id", "article_id"])["days_ago"].min(),
        np.nan
    )
    out["f_item_recency"] = one_map(
        "article_id", h.groupby("article_id")["days_ago"].min(), np.nan
    )
    out["f_user_recency"] = one_map(
        "customer_id", h.groupby("customer_id")["days_ago"].min(), np.nan
    )

    weighted = h.assign(_weight=np.exp(-h["days_ago"].to_numpy() / 21.0))
    out["f_item_decay"] = one_map(
        "article_id", weighted.groupby("article_id")["_weight"].sum()
    )
    out["f_user_decay"] = one_map(
        "customer_id", weighted.groupby("customer_id")["_weight"].sum()
    )
    out["f_pair_decay"] = pair_map(
        weighted.groupby(["customer_id", "article_id"])["_weight"].sum()
    )

    category_specs = (
        ("product_code", "raw_i_product_code", "product"),
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("section_no", "raw_i_section_no", "section"),
        ("department_no", "raw_i_department_no", "department"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
        ("index_group_no", "raw_i_index_group_no", "index"),
    )
    for hc, xc, name in category_specs:
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[xc].to_numpy()]
        )
        vals = h.groupby(["customer_id", hc]).size()
        out["f_user_%s_count" % name] = vals.reindex(keys).fillna(0).to_numpy()

    item_price = h.groupby("article_id")["price"].mean()
    user_price = h.groupby("customer_id")["price"].mean()
    ip = one_map("article_id", item_price, np.nan)
    up = one_map("customer_id", user_price, np.nan)
    out["f_item_mean_price"] = ip
    out["f_price_ratio_user"] = np.divide(
        ip, up, out=np.full(n, np.nan), where=np.isfinite(up) & (up != 0)
    )

    static = (
        "raw_u_age", "raw_u_fn", "raw_u_active",
        "raw_u_club_member_status", "raw_u_fashion_news_frequency",
        "raw_i_product_code", "raw_i_product_type_no",
        "raw_i_section_no", "raw_i_department_no",
        "raw_i_garment_group_no",
    )
    for col in static:
        out["f_static_" + col[4:]] = X[col].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
