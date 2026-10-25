def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    if len(h):
        for window in (7, 30, 90):
            counts = h.loc[h["days_ago"] <= window].groupby("article_id", sort=False).size()
            out[f"f_item_count_{window}d"] = X["article_id"].map(counts).fillna(0).to_numpy()

        item = h.groupby("article_id", sort=False)
        item_total = item.size()
        out["f_item_lifetime_count"] = X["article_id"].map(item_total).fillna(0).to_numpy()
        out["f_item_recency"] = X["article_id"].map(item["days_ago"].min()).to_numpy()
        out["f_item_mean_price"] = X["article_id"].map(item["price"].mean()).to_numpy()

        user_item = h.groupby(["customer_id", "article_id"], sort=False).size().to_dict()
        out["f_user_item_count"] = np.fromiter(
            (user_item.get((u, a), 0) for u, a in zip(X["customer_id"].to_numpy(), X["article_id"].to_numpy())),
            dtype=np.float32, count=n
        )

        for column, raw, label in (
            ("section_no", "raw_i_section_no", "section"),
            ("product_code", "raw_i_product_code", "product"),
            ("product_type_no", "raw_i_product_type_no", "type"),
        ):
            lookup = h.groupby(["customer_id", column], sort=False).size().to_dict()
            out[f"f_user_{label}_count"] = np.fromiter(
                (lookup.get((u, v), 0) for u, v in zip(X["customer_id"].to_numpy(), X[raw].to_numpy())),
                dtype=np.float32, count=n
            )

        users = h.groupby("customer_id", sort=False)
        out["f_customer_history_count"] = X["customer_id"].map(users.size()).fillna(0).to_numpy()
        out["f_customer_recency"] = X["customer_id"].map(users["days_ago"].min()).to_numpy()

        channel = h.groupby("customer_id", sort=False)["sales_channel_id"].mean()
        out["f_customer_channel_mean"] = X["customer_id"].map(channel).to_numpy()

        ages = h.groupby("customer_id", sort=False)["customer_age"].median()
        out["f_customer_age_history"] = X["customer_id"].map(ages).to_numpy()
    else:
        for name in (
            "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
            "f_item_lifetime_count", "f_user_item_count", "f_user_section_count",
            "f_user_product_count", "f_user_type_count", "f_customer_history_count",
        ):
            out[name] = np.zeros(n, dtype=np.float32)
        for name in (
            "f_item_recency", "f_item_mean_price", "f_customer_recency",
            "f_customer_channel_mean", "f_customer_age_history",
        ):
            out[name] = np.full(n, np.nan)

    return out.reindex(X.index)
