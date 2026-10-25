def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    n = len(X)
    h = history

    def mapped(series, mapping, fill=0):
        return series.map(mapping).fillna(fill).to_numpy()

    def group_count(keys, values):
        return values.groupby(keys, sort=False).size()

    if h.empty:
        for name in (
            "f_item_purchases_7d", "f_item_purchases_30d",
            "f_item_purchases_90d", "f_item_purchases_all",
            "f_item_recency", "f_item_mean_price",
            "f_user_item_purchases_all", "f_user_item_recency",
            "f_user_purchases_30d", "f_user_purchases_90d",
            "f_user_department_purchases", "f_user_product_type_purchases",
        ):
            out[name] = np.nan if name.endswith(("recency", "price")) else 0.0
        return out

    customer = X["customer_id"]
    article = X["article_id"]
    days = h["days_ago"]

    for window in (7, 30, 90):
        counts = h.loc[days <= window].groupby("article_id", sort=False).size()
        out[f"f_item_purchases_{window}d"] = mapped(article, counts)

    item = h.groupby("article_id", sort=False)
    out["f_item_purchases_all"] = mapped(article, item.size())
    out["f_item_recency"] = mapped(article, item["days_ago"].min(), np.nan)
    out["f_item_mean_price"] = mapped(article, item["price"].mean(), np.nan)

    pair_index = pd.MultiIndex.from_arrays([customer.to_numpy(), article.to_numpy()])
    pair = h.groupby(["customer_id", "article_id"], sort=False)
    out["f_user_item_purchases_all"] = pair.size().reindex(pair_index).fillna(0).to_numpy()
    out["f_user_item_recency"] = pair["days_ago"].min().reindex(pair_index).to_numpy()

    for window in (30, 90):
        user_counts = h.loc[days <= window].groupby("customer_id", sort=False).size()
        out[f"f_user_purchases_{window}d"] = mapped(customer, user_counts)

    for hist_col, raw_col, name in (
        ("department_no", "raw_i_department_no", "f_user_department_purchases"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_type_purchases"),
    ):
        if hist_col in h.columns and raw_col in X.columns:
            counts = h.groupby(["customer_id", hist_col], sort=False).size()
            keys = pd.MultiIndex.from_arrays([customer.to_numpy(), X[raw_col].to_numpy()])
            out[name] = counts.reindex(keys).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    return out.reindex(X.index)
