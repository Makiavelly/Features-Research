def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def pair_lookup(grouped, left, right, key_left, key_right):
        lookup = grouped.to_dict()
        keys = zip(left.to_numpy(), right.to_numpy())
        return np.fromiter((lookup.get(k, 0) for k in keys), dtype=np.float32, count=n)

    def add_pair_count(name, hist_left, hist_right, cand_left, cand_right):
        if hist_left in h.columns and hist_right in h.columns:
            counts = h.groupby([hist_left, hist_right], sort=False).size()
            out[name] = pair_lookup(
                counts, X[cand_left], X[cand_right], hist_left, hist_right
            )

    if len(h):
        for window in (7, 30, 90):
            counts = h.loc[h["days_ago"] <= window].groupby("article_id", sort=False).size()
            out[f"f_item_count_{window}d"] = X["article_id"].map(counts).fillna(0).to_numpy()

        recency = h.groupby("article_id", sort=False)["days_ago"].min()
        out["f_item_recency"] = X["article_id"].map(recency).to_numpy()

        add_pair_count(
            "f_user_item_count", "customer_id", "article_id",
            "customer_id", "article_id"
        )

        for attr, raw, name in (
            ("section_no", "raw_i_section_no", "f_user_section_count"),
            ("product_code", "raw_i_product_code", "f_user_product_count"),
            ("garment_group_no", "raw_i_garment_group_no", "f_user_garment_count"),
        ):
            if attr in h.columns and raw in X.columns:
                counts = h.groupby(["customer_id", attr], sort=False).size()
                out[name] = pair_lookup(
                    counts, X["customer_id"], X[raw], "customer_id", attr
                )

        user_recency = h.groupby("customer_id", sort=False)["days_ago"].min()
        out["f_customer_recency"] = X["customer_id"].map(user_recency).to_numpy()

    else:
        for window in (7, 30, 90):
            out[f"f_item_count_{window}d"] = np.zeros(n, dtype=np.float32)
        out["f_item_recency"] = np.full(n, np.nan)
        out["f_user_item_count"] = np.zeros(n, dtype=np.float32)
        out["f_user_section_count"] = np.zeros(n, dtype=np.float32)
        out["f_user_product_count"] = np.zeros(n, dtype=np.float32)
        out["f_user_garment_count"] = np.zeros(n, dtype=np.float32)
        out["f_customer_recency"] = np.full(n, np.nan)

    return out.reindex(X.index)
