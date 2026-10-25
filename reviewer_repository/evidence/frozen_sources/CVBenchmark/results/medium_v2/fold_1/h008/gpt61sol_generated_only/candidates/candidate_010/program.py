def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_count_all", "f_user_count_30d", "f_user_count_all",
        "f_pair_count_all", "f_pair_recency", "f_user_type_count",
        "f_user_department_count", "f_item_mean_price",
    ]

    if history is None or len(history) == 0:
        for name in names:
            out[name] = np.nan if name == "f_pair_recency" or name == "f_item_mean_price" else 0.0
        return out[names]

    h = history
    days = pd.to_numeric(h["days_ago"], errors="coerce")

    for window in (7, 30, 90):
        counts = h.loc[days <= window].groupby("article_id").size()
        out["f_item_count_%dd" % window] = X["article_id"].map(counts).fillna(0).to_numpy()

    out["f_item_count_all"] = X["article_id"].map(h.groupby("article_id").size()).fillna(0).to_numpy()

    user_counts_30 = h.loc[days <= 30].groupby("customer_id").size()
    out["f_user_count_30d"] = X["customer_id"].map(user_counts_30).fillna(0).to_numpy()
    out["f_user_count_all"] = X["customer_id"].map(h.groupby("customer_id").size()).fillna(0).to_numpy()

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(["size", "min"])
    keys = pd.MultiIndex.from_arrays(
        [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
    )
    out["f_pair_count_all"] = pair["size"].reindex(keys).fillna(0).to_numpy()
    out["f_pair_recency"] = pair["min"].reindex(keys).to_numpy()

    for hist_col, raw_col, name in (
        ("product_type_no", "raw_i_product_type_no", "f_user_type_count"),
        ("department_no", "raw_i_department_no", "f_user_department_count"),
    ):
        counts = h.groupby(["customer_id", hist_col]).size()
        cat_keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[raw_col].to_numpy()]
        )
        out[name] = counts.reindex(cat_keys).fillna(0).to_numpy()

    mean_price = h.groupby("article_id")["price"].mean()
    out["f_item_mean_price"] = X["article_id"].map(mean_price).to_numpy()

    return out[names]
