def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def pair_map(g, left, right, missing=0.0):
        d = g.to_dict()
        return np.fromiter(
            (d.get((a, b), missing) for a, b in zip(left.to_numpy(), right.to_numpy())),
            dtype=np.float32, count=n
        )

    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_lifetime_count", "f_item_recency", "f_user_item_count",
        "f_user_item_recency", "f_user_section_count", "f_user_product_count",
        "f_user_type_count", "f_customer_history_count", "f_customer_recency",
        "f_item_recent_fraction", "f_item_mean_price"
    ]

    if len(h):
        for days in (7, 30, 90):
            g = h.loc[h["days_ago"] <= days].groupby("article_id", sort=False).size()
            out[f"f_item_count_{days}d"] = X["article_id"].map(g).fillna(0).to_numpy()

        items = h.groupby("article_id", sort=False)
        lifetime = items.size()
        total = X["article_id"].map(lifetime).fillna(0).to_numpy()
        out["f_item_lifetime_count"] = total
        out["f_item_recency"] = X["article_id"].map(
            items["days_ago"].min()
        ).to_numpy()
        out["f_item_mean_price"] = X["article_id"].map(
            items["price"].mean()
        ).to_numpy()

        pairs = h.groupby(["customer_id", "article_id"], sort=False)
        out["f_user_item_count"] = pair_map(
            pairs.size(), X["customer_id"], X["article_id"]
        )
        out["f_user_item_recency"] = pair_map(
            pairs["days_ago"].min(), X["customer_id"], X["article_id"], np.nan
        )

        for column, raw, label in (
            ("section_no", "raw_i_section_no", "section"),
            ("product_code", "raw_i_product_code", "product"),
            ("product_type_no", "raw_i_product_type_no", "type"),
        ):
            grouped = h.groupby(["customer_id", column], sort=False).size()
            out[f"f_user_{label}_count"] = pair_map(
                grouped, X["customer_id"], X[raw]
            )

        users = h.groupby("customer_id", sort=False)
        out["f_customer_history_count"] = X["customer_id"].map(
            users.size()
        ).fillna(0).to_numpy()
        out["f_customer_recency"] = X["customer_id"].map(
            users["days_ago"].min()
        ).to_numpy()

        recent = h.loc[h["days_ago"] <= 30].groupby(
            "article_id", sort=False
        ).size()
        out["f_item_recent_fraction"] = (
            X["article_id"].map(recent).fillna(0).to_numpy() / (total + 1.0)
        )
    else:
        for name in names:
            out[name] = np.zeros(n, dtype=np.float32)
        out["f_item_recency"] = np.full(n, np.nan)
        out["f_user_item_recency"] = np.full(n, np.nan)
        out["f_item_mean_price"] = np.full(n, np.nan)

    return out.reindex(X.index)
