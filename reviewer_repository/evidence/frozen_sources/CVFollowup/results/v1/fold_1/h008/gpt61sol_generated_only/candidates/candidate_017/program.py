def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    names = [
        "f_user_item_count",
        "f_user_item_recency",
        "f_item_pop_7d",
        "f_item_pop_30d",
        "f_item_pop_180d",
        "f_item_recency",
        "f_user_activity_7d",
        "f_user_activity_30d",
        "f_user_activity_180d",
        "f_user_department_count",
        "f_user_product_type_count",
        "f_user_section_count",
    ]

    h = history
    n = len(X)

    if h is None or len(h) == 0:
        for c in names:
            out[c] = np.zeros(n, dtype=float)
        out["f_user_item_recency"] = np.full(n, 10000.0, dtype=float)
        out["f_item_recency"] = np.full(n, 10000.0, dtype=float)
        return out

    def one_map(s, key, default=0.0):
        v = X[key].map(s)
        return v.fillna(default).to_numpy(dtype=float)

    def pair_map(s, key, default=0.0):
        idx = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X[key].to_numpy()
        ])
        v = s.reindex(idx).to_numpy(dtype=float)
        if default != 0.0:
            v = np.where(np.isnan(v), default, v)
        else:
            v = np.nan_to_num(v, nan=0.0, posinf=0.0, neginf=0.0)
        return v

    ui = h.groupby(["customer_id", "article_id"], sort=False)
    item = h.groupby("article_id", sort=False)

    out["f_user_item_count"] = pair_map(ui.size(), "article_id")
    out["f_user_item_recency"] = pair_map(ui["days_ago"].min(), "article_id", 10000.0)

    for window, name in (
        (7, "f_item_pop_7d"),
        (30, "f_item_pop_30d"),
        (180, "f_item_pop_180d"),
    ):
        q = h.loc[h["days_ago"] <= window]
        out[name] = one_map(q.groupby("article_id", sort=False).size(), "article_id")

    out["f_item_recency"] = one_map(item["days_ago"].min(), "article_id", 10000.0)

    for window, name in (
        (7, "f_user_activity_7d"),
        (30, "f_user_activity_30d"),
        (180, "f_user_activity_180d"),
    ):
        q = h.loc[h["days_ago"] <= window]
        out[name] = one_map(q.groupby("customer_id", sort=False).size(), "customer_id")

    for hist_col, raw_col, name in (
        ("department_no", "raw_i_department_no", "f_user_department_count"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_type_count"),
        ("section_no", "raw_i_section_no", "f_user_section_count"),
    ):
        s = h.groupby(["customer_id", hist_col], sort=False).size()
        out[name] = pair_map(s, raw_col)

    return out.replace([np.inf, -np.inf], np.nan)
