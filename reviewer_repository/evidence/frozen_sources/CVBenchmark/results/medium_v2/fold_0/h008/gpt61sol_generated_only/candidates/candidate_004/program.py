def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    if history.empty:
        for name in (
            "f_item_purchases_7d", "f_item_purchases_30d",
            "f_item_purchases_90d", "f_item_purchases_all",
            "f_user_item_purchases_all", "f_user_item_recency",
            "f_user_purchases_30d", "f_user_department_purchases",
            "f_user_product_type_purchases",
            "f_user_product_code_purchases",
        ):
            out[name] = np.full(n, np.nan) if name.endswith("recency") else np.zeros(n)
        return out

    h = history
    customer = X["customer_id"]
    article = X["article_id"]
    days = h["days_ago"]

    for window in (7, 30, 90):
        counts = h.loc[days <= window].groupby("article_id").size()
        out[f"f_item_purchases_{window}d"] = article.map(counts).fillna(0).to_numpy()

    out["f_item_purchases_all"] = article.map(h.groupby("article_id").size()).fillna(0).to_numpy()

    pairs = pd.MultiIndex.from_arrays([customer.to_numpy(), article.to_numpy()])
    pair_counts = h.groupby(["customer_id", "article_id"]).size()
    pair_recency = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    out["f_user_item_purchases_all"] = pair_counts.reindex(pairs).fillna(0).to_numpy()
    out["f_user_item_recency"] = pair_recency.reindex(pairs).to_numpy()

    recent_user_counts = h.loc[days <= 30].groupby("customer_id").size()
    out["f_user_purchases_30d"] = customer.map(recent_user_counts).fillna(0).to_numpy()

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
