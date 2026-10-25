def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def pair_map(g, a, b, default=0.0):
        d = g.to_dict()
        return np.fromiter(
            (d.get((u, v), default) for u, v in zip(a.to_numpy(), b.to_numpy())),
            dtype=np.float32,
            count=n,
        )

    if len(h):
        for days in (7, 30, 90):
            g = h.loc[h["days_ago"] <= days].groupby("article_id", sort=False).size()
            out[f"f_item_count_{days}d"] = X["article_id"].map(g).fillna(0).to_numpy()

        items = h.groupby("article_id", sort=False)
        lifetime = items.size()
        out["f_item_lifetime_count"] = X["article_id"].map(lifetime).fillna(0).to_numpy()
        out["f_item_recency"] = X["article_id"].map(items["days_ago"].min()).to_numpy()
        out["f_item_mean_price"] = X["article_id"].map(items["price"].mean()).to_numpy()

        pair = h.groupby(["customer_id", "article_id"], sort=False)
        out["f_user_item_count"] = pair_map(
            pair.size(), X["customer_id"], X["article_id"]
        )
        out["f_user_item_recency"] = pair_map(
            pair["days_ago"].min(), X["customer_id"], X["article_id"], np.nan
        )

        for col, raw, name in (
            ("section_no", "raw_i_section_no", "section"),
            ("product_code", "raw_i_product_code", "product"),
            ("product_type_no", "raw_i_product_type_no", "type"),
            ("garment_group_no", "raw_i_garment_group_no", "garment"),
        ):
            g = h.groupby(["customer_id", col], sort=False).size()
            out[f"f_user_{name}_count"] = pair_map(g, X["customer_id"], X[raw])

        users = h.groupby("customer_id", sort=False)
        out["f_customer_history_count"] = X["customer_id"].map(users.size()).fillna(0).to_numpy()
        out["f_customer_recency"] = X["customer_id"].map(users["days_ago"].min()).to_numpy()

        recent = h.loc[h["days_ago"] <= 30].groupby("article_id", sort=False).size()
        a = X["article_id"].map(recent).fillna(0).to_numpy()
        b = X["article_id"].map(lifetime).fillna(0).to_numpy()
        out["f_item_recent_fraction"] = a / (b + 1.0)
    else:
        for name in (
            "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
            "f_item_lifetime_count", "f_user_item_count", "f_user_section_count",
            "f_user_product_count", "f_user_type_count", "f_user_garment_count",
            "f_customer_history_count", "f_item_recent_fraction",
        ):
            out[name] = np.zeros(n, dtype=np.float32)
        for name in (
            "f_item_recency", "f_item_mean_price", "f_user_item_recency",
            "f_customer_recency",
        ):
            out[name] = np.full(n, np.nan)

    return out.reindex(X.index)
