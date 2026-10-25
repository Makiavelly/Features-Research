def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    if h.empty:
        for name in (
            "item_count_7d", "item_count_30d", "item_count_90d",
            "item_recency", "customer_recency", "customer_count_7d",
            "customer_count_30d", "exact_purchase_count",
            "exact_purchase_recency", "customer_department_affinity",
            "customer_section_affinity", "customer_product_type_affinity",
            "customer_product_code_affinity", "department_count_30d",
            "customer_department_recency", "customer_section_recency",
            "customer_department_count_30d", "item_mean_price",
        ):
            out["f_" + name] = np.nan if name.endswith(("recency", "price")) else 0.0
        return out

    for window in (7, 30, 90):
        counts = h.loc[h["days_ago"] <= window].groupby("article_id").size()
        out["f_item_count_" + str(window) + "d"] = X["article_id"].map(counts).fillna(0).to_numpy()

    out["f_item_recency"] = X["article_id"].map(h.groupby("article_id")["days_ago"].min()).to_numpy()
    out["f_customer_recency"] = X["customer_id"].map(h.groupby("customer_id")["days_ago"].min()).to_numpy()

    for window in (7, 30):
        counts = h.loc[h["days_ago"] <= window].groupby("customer_id").size()
        out["f_customer_count_" + str(window) + "d"] = X["customer_id"].map(counts).fillna(0).to_numpy()

    exact = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].agg(["size", "min"])
    keys = pd.MultiIndex.from_arrays([X["customer_id"].to_numpy(), X["article_id"].to_numpy()])
    out["f_exact_purchase_count"] = exact["size"].reindex(keys).fillna(0).to_numpy()
    out["f_exact_purchase_recency"] = exact["min"].reindex(keys).to_numpy()

    for col in ("department_no", "section_no", "product_type_no", "product_code"):
        grouped = h.groupby(["customer_id", col], sort=False).size()
        keys = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()
        ])
        out["f_customer_" + col.replace("_no", "") + "_affinity"] = grouped.reindex(keys).fillna(0).to_numpy()

    recent = h.loc[h["days_ago"] <= 30]
    out["f_department_count_30d"] = X["raw_i_department_no"].map(
        recent.groupby("department_no").size()
    ).fillna(0).to_numpy()

    for col in ("department_no", "section_no"):
        rec = h.groupby(["customer_id", col], sort=False)["days_ago"].min()
        keys = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()
        ])
        out["f_customer_" + col.replace("_no", "") + "_recency"] = rec.reindex(keys).to_numpy()

    dept_recent = recent.groupby(["customer_id", "department_no"], sort=False).size()
    keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["raw_i_department_no"].to_numpy()
    ])
    out["f_customer_department_count_30d"] = dept_recent.reindex(keys).fillna(0).to_numpy()

    mean_price = h.groupby("article_id")["price"].mean()
    out["f_item_mean_price"] = X["article_id"].map(mean_price).to_numpy()
    return out.replace([np.inf, -np.inf], np.nan)
