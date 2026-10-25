import numpy as np
import pandas as pd


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    def one_map(values, key):
        return X[key].map(values).fillna(0.0).to_numpy()

    def two_map(values, left, right):
        keys = pd.MultiIndex.from_arrays(
            [X[left].to_numpy(), X[right].to_numpy()]
        )
        return pd.Series(keys.map(values), index=X.index).fillna(0.0).to_numpy()

    for days, tag in ((7, "7d"), (30, "30d"), (90, "90d")):
        z = h.loc[h["days_ago"] <= days]
        out["f_user_count_" + tag] = one_map(
            z.groupby("customer_id", sort=False).size(), "customer_id"
        )
        out["f_item_count_" + tag] = one_map(
            z.groupby("article_id", sort=False).size(), "article_id"
        )

    if len(h):
        pair = ["customer_id", "article_id"]
        out["f_pair_count_all"] = two_map(
            h.groupby(pair, sort=False).size(), *pair
        )
        out["f_pair_count_30d"] = two_map(
            h.loc[h["days_ago"] <= 30].groupby(pair, sort=False).size(), *pair
        )
        out["f_pair_recency"] = two_map(
            h.groupby(pair, sort=False)["days_ago"].min(), *pair
        )

        out["f_customer_recency"] = one_map(
            h.groupby("customer_id", sort=False)["days_ago"].min(), "customer_id"
        )
        out["f_item_recency"] = one_map(
            h.groupby("article_id", sort=False)["days_ago"].min(), "article_id"
        )
        out["f_item_count_all"] = one_map(
            h.groupby("article_id", sort=False).size(), "article_id"
        )
        out["f_item_unique_users"] = one_map(
            h.groupby("article_id", sort=False)["customer_id"].nunique(), "article_id"
        )

        item_all = h.groupby("article_id", sort=False).size()
        item_30 = h.loc[h["days_ago"] <= 30].groupby(
            "article_id", sort=False
        ).size()
        out["f_item_recent_share"] = one_map(item_30, "article_id") / (
            one_map(item_all, "article_id") + 1.0
        )

        for col, name in (
            ("product_code", "product"),
            ("product_type_no", "type"),
            ("department_no", "department"),
            ("section_no", "section"),
            ("garment_group_no", "garment"),
            ("colour_group_code", "colour"),
        ):
            values = h.groupby(["customer_id", col], sort=False).size()
            out["f_user_" + name + "_count"] = two_map(
                values, "customer_id", "raw_i_" + col
            )

        recent = h.loc[h["days_ago"] <= 30]
        for col, name in (
            ("product_type_no", "type"),
            ("department_no", "department"),
            ("section_no", "section"),
        ):
            values = recent.groupby(["customer_id", col], sort=False).size()
            out["f_user_" + name + "_count_30d"] = two_map(
                values, "customer_id", "raw_i_" + col
            )

        weighted = h.assign(
            _w=np.exp(-h["days_ago"].astype(float) / 21.0)
        )
        for col, name in (
            ("product_type_no", "type"),
            ("department_no", "department"),
            ("colour_group_code", "colour"),
        ):
            values = weighted.groupby(
                ["customer_id", col], sort=False
            )["_w"].sum()
            out["f_user_" + name + "_decay"] = two_map(
                values, "customer_id", "raw_i_" + col
            )
    else:
        names = (
            "f_pair_count_all", "f_pair_count_30d", "f_pair_recency",
            "f_customer_recency", "f_item_recency", "f_item_count_all",
            "f_item_unique_users", "f_item_recent_share",
            "f_user_product_count", "f_user_type_count",
            "f_user_department_count", "f_user_section_count",
            "f_user_garment_count", "f_user_colour_count",
            "f_user_type_count_30d", "f_user_department_count_30d",
            "f_user_section_count_30d", "f_user_type_decay",
            "f_user_department_decay", "f_user_colour_decay",
        )
        for name in names:
            out[name] = 0.0

    out["f_static_age"] = X["raw_u_age"]
    out["f_static_fn"] = X["raw_u_fn"]
    out["f_static_active"] = X["raw_u_active"]
    out["f_static_product_type"] = X["raw_i_product_type_no"]
    out["f_static_department"] = X["raw_i_department_no"]
    out["f_static_section"] = X["raw_i_section_no"]
    out["f_static_garment"] = X["raw_i_garment_group_no"]

    return out.astype(float)
