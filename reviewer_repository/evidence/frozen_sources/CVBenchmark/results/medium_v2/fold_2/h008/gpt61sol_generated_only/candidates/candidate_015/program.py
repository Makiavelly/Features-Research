import numpy as np
import pandas as pd


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    def mapped(series, key):
        return X[key].map(series).fillna(0.0)

    def pair_map(series, left, right):
        keys = pd.MultiIndex.from_arrays(
            [X[left].to_numpy(), X[right].to_numpy()]
        )
        return pd.Series(keys.map(series), index=X.index).fillna(0.0)

    for days, tag in ((7, "7d"), (30, "30d"), (180, "180d")):
        z = h.loc[h["days_ago"] <= days]
        out["f_user_count_" + tag] = mapped(
            z.groupby("customer_id", sort=False).size(), "customer_id"
        )
        out["f_item_count_" + tag] = mapped(
            z.groupby("article_id", sort=False).size(), "article_id"
        )

    out["f_item_count_all"] = mapped(
        h.groupby("article_id", sort=False).size(), "article_id"
    )

    if len(h):
        pair_cols = ["customer_id", "article_id"]
        pair_counts = h.groupby(pair_cols, sort=False).size()
        out["f_pair_count_all"] = pair_map(pair_counts, *pair_cols)

        pair_recent = h.groupby(pair_cols, sort=False)["days_ago"].min()
        out["f_pair_recency"] = pair_map(pair_recent, *pair_cols)

        user_recent = h.groupby("customer_id", sort=False)["days_ago"].min()
        out["f_customer_recency"] = X["customer_id"].map(user_recent)

        for col, feat in (
            ("product_type_no", "f_user_type_count"),
            ("department_no", "f_user_department_count"),
            ("product_code", "f_user_product_count"),
            ("colour_group_code", "f_user_colour_count"),
        ):
            counts = h.groupby(["customer_id", col], sort=False).size()
            out[feat] = pair_map(
                counts, "customer_id", "raw_i_" + col
            )

        weighted = h.assign(_weight=np.exp(-h["days_ago"].astype(float) / 30.0))
        for col, feat in (
            ("product_type_no", "f_user_type_recency_weight"),
            ("department_no", "f_user_department_recency_weight"),
        ):
            sums = weighted.groupby(["customer_id", col], sort=False)["_weight"].sum()
            out[feat] = pair_map(sums, "customer_id", "raw_i_" + col)

        unique_users = h.groupby("article_id", sort=False)["customer_id"].nunique()
        out["f_item_unique_users"] = mapped(unique_users, "article_id")

        all_counts = h.groupby("article_id", sort=False).size()
        recent_counts = h.loc[h["days_ago"] <= 30].groupby(
            "article_id", sort=False
        ).size()
        out["f_item_recent_share"] = mapped(recent_counts, "article_id") / (
            mapped(all_counts, "article_id") + 1.0
        )
    else:
        for name in (
            "f_pair_count_all", "f_pair_recency", "f_customer_recency",
            "f_user_type_count", "f_user_department_count",
            "f_user_product_count", "f_user_colour_count",
            "f_user_type_recency_weight", "f_user_department_recency_weight",
            "f_item_unique_users", "f_item_recent_share",
        ):
            out[name] = 0.0

    out["f_static_age"] = X["raw_u_age"]
    out["f_static_product_type"] = X["raw_i_product_type_no"]
    out["f_static_department"] = X["raw_i_department_no"]
    return out.astype(float)
