import numpy as np
import pandas as pd


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    def cmap(s, key, fill=0.0):
        v = X[key].map(s)
        return v.fillna(fill) if fill is not None else v

    def pmap(s, left, right, fill=0.0):
        k = pd.MultiIndex.from_arrays(
            [X[left].to_numpy(), X[right].to_numpy()]
        )
        v = pd.Series(k.map(s), index=X.index)
        return v.fillna(fill) if fill is not None else v

    pair_cols = ["customer_id", "article_id"]
    all_item = h.groupby("article_id", sort=False).size()
    all_user = h.groupby("customer_id", sort=False).size()

    out["f_item_count_all"] = cmap(all_item, "article_id")
    out["f_user_count_all"] = cmap(all_user, "customer_id")

    for d, tag in ((7, "7"), (30, "30"), (90, "90")):
        z = h.loc[h["days_ago"] <= d]
        out["f_item_count_" + tag] = cmap(
            z.groupby("article_id", sort=False).size(), "article_id"
        )
        out["f_user_count_" + tag] = cmap(
            z.groupby("customer_id", sort=False).size(), "customer_id"
        )

    item_recent = h.groupby("article_id", sort=False)["days_ago"].min()
    user_recent = h.groupby("customer_id", sort=False)["days_ago"].min()
    out["f_item_recency"] = cmap(item_recent, "article_id", None)
    out["f_user_recency"] = cmap(user_recent, "customer_id", None)

    pair_count = h.groupby(pair_cols, sort=False).size()
    pair_recent = h.groupby(pair_cols, sort=False)["days_ago"].min()
    out["f_pair_count"] = pmap(pair_count, *pair_cols)
    out["f_pair_recency"] = pmap(pair_recent, *pair_cols, fill=None)

    h30 = h.loc[h["days_ago"] <= 30]
    h7 = h.loc[h["days_ago"] <= 7]
    out["f_pair_count_30"] = pmap(
        h30.groupby(pair_cols, sort=False).size(), *pair_cols
    )
    out["f_pair_count_7"] = pmap(
        h7.groupby(pair_cols, sort=False).size(), *pair_cols
    )

    w = h.assign(_w=np.exp(-h["days_ago"].astype(float) / 21.0))
    pair_w = w.groupby(pair_cols, sort=False)["_w"].sum()
    out["f_pair_decay"] = pmap(pair_w, *pair_cols)

    for col, name in (
        ("product_code", "product"),
        ("product_type_no", "type"),
        ("department_no", "department"),
        ("section_no", "section"),
        ("colour_group_code", "colour"),
    ):
        raw = "raw_i_" + col
        counts = h.groupby(["customer_id", col], sort=False).size()
        recent_counts = h30.groupby(["customer_id", col], sort=False).size()
        out["f_user_" + name + "_count"] = pmap(
            counts, "customer_id", raw
        )
        out["f_user_" + name + "_count_30"] = pmap(
            recent_counts, "customer_id", raw
        )

    for col, name in (
        ("product_type_no", "type"),
        ("department_no", "department"),
        ("section_no", "section"),
    ):
        raw = "raw_i_" + col
        sums = w.groupby(["customer_id", col], sort=False)["_w"].sum()
        out["f_user_" + name + "_decay"] = pmap(
            sums, "customer_id", raw
        )

    item_users = h.groupby("article_id", sort=False)["customer_id"].nunique()
    out["f_item_unique_users"] = cmap(item_users, "article_id")

    item30 = h30.groupby("article_id", sort=False).size()
    out["f_item_recent_share"] = cmap(item30, "article_id") / (
        cmap(all_item, "article_id") + 1.0
    )

    out["f_static_age"] = X["raw_u_age"]
    out["f_static_fn"] = X["raw_u_fn"]
    out["f_static_active"] = X["raw_u_active"]
    out["f_static_club"] = X["raw_u_club_member_status"]
    out["f_static_type"] = X["raw_i_product_type_no"]
    out["f_static_department"] = X["raw_i_department_no"]
    out["f_static_section"] = X["raw_i_section_no"]
    out["f_static_garment"] = X["raw_i_garment_group_no"]

    return out.astype(float)
