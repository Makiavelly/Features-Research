def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history

    names = (
        "f_item_count_30d",
        "f_item_count_90d",
        "f_item_recency",
        "f_customer_recency",
        "f_customer_count_30d",
        "f_customer_count_90d",
        "f_pair_count",
        "f_pair_recency",
        "f_department_affinity",
        "f_section_affinity",
        "f_product_type_affinity",
        "f_product_code_affinity",
        "f_customer_department_recency",
        "f_item_mean_price",
    )
    if h.empty:
        for name in names:
            out[name] = np.nan if name.endswith(("recency", "price")) else 0.0
        return out

    for window in (30, 90):
        counts = h.loc[h["days_ago"] <= window].groupby("article_id").size()
        vals = X["article_id"].map(counts).fillna(0).to_numpy()
        out["f_item_count_" + str(window) + "d"] = vals

    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()
    ).to_numpy()
    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()
    ).to_numpy()

    for window in (30, 90):
        counts = h.loc[h["days_ago"] <= window].groupby("customer_id").size()
        out["f_customer_count_" + str(window) + "d"] = (
            X["customer_id"].map(counts).fillna(0).to_numpy()
        )

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(["size", "min"])
    pair_keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])
    out["f_pair_count"] = pair["size"].reindex(pair_keys).fillna(0).to_numpy()
    out["f_pair_recency"] = pair["min"].reindex(pair_keys).to_numpy()

    for col, label in (
        ("department_no", "department"),
        ("section_no", "section"),
        ("product_type_no", "product_type"),
        ("product_code", "product_code"),
    ):
        counts = h.groupby(["customer_id", col]).size()
        keys = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()
        ])
        out["f_" + label + "_affinity"] = counts.reindex(keys).fillna(0).to_numpy()

    rec = h.groupby(["customer_id", "department_no"])["days_ago"].min()
    keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["raw_i_department_no"].to_numpy()
    ])
    out["f_customer_department_recency"] = rec.reindex(keys).to_numpy()

    out["f_item_mean_price"] = X["article_id"].map(
        h.groupby("article_id")["price"].mean()
    ).to_numpy()

    return out.replace([np.inf, -np.inf], np.nan)
