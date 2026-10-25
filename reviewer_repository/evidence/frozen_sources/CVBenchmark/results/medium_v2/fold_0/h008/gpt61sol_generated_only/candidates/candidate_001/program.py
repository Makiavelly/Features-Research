def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def history_column(name, default=np.nan):
        if name in history.columns:
            return history[name]
        return pd.Series(default, index=history.index)

    def candidate_column(name, default=np.nan):
        if name in X.columns:
            return X[name]
        return pd.Series(default, index=X.index)

    if history.empty:
        for name in (
            "f_item_purchases_7d", "f_item_purchases_30d",
            "f_item_purchases_90d", "f_item_purchases_all",
            "f_user_item_purchases_all", "f_user_item_recency",
            "f_user_purchases_30d", "f_user_department_purchases",
            "f_user_product_type_purchases",
        ):
            out[name] = np.zeros(n) if name != "f_user_item_recency" else np.full(n, np.nan)
        return out

    h = history
    days = history_column("days_ago")
    article = history_column("article_id")
    customer = history_column("customer_id")

    for window in (7, 30, 90):
        counts = h.loc[days <= window].groupby("article_id").size()
        out[f"f_item_purchases_{window}d"] = candidate_column("article_id").map(counts).fillna(0).to_numpy()

    all_item_counts = h.groupby("article_id").size()
    out["f_item_purchases_all"] = candidate_column("article_id").map(all_item_counts).fillna(0).to_numpy()

    pair_counts = h.groupby(["customer_id", "article_id"]).size()
    pair_recency = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    candidate_pairs = pd.MultiIndex.from_arrays(
        [candidate_column("customer_id").to_numpy(), candidate_column("article_id").to_numpy()]
    )
    out["f_user_item_purchases_all"] = pair_counts.reindex(candidate_pairs).fillna(0).to_numpy()
    out["f_user_item_recency"] = pair_recency.reindex(candidate_pairs).to_numpy()

    recent_users = h.loc[days <= 30].groupby("customer_id").size()
    out["f_user_purchases_30d"] = candidate_column("customer_id").map(recent_users).fillna(0).to_numpy()

    for history_name, raw_name, feature_name in (
        ("department_no", "raw_i_department_no", "f_user_department_purchases"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_type_purchases"),
    ):
        if history_name in h.columns and raw_name in X.columns:
            counts = h.groupby(["customer_id", history_name]).size()
            keys = pd.MultiIndex.from_arrays(
                [candidate_column("customer_id").to_numpy(), candidate_column(raw_name).to_numpy()]
            )
            out[feature_name] = counts.reindex(keys).fillna(0).to_numpy()
        else:
            out[feature_name] = np.zeros(n)

    return out.reindex(X.index)
