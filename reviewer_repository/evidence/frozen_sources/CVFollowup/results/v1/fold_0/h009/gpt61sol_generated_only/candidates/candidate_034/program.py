def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history

    feature_names = [
        "f_item_7d", "f_item_30d", "f_item_90d", "f_item_recency",
        "f_customer_7d", "f_customer_30d", "f_customer_recency",
        "f_pair_count", "f_pair_recency", "f_department_affinity",
        "f_section_affinity", "f_type_affinity", "f_product_affinity",
        "f_customer_department_30d", "f_department_30d", "f_item_total",
        "f_customer_total", "f_item_mean_price"
    ]

    if h.empty:
        for name in feature_names:
            out[name] = np.nan if name.endswith(("recency", "price")) else 0.0
        return out

    users = X["customer_id"]
    items = X["article_id"]

    for days in (7, 30, 90):
        s = h.loc[h["days_ago"] <= days].groupby("article_id").size()
        out["f_item_" + str(days) + "d"] = items.map(s).fillna(0).to_numpy()

    out["f_item_recency"] = items.map(
        h.groupby("article_id")["days_ago"].min()
    ).to_numpy()
    out["f_customer_recency"] = users.map(
        h.groupby("customer_id")["days_ago"].min()
    ).to_numpy()

    for days in (7, 30):
        s = h.loc[h["days_ago"] <= days].groupby("customer_id").size()
        out["f_customer_" + str(days) + "d"] = users.map(s).fillna(0).to_numpy()

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(["size", "min"])
    pair_keys = pd.MultiIndex.from_arrays([
        users.to_numpy(), items.to_numpy()
    ])
    out["f_pair_count"] = pair["size"].reindex(pair_keys).fillna(0).to_numpy()
    out["f_pair_recency"] = pair["min"].reindex(pair_keys).to_numpy()

    for column, label in (
        ("department_no", "department"),
        ("section_no", "section"),
        ("product_type_no", "type"),
        ("product_code", "product"),
    ):
        values = h.groupby(["customer_id", column]).size()
        keys = pd.MultiIndex.from_arrays([
            users.to_numpy(), X["raw_i_" + column].to_numpy()
        ])
        out["f_" + label + "_affinity"] = values.reindex(keys).fillna(0).to_numpy()

    recent = h.loc[h["days_ago"] <= 30]
    out["f_customer_department_30d"] = recent.groupby(
        ["customer_id", "department_no"]
    ).size().reindex(pd.MultiIndex.from_arrays([
        users.to_numpy(), X["raw_i_department_no"].to_numpy()
    ])).fillna(0).to_numpy()

    out["f_department_30d"] = X["raw_i_department_no"].map(
        recent.groupby("department_no").size()
    ).fillna(0).to_numpy()
    out["f_item_total"] = items.map(h.groupby("article_id").size()).fillna(0).to_numpy()
    out["f_customer_total"] = users.map(h.groupby("customer_id").size()).fillna(0).to_numpy()
    out["f_item_mean_price"] = items.map(
        h.groupby("article_id")["price"].mean()
    ).to_numpy()

    return out.replace([np.inf, -np.inf], np.nan)
