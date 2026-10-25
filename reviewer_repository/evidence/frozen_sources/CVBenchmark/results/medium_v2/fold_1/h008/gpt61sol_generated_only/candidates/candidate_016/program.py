def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history

    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_count_all", "f_user_count_30d", "f_user_count_all",
        "f_pair_count_all", "f_pair_recency",
        "f_user_type_count", "f_user_department_count",
        "f_item_mean_price", "f_user_type_count_30d",
    ]
    if h is None or len(h) == 0:
        for name in names:
            out[name] = np.nan if name in ("f_pair_recency", "f_item_mean_price") else 0.0
        return out[names]

    days = pd.to_numeric(h["days_ago"], errors="coerce")
    for window in (7, 30, 90):
        counts = h.loc[days <= window].groupby("article_id").size()
        out["f_item_count_%dd" % window] = X["article_id"].map(counts).fillna(0).to_numpy()

    item_all = h.groupby("article_id").size()
    out["f_item_count_all"] = X["article_id"].map(item_all).fillna(0).to_numpy()

    for window, name in ((30, "f_user_count_30d"), (None, "f_user_count_all")):
        hh = h if window is None else h.loc[days <= window]
        counts = hh.groupby("customer_id").size()
        out[name] = X["customer_id"].map(counts).fillna(0).to_numpy()

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(
        ["size", "min"]
    )
    keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])
    out["f_pair_count_all"] = pair["size"].reindex(keys).fillna(0).to_numpy()
    out["f_pair_recency"] = pair["min"].reindex(keys).to_numpy()

    for hist_col, raw_col, name in (
        ("product_type_no", "raw_i_product_type_no", "f_user_type_count"),
        ("department_no", "raw_i_department_no", "f_user_department_count"),
    ):
        counts = h.groupby(["customer_id", hist_col]).size()
        cat_keys = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X[raw_col].to_numpy()
        ])
        out[name] = counts.reindex(cat_keys).fillna(0).to_numpy()

    recent = h.loc[days <= 30]
    counts30 = recent.groupby(["customer_id", "product_type_no"]).size()
    type_keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["raw_i_product_type_no"].to_numpy()
    ])
    out["f_user_type_count_30d"] = counts30.reindex(type_keys).fillna(0).to_numpy()

    mean_price = h.groupby("article_id")["price"].mean()
    out["f_item_mean_price"] = X["article_id"].map(mean_price).to_numpy()

    return out[names]
