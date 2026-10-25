def modify_features(X, history):
    import numpy as np
    import pandas as pd

    out = pd.DataFrame(index=X.index)
    n = len(X)

    def mapped(keys, values):
        return keys.map(values).fillna(0).to_numpy()

    def pair_values(grouped, customer, article, fill=0):
        keys = pd.MultiIndex.from_arrays(
            [customer.to_numpy(), article.to_numpy()]
        )
        return grouped.reindex(keys).fillna(fill).to_numpy()

    customer = X["customer_id"]
    article = X["article_id"]

    if history.empty:
        for name in (
            "f_item_purchases_7d", "f_item_purchases_30d",
            "f_item_purchases_90d", "f_item_purchases_all",
            "f_item_recency", "f_item_mean_price",
            "f_user_item_purchases_all", "f_user_item_recency",
            "f_user_purchases_30d", "f_user_department_purchases",
            "f_user_product_type_purchases", "f_user_product_code_purchases",
        ):
            out[name] = np.full(n, np.nan) if name.endswith(("recency", "price")) else np.zeros(n)
        return out

    h = history
    days = h["days_ago"]

    for window in (7, 30, 90):
        counts = h.loc[days <= window].groupby("article_id").size()
        out[f"f_item_purchases_{window}d"] = mapped(article, counts)

    items = h.groupby("article_id")
    out["f_item_purchases_all"] = mapped(article, items.size())
    out["f_item_recency"] = article.map(items["days_ago"].min()).to_numpy()
    out["f_item_mean_price"] = article.map(items["price"].mean()).to_numpy()

    pairs = h.groupby(["customer_id", "article_id"])
    out["f_user_item_purchases_all"] = pair_values(
        pairs.size(), customer, article
    )
    out["f_user_item_recency"] = pair_values(
        pairs["days_ago"].min(), customer, article, fill=np.nan
    )

    user_recent = h.loc[days <= 30].groupby("customer_id").size()
    out["f_user_purchases_30d"] = mapped(customer, user_recent)

    for history_col, raw_col, feature in (
        ("department_no", "raw_i_department_no", "f_user_department_purchases"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_type_purchases"),
        ("product_code", "raw_i_product_code", "f_user_product_code_purchases"),
    ):
        if history_col in h.columns and raw_col in X.columns:
            grouped = h.groupby(["customer_id", history_col]).size()
            keys = pd.MultiIndex.from_arrays(
                [customer.to_numpy(), X[raw_col].to_numpy()]
            )
            out[feature] = grouped.reindex(keys).fillna(0).to_numpy()
        else:
            out[feature] = np.zeros(n)

    return out.reindex(X.index)
