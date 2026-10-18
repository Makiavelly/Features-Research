import pandas as pd
import numpy as np


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    def mapped_counts(frame, key, target):
        if len(frame) == 0:
            return pd.Series(0.0, index=X.index)
        counts = frame.groupby(key, sort=False).size()
        return X[target].map(counts).fillna(0.0)

    def pair_counts(frame, left, right):
        if len(frame) == 0:
            return pd.Series(0.0, index=X.index)
        counts = frame.groupby(right, sort=False).size()
        keys = pd.MultiIndex.from_frame(X[left])
        return pd.Series(keys.map(counts), index=X.index).fillna(0.0)

    for days, tag in ((7, "7d"), (30, "30d"), (180, "180d")):
        z = h.loc[h["days_ago"] <= days]
        out["f_user_count_" + tag] = mapped_counts(z, "customer_id", "customer_id")
        out["f_item_count_" + tag] = mapped_counts(z, "article_id", "article_id")
        out["f_pair_count_" + tag] = pair_counts(
            z, ["customer_id", "article_id"], ["customer_id", "article_id"]
        )

    if len(h):
        pair_rec = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
        pair_keys = pd.MultiIndex.from_frame(X[["customer_id", "article_id"]])
        out["f_pair_recency"] = pd.Series(pair_keys.map(pair_rec), index=X.index)

        user_rec = h.groupby("customer_id", sort=False)["days_ago"].min()
        out["f_customer_recency"] = X["customer_id"].map(user_rec)

        for col, feat in (
            ("product_type_no", "f_user_type_count"),
            ("department_no", "f_user_department_count"),
            ("product_code", "f_user_product_count"),
        ):
            counts = h.groupby(["customer_id", col], sort=False).size()
            keys = pd.MultiIndex.from_arrays(
                [X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()]
            )
            out[feat] = pd.Series(keys.map(counts), index=X.index).fillna(0.0)

        for col, feat in (
            ("colour_group_code", "f_user_colour_count"),
            ("section_no", "f_user_section_count"),
        ):
            counts = h.groupby(["customer_id", col], sort=False).size()
            keys = pd.MultiIndex.from_arrays(
                [X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()]
            )
            out[feat] = pd.Series(keys.map(counts), index=X.index).fillna(0.0)

        item_users = h.groupby("article_id", sort=False)["customer_id"].nunique()
        out["f_item_unique_users"] = X["article_id"].map(item_users).fillna(0.0)

        item_recent = h.loc[h["days_ago"] <= 30].groupby(
            "article_id", sort=False
        ).size()
        out["f_item_recent_share"] = (
            X["article_id"].map(item_recent).fillna(0.0)
            / (X["article_id"].map(h.groupby("article_id", sort=False).size()).fillna(0.0) + 1.0)
        )
    else:
        out["f_pair_recency"] = np.nan
        out["f_customer_recency"] = np.nan
        for feat in (
            "f_user_type_count", "f_user_department_count", "f_user_product_count",
            "f_user_colour_count", "f_user_section_count", "f_item_unique_users",
            "f_item_recent_share",
        ):
            out[feat] = 0.0

    return out.astype(float)
