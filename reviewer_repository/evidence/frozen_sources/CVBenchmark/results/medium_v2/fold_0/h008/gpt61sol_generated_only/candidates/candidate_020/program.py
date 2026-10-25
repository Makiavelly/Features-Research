def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def mapped(col, values, default=0):
        return X[col].map(values).fillna(default).to_numpy()

    def pair_values(values, default=0):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        return values.reindex(keys).fillna(default).to_numpy()

    if len(h) == 0:
        hdays = np.array([], dtype=float)
    else:
        hdays = h["days_ago"].to_numpy(dtype=float)

    for window in (7, 30, 90):
        hw = h.loc[h["days_ago"] <= window]
        out["f_item_count_%d" % window] = mapped(
            "article_id", hw.groupby("article_id").size()
        )
        out["f_user_count_%d" % window] = mapped(
            "customer_id", hw.groupby("customer_id").size()
        )

    out["f_item_count_all"] = mapped("article_id", h.groupby("article_id").size())
    out["f_user_count_all"] = mapped("customer_id", h.groupby("customer_id").size())
    out["f_pair_count"] = pair_values(
        h.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_count_30d"] = pair_values(
        h.loc[h["days_ago"] <= 30].groupby(["customer_id", "article_id"]).size()
    )

    out["f_pair_recency"] = pair_values(
        h.groupby(["customer_id", "article_id"])["days_ago"].min(), np.nan
    )
    out["f_item_recency"] = mapped(
        "article_id", h.groupby("article_id")["days_ago"].min(), np.nan
    )
    out["f_user_recency"] = mapped(
        "customer_id", h.groupby("customer_id")["days_ago"].min(), np.nan
    )

    if len(h):
        w7 = np.exp(-h["days_ago"].to_numpy(dtype=float) / 7.0)
        w30 = np.exp(-h["days_ago"].to_numpy(dtype=float) / 30.0)
        hw = h.copy()
        hw["_w7"] = w7
        hw["_w30"] = w30
        out["f_item_decay7"] = mapped(
            "article_id", hw.groupby("article_id")["_w7"].sum()
        )
        out["f_user_decay7"] = mapped(
            "customer_id", hw.groupby("customer_id")["_w7"].sum()
        )
        out["f_pair_decay30"] = pair_values(
            hw.groupby(["customer_id", "article_id"])["_w30"].sum()
        )
    else:
        out["f_item_decay7"] = 0.0
        out["f_user_decay7"] = 0.0
        out["f_pair_decay30"] = 0.0

    category_specs = (
        ("product_code", "raw_i_product_code", "product"),
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
        ("section_no", "raw_i_section_no", "section"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
        ("colour_group_code", "raw_i_colour_group_code", "colour"),
    )

    for hc, xc, name in category_specs:
        out["f_user_" + name] = pair_values(
            h.groupby(["customer_id", hc]).size()
        )
        out["f_item_" + name] = mapped(xc, h.groupby(hc).size())

    user_total = h.groupby("customer_id").size()
    for hc, xc, name in category_specs[:5]:
        a = out["f_user_" + name].to_numpy(dtype=float)
        b = mapped("customer_id", user_total, np.nan).astype(float)
        out["f_user_" + name + "_share"] = np.divide(
            a, b, out=np.full(n, np.nan), where=np.isfinite(b) & (b != 0)
        )

    item_price = h.groupby("article_id")["price"].mean()
    user_price = h.groupby("customer_id")["price"].mean()
    ip = mapped("article_id", item_price, np.nan).astype(float)
    up = mapped("customer_id", user_price, np.nan).astype(float)
    out["f_item_mean_price"] = ip
    out["f_price_vs_user"] = np.divide(
        ip, up, out=np.full(n, np.nan), where=np.isfinite(up) & (up != 0)
    )

    for col in (
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
        out["f_static_" + col[4:]] = X[col].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
