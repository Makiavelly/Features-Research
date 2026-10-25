def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def pair_map(grouped, a, b):
        d = grouped.to_dict()
        return np.fromiter(
            (d.get((u, v), 0) for u, v in zip(a.to_numpy(), b.to_numpy())),
            dtype=np.float32,
            count=n,
        )

    if len(h):
        for days in (7, 30, 90):
            counts = h.loc[h["days_ago"] <= days].groupby("article_id", sort=False).size()
            out[f"f_item_count_{days}d"] = X["article_id"].map(counts).fillna(0).to_numpy()

        items = h.groupby("article_id", sort=False)
        total = items.size()
        out["f_item_lifetime_count"] = X["article_id"].map(total).fillna(0).to_numpy()
        out["f_item_recency"] = X["article_id"].map(items["days_ago"].min()).to_numpy()

        pairs = h.groupby(["customer_id", "article_id"], sort=False)
        out["f_user_item_count"] = pair_map(pairs.size(), X["customer_id"], X["article_id"])
        out["f_user_item_recency"] = pair_map(
            pairs["days_ago"].min(), X["customer_id"], X["article_id"]
        )

        for attr, raw, label in (
            ("section_no", "raw_i_section_no", "section"),
            ("product_code", "raw_i_product_code", "product"),
            ("product_type_no", "raw_i_product_type_no", "type"),
        ):
            counts = h.groupby(["customer_id", attr], sort=False).size()
            out[f"f_user_{label}_count"] = pair_map(
                counts, X["customer_id"], X[raw]
            )

        users = h.groupby("customer_id", sort=False)
        out["f_customer_history_count"] = X["customer_id"].map(users.size()).fillna(0).to_numpy()
        out["f_customer_recency"] = X["customer_id"].map(
            users["days_ago"].min()
        ).to_numpy()

        recent_count = X["article_id"].map(
            h.loc[h["days_ago"] <= 30].groupby("article_id", sort=False).size()
        ).fillna(0).to_numpy()
        all_count = X["article_id"].map(total).fillna(0).to_numpy()
        out["f_item_recent_share"] = recent_count / (all_count + 1.0)

        price = items["price"].mean()
        out["f_item_mean_price"] = X["article_id"].map(price).to_numpy()

        channel = h.groupby(["customer_id", "article_id"], sort=False)["sales_channel_id"].mean()
        out["f_user_item_channel"] = pair_map(
            channel, X["customer_id"], X["article_id"]
        )
    else:
        zero_names = (
            "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
            "f_item_lifetime_count", "f_user_item_count", "f_user_section_count",
            "f_user_product_count", "f_user_type_count", "f_customer_history_count",
            "f_item_recent_share",
        )
        for name in zero_names:
            out[name] = np.zeros(n, dtype=np.float32)
        for name in (
            "f_item_recency", "f_user_item_recency", "f_customer_recency",
            "f_item_mean_price", "f_user_item_channel",
        ):
            out[name] = np.full(n, np.nan)

    return out.reindex(X.index)
