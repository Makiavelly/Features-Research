def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    if len(h):
        for window in (7, 30, 90):
            c = h.loc[h["days_ago"] <= window].groupby("article_id", sort=False).size()
            out[f"f_item_count_{window}d"] = X["article_id"].map(c).fillna(0).to_numpy()

        items = h.groupby("article_id", sort=False)
        total = items.size()
        out["f_item_lifetime_count"] = X["article_id"].map(total).fillna(0).to_numpy()
        out["f_item_recency"] = X["article_id"].map(items["days_ago"].min()).to_numpy()
        out["f_item_mean_price"] = X["article_id"].map(items["price"].mean()).to_numpy()

        def pair_counts(attribute, candidate):
            d = h.groupby(["customer_id", attribute], sort=False).size().to_dict()
            return np.fromiter(
                (d.get((u, v), 0) for u, v in
                 zip(X["customer_id"].to_numpy(), X[candidate].to_numpy())),
                dtype=np.float32, count=n
            )

        out["f_user_item_count"] = pair_counts("article_id", "article_id")
        out["f_user_section_count"] = pair_counts("section_no", "raw_i_section_no")
        out["f_user_product_count"] = pair_counts("product_code", "raw_i_product_code")
        out["f_user_type_count"] = pair_counts("product_type_no", "raw_i_product_type_no")

        users = h.groupby("customer_id", sort=False)
        out["f_customer_history_count"] = X["customer_id"].map(users.size()).fillna(0).to_numpy()
        out["f_customer_recency"] = X["customer_id"].map(users["days_ago"].min()).to_numpy()
        out["f_customer_channel_mean"] = X["customer_id"].map(
            users["sales_channel_id"].mean()
        ).to_numpy()

        recent = h.loc[h["days_ago"] <= 30].groupby("article_id", sort=False).size()
        r = X["article_id"].map(recent).fillna(0).to_numpy()
        t = X["article_id"].map(total).fillna(0).to_numpy()
        out["f_item_recent_fraction"] = r / (t + 1.0)
    else:
        for name in (
            "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
            "f_item_lifetime_count", "f_user_item_count", "f_user_section_count",
            "f_user_product_count", "f_user_type_count", "f_customer_history_count",
            "f_item_recent_fraction",
        ):
            out[name] = np.zeros(n, dtype=np.float32)
        for name in (
            "f_item_recency", "f_item_mean_price", "f_customer_recency",
            "f_customer_channel_mean",
        ):
            out[name] = np.full(n, np.nan)

    return out.reindex(X.index)
