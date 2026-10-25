def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history

    names = [
        "f_item_7d", "f_item_30d", "f_item_90d", "f_item_recency",
        "f_item_decay", "f_customer_7d", "f_customer_30d",
        "f_customer_recency", "f_pair_count", "f_pair_recency",
        "f_department_affinity", "f_section_affinity",
        "f_type_affinity", "f_colour_affinity", "f_department_recent",
        "f_customer_department_recent", "f_item_total", "f_customer_total",
        "f_item_price"
    ]
    if h.empty:
        for c in names:
            out[c] = np.nan if c.endswith(("recency", "price")) else 0.0
        return out

    def item_map(s):
        return X["article_id"].map(s).to_numpy()

    def user_map(s):
        return X["customer_id"].map(s).to_numpy()

    for w in (7, 30, 90):
        s = h.loc[h["days_ago"] <= w].groupby("article_id").size()
        out["f_item_" + str(w) + "d"] = item_map(s)
        out["f_item_" + str(w) + "d"] = np.nan_to_num(
            out["f_item_" + str(w) + "d"], nan=0.0
        )

    weighted = h.assign(
        _weight=np.exp(-h["days_ago"].to_numpy(dtype=float) / 21.0)
    ).groupby("article_id")["_weight"].sum()
    out["f_item_decay"] = item_map(weighted)
    out["f_item_recency"] = item_map(h.groupby("article_id")["days_ago"].min())

    for w in (7, 30):
        s = h.loc[h["days_ago"] <= w].groupby("customer_id").size()
        out["f_customer_" + str(w) + "d"] = user_map(s)
        out["f_customer_" + str(w) + "d"] = np.nan_to_num(
            out["f_customer_" + str(w) + "d"], nan=0.0
        )
    out["f_customer_recency"] = user_map(
        h.groupby("customer_id")["days_ago"].min()
    )

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(["size", "min"])
    pk = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])
    out["f_pair_count"] = pair["size"].reindex(pk).fillna(0).to_numpy()
    out["f_pair_recency"] = pair["min"].reindex(pk).to_numpy()

    for col, label in (
        ("department_no", "department"),
        ("section_no", "section"),
        ("product_type_no", "type"),
        ("colour_group_code", "colour"),
    ):
        g = h.groupby(["customer_id", col]).size()
        k = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()
        ])
        out["f_" + label + "_affinity"] = g.reindex(k).fillna(0).to_numpy()

    recent = h.loc[h["days_ago"] <= 30]
    out["f_department_recent"] = X["raw_i_department_no"].map(
        recent.groupby("department_no").size()
    ).fillna(0).to_numpy()

    k = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["raw_i_department_no"].to_numpy()
    ])
    out["f_customer_department_recent"] = recent.groupby(
        ["customer_id", "department_no"]
    ).size().reindex(k).fillna(0).to_numpy()

    out["f_item_total"] = item_map(h.groupby("article_id").size())
    out["f_customer_total"] = user_map(h.groupby("customer_id").size())
    out["f_item_price"] = item_map(h.groupby("article_id")["price"].mean())

    return out.replace([np.inf, -np.inf], np.nan)
