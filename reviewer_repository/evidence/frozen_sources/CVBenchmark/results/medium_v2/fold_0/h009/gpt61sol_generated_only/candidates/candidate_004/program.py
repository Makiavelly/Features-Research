def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def mapped_count(grouped, left, right):
        lookup = grouped.to_dict()
        return np.fromiter(
            (lookup.get((a, b), 0) for a, b in zip(left.to_numpy(), right.to_numpy())),
            dtype=np.float32,
            count=n,
        )

    if len(h):
        for window in (7, 30, 90):
            counts = h.loc[h["days_ago"] <= window].groupby("article_id", sort=False).size()
            out[f"f_item_count_{window}d"] = X["article_id"].map(counts).fillna(0).to_numpy()

        item_count = h.groupby("article_id", sort=False).size()
        out["f_item_count_all"] = X["article_id"].map(item_count).fillna(0).to_numpy()
        item_recency = h.groupby("article_id", sort=False)["days_ago"].min()
        out["f_item_recency"] = X["article_id"].map(item_recency).to_numpy()

        user_item = h.groupby(["customer_id", "article_id"], sort=False).size()
        out["f_user_item_count"] = mapped_count(
            user_item, X["customer_id"], X["article_id"]
        )
        recent_pair = h.loc[h["days_ago"] <= 90].groupby(
            ["customer_id", "article_id"], sort=False
        ).size()
        out["f_user_item_count_90d"] = mapped_count(
            recent_pair, X["customer_id"], X["article_id"]
        )

        user_recency = h.groupby("customer_id", sort=False)["days_ago"].min()
        out["f_customer_recency"] = X["customer_id"].map(user_recency).to_numpy()
        user_count = h.groupby("customer_id", sort=False).size()
        out["f_customer_count"] = X["customer_id"].map(user_count).fillna(0).to_numpy()
        recent_user_count = h.loc[h["days_ago"] <= 30].groupby(
            "customer_id", sort=False
        ).size()
        out["f_customer_count_30d"] = (
            X["customer_id"].map(recent_user_count).fillna(0).to_numpy()
        )

        for attr, raw, name in (
            ("section_no", "raw_i_section_no", "section"),
            ("product_code", "raw_i_product_code", "product"),
            ("garment_group_no", "raw_i_garment_group_no", "garment"),
        ):
            counts = h.groupby(["customer_id", attr], sort=False).size()
            out[f"f_user_{name}_count"] = mapped_count(
                counts, X["customer_id"], X[raw]
            )

        recent_item = h.loc[h["days_ago"] <= 30].groupby(
            "article_id", sort=False
        ).size()
        out["f_item_recent_share"] = (
            X["article_id"].map(recent_item).fillna(0).to_numpy()
            / (X["article_id"].map(item_count).fillna(0).to_numpy() + 1.0)
        )
    else:
        for name in (
            "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
            "f_item_count_all", "f_user_item_count", "f_user_item_count_90d",
            "f_customer_count", "f_customer_count_30d",
            "f_user_section_count", "f_user_product_count",
            "f_user_garment_count",
        ):
            out[name] = np.zeros(n, dtype=np.float32)
        out["f_item_recency"] = np.full(n, np.nan)
        out["f_customer_recency"] = np.full(n, np.nan)
        out["f_item_recent_share"] = np.zeros(n, dtype=np.float32)

    return out.reindex(X.index)
