def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    n = len(X)
    names = [
        "f_item_purchases_7d", "f_item_purchases_30d",
        "f_item_purchases_90d", "f_item_purchases_all",
        "f_item_recency", "f_user_item_purchases_all",
        "f_user_item_purchases_30d", "f_user_item_recency",
        "f_user_purchases_30d", "f_user_purchases_90d",
        "f_user_department_purchases_90d",
        "f_user_product_type_purchases_90d",
    ]

    if history.empty:
        for name in names:
            out[name] = np.full(n, np.nan) if "recency" in name else np.zeros(n)
        return out

    h = history
    customer = X["customer_id"]
    article = X["article_id"]
    days = h["days_ago"]

    def article_counts(frame):
        return frame.groupby("article_id").size()

    for window in (7, 30, 90):
        counts = article_counts(h.loc[days <= window])
        out[f"f_item_purchases_{window}d"] = (
            article.map(counts).fillna(0).to_numpy()
        )

    all_item = h.groupby("article_id").size()
    out["f_item_purchases_all"] = article.map(all_item).fillna(0).to_numpy()

    item_recency = h.groupby("article_id")["days_ago"].min()
    out["f_item_recency"] = article.map(item_recency).to_numpy()

    pair_keys = pd.MultiIndex.from_arrays(
        [customer.to_numpy(), article.to_numpy()]
    )
    pair_all = h.groupby(["customer_id", "article_id"]).size()
    out["f_user_item_purchases_all"] = (
        pair_all.reindex(pair_keys).fillna(0).to_numpy()
    )

    pair_recent = h.loc[days <= 30].groupby(
        ["customer_id", "article_id"]
    ).size()
    out["f_user_item_purchases_30d"] = (
        pair_recent.reindex(pair_keys).fillna(0).to_numpy()
    )

    pair_recency = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    out["f_user_item_recency"] = pair_recency.reindex(pair_keys).to_numpy()

    for window in (30, 90):
        user_counts = h.loc[days <= window].groupby("customer_id").size()
        out[f"f_user_purchases_{window}d"] = (
            customer.map(user_counts).fillna(0).to_numpy()
        )

    recent = h.loc[days <= 90]
    for hcol, xcol, name in (
        ("department_no", "raw_i_department_no",
         "f_user_department_purchases_90d"),
        ("product_type_no", "raw_i_product_type_no",
         "f_user_product_type_purchases_90d"),
    ):
        counts = recent.groupby(["customer_id", hcol]).size()
        keys = pd.MultiIndex.from_arrays(
            [customer.to_numpy(), X[xcol].to_numpy()]
        )
        out[name] = counts.reindex(keys).fillna(0).to_numpy()

    return out.reindex(X.index)
