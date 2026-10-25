def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def mapped(series, key, fill=0.0):
        if h.empty:
            return np.full(n, fill, dtype=float)
        return X[key].map(series).fillna(fill).to_numpy(dtype=float)

    def pair_mapped(series, key):
        if h.empty:
            return np.zeros(n, dtype=float)
        idx = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[key].to_numpy()]
        )
        return np.nan_to_num(
            series.reindex(idx).to_numpy(dtype=float),
            nan=0.0, posinf=0.0, neginf=0.0
        )

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

    ui_count = ui.size()
    out["f_user_item_count"] = pair_mapped(ui_count, "article_id")
    out["f_user_item_recency"] = pair_mapped(ui["days_ago"].min(), "article_id")
    out["f_item_pop_7d"] = mapped(
        h.loc[h["days_ago"] <= 7].groupby("article_id").size(), "article_id"
    )
    out["f_item_pop_30d"] = mapped(
        h.loc[h["days_ago"] <= 30].groupby("article_id").size(), "article_id"
    )
    out["f_item_recency"] = mapped(item["days_ago"].min(), "article_id", 10000.0)
    out["f_user_activity_30d"] = mapped(
        h.loc[h["days_ago"] <= 30].groupby("customer_id").size(), "customer_id"
    )
    out["f_user_activity_90d"] = mapped(
        h.loc[h["days_ago"] <= 90].groupby("customer_id").size(), "customer_id"
    )

    item_n = mapped(item.size(), "article_id")
    out["f_user_item_popularity_ratio"] = (
        out["f_user_item_count"].to_numpy() / np.maximum(item_n, 1.0)
    )

    for hist_col, raw_col, name in (
        ("department_no", "raw_i_department_no", "f_user_department_count"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_count"),
        ("colour_group_code", "raw_i_colour_group_code", "f_user_colour_count"),
    ):
        out[name] = pair_mapped(
            h.groupby(["customer_id", hist_col], sort=False).size(), raw_col
        )

    out["f_user_item_price_mean"] = pair_mapped(ui["price"].mean(), "article_id")
    return out.replace([np.inf, -np.inf], np.nan)
