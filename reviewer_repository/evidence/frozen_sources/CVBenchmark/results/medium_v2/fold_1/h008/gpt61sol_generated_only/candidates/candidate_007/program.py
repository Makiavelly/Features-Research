def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def map_single(series, key, fill=0.0):
        if len(series) == 0:
            return np.full(n, fill, dtype=float)
        return X[key].map(series).fillna(fill).to_numpy(dtype=float)

    def map_pair(series, category, raw_column, fill=0.0):
        if len(series) == 0:
            return np.full(n, fill, dtype=float)
        idx = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[raw_column].to_numpy()]
        )
        values = series.reindex(idx).to_numpy(dtype=float)
        return np.where(np.isfinite(values), values, fill)

    if h.empty:
        out["f_user_item_count"] = 0.0
        out["f_user_item_recency"] = np.nan
        out["f_item_count_7d"] = 0.0
        out["f_item_count_30d"] = 0.0
        out["f_item_count_90d"] = 0.0
        out["f_item_recency"] = np.nan
        out["f_user_activity_30d"] = 0.0
        out["f_user_activity_90d"] = 0.0
        out["f_user_department_count"] = 0.0
        out["f_user_product_count"] = 0.0
        out["f_user_section_count"] = 0.0
        return out

    out["f_user_item_count"] = map_pair(
        h.groupby(["customer_id", "article_id"], sort=False).size(),
        "article_id", "article_id"
    )
    out["f_user_item_recency"] = map_pair(
        h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min(),
        "article_id", "article_id", fill=np.nan
    )

    for days in (7, 30, 90):
        recent = h.loc[h["days_ago"] <= days]
        counts = recent.groupby("article_id", sort=False).size()
        out["f_item_count_%dd" % days] = map_single(counts, "article_id")

    out["f_item_recency"] = map_single(
        h.groupby("article_id", sort=False)["days_ago"].min(),
        "article_id", fill=np.nan
    )
    for days in (30, 90):
        counts = h.loc[h["days_ago"] <= days].groupby("customer_id", sort=False).size()
        out["f_user_activity_%dd" % days] = map_single(counts, "customer_id")

    for category, raw_column, name in (
        ("department_no", "raw_i_department_no", "department"),
        ("product_type_no", "raw_i_product_type_no", "product"),
        ("section_no", "raw_i_section_no", "section"),
    ):
        counts = h.groupby(["customer_id", category], sort=False).size()
        out["f_user_%s_count" % name] = map_pair(counts, category, raw_column)

    return out.replace([np.inf, -np.inf], np.nan)
