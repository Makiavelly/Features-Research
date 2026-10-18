def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def map_one(series, key):
        if h.empty or series.empty:
            return np.zeros(n, dtype=float)
        return X[key].map(series).fillna(0).to_numpy(dtype=float)

    def map_pair(series, raw_col):
        if h.empty or series.empty:
            return np.zeros(n, dtype=float)
        idx = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[raw_col].to_numpy()]
        )
        vals = series.reindex(idx).to_numpy(dtype=float)
        return np.nan_to_num(vals, nan=0.0, posinf=0.0, neginf=0.0)

    if h.empty:
        for name in (
            "f_user_item_count", "f_user_item_recency", "f_item_pop_7d",
            "f_item_pop_30d", "f_item_recency", "f_user_activity_30d",
            "f_user_activity_90d", "f_user_item_popularity_ratio",
            "f_user_department_count", "f_user_product_count",
            "f_user_colour_count", "f_user_item_price_mean"
        ):
            out[name] = 0.0
        return out

    ui = h.groupby(["customer_id", "article_id"], sort=False)
    item = h.groupby("article_id", sort=False)
    user = h.groupby("customer_id", sort=False)

    ui_count = ui.size()
    ui_recency = ui["days_ago"].min()
    out["f_user_item_count"] = map_pair(ui_count, "article_id")
    rec = ui_recency.reindex(pd.MultiIndex.from_arrays(
        [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
    )).to_numpy(dtype=float)
    out["f_user_item_recency"] = np.nan_to_num(rec, nan=10000.0)

    out["f_item_pop_7d"] = map_one(h.loc[h["days_ago"] <= 7].groupby("article_id").size(), "article_id")
    out["f_item_pop_30d"] = map_one(h.loc[h["days_ago"] <= 30].groupby("article_id").size(), "article_id")
    item_rec = item["days_ago"].min()
    out["f_item_recency"] = X["article_id"].map(item_rec).fillna(10000.0).to_numpy(dtype=float)
    out["f_user_activity_30d"] = X["customer_id"].map(
        h.loc[h["days_ago"] <= 30].groupby("customer_id").size()
    ).fillna(0).to_numpy(dtype=float)
    out["f_user_activity_90d"] = X["customer_id"].map(
        h.loc[h["days_ago"] <= 90].groupby("customer_id").size()
    ).fillna(0).to_numpy(dtype=float)

    pop = item.size()
    user_n = X["customer_id"].map(user.size()).fillna(0).to_numpy(dtype=float)
    item_n = X["article_id"].map(pop).fillna(0).to_numpy(dtype=float)
    out["f_user_item_popularity_ratio"] = out["f_user_item_count"].to_numpy() / np.maximum(item_n, 1)

    for hist_col, raw_col, name in (
        ("department_no", "raw_i_department_no", "f_user_department_count"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_count"),
        ("colour_group_code", "raw_i_colour_group_code", "f_user_colour_count"),
    ):
        counts = h.groupby(["customer_id", hist_col], sort=False).size()
        out[name] = map_pair(counts, raw_col)

    price_mean = ui["price"].mean()
    vals = price_mean.reindex(pd.MultiIndex.from_arrays(
        [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
    )).to_numpy(dtype=float)
    out["f_user_item_price_mean"] = np.nan_to_num(vals, nan=0.0)

    return out.replace([np.inf, -np.inf], np.nan)
