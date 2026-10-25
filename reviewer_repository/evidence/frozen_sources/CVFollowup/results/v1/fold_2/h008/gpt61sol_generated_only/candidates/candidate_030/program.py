import numpy as np
import pandas as pd


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def single_map(series, key, fill=0.0):
        return X[key].map(series).fillna(fill).to_numpy()

    def pair_map(series, left, right, fill=0.0):
        keys = pd.MultiIndex.from_arrays(
            [X[left].to_numpy(), X[right].to_numpy()],
            names=series.index.names,
        )
        return pd.Series(series.reindex(keys).to_numpy()).fillna(fill).to_numpy()

    if len(h):
        h30 = h.loc[h["days_ago"] <= 30]
        h90 = h.loc[h["days_ago"] <= 90]

        pair = h.groupby(["customer_id", "article_id"], sort=False)
        out["f_pair_count_all"] = pair_map(pair.size(), "customer_id", "article_id")
        out["f_pair_count_30d"] = pair_map(
            h30.groupby(["customer_id", "article_id"], sort=False).size(),
            "customer_id",
            "article_id",
        )
        out["f_pair_recency"] = pair_map(
            pair["days_ago"].min(), "customer_id", "article_id", 999.0
        )

        out["f_customer_recency"] = single_map(
            h.groupby("customer_id", sort=False)["days_ago"].min(),
            "customer_id",
            999.0,
        )

        out["f_item_count_7d"] = single_map(
            h.loc[h["days_ago"] <= 7].groupby("article_id", sort=False).size(),
            "article_id",
        )
        out["f_item_count_30d"] = single_map(
            h30.groupby("article_id", sort=False).size(), "article_id"
        )
        out["f_item_recency"] = single_map(
            h.groupby("article_id", sort=False)["days_ago"].min(),
            "article_id",
            999.0,
        )

        out["f_user_type_count_90d"] = pair_map(
            h90.groupby(["customer_id", "product_type_no"], sort=False).size(),
            "customer_id",
            "raw_i_product_type_no",
        )
        out["f_user_department_count_90d"] = pair_map(
            h90.groupby(["customer_id", "department_no"], sort=False).size(),
            "customer_id",
            "raw_i_department_no",
        )
        out["f_user_product_count_all"] = pair_map(
            h.groupby(["customer_id", "product_code"], sort=False).size(),
            "customer_id",
            "raw_i_product_code",
        )
    else:
        for name in (
            "f_pair_count_all",
            "f_pair_count_30d",
            "f_pair_recency",
            "f_customer_recency",
            "f_item_count_7d",
            "f_item_count_30d",
            "f_item_recency",
            "f_user_type_count_90d",
            "f_user_department_count_90d",
            "f_user_product_count_all",
        ):
            out[name] = 999.0 if "recency" in name else 0.0

    out["f_static_age"] = X["raw_u_age"]
    out["f_static_product_type"] = X["raw_i_product_type_no"]

    return out.astype(float)
