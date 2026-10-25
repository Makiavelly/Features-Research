import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def mapped(values, keys):
        return keys.map(values).fillna(0).to_numpy()

    def pair_values(values):
        if len(values) == 0:
            return np.zeros(n)
        keys = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X["article_id"].to_numpy()
        ])
        return values.reindex(keys).fillna(0).to_numpy()

    base = [
        "f_customer_count", "f_item_count", "f_customer_recency",
        "f_pair_count", "f_pair_recency",
        "f_customer_count_7", "f_item_count_7",
        "f_customer_count_30", "f_item_count_30",
        "f_customer_count_90", "f_item_count_90",
        "f_pair_count_7", "f_pair_count_30", "f_pair_count_90",
        "f_affinity_type", "f_affinity_section", "f_affinity_garment",
        "f_affinity_department", "f_pop_type", "f_pop_section",
        "f_pop_garment", "f_pop_department", "f_customer_price",
        "f_item_price", "f_customer_channels", "f_item_channels"
    ]
    for name in base:
        out[name] = 0.0

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

        for days in (7, 30, 90):
            z = h[h["days_ago"] <= days]
            out["f_customer_count_" + str(days)] = mapped(
                z.groupby("customer_id").size(), X["customer_id"])
            out["f_item_count_" + str(days)] = mapped(
                z.groupby("article_id").size(), X["article_id"])
            out["f_pair_count_" + str(days)] = pair_values(
                z.groupby(["customer_id", "article_id"]).size())

        for name, col in (
            ("type", "product_type_no"),
            ("section", "section_no"),
            ("garment", "garment_group_no"),
            ("department", "department_no")
        ):
            key = pd.MultiIndex.from_arrays([
                X["customer_id"].to_numpy(),
                X["raw_i_" + col].to_numpy()
            ])
            out["f_affinity_" + name] = (
                h.groupby(["customer_id", col]).size()
                .reindex(key).fillna(0).to_numpy()
            )
            out["f_pop_" + name] = mapped(
                h.groupby(col).size(), X["raw_i_" + col])

        out["f_customer_price"] = mapped(
            h.groupby("customer_id")["price"].mean(), X["customer_id"])
        out["f_item_price"] = mapped(
            h.groupby("article_id")["price"].mean(), X["article_id"])
        out["f_customer_channels"] = mapped(
            h.groupby("customer_id")["sales_channel_id"].nunique(),
            X["customer_id"])
        out["f_item_channels"] = mapped(
            h.groupby("article_id")["sales_channel_id"].nunique(),
            X["article_id"])

    out["f_pair_rate"] = (
        out["f_pair_count"] / (out["f_customer_count"] + 1.0)
    )
    out["f_pair_recent_rate"] = (
        out["f_pair_count_7"] / (out["f_pair_count_30"] + 1.0)
    )
    out["f_customer_recent_rate"] = (
        out["f_customer_count_7"] /
        (out["f_customer_count_30"] + 1.0)
    )
    out["f_item_recent_rate"] = (
        out["f_item_count_7"] / (out["f_item_count_30"] + 1.0)
    )
    out["f_pair_recency_score"] = (
        np.exp(-out["f_pair_recency"].clip(lower=0) / 21.0) *
        (out["f_pair_count"] > 0).astype(float)
    )
    out["f_customer_recency_score"] = np.exp(
        -out["f_customer_recency"].clip(lower=0) / 21.0
    )
    out["f_affinity_rate"] = (
        out["f_affinity_type"] / (out["f_customer_count"] + 1.0)
    )
    out["f_item_velocity"] = (
        out["f_item_count_7"] / (out["f_item_count_90"] + 1.0)
    )
    out["f_customer_velocity"] = (
        out["f_customer_count_7"] /
        (out["f_customer_count_90"] + 1.0)
    )
    out["f_item_log_count"] = np.log1p(out["f_item_count"])

    return out.astype(float)
