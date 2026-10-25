def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    recent = h.loc[h["days_ago"] <= 30]
    older = h.loc[h["days_ago"] <= 90]

    def mapped(column, mapping, default=np.nan):
        return X[column].map(mapping).to_numpy()

    def safe_ratio(a, b):
        a = np.asarray(a, dtype=float)
        b = np.asarray(b, dtype=float)
        return np.divide(a, b, out=np.full(a.shape, np.nan), where=(b != 0))

    item30 = recent.groupby("article_id").size()
    item90 = older.groupby("article_id").size()
    user30 = recent.groupby("customer_id").size()
    user90 = older.groupby("customer_id").size()
    user_all = h.groupby("customer_id").size()
    item_all = h.groupby("article_id").size()

    out["f_item_popularity_30d"] = mapped("article_id", item30, 0)
    out["f_item_popularity_90d"] = mapped("article_id", item90, 0)
    out["f_item_popularity_all"] = mapped("article_id", item_all, 0)
    out["f_user_activity_30d"] = mapped("customer_id", user30, 0)
    out["f_user_activity_90d"] = mapped("customer_id", user90, 0)
    out["f_user_activity_all"] = mapped("customer_id", user_all, 0)

    last_item = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    pairs = pd.MultiIndex.from_arrays([X["customer_id"].to_numpy(), X["article_id"].to_numpy()])
    out["f_user_item_recency"] = last_item.reindex(pairs).to_numpy()

    pair30 = recent.groupby(["customer_id", "article_id"]).size()
    out["f_user_item_count_30d"] = pair30.reindex(pairs, fill_value=0).to_numpy()

    cust_recency = h.groupby("customer_id")["days_ago"].min()
    out["f_customer_recency"] = mapped("customer_id", cust_recency)

    item_price = h.groupby("article_id")["price"].mean()
    user_price = h.groupby("customer_id")["price"].mean()
    candidate_price = mapped("article_id", item_price)
    typical_price = mapped("customer_id", user_price)
    out["f_item_mean_price"] = candidate_price
    out["f_user_price_affinity"] = safe_ratio(candidate_price, typical_price)

    category_cols = [
        ("product_code", "raw_i_product_code"),
        ("product_type_no", "raw_i_product_type_no"),
        ("department_no", "raw_i_department_no"),
    ]
    for hist_col, x_col in category_cols:
        counts = h.groupby(hist_col).size()
        out["f_category_pop_" + hist_col] = X[x_col].map(counts).to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
