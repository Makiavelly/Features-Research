def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    names = [
        "f_user_item_count", "f_user_item_recency", "f_user_item_7d",
        "f_user_item_30d", "f_item_pop_7d", "f_item_pop_30d",
        "f_item_recency", "f_user_activity_7d", "f_user_activity_30d",
        "f_user_activity_90d", "f_user_department_count",
        "f_user_department_30d", "f_user_product_count",
        "f_user_colour_count", "f_user_item_popularity_ratio"
    ]
    for name in names:
        out[name] = 0.0
    if history.empty or len(X) == 0:
        out["f_user_item_recency"] = 10000.0
        out["f_item_recency"] = 10000.0
        return out

    h = history
    n = len(X)
    users = X["customer_id"]
    items = X["article_id"]
    pair_index = pd.MultiIndex.from_arrays(
        [users.to_numpy(), items.to_numpy()]
    )

    def one(values, key):
        return X[key].map(values).fillna(0).to_numpy(dtype=float)

    def pair(values, raw_key):
        idx = pd.MultiIndex.from_arrays(
            [users.to_numpy(), X[raw_key].to_numpy()]
        )
        return np.nan_to_num(
            values.reindex(idx).to_numpy(dtype=float),
            nan=0.0, posinf=0.0, neginf=0.0
        )

    ui = h.groupby(["customer_id", "article_id"], sort=False)
    item = h.groupby("article_id", sort=False)
    user = h.groupby("customer_id", sort=False)

    ui_count = ui.size()
    out["f_user_item_count"] = np.nan_to_num(
        ui_count.reindex(pair_index).to_numpy(dtype=float), nan=0.0
    )
    out["f_user_item_recency"] = np.nan_to_num(
        ui["days_ago"].min().reindex(pair_index).to_numpy(dtype=float),
        nan=10000.0
    )

    for limit, name in ((7, "f_user_item_7d"), (30, "f_user_item_30d")):
        hh = h.loc[h["days_ago"] <= limit]
        vals = hh.groupby(["customer_id", "article_id"], sort=False).size()
        out[name] = np.nan_to_num(
            vals.reindex(pair_index).to_numpy(dtype=float), nan=0.0
        )

    for limit, name in ((7, "f_item_pop_7d"), (30, "f_item_pop_30d")):
        hh = h.loc[h["days_ago"] <= limit]
        out[name] = one(hh.groupby("article_id", sort=False).size(), "article_id")

    out["f_item_recency"] = one(item["days_ago"].min(), "article_id")
    out["f_item_recency"] = np.where(
        out["f_item_recency"].to_numpy() == 0,
        out["f_item_recency"].to_numpy(),
        out["f_item_recency"].to_numpy()
    )
    missing_item = ~items.isin(item.size().index)
    out.loc[missing_item.to_numpy(), "f_item_recency"] = 10000.0

    for limit, name in (
        (7, "f_user_activity_7d"),
        (30, "f_user_activity_30d"),
        (90, "f_user_activity_90d"),
    ):
        hh = h.loc[h["days_ago"] <= limit]
        out[name] = one(hh.groupby("customer_id", sort=False).size(), "customer_id")

    for hist_col, raw_col, name in (
        ("department_no", "raw_i_department_no", "f_user_department_count"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_count"),
        ("colour_group_code", "raw_i_colour_group_code", "f_user_colour_count"),
    ):
        vals = h.groupby(["customer_id", hist_col], sort=False).size()
        out[name] = pair(vals, raw_col)

    recent = h.loc[h["days_ago"] <= 30]
    dept_recent = recent.groupby(
        ["customer_id", "department_no"], sort=False
    ).size()
    out["f_user_department_30d"] = pair(
        dept_recent, "raw_i_department_no"
    )

    item_counts = one(item.size(), "article_id")
    out["f_user_item_popularity_ratio"] = (
        out["f_user_item_count"].to_numpy(dtype=float) /
        np.maximum(item_counts, 1.0)
    )

    return out.replace([np.inf, -np.inf], np.nan)
