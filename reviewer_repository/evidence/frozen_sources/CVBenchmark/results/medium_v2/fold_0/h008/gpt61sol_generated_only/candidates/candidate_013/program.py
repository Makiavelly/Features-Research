def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    n = len(X)

    def mapped(series, index):
        return index.map(series).fillna(0).to_numpy()

    if history.empty:
        for name in (
            "f_item_purchases_7d", "f_item_purchases_30d",
            "f_item_purchases_90d", "f_item_purchases_all",
            "f_item_recency", "f_item_mean_price",
            "f_user_item_purchases_all", "f_user_item_recency",
            "f_user_purchases_30d", "f_user_department_purchases",
            "f_user_product_type_purchases", "f_user_product_code_purchases",
        ):
            out[name] = np.full(n, np.nan) if "recency" in name or "price" in name else np.zeros(n)
        return out

    h = history
    customer = X["customer_id"]
    article = X["article_id"]
    days = h["days_ago"]

    for window in (7, 30, 90):
        counts = h.loc[days <= window].groupby("article_id").size()
        out[f"f_item_purchases_{window}d"] = mapped(counts, article)

    item = h.groupby("article_id")
    out["f_item_purchases_all"] = mapped(item.size(), article)
    out["f_item_recency"] = article.map(item["days_ago"].min()).to_numpy()
    out["f_item_mean_price"] = article.map(item["price"].mean()).to_numpy()

    pairs = pd.MultiIndex.from_arrays([customer.to_numpy(), article.to_numpy()])
    pair = h.groupby(["customer_id", "article_id"])
    out["f_user_item_purchases_all"] = pair.size().reindex(pairs).fillna(0).to_numpy()
    out["f_user_item_recency"] = pair["days_ago"].min().reindex(pairs).to_numpy()

    recent = h.loc[days <= 30].groupby("customer_id").size()
    out["f_user_purchases_30d"] = mapped(recent, customer)

    for history_col, raw_col, feature in (
        ("department_no", "raw_i_department_no", "f_user_department_purchases"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_type_purchases"),
        ("product_code", "raw_i_product_code", "f_user_product_code_purchases"),
    ):
        if history_col in h.columns and raw_col in X.columns:
            counts = h.groupby(["customer_id", history_col]).size()
            keys = pd.MultiIndex.from_arrays(
                [customer.to_numpy(), X[raw_col].to_numpy()]
            )
            out[feature] = counts.reindex(keys).fillna(0).to_numpy()
        else:
            out[feature] = np.zeros(n)

    return out.reindex(X.index)
