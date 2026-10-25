def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history

    if h.empty:
        for name in (
            "f_item_30d", "f_item_90d", "f_item_recency",
            "f_customer_recency", "f_customer_30d", "f_pair_count",
            "f_pair_recency", "f_department_affinity", "f_section_affinity",
            "f_type_affinity", "f_colour_affinity", "f_customer_total",
            "f_item_total", "f_department_30d",
        ):
            out[name] = np.nan if name.endswith("recency") else 0.0
        return out

    def item_map(values):
        return X["article_id"].map(values).to_numpy()

    def pair_reindex(values, col):
        keys = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()
        ])
        return values.reindex(keys)

    for w in (30, 90):
        counts = h.loc[h["days_ago"] <= w].groupby("article_id").size()
        out["f_item_" + str(w) + "d"] = item_map(counts)
        out["f_item_" + str(w) + "d"] = np.nan_to_num(
            out["f_item_" + str(w) + "d"], nan=0.0
        )

    out["f_item_recency"] = item_map(h.groupby("article_id")["days_ago"].min())
    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()
    ).to_numpy()

    c30 = h.loc[h["days_ago"] <= 30].groupby("customer_id").size()
    out["f_customer_30d"] = X["customer_id"].map(c30).fillna(0).to_numpy()

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
        out["f_" + label + "_affinity"] = pair_reindex(g, col).fillna(0).to_numpy()

    out["f_customer_total"] = X["customer_id"].map(
        h.groupby("customer_id").size()
    ).fillna(0).to_numpy()
    out["f_item_total"] = item_map(h.groupby("article_id").size())

    out["f_department_30d"] = X["raw_i_department_no"].map(
        h.loc[h["days_ago"] <= 30].groupby("department_no").size()
    ).fillna(0).to_numpy()

    return out.replace([np.inf, -np.inf], np.nan)
