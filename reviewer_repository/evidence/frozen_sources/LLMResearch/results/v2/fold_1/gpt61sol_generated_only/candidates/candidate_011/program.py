import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def one(s, k):
        return k.map(s).fillna(0).to_numpy()

    def pair(s):
        if len(s) == 0:
            return np.zeros(n)
        k = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X["article_id"].to_numpy()
        ])
        return s.reindex(k).fillna(0).to_numpy()

    if len(history):
        h = history
        out["f_customer_count"] = one(
            h.groupby("customer_id").size(), X["customer_id"])
        out["f_item_count"] = one(
            h.groupby("article_id").size(), X["article_id"])
        out["f_customer_recency"] = one(
            h.groupby("customer_id")["days_ago"].min(), X["customer_id"])
        out["f_pair_count"] = pair(
            h.groupby(["customer_id", "article_id"]).size())
        out["f_pair_recency"] = pair(
            h.groupby(["customer_id", "article_id"])["days_ago"].min())

        for d in (7, 30, 90):
            z = h[h["days_ago"] <= d]
            out["f_customer_count_" + str(d)] = one(
                z.groupby("customer_id").size(), X["customer_id"])
            out["f_item_count_" + str(d)] = one(
                z.groupby("article_id").size(), X["article_id"])

        for j, col in enumerate(("product_type_no", "section_no",
                                 "garment_group_no")):
            k = pd.MultiIndex.from_arrays([
                X["customer_id"].to_numpy(),
                X["raw_i_" + col].to_numpy()
            ])
            out["f_affinity_" + str(j)] = (
                h.groupby(["customer_id", col]).size()
                .reindex(k).fillna(0).to_numpy()
            )
            out["f_category_pop_" + str(j)] = one(
                h.groupby(col).size(), X["raw_i_" + col])

        out["f_customer_price"] = one(
            h.groupby("customer_id")["price"].mean(), X["customer_id"])
        out["f_item_price"] = one(
            h.groupby("article_id")["price"].mean(), X["article_id"])
    else:
        cols = [
            "f_customer_count", "f_item_count", "f_customer_recency",
            "f_pair_count", "f_pair_recency",
            "f_customer_count_7", "f_item_count_7",
            "f_customer_count_30", "f_item_count_30",
            "f_customer_count_90", "f_item_count_90",
            "f_affinity_0", "f_category_pop_0",
            "f_affinity_1", "f_category_pop_1",
            "f_affinity_2", "f_category_pop_2",
            "f_customer_price", "f_item_price"
        ]
        for c in cols:
            out[c] = 0.0

    out["f_pair_rate"] = out["f_pair_count"] / (out["f_customer_count"] + 1.0)
    out["f_item_recent_rate"] = (
        out["f_item_count_7"] / (out["f_item_count_30"] + 1.0)
    )
    out["f_customer_recent_rate"] = (
        out["f_customer_count_7"] / (out["f_customer_count_30"] + 1.0)
    )
    out["f_recency_score"] = np.exp(
        -out["f_pair_recency"].clip(lower=0) / 30.0
    ) * (out["f_pair_count"] > 0).astype(float)

    return out.astype(float)
