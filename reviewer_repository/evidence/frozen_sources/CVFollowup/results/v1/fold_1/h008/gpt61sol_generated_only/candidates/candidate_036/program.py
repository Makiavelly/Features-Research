def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    n = len(X)

    names = (
        "f_user_item_count",
        "f_user_item_count_30d",
        "f_user_item_recency",
        "f_item_pop_7d",
        "f_item_pop_30d",
        "f_item_recency",
        "f_user_activity_7d",
        "f_user_activity_30d",
        "f_user_activity_90d",
        "f_user_department_count",
        "f_user_product_count",
        "f_user_colour_count",
    )

    if history.empty:
        for name in names:
            out[name] = 10000.0 if name.endswith("recency") else 0.0
        return out

    h = history
    customers = X["customer_id"]
    articles = X["article_id"]

    def one_key(values, key):
        return (
            X[key].map(values)
            .fillna(0.0)
            .to_numpy(dtype=float)
        )

    pair_index = pd.MultiIndex.from_arrays(
        [customers.to_numpy(), articles.to_numpy()]
    )

    def pair_values(values, fill=0.0):
        z = values.reindex(pair_index).to_numpy(dtype=float)
        return np.nan_to_num(z, nan=fill, posinf=fill, neginf=fill)

    pairs = h.groupby(["customer_id", "article_id"], sort=False)
    items = h.groupby("article_id", sort=False)
    users = h.groupby("customer_id", sort=False)

    out["f_user_item_count"] = pair_values(pairs.size())
    out["f_user_item_count_30d"] = pair_values(
        h.loc[h["days_ago"] <= 30]
        .groupby(["customer_id", "article_id"], sort=False)
        .size()
    )
    out["f_user_item_recency"] = pair_values(
        pairs["days_ago"].min(), fill=10000.0
    )

    out["f_item_pop_7d"] = one_key(
        h.loc[h["days_ago"] <= 7].groupby("article_id", sort=False).size(),
        "article_id",
    )
    out["f_item_pop_30d"] = one_key(
        h.loc[h["days_ago"] <= 30].groupby("article_id", sort=False).size(),
        "article_id",
    )
    out["f_item_recency"] = (
        articles.map(items["days_ago"].min())
        .fillna(10000.0)
        .to_numpy(dtype=float)
    )

    out["f_user_activity_7d"] = one_key(
        h.loc[h["days_ago"] <= 7].groupby("customer_id", sort=False).size(),
        "customer_id",
    )
    out["f_user_activity_30d"] = one_key(
        h.loc[h["days_ago"] <= 30].groupby("customer_id", sort=False).size(),
        "customer_id",
    )
    out["f_user_activity_90d"] = one_key(
        h.loc[h["days_ago"] <= 90].groupby("customer_id", sort=False).size(),
        "customer_id",
    )

    for hist_col, raw_col, name in (
        ("department_no", "raw_i_department_no", "f_user_department_count"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_count"),
        ("colour_group_code", "raw_i_colour_group_code", "f_user_colour_count"),
    ):
        vals = h.groupby(["customer_id", hist_col], sort=False).size()
        idx = pd.MultiIndex.from_arrays(
            [customers.to_numpy(), X[raw_col].to_numpy()]
        )
        z = vals.reindex(idx).to_numpy(dtype=float)
        out[name] = np.nan_to_num(z, nan=0.0, posinf=0.0, neginf=0.0)

    return out.replace([np.inf, -np.inf], np.nan)
