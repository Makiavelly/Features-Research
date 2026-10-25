def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def pairs(g, a, b, default=0.0):
        d = g.to_dict()
        return np.fromiter(
            (d.get((u, v), default) for u, v in zip(a.to_numpy(), b.to_numpy())),
            dtype=np.float32, count=n
        )

    cols = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_lifetime_count", "f_item_recency", "f_item_recency_score",
        "f_user_item_count", "f_user_item_recency", "f_user_history_count",
        "f_user_recency", "f_user_section_count", "f_user_product_count",
        "f_item_mean_price"
    ]

    if len(h):
        for d in (7, 30, 90):
            g = h.loc[h["days_ago"] <= d].groupby("article_id", sort=False).size()
            out[f"f_item_count_{d}d"] = X["article_id"].map(g).fillna(0).to_numpy()

        items = h.groupby("article_id", sort=False)
        total = items.size()
        rec = items["days_ago"].min()
        out["f_item_lifetime_count"] = X["article_id"].map(total).fillna(0).to_numpy()
        out["f_item_recency"] = X["article_id"].map(rec).to_numpy()
        out["f_item_recency_score"] = np.exp(
            -X["article_id"].map(rec).fillna(999.0).to_numpy() / 30.0
        ).astype(np.float32)
        out["f_item_mean_price"] = X["article_id"].map(items["price"].mean()).to_numpy()

        pi = h.groupby(["customer_id", "article_id"], sort=False)
        out["f_user_item_count"] = pairs(
            pi.size(), X["customer_id"], X["article_id"]
        )
        out["f_user_item_recency"] = pairs(
            pi["days_ago"].min(), X["customer_id"], X["article_id"], np.nan
        )

        users = h.groupby("customer_id", sort=False)
        out["f_user_history_count"] = X["customer_id"].map(
            users.size()
        ).fillna(0).to_numpy()
        out["f_user_recency"] = X["customer_id"].map(
            users["days_ago"].min()
        ).to_numpy()

        for col, raw, name in (
            ("section_no", "raw_i_section_no", "section"),
            ("product_code", "raw_i_product_code", "product"),
        ):
            g = h.groupby(["customer_id", col], sort=False).size()
            out[f"f_user_{name}_count"] = pairs(
                g, X["customer_id"], X[raw]
            )
    else:
        for c in cols:
            out[c] = np.zeros(n, dtype=np.float32)
        for c in (
            "f_item_recency", "f_user_item_recency", "f_item_mean_price"
        ):
            out[c] = np.full(n, np.nan)

    return out.reindex(X.index)
