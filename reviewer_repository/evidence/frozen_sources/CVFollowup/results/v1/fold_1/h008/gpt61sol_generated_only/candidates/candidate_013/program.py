def modify_features(X, history):
    import pandas as pd
    import numpy as np

    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_count_all", "f_user_count_30d", "f_user_count_all",
        "f_pair_count_all", "f_pair_recency", "f_user_type_count",
        "f_user_department_count", "f_item_mean_price", "f_user_article_affinity",
    ]
    out = pd.DataFrame(index=X.index)
    h = history

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

    pair = h.groupby(["customer_id", "article_id"]).agg(
        f_pair_count_all=("days_ago", "size"),
        f_pair_recency=("days_ago", "min"),
    )
    keys = pd.MultiIndex.from_arrays(
        [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
    )
    out["f_pair_count_all"] = pair["f_pair_count_all"].reindex(keys).fillna(0).to_numpy()
    out["f_pair_recency"] = pair["f_pair_recency"].reindex(keys).to_numpy()

    for hist_col, raw_col, name in (
        ("product_type_no", "raw_i_product_type_no", "f_user_type_count"),
        ("department_no", "raw_i_department_no", "f_user_department_count"),
    ):
        agg = h.groupby(["customer_id", hist_col]).size()
        cat_keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[raw_col].to_numpy()]
        )
        out[name] = agg.reindex(cat_keys).fillna(0).to_numpy()

    mean_price = h.groupby("article_id")["price"].mean()
    out["f_item_mean_price"] = X["article_id"].map(mean_price).to_numpy()

    user_sizes = h.groupby("customer_id").size()
    item_sizes = h.groupby("article_id").size()
    u = X["customer_id"].map(user_sizes).fillna(0).to_numpy(dtype=float)
    i = X["article_id"].map(item_sizes).fillna(0).to_numpy(dtype=float)
    out["f_user_article_affinity"] = np.log1p(out["f_pair_count_all"].to_numpy(dtype=float)) - (
        np.log1p(u) + np.log1p(i) - np.log1p(len(h))
    )

    return out[names]
