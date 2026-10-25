def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    if h.empty:
        for name in (
            "f_item_7d", "f_item_30d", "f_item_90d", "f_item_recency",
            "f_customer_recency", "f_customer_30d", "f_customer_90d",
            "f_pair_count", "f_pair_recency", "f_dept_affinity",
            "f_section_affinity", "f_type_affinity", "f_colour_affinity",
            "f_channel1_share", "f_item_channel1_share",
            "f_customer_age", "f_customer_price_mean",
        ):
            out[name] = np.nan if name.endswith(("recency", "share", "mean", "age")) else 0.0
        return out

    def map_item(series):
        return X["article_id"].map(series).to_numpy()

    def map_customer(series):
        return X["customer_id"].map(series).to_numpy()

    for window in (7, 30, 90):
        counts = h.loc[h["days_ago"] <= window].groupby("article_id").size()
        out["f_item_" + str(window) + "d"] = map_item(counts).astype(float)
        out["f_item_" + str(window) + "d"] = np.nan_to_num(
            out["f_item_" + str(window) + "d"], nan=0.0
        )

    out["f_item_recency"] = map_item(h.groupby("article_id")["days_ago"].min())
    out["f_customer_recency"] = map_customer(h.groupby("customer_id")["days_ago"].min())

    for window in (30, 90):
        counts = h.loc[h["days_ago"] <= window].groupby("customer_id").size()
        out["f_customer_" + str(window) + "d"] = map_customer(counts)
        out["f_customer_" + str(window) + "d"] = np.nan_to_num(
            out["f_customer_" + str(window) + "d"], nan=0.0
        )

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(["size", "min"])
    pair_keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])
    out["f_pair_count"] = pair["size"].reindex(pair_keys).fillna(0).to_numpy()
    out["f_pair_recency"] = pair["min"].reindex(pair_keys).to_numpy()

    for col, label in (
        ("department_no", "dept"),
        ("section_no", "section"),
        ("product_type_no", "type"),
        ("colour_group_code", "colour"),
    ):
        counts = h.groupby(["customer_id", col]).size()
        keys = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()
        ])
        out["f_" + label + "_affinity"] = counts.reindex(keys).fillna(0).to_numpy()

    out["f_channel1_share"] = map_customer(
        h.assign(_c1=(h["sales_channel_id"] == 1).astype(float))
        .groupby("customer_id")["_c1"].mean()
    )

    channel_item = h.assign(_c1=(h["sales_channel_id"] == 1).astype(float)).groupby(
        "article_id"
    )["_c1"].mean()
    out["f_item_channel1_share"] = map_item(channel_item)

    out["f_customer_age"] = map_customer(h.groupby("customer_id")["customer_age"].mean())
    out["f_customer_price_mean"] = map_customer(h.groupby("customer_id")["price"].mean())

    return out.replace([np.inf, -np.inf], np.nan)
