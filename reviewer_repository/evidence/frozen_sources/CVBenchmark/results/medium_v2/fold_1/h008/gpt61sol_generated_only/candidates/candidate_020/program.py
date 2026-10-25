def modify_features(X, history):
    import pandas as pd
    import numpy as np

    names = [
        "f_user_item_count",
        "f_user_item_recency",
        "f_item_pop_7d",
        "f_item_pop_30d",
        "f_item_recency",
        "f_user_activity_7d",
        "f_user_activity_30d",
        "f_user_item_popularity_ratio",
        "f_user_department_count",
        "f_user_product_count",
        "f_user_item_price_mean",
        "f_user_department_recent",
    ]
    out = pd.DataFrame(index=X.index)
    h = history

    def one_map(s, key, default=0.0):
        if h.empty:
            return np.full(len(X), default, dtype=float)
        return X[key].map(s).fillna(default).to_numpy(dtype=float)

    def pair_map(s, key, default=0.0):
        if h.empty:
            return np.full(len(X), default, dtype=float)
        mi = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[key].to_numpy()]
        )
        v = s.reindex(mi).to_numpy(dtype=float)
        return np.nan_to_num(v, nan=default, posinf=default, neginf=default)

    if h.empty:
        for c in names:
            out[c] = 10000.0 if c in (
                "f_user_item_recency", "f_item_recency"
            ) else 0.0
        return out

    ui = h.groupby(["customer_id", "article_id"], sort=False)
    item = h.groupby("article_id", sort=False)
    user = h.groupby("customer_id", sort=False)

    ui_count = ui.size()
    ui_recency = ui["days_ago"].min()
    out["f_user_item_count"] = pair_map(ui_count, "article_id")
    out["f_user_item_recency"] = pair_map(ui_recency, "article_id", 10000.0)

    p7 = h.loc[h["days_ago"] <= 7].groupby("article_id", sort=False).size()
    p30 = h.loc[h["days_ago"] <= 30].groupby("article_id", sort=False).size()
    out["f_item_pop_7d"] = one_map(p7, "article_id")
    out["f_item_pop_30d"] = one_map(p30, "article_id")

    out["f_item_recency"] = one_map(
        item["days_ago"].min(), "article_id", 10000.0
    )
    out["f_user_activity_7d"] = one_map(
        h.loc[h["days_ago"] <= 7].groupby("customer_id", sort=False).size(),
        "customer_id"
    )
    out["f_user_activity_30d"] = one_map(
        h.loc[h["days_ago"] <= 30].groupby("customer_id", sort=False).size(),
        "customer_id"
    )

    item_total = one_map(item.size(), "article_id")
    out["f_user_item_popularity_ratio"] = (
        out["f_user_item_count"].to_numpy(dtype=float) /
        np.maximum(item_total, 1.0)
    )

    dept = h.groupby(["customer_id", "department_no"], sort=False).size()
    prod = h.groupby(["customer_id", "product_type_no"], sort=False).size()
    out["f_user_department_count"] = pair_map(dept, "raw_i_department_no")
    out["f_user_product_count"] = pair_map(prod, "raw_i_product_type_no")

    out["f_user_item_price_mean"] = pair_map(ui["price"].mean(), "article_id")

    recent_dept = h.loc[h["days_ago"] <= 30].groupby(
        ["customer_id", "department_no"], sort=False
    ).size()
    out["f_user_department_recent"] = pair_map(
        recent_dept, "raw_i_department_no"
    )

    return out.replace([np.inf, -np.inf], np.nan)
