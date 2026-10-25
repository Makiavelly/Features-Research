def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def map_one(col, values, default=0.0):
        return X[col].map(values).fillna(default).to_numpy()

    def map_pair(values, default=0.0):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        return values.reindex(keys).fillna(default).to_numpy()

    def map_user_category(hist_col, x_col):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[x_col].to_numpy()]
        )
        values = h.groupby(["customer_id", hist_col]).size()
        return values.reindex(keys).fillna(0).to_numpy()

    days = h["days_ago"]
    windows = {}
    for window in (7, 30, 90):
        hw = h.loc[days <= window]
        windows[window] = hw
        out["f_item_pop_%dd" % window] = map_one(
            "article_id", hw.groupby("article_id").size()
        )
        out["f_user_activity_%dd" % window] = map_one(
            "customer_id", hw.groupby("customer_id").size()
        )

    out["f_user_activity_all"] = map_one(
        "customer_id", h.groupby("customer_id").size()
    )
    weighted = h.assign(_weight=np.exp(-days.to_numpy() / 21.0))
    out["f_item_pop_decay"] = map_one(
        "article_id", weighted.groupby("article_id")["_weight"].sum()
    )

    out["f_pair_count"] = map_pair(
        h.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_count_30d"] = map_pair(
        windows[30].groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_recency"] = map_pair(
        h.groupby(["customer_id", "article_id"])["days_ago"].min(), np.nan
    )
    out["f_customer_recency"] = map_one(
        "customer_id", h.groupby("customer_id")["days_ago"].min(), np.nan
    )
    out["f_item_recency"] = map_one(
        "article_id", h.groupby("article_id")["days_ago"].min(), np.nan
    )

    for hist_col, x_col, name in (
        ("product_code", "raw_i_product_code", "product"),
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("section_no", "raw_i_section_no", "section"),
        ("department_no", "raw_i_department_no", "department"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
        ("colour_group_code", "raw_i_colour_group_code", "colour"),
    ):
        affinity = map_user_category(hist_col, x_col)
        out["f_user_" + name] = affinity
        out["f_user_" + name + "_share"] = np.divide(
            affinity,
            out["f_user_activity_all"].to_numpy(),
            out=np.zeros(n, dtype=float),
            where=out["f_user_activity_all"].to_numpy() > 0,
        )

    item_price = h.groupby("article_id")["price"].mean()
    user_price = h.groupby("customer_id")["price"].mean()
    ip = map_one("article_id", item_price, np.nan)
    up = map_one("customer_id", user_price, np.nan)
    out["f_item_mean_price"] = ip
    out["f_price_vs_user"] = np.divide(
        ip,
        up,
        out=np.full(n, np.nan),
        where=np.isfinite(up) & (up != 0),
    )

    out["f_static_age"] = X["raw_u_age"].to_numpy()
    out["f_static_active"] = X["raw_u_active"].to_numpy()
    out["f_static_product_type_no"] = X["raw_i_product_type_no"].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
