def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def pair_values(grouped, a, b):
        d = grouped.to_dict()
        return np.fromiter(
            (d.get((x, y), 0) for x, y in zip(a.to_numpy(), b.to_numpy())),
            dtype=np.float32,
            count=n,
        )

    if len(h):
        for window in (7, 30, 90):
            g = h.loc[h["days_ago"] <= window].groupby("article_id", sort=False).size()
            out[f"f_item_count_{window}d"] = X["article_id"].map(g).fillna(0).to_numpy()

        item_total = h.groupby("article_id", sort=False).size()
        item_recent = h.loc[h["days_ago"] <= 30].groupby("article_id", sort=False).size()
        out["f_item_lifetime_count"] = X["article_id"].map(item_total).fillna(0).to_numpy()
        out["f_item_recency"] = X["article_id"].map(
            h.groupby("article_id", sort=False)["days_ago"].min()
        ).to_numpy()

        out["f_user_item_count"] = pair_values(
            h.groupby(["customer_id", "article_id"], sort=False).size(),
            X["customer_id"], X["article_id"]
        )
        out["f_user_item_recency"] = pair_values(
            h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min(),
            X["customer_id"], X["article_id"]
        )

        for attr, raw, name in (
            ("section_no", "raw_i_section_no", "section"),
            ("product_code", "raw_i_product_code", "product"),
            ("product_type_no", "raw_i_product_type_no", "type"),
            ("colour_group_code", "raw_i_colour_group_code", "colour"),
        ):
            counts = h.groupby(["customer_id", attr], sort=False).size()
            out[f"f_user_{name}_count"] = pair_values(
                counts, X["customer_id"], X[raw]
            )

        uc = h.groupby("customer_id", sort=False).size()
        out["f_customer_history_count"] = X["customer_id"].map(uc).fillna(0).to_numpy()
        out["f_customer_recency"] = X["customer_id"].map(
            h.groupby("customer_id", sort=False)["days_ago"].min()
        ).to_numpy()

        ic = X["article_id"].map(item_total).fillna(0).to_numpy()
        rc = X["article_id"].map(item_recent).fillna(0).to_numpy()
        out["f_item_recent_fraction"] = rc / (ic + 1.0)

        pmean = h.groupby("article_id", sort=False)["price"].mean()
        out["f_item_mean_price"] = X["article_id"].map(pmean).to_numpy()
    else:
        for name in (
            "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
            "f_item_lifetime_count", "f_user_item_count", "f_user_section_count",
            "f_user_product_count", "f_user_type_count", "f_user_colour_count",
            "f_customer_history_count", "f_item_recent_fraction",
        ):
            out[name] = np.zeros(n, dtype=np.float32)
        out["f_item_recency"] = np.nan
        out["f_user_item_recency"] = np.nan
        out["f_customer_recency"] = np.nan
        out["f_item_mean_price"] = np.nan

    return out.reindex(X.index)
