def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    u = X["customer_id"]
    a = X["article_id"]

    names = [
        "f_item_7d", "f_item_30d", "f_item_90d", "f_item_recency",
        "f_customer_7d", "f_customer_30d", "f_customer_recency",
        "f_pair_count", "f_pair_7d", "f_pair_recency",
        "f_department_affinity", "f_section_affinity",
        "f_type_affinity", "f_department_30d", "f_customer_department_30d",
        "f_item_total", "f_customer_total"
    ]

    if h.empty:
        for name in names:
            out[name] = np.nan if name.endswith("recency") else 0.0
        return out

    for days in (7, 30, 90):
        s = h.loc[h["days_ago"] <= days].groupby("article_id").size()
        out["f_item_" + str(days) + "d"] = a.map(s).fillna(0).to_numpy()

    out["f_item_recency"] = a.map(
        h.groupby("article_id")["days_ago"].min()
    ).to_numpy()

    for days in (7, 30):
        s = h.loc[h["days_ago"] <= days].groupby("customer_id").size()
        out["f_customer_" + str(days) + "d"] = u.map(s).fillna(0).to_numpy()

    out["f_customer_recency"] = u.map(
        h.groupby("customer_id")["days_ago"].min()
    ).to_numpy()

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(["size", "min"])
    keys = pd.MultiIndex.from_arrays([u.to_numpy(), a.to_numpy()])
    out["f_pair_count"] = pair["size"].reindex(keys).fillna(0).to_numpy()
    out["f_pair_recency"] = pair["min"].reindex(keys).to_numpy()

    recent_pair = h.loc[h["days_ago"] <= 7].groupby(
        ["customer_id", "article_id"]
    ).size()
    out["f_pair_7d"] = recent_pair.reindex(keys).fillna(0).to_numpy()

    for col, label in (
        ("department_no", "department"),
        ("section_no", "section"),
        ("product_type_no", "type"),
    ):
        values = h.groupby(["customer_id", col]).size()
        keys2 = pd.MultiIndex.from_arrays([
            u.to_numpy(), X["raw_i_" + col].to_numpy()
        ])
        out["f_" + label + "_affinity"] = values.reindex(keys2).fillna(0).to_numpy()

    recent = h.loc[h["days_ago"] <= 30]
    out["f_department_30d"] = X["raw_i_department_no"].map(
        recent.groupby("department_no").size()
    ).fillna(0).to_numpy()

    keys2 = pd.MultiIndex.from_arrays([
        u.to_numpy(), X["raw_i_department_no"].to_numpy()
    ])
    out["f_customer_department_30d"] = recent.groupby(
        ["customer_id", "department_no"]
    ).size().reindex(keys2).fillna(0).to_numpy()

    out["f_item_total"] = a.map(h.groupby("article_id").size()).fillna(0).to_numpy()
    out["f_customer_total"] = u.map(h.groupby("customer_id").size()).fillna(0).to_numpy()

    return out.replace([np.inf, -np.inf], np.nan)
