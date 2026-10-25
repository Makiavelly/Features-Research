import pandas as pd
import numpy as np


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    def map_grouped(frame, keys, value, agg="size"):
        if frame.empty:
            return pd.Series(dtype=float)
        grouped = frame.groupby(keys, sort=False)[value].agg(agg) if value else frame.groupby(keys, sort=False).size()
        return grouped

    def map_pair(grouped, left, right):
        keys = pd.MultiIndex.from_arrays([X[left].to_numpy(), X[right].to_numpy()])
        return pd.Series(keys.map(grouped), index=X.index)

    if h.empty:
        for name in (
            "f_user_count_7d", "f_item_count_7d", "f_pair_count_7d",
            "f_user_count_30d", "f_item_count_30d", "f_pair_count_30d",
            "f_user_count_180d", "f_item_count_180d", "f_pair_count_180d",
            "f_pair_recency", "f_customer_recency", "f_user_type_count",
            "f_user_department_count", "f_user_product_count",
            "f_user_colour_count", "f_user_section_count", "f_item_unique_users",
            "f_item_recent_share",
        ):
            out[name] = np.nan if name.endswith("recency") else 0.0
        return out.astype(float)

    for days, tag in ((7, "7d"), (30, "30d"), (180, "180d")):
        z = h.loc[h["days_ago"] <= days]
        for entity, key in (("user", "customer_id"), ("item", "article_id")):
            counts = z.groupby(key, sort=False).size()
            out[f"f_{entity}_count_{tag}"] = X[key].map(counts).fillna(0.0)
        counts = z.groupby(["customer_id", "article_id"], sort=False).size()
        out[f"f_pair_count_{tag}"] = map_pair(counts, "customer_id", "article_id").fillna(0.0)

    pair_rec = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
    out["f_pair_recency"] = map_pair(pair_rec, "customer_id", "article_id")
    user_rec = h.groupby("customer_id", sort=False)["days_ago"].min()
    out["f_customer_recency"] = X["customer_id"].map(user_rec)

    for col, feat in (
        ("product_type_no", "f_user_type_count"),
        ("department_no", "f_user_department_count"),
        ("product_code", "f_user_product_count"),
        ("colour_group_code", "f_user_colour_count"),
        ("section_no", "f_user_section_count"),
    ):
        counts = h.groupby(["customer_id", col], sort=False).size()
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()]
        )
        out[feat] = pd.Series(keys.map(counts), index=X.index).fillna(0.0)

    users = h.groupby("article_id", sort=False)["customer_id"].nunique()
    out["f_item_unique_users"] = X["article_id"].map(users).fillna(0.0)
    item_total = h.groupby("article_id", sort=False).size()
    item_recent = h.loc[h["days_ago"] <= 30].groupby("article_id", sort=False).size()
    total = X["article_id"].map(item_total).fillna(0.0)
    recent = X["article_id"].map(item_recent).fillna(0.0)
    out["f_item_recent_share"] = recent / (total + 1.0)

    return out.astype(float)
