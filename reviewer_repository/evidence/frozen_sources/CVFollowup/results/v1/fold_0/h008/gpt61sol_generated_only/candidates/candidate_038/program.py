def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    n = len(X)
    h = history

    def mapped(keys, values, fill=0.0):
        result = keys.map(values)
        if fill is not None:
            result = result.fillna(fill)
        return result.to_numpy()

    def grouped_count(frame, key):
        if frame.empty:
            return pd.Series(dtype=float)
        return frame.groupby(key, sort=False).size()

    def grouped_min(frame, key, value):
        if frame.empty:
            return pd.Series(dtype=float)
        return frame.groupby(key, sort=False)[value].min()

    if h.empty:
        for name in (
            "f_item_purchases_7d", "f_item_purchases_30d",
            "f_item_purchases_90d", "f_item_purchases_all",
            "f_user_purchases_30d", "f_user_purchases_all",
            "f_item_recency", "f_user_recency",
            "f_user_item_purchases_all", "f_user_item_recency",
            "f_user_product_type_purchases",
        ):
            out[name] = np.full(n, np.nan) if name.endswith("recency") else np.zeros(n)
        return out

    customer = X["customer_id"]
    article = X["article_id"]
    days = h["days_ago"]

    for window in (7, 30, 90):
        counts = grouped_count(h.loc[days <= window], "article_id")
        out[f"f_item_purchases_{window}d"] = mapped(article, counts)

    item_counts = grouped_count(h, "article_id")
    out["f_item_purchases_all"] = mapped(article, item_counts)
    out["f_item_recency"] = mapped(article, grouped_min(h, "article_id", "days_ago"), None)

    user_counts = grouped_count(h, "customer_id")
    out["f_user_purchases_all"] = mapped(customer, user_counts)
    recent_users = grouped_count(h.loc[days <= 30], "customer_id")
    out["f_user_purchases_30d"] = mapped(customer, recent_users)
    out["f_user_recency"] = mapped(customer, grouped_min(h, "customer_id", "days_ago"), None)

    pair_counts = h.groupby(["customer_id", "article_id"], sort=False).size()
    pair_recency = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
    keys = pd.MultiIndex.from_arrays(
        [customer.to_numpy(), article.to_numpy()],
        names=["customer_id", "article_id"],
    )
    out["f_user_item_purchases_all"] = pair_counts.reindex(keys).fillna(0).to_numpy()
    out["f_user_item_recency"] = pair_recency.reindex(keys).to_numpy()

    type_counts = h.groupby(["customer_id", "product_type_no"], sort=False).size()
    type_keys = pd.MultiIndex.from_arrays(
        [customer.to_numpy(), X["raw_i_product_type_no"].to_numpy()],
        names=["customer_id", "product_type_no"],
    )
    out["f_user_product_type_purchases"] = type_counts.reindex(type_keys).fillna(0).to_numpy()

    return out.reindex(X.index)
