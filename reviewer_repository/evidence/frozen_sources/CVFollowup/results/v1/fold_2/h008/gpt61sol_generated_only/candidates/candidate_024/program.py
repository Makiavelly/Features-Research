import numpy as np
import pandas as pd


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    def mapped(values, key):
        return X[key].map(values).fillna(0.0)

    def pair_mapped(values, left, right, fill=0.0):
        keys = pd.MultiIndex.from_arrays(
            [X[left].to_numpy(), X[right].to_numpy()]
        )
        result = pd.Series(values.reindex(keys).to_numpy(), index=X.index)
        if fill is not None:
            result = result.fillna(fill)
        return result

    for window, tag in ((7, "7d"), (30, "30d"), (180, "180d")):
        z = h.loc[h["days_ago"] <= window]
        out["f_user_purchases_" + tag] = mapped(
            z.groupby("customer_id", sort=False).size(), "customer_id"
        )
        out["f_item_purchases_" + tag] = mapped(
            z.groupby("article_id", sort=False).size(), "article_id"
        )

    out["f_item_purchases_all"] = mapped(
        h.groupby("article_id", sort=False).size(), "article_id"
    )

    pair_cols = ["customer_id", "article_id"]
    out["f_pair_purchases"] = pair_mapped(
        h.groupby(pair_cols, sort=False).size(),
        "customer_id",
        "article_id",
    )
    out["f_pair_purchases_30d"] = pair_mapped(
        h.loc[h["days_ago"] <= 30].groupby(pair_cols, sort=False).size(),
        "customer_id",
        "article_id",
    )
    out["f_pair_recency"] = pair_mapped(
        h.groupby(pair_cols, sort=False)["days_ago"].min(),
        "customer_id",
        "article_id",
        fill=None,
    )

    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id", sort=False)["days_ago"].min()
    )
    out["f_item_unique_customers"] = mapped(
        h.groupby("article_id", sort=False)["customer_id"].nunique(),
        "article_id",
    )

    recent = h.loc[h["days_ago"] <= 30]
    all_item = h.groupby("article_id", sort=False).size()
    recent_item = recent.groupby("article_id", sort=False).size()
    out["f_item_recent_share"] = (
        mapped(recent_item, "article_id") /
        (mapped(all_item, "article_id") + 1.0)
    )

    weighted = h.assign(
        _w=np.exp(-h["days_ago"].astype(float) / 30.0)
    )
    out["f_item_decay_popularity"] = mapped(
        weighted.groupby("article_id", sort=False)["_w"].sum(),
        "article_id",
    )

    for column, suffix in (
        ("product_code", "product"),
        ("product_type_no", "type"),
        ("department_no", "department"),
    ):
        values = h.groupby(
            ["customer_id", column], sort=False
        ).size()
        out["f_user_" + suffix + "_affinity"] = pair_mapped(
            values,
            "customer_id",
            "raw_i_" + column,
        )

    out["f_static_age"] = X["raw_u_age"]
    out["f_static_item_type"] = X["raw_i_product_type_no"]
    out["f_static_department"] = X["raw_i_department_no"]

    return out.astype(float)
