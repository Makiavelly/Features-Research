def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history

    cols = [
        "f_item_7d", "f_item_30d", "f_item_90d", "f_item_recency",
        "f_customer_7d", "f_customer_30d", "f_customer_recency",
        "f_pair_count", "f_pair_recency", "f_department_affinity",
        "f_section_affinity", "f_type_affinity", "f_department_recent",
        "f_item_total", "f_customer_total", "f_customer_item_share",
        "f_item_mean_price"
    ]
    if h.empty:
        for c in cols:
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

    keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])
    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(["size", "min"])
    out["f_pair_count"] = pair["size"].reindex(keys).fillna(0).to_numpy()
    out["f_pair_recency"] = pair["min"].reindex(keys).to_numpy()

    total_user = h.groupby("customer_id").size()
    out["f_customer_total"] = user_map(total_user)
    out["f_customer_item_share"] = (
        out["f_pair_count"] / out["f_customer_total"].replace(0, np.nan)
    )

    for col, name in (
        ("department_no", "department"),
        ("section_no", "section"),
        ("product_type_no", "type"),
    ):
        s = h.groupby(["customer_id", col]).size()
        k = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()
        ])
        out["f_" + name + "_affinity"] = s.reindex(k).fillna(0).to_numpy()

    recent = h.loc[h["days_ago"] <= 30]
    out["f_department_recent"] = X["raw_i_department_no"].map(
        recent.groupby("department_no").size()
    ).fillna(0).to_numpy()
    out["f_item_total"] = item_map(h.groupby("article_id").size())
    out["f_item_mean_price"] = item_map(h.groupby("article_id")["price"].mean())

    return out.replace([np.inf, -np.inf], np.nan)
