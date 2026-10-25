import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def mapped(s, key):
        return key.map(s).fillna(0).to_numpy()

    def pair_values(s):
        if len(s) == 0:
            return np.zeros(n)
        keys = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X["article_id"].to_numpy()
        ])
        return s.reindex(keys).fillna(0).to_numpy()

    names = [
        "f_customer_count", "f_item_count", "f_customer_recency",
        "f_pair_count", "f_pair_recency"
    ]
    for d in (7, 30, 90):
        names.extend([
            "f_customer_count_" + str(d),
            "f_item_count_" + str(d),
            "f_pair_count_" + str(d)
        ])
    for j in range(4):
        names.extend([
            "f_affinity_" + str(j),
            "f_affinity30_" + str(j),
            "f_category_pop_" + str(j)
        ])
    names.extend([
        "f_customer_price", "f_item_price",
        "f_pair_rate", "f_pair_recent_rate",
        "f_item_recent_rate", "f_pair_recency_score"
    ])

    if len(history):
        h = history
        out["f_customer_count"] = mapped(
            h.groupby("customer_id").size(), X["customer_id"])
        out["f_item_count"] = mapped(
            h.groupby("article_id").size(), X["article_id"])
        out["f_customer_recency"] = mapped(
            h.groupby("customer_id")["days_ago"].min(), X["customer_id"])
        out["f_pair_count"] = pair_values(
            h.groupby(["customer_id", "article_id"]).size())
        out["f_pair_recency"] = pair_values(
            h.groupby(["customer_id", "article_id"])["days_ago"].min())

        for d in (7, 30, 90):
            z = h.loc[h["days_ago"] <= d]
            out["f_customer_count_" + str(d)] = mapped(
                z.groupby("customer_id").size(), X["customer_id"])
            out["f_item_count_" + str(d)] = mapped(
                z.groupby("article_id").size(), X["article_id"])
            out["f_pair_count_" + str(d)] = pair_values(
                z.groupby(["customer_id", "article_id"]).size())

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
            z = h.loc[h["days_ago"] <= 30]
            out["f_affinity30_" + str(j)] = (
                z.groupby(["customer_id", col]).size()
                .reindex(keys).fillna(0).to_numpy()
            )
            out["f_category_pop_" + str(j)] = mapped(
                h.groupby(col).size(), X["raw_i_" + col])

        out["f_customer_price"] = mapped(
            h.groupby("customer_id")["price"].mean(), X["customer_id"])
        out["f_item_price"] = mapped(
            h.groupby("article_id")["price"].mean(), X["article_id"])
    else:
        for name in names:
            out[name] = 0.0

    out["f_pair_rate"] = (
        out["f_pair_count"] / (out["f_customer_count"] + 1.0)
    )
    out["f_pair_recent_rate"] = (
        out["f_pair_count_7"] / (out["f_pair_count_30"] + 1.0)
    )
    out["f_item_recent_rate"] = (
        out["f_item_count_7"] / (out["f_item_count_30"] + 1.0)
    )
    out["f_pair_recency_score"] = (
        np.exp(-out["f_pair_recency"].clip(lower=0) / 30.0) *
        (out["f_pair_count"] > 0).astype(float)
    )

    return out.astype(float)
