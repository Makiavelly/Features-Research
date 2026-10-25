def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def mapped(col, values, default=0.0):
        return X[col].map(values).fillna(default).to_numpy()

    pair_keys = pd.MultiIndex.from_arrays(
        [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
    )

    def pair_mapped(values, default=0.0):
        return values.reindex(pair_keys).fillna(default).to_numpy()

    for w in (7, 30, 90):
        hw = h.loc[h["days_ago"] <= w]
        out["f_item_count_%d" % w] = mapped(
            "article_id", hw.groupby("article_id").size()
        )
        out["f_user_count_%d" % w] = mapped(
            "customer_id", hw.groupby("customer_id").size()
        )

    out["f_item_count_all"] = mapped(
        "article_id", h.groupby("article_id").size()
    )
    out["f_user_count_all"] = mapped(
        "customer_id", h.groupby("customer_id").size()
    )
    out["f_pair_count"] = pair_mapped(
        h.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_count_30d"] = pair_mapped(
        h.loc[h["days_ago"] <= 30].groupby(
            ["customer_id", "article_id"]
        ).size()
    )
    out["f_pair_recency"] = pair_mapped(
        h.groupby(["customer_id", "article_id"])["days_ago"].min(),
        np.nan
    )
    out["f_item_recency"] = mapped(
        "article_id", h.groupby("article_id")["days_ago"].min(), np.nan
    )
    out["f_user_recency"] = mapped(
        "customer_id", h.groupby("customer_id")["days_ago"].min(), np.nan
    )

    if len(h):
        hh = h.copy()
        hh["_decay7"] = np.exp(-hh["days_ago"].to_numpy(dtype=float) / 7.0)
        hh["_decay30"] = np.exp(-hh["days_ago"].to_numpy(dtype=float) / 30.0)
        out["f_item_decay7"] = mapped(
            "article_id", hh.groupby("article_id")["_decay7"].sum()
        )
        out["f_user_decay7"] = mapped(
            "customer_id", hh.groupby("customer_id")["_decay7"].sum()
        )
        out["f_pair_decay30"] = pair_mapped(
            hh.groupby(["customer_id", "article_id"])["_decay30"].sum()
        )
    else:
        out["f_item_decay7"] = 0.0
        out["f_user_decay7"] = 0.0
        out["f_pair_decay30"] = 0.0

    specs = (
        ("product_code", "raw_i_product_code", "product"),
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
        ("section_no", "raw_i_section_no", "section"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
    )
    for hc, xc, name in specs:
        out["f_user_" + name] = pair_mapped(
            h.groupby(["customer_id", hc]).size()
        )
        out["f_item_" + name] = mapped(
            xc, h.groupby(hc).size()
        )

    item_price = mapped(
        "article_id", h.groupby("article_id")["price"].mean(), np.nan
    ).astype(float)
    user_price = mapped(
        "customer_id", h.groupby("customer_id")["price"].mean(), np.nan
    ).astype(float)
    out["f_item_mean_price"] = item_price
    out["f_price_vs_user"] = np.divide(
        item_price,
        user_price,
        out=np.full(n, np.nan),
        where=np.isfinite(user_price) & (user_price != 0)
    )

    for col in (
        "raw_u_age",
        "raw_u_active",
        "raw_u_club_member_status",
        "raw_u_fashion_news_frequency",
        "raw_i_product_type_no",
        "raw_i_department_no",
        "raw_i_section_no",
        "raw_i_garment_group_no",
    ):
        out["f_static_" + col[4:]] = X[col].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
