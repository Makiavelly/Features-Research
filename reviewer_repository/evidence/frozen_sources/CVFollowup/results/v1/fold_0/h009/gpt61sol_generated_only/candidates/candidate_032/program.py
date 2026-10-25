def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def lookup_pair(g, a, b, default=0.0):
        d = g.to_dict()
        return np.fromiter(
            (d.get((u, v), default) for u, v in zip(a.to_numpy(), b.to_numpy())),
            dtype=np.float32, count=n
        )

    if len(h):
        for days in (7, 30, 90):
            g = h.loc[h["days_ago"] <= days].groupby("article_id", sort=False).size()
            out[f"f_item_count_{days}d"] = X["article_id"].map(g).fillna(0).to_numpy()

        item = h.groupby("article_id", sort=False)
        total = item.size()
        out["f_item_total"] = X["article_id"].map(total).fillna(0).to_numpy()
        out["f_item_recency"] = X["article_id"].map(item["days_ago"].min()).to_numpy()
        out["f_item_price"] = X["article_id"].map(item["price"].mean()).to_numpy()

        pair = h.groupby(["customer_id", "article_id"], sort=False)
        out["f_user_item_count"] = lookup_pair(
            pair.size(), X["customer_id"], X["article_id"]
        )
        out["f_user_item_recency"] = lookup_pair(
            pair["days_ago"].min(), X["customer_id"], X["article_id"], np.nan
        )

        for col, raw, name in (
            ("section_no", "raw_i_section_no", "section"),
            ("product_code", "raw_i_product_code", "product"),
            ("product_type_no", "raw_i_product_type_no", "type"),
        ):
            g = h.groupby(["customer_id", col], sort=False).size()
            out[f"f_user_{name}"] = lookup_pair(g, X["customer_id"], X[raw])

        user = h.groupby("customer_id", sort=False)
        out["f_user_total"] = X["customer_id"].map(user.size()).fillna(0).to_numpy()
        out["f_user_recency"] = X["customer_id"].map(user["days_ago"].min()).to_numpy()
        out["f_user_channel"] = X["customer_id"].map(
            user["sales_channel_id"].mean()
        ).to_numpy()
    else:
        for name in (
            "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
            "f_item_total", "f_user_item_count", "f_user_section",
            "f_user_product", "f_user_type", "f_user_total",
        ):
            out[name] = np.zeros(n, dtype=np.float32)
        for name in (
            "f_item_recency", "f_item_price", "f_user_item_recency",
            "f_user_recency", "f_user_channel",
        ):
            out[name] = np.full(n, np.nan)

    return out.reindex(X.index)
