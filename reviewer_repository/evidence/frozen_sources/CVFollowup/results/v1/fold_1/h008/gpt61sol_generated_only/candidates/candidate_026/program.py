def modify_features(X, history):
    import pandas as pd
    import numpy as np

    names = [
        "f_user_item_count", "f_user_item_recency", "f_item_pop_7d",
        "f_item_pop_30d", "f_item_pop_90d", "f_item_pop_all",
        "f_item_recency", "f_user_activity_7d", "f_user_activity_30d",
        "f_user_activity_90d", "f_user_department_count",
        "f_user_product_count", "f_user_section_count",
        "f_user_colour_count", "f_user_item_popularity_ratio",
        "f_user_mean_price", "f_item_mean_price", "f_user_item_price_mean"
    ]
    out = pd.DataFrame(index=X.index)
    n = len(X)

    for name in names:
        out[name] = 0.0

    if history is None or len(history) == 0 or n == 0:
        out["f_user_item_recency"] = 10000.0
        out["f_item_recency"] = 10000.0
        return out

    h = history
    users = X["customer_id"]
    articles = X["article_id"]
    pair_index = pd.MultiIndex.from_arrays(
        [users.to_numpy(), articles.to_numpy()]
    )

    def item_map(s, default=0.0):
        return articles.map(s).fillna(default).to_numpy(dtype=float)

    def user_map(s, default=0.0):
        return users.map(s).fillna(default).to_numpy(dtype=float)

    def pair_map(s, default=0.0):
        v = s.reindex(pair_index).to_numpy(dtype=float)
        return np.nan_to_num(v, nan=default, posinf=default, neginf=default)

    ui = h.groupby(["customer_id", "article_id"], sort=False)
    item = h.groupby("article_id", sort=False)
    user = h.groupby("customer_id", sort=False)

    ui_count = ui.size()
    out["f_user_item_count"] = pair_map(ui_count)
    out["f_user_item_recency"] = pair_map(ui["days_ago"].min(), 10000.0)
    out["f_item_recency"] = item_map(item["days_ago"].min(), 10000.0)

    for days, name in (
        (7, "f_item_pop_7d"),
        (30, "f_item_pop_30d"),
        (90, "f_item_pop_90d"),
    ):
        out[name] = item_map(
            h.loc[h["days_ago"] <= days].groupby("article_id").size()
        )

    out["f_item_pop_all"] = item_map(item.size())

    for days, name in (
        (7, "f_user_activity_7d"),
        (30, "f_user_activity_30d"),
        (90, "f_user_activity_90d"),
    ):
        out[name] = user_map(
            h.loc[h["days_ago"] <= days].groupby("customer_id").size()
        )

    for hist_col, raw_col, name in (
        ("department_no", "raw_i_department_no", "f_user_department_count"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_count"),
        ("section_no", "raw_i_section_no", "f_user_section_count"),
        ("colour_group_code", "raw_i_colour_group_code", "f_user_colour_count"),
    ):
        s = h.groupby(["customer_id", hist_col], sort=False).size()
        idx = pd.MultiIndex.from_arrays([
            users.to_numpy(), X[raw_col].to_numpy()
        ])
        v = s.reindex(idx).to_numpy(dtype=float)
        out[name] = np.nan_to_num(v, nan=0.0, posinf=0.0, neginf=0.0)

    item_counts = item.size()
    pair_counts = out["f_user_item_count"].to_numpy(dtype=float)
    global_counts = item_map(item_counts)
    out["f_user_item_popularity_ratio"] = (
        pair_counts / np.maximum(global_counts, 1.0)
    )

    out["f_user_mean_price"] = user_map(user["price"].mean())
    out["f_item_mean_price"] = item_map(item["price"].mean())
    out["f_user_item_price_mean"] = pair_map(ui["price"].mean())

    return out.replace([np.inf, -np.inf], np.nan)
