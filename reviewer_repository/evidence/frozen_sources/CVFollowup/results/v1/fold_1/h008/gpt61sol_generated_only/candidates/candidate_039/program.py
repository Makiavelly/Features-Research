def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def one(s, col, default=0.0):
        if len(h) == 0 or len(s) == 0:
            return np.full(n, default, dtype=float)
        return X[col].map(s).fillna(default).to_numpy(dtype=float)

    def pair(s, col, default=0.0):
        if len(h) == 0 or len(s) == 0:
            return np.full(n, default, dtype=float)
        ix = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[col].to_numpy()]
        )
        return np.nan_to_num(
            s.reindex(ix).to_numpy(dtype=float),
            nan=default, posinf=default, neginf=default
        )

    def cat_pair(s, raw_col, default=0.0):
        if len(h) == 0 or len(s) == 0:
            return np.full(n, default, dtype=float)
        ix = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[raw_col].to_numpy()]
        )
        return np.nan_to_num(
            s.reindex(ix).to_numpy(dtype=float),
            nan=default, posinf=default, neginf=default
        )

    if len(h):
        user = h.groupby("customer_id", sort=False)
        item = h.groupby("article_id", sort=False)
        ui = h.groupby(["customer_id", "article_id"], sort=False)

        out["f_user_item_count"] = pair(ui.size(), "article_id")
        out["f_user_item_recency"] = pair(ui["days_ago"].min(), "article_id", 10000.0)
        out["f_item_count"] = one(item.size(), "article_id")
        out["f_item_recency"] = one(item["days_ago"].min(), "article_id", 10000.0)
        out["f_user_count"] = one(user.size(), "customer_id")

        for d, tag in ((3, "3d"), (7, "7d"), (14, "14d"), (30, "30d"), (90, "90d")):
            r = h.loc[h["days_ago"] <= d]
            out["f_item_pop_" + tag] = one(
                r.groupby("article_id", sort=False).size(), "article_id"
            )
            out["f_user_activity_" + tag] = one(
                r.groupby("customer_id", sort=False).size(), "customer_id"
            )

        total_item = one(item.size(), "article_id")
        total_pair = out["f_user_item_count"].to_numpy(dtype=float)
        out["f_pair_item_share"] = total_pair / np.maximum(total_item, 1.0)

        for hc, rc, name in (
            ("product_code", "raw_i_product_code", "f_user_product_code_count"),
            ("product_type_no", "raw_i_product_type_no", "f_user_type_count"),
            ("department_no", "raw_i_department_no", "f_user_department_count"),
            ("section_no", "raw_i_section_no", "f_user_section_count"),
            ("colour_group_code", "raw_i_colour_group_code", "f_user_colour_count"),
        ):
            s = h.groupby(["customer_id", hc], sort=False).size()
            out[name] = cat_pair(s, rc)

        out["f_user_price_mean"] = one(user["price"].mean(), "customer_id")
        out["f_item_price_mean"] = one(item["price"].mean(), "article_id")
        out["f_pair_price_mean"] = pair(ui["price"].mean(), "article_id")
    else:
        for name, default in (
            ("f_user_item_count", 0), ("f_user_item_recency", 10000),
            ("f_item_count", 0), ("f_item_recency", 10000),
            ("f_user_count", 0), ("f_pair_item_share", 0),
            ("f_user_price_mean", 0), ("f_item_price_mean", 0),
            ("f_pair_price_mean", 0),
        ):
            out[name] = float(default)
        for d, tag in ((3, "3d"), (7, "7d"), (14, "14d"), (30, "30d"), (90, "90d")):
            out["f_item_pop_" + tag] = 0.0
            out["f_user_activity_" + tag] = 0.0
        for name in (
            "f_user_product_code_count", "f_user_type_count",
            "f_user_department_count", "f_user_section_count",
            "f_user_colour_count"
        ):
            out[name] = 0.0

    for rc, name in (
        ("raw_u_age", "f_user_age"),
        ("raw_u_club_member_status", "f_user_club_status"),
        ("raw_u_fashion_news_frequency", "f_user_news_frequency"),
        ("raw_i_product_code", "f_item_product_code"),
        ("raw_i_product_type_no", "f_item_product_type"),
        ("raw_i_department_no", "f_item_department"),
        ("raw_i_section_no", "f_item_section"),
        ("raw_i_garment_group_no", "f_item_garment_group"),
        ("raw_i_colour_group_code", "f_item_colour"),
    ):
        out[name] = pd.to_numeric(X[rc], errors="coerce").to_numpy(dtype=float)

    return out.replace([np.inf, -np.inf], np.nan)
