import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)

    if len(history) == 0:
        for name in (
            "f_pair_count_7d", "f_pair_count_30d", "f_pair_count_90d",
            "f_pair_recency", "f_customer_count_30d", "f_customer_count_90d",
            "f_customer_recency", "f_item_count_7d", "f_item_count_30d",
            "f_item_count_90d", "f_item_recency", "f_pair_decay",
            "f_customer_decay", "f_item_decay", "f_affinity_type_30d",
            "f_affinity_department_30d", "f_affinity_garment_30d"
        ):
            out[name] = 0.0
        return out

    h = history
    d = h["days_ago"].astype(float)

    def grouped_count(frame, keys):
        if len(frame) == 0:
            return pd.Series(dtype=float)
        return frame.groupby(keys, sort=False).size()

    def pair_count(days):
        z = h.loc[d <= days]
        s = grouped_count(z, ["customer_id", "article_id"])
        idx = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        return pd.Series(s.reindex(idx).fillna(0).to_numpy(), index=X.index)

    def pair_value(func):
        s = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].agg(func)
        idx = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        return pd.Series(s.reindex(idx).to_numpy(), index=X.index)

    def one_key_count(column, days):
        z = h.loc[d <= days]
        s = grouped_count(z, column)
        return X[column].map(s).fillna(0)

    def customer_count(days):
        return X["customer_id"].map(
            grouped_count(h.loc[d <= days], "customer_id")
        ).fillna(0)

    def item_count(days):
        return X["article_id"].map(
            grouped_count(h.loc[d <= days], "article_id")
        ).fillna(0)

    def affinity(history_column, candidate_column, days):
        z = h.loc[d <= days]
        s = grouped_count(z, ["customer_id", history_column])
        idx = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X[candidate_column].to_numpy()
        ])
        return pd.Series(s.reindex(idx).fillna(0).to_numpy(), index=X.index)

    out["f_pair_count_7d"] = pair_count(7)
    out["f_pair_count_30d"] = pair_count(30)
    out["f_pair_count_90d"] = pair_count(90)
    out["f_pair_recency"] = pair_value("min")
    out["f_customer_count_30d"] = customer_count(30)
    out["f_customer_count_90d"] = customer_count(90)
    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id", sort=False)["days_ago"].min()
    )
    out["f_item_count_7d"] = item_count(7)
    out["f_item_count_30d"] = item_count(30)
    out["f_item_count_90d"] = item_count(90)
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    )

    decay = np.exp(-d / 30.0)
    out["f_pair_decay"] = X["article_id"].map(
        pd.Series(decay, index=h.index).groupby(
            [h["customer_id"], h["article_id"]]
        ).sum()
    ).fillna(0).to_numpy()
    out["f_customer_decay"] = X["customer_id"].map(
        pd.Series(decay, index=h.index).groupby(h["customer_id"]).sum()
    ).fillna(0)
    out["f_item_decay"] = X["article_id"].map(
        pd.Series(decay, index=h.index).groupby(h["article_id"]).sum()
    ).fillna(0)

    out["f_affinity_type_30d"] = affinity(
        "product_type_no", "raw_i_product_type_no", 30
    )
    out["f_affinity_department_30d"] = affinity(
        "department_no", "raw_i_department_no", 30
    )
    out["f_affinity_garment_30d"] = affinity(
        "garment_group_no", "raw_i_garment_group_no", 30
    )

    return out.astype(float)
