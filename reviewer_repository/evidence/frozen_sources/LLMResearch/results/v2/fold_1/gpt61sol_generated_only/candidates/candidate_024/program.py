import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def mp(s, x):
        return x.map(s).fillna(0).to_numpy()

    def pair(s):
        if len(s) == 0:
            return np.zeros(n)
        k = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X["article_id"].to_numpy()
        ])
        return s.reindex(k).fillna(0).to_numpy()

    names = [
        "f_customer_count", "f_item_count", "f_customer_recency",
        "f_pair_count", "f_pair_recency",
        "f_customer_count_7", "f_item_count_7", "f_pair_count_7",
        "f_customer_count_30", "f_item_count_30", "f_pair_count_30",
        "f_customer_count_90", "f_item_count_90", "f_pair_count_90",
        "f_affinity_0", "f_affinity_1", "f_affinity_2", "f_affinity_3",
        "f_affinity30_0", "f_affinity30_1", "f_affinity30_2",
        "f_affinity30_3", "f_category_pop_0", "f_category_pop_1",
        "f_category_pop_2", "f_category_pop_3", "f_customer_price",
        "f_item_price", "f_pair_rate", "f_pair_recent_rate",
        "f_item_recent_rate", "f_pair_recency_score"
    ]
    for c in names:
        out[c] = 0.0

    if len(history):
        h = history
        out["f_customer_count"] = mp(
            h.groupby("customer_id").size(), X["customer_id"])
        out["f_item_count"] = mp(
            h.groupby("article_id").size(), X["article_id"])
        out["f_customer_recency"] = mp(
            h.groupby("customer_id")["days_ago"].min(), X["customer_id"])
        out["f_pair_count"] = pair(
            h.groupby(["customer_id", "article_id"]).size())
        out["f_pair_recency"] = pair(
            h.groupby(["customer_id", "article_id"])["days_ago"].min())

        for d in (7, 30, 90):
            z = h[h["days_ago"] <= d]
            out["f_customer_count_" + str(d)] = mp(
                z.groupby("customer_id").size(), X["customer_id"])
            out["f_item_count_" + str(d)] = mp(
                z.groupby("article_id").size(), X["article_id"])
            out["f_pair_count_" + str(d)] = pair(
                z.groupby(["customer_id", "article_id"]).size())

        z30 = h[h["days_ago"] <= 30]
        for j, col in enumerate((
            "product_type_no", "section_no",
            "garment_group_no", "department_no"
        )):
            keys = pd.MultiIndex.from_arrays([
                X["customer_id"].to_numpy(),
                X["raw_i_" + col].to_numpy()
            ])
            out["f_affinity_" + str(j)] = (
                h.groupby(["customer_id", col]).size()
                .reindex(keys).fillna(0).to_numpy()
            )
            out["f_affinity30_" + str(j)] = (
                z30.groupby(["customer_id", col]).size()
                .reindex(keys).fillna(0).to_numpy()
            )
            out["f_category_pop_" + str(j)] = mp(
                h.groupby(col).size(), X["raw_i_" + col])

        out["f_customer_price"] = mp(
            h.groupby("customer_id")["price"].mean(), X["customer_id"])
        out["f_item_price"] = mp(
            h.groupby("article_id")["price"].mean(), X["article_id"])

    out["f_pair_rate"] = out["f_pair_count"] / (out["f_customer_count"] + 1)
    out["f_pair_recent_rate"] = (
        out["f_pair_count_7"] / (out["f_pair_count_30"] + 1)
    )
    out["f_item_recent_rate"] = (
        out["f_item_count_7"] / (out["f_item_count_30"] + 1)
    )
    out["f_pair_recency_score"] = (
        np.exp(-out["f_pair_recency"].clip(lower=0) / 30) *
        (out["f_pair_count"] > 0).astype(float)
    )
    return out.astype(float)
