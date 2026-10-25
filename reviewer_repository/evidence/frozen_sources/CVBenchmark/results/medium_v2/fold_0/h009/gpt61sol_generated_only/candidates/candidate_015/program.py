def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history

    if h.empty:
        for name in (
            "f_item_count_30d", "f_item_count_90d", "f_item_decay",
            "f_item_recency", "f_customer_recency", "f_customer_count_30d",
            "f_pair_count", "f_pair_recency", "f_department_affinity",
            "f_section_affinity", "f_product_type_affinity",
            "f_department_popularity_30d", "f_item_mean_price",
        ):
            out[name] = np.nan if name.endswith(("recency", "price")) else 0.0
        return out

    def item_map(s):
        return X["article_id"].map(s).to_numpy()

    for days in (30, 90):
        cnt = h.loc[h["days_ago"] <= days].groupby("article_id").size()
        out["f_item_count_" + str(days) + "d"] = item_map(cnt)
        out["f_item_count_" + str(days) + "d"] = np.nan_to_num(
            out["f_item_count_" + str(days) + "d"], nan=0.0
        )

    decay = np.exp(-h["days_ago"].to_numpy() / 30.0)
    weighted = h.assign(_w=decay).groupby("article_id")["_w"].sum()
    out["f_item_decay"] = item_map(weighted)
    out["f_item_recency"] = item_map(h.groupby("article_id")["days_ago"].min())
    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()
    ).to_numpy()

    c30 = h.loc[h["days_ago"] <= 30].groupby("customer_id").size()
    out["f_customer_count_30d"] = X["customer_id"].map(c30).fillna(0).to_numpy()

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(["size", "min"])
    keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])
    out["f_pair_count"] = pair["size"].reindex(keys).fillna(0).to_numpy()
    out["f_pair_recency"] = pair["min"].reindex(keys).to_numpy()

    for col, label in (
        ("department_no", "department"),
        ("section_no", "section"),
        ("product_type_no", "product_type"),
    ):
        counts = h.groupby(["customer_id", col]).size()
        keys = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()
        ])
        out["f_" + label + "_affinity"] = counts.reindex(keys).fillna(0).to_numpy()

    pop = h.loc[h["days_ago"] <= 30].groupby("department_no").size()
    out["f_department_popularity_30d"] = X["raw_i_department_no"].map(pop).fillna(0).to_numpy()
    out["f_item_mean_price"] = item_map(h.groupby("article_id")["price"].mean())

    return out.replace([np.inf, -np.inf], np.nan)
