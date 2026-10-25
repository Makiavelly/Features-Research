def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history

    if h.empty:
        for name in (
            "f_item_count_30d", "f_item_count_90d", "f_item_recency",
            "f_customer_recency", "f_customer_count_30d",
            "f_pair_count", "f_pair_recency", "f_department_affinity",
            "f_section_affinity", "f_product_type_affinity",
            "f_product_code_affinity", "f_customer_department_30d",
            "f_item_popularity", "f_customer_total",
        ):
            out[name] = np.nan if name.endswith("recency") else 0.0
        return out

    def map_item(s):
        return X["article_id"].map(s).to_numpy()

    out["f_item_count_30d"] = map_item(
        h.loc[h["days_ago"] <= 30].groupby("article_id").size()
    )
    out["f_item_count_90d"] = map_item(
        h.loc[h["days_ago"] <= 90].groupby("article_id").size()
    )
    out["f_item_recency"] = map_item(h.groupby("article_id")["days_ago"].min())
    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()
    ).to_numpy()
    out["f_customer_count_30d"] = X["customer_id"].map(
        h.loc[h["days_ago"] <= 30].groupby("customer_id").size()
    ).fillna(0).to_numpy()

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
        ("product_code", "product_code"),
    ):
        counts = h.groupby(["customer_id", col]).size()
        k = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()
        ])
        out["f_" + label + "_affinity"] = counts.reindex(k).fillna(0).to_numpy()

    recent = h.loc[h["days_ago"] <= 30]
    k = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["raw_i_department_no"].to_numpy()
    ])
    out["f_customer_department_30d"] = recent.groupby(
        ["customer_id", "department_no"]
    ).size().reindex(k).fillna(0).to_numpy()

    out["f_item_popularity"] = map_item(h.groupby("article_id").size())
    out["f_customer_total"] = X["customer_id"].map(
        h.groupby("customer_id").size()
    ).fillna(0).to_numpy()

    return out.replace([np.inf, -np.inf], np.nan)
