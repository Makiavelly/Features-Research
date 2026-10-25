import numpy as np
import pandas as pd


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    def cmap(s, key):
        return X[key].map(s).fillna(0.0)

    def pmap(s, left, right, fill=True):
        keys = pd.MultiIndex.from_arrays(
            [X[left].to_numpy(), X[right].to_numpy()]
        )
        v = pd.Series(keys.map(s), index=X.index)
        return v.fillna(0.0) if fill else v

    def counts(z, col):
        return z.groupby(col, sort=False).size()

    h7 = h.loc[h["days_ago"] <= 7]
    h30 = h.loc[h["days_ago"] <= 30]
    h90 = h.loc[h["days_ago"] <= 90]

    out["f_item_count_7d"] = cmap(counts(h7, "article_id"), "article_id")
    out["f_item_count_30d"] = cmap(counts(h30, "article_id"), "article_id")
    out["f_item_count_90d"] = cmap(counts(h90, "article_id"), "article_id")
    out["f_item_count_all"] = cmap(counts(h, "article_id"), "article_id")

    out["f_user_count_7d"] = cmap(counts(h7, "customer_id"), "customer_id")
    out["f_user_count_30d"] = cmap(counts(h30, "customer_id"), "customer_id")
    out["f_user_count_90d"] = cmap(counts(h90, "customer_id"), "customer_id")
    out["f_user_count_all"] = cmap(counts(h, "customer_id"), "customer_id")

    pair = ["customer_id", "article_id"]
    pair_all = h.groupby(pair, sort=False).size()
    pair_30 = h30.groupby(pair, sort=False).size()
    pair_rec = h.groupby(pair, sort=False)["days_ago"].min()

    out["f_pair_count_all"] = pmap(pair_all, *pair)
    out["f_pair_count_30d"] = pmap(pair_30, *pair)
    out["f_pair_recency"] = pmap(pair_rec, *pair, fill=False)
    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id", sort=False)["days_ago"].min()
    )

    for col, name in (
        ("product_type_no", "type"),
        ("department_no", "department"),
        ("section_no", "section"),
        ("garment_group_no", "garment"),
        ("colour_group_code", "colour"),
    ):
        s = h.groupby(["customer_id", col], sort=False).size()
        out["f_user_" + name + "_count"] = pmap(
            s, "customer_id", "raw_i_" + col
        )

    if len(h):
        w = h.assign(_w=np.exp(-h["days_ago"].astype(float) / 30.0))
        for col, name in (
            ("product_type_no", "type"),
            ("department_no", "department"),
            ("section_no", "section"),
        ):
            s = w.groupby(["customer_id", col], sort=False)["_w"].sum()
            out["f_user_" + name + "_weight"] = pmap(
                s, "customer_id", "raw_i_" + col
            )
    else:
        out["f_user_type_weight"] = 0.0
        out["f_user_department_weight"] = 0.0
        out["f_user_section_weight"] = 0.0

    item_users = h.groupby("article_id", sort=False)["customer_id"].nunique()
    item_rec = h.groupby("article_id", sort=False)["days_ago"].min()
    out["f_item_unique_users"] = cmap(item_users, "article_id")
    out["f_item_recency"] = X["article_id"].map(item_rec)

    i7 = cmap(counts(h7, "article_id"), "article_id")
    i30 = cmap(counts(h30, "article_id"), "article_id")
    u7 = cmap(counts(h7, "customer_id"), "customer_id")
    u30 = cmap(counts(h30, "customer_id"), "customer_id")
    out["f_item_recent_share"] = i30 / (cmap(counts(h, "article_id"), "article_id") + 1.0)
    out["f_item_week_momentum"] = i7 / (i30 + 1.0)
    out["f_user_week_share"] = u7 / (u30 + 1.0)

    user_price = h.groupby("customer_id", sort=False)["price"].mean()
    item_price = h.groupby("article_id", sort=False)["price"].mean()
    up = X["customer_id"].map(user_price)
    ip = X["article_id"].map(item_price)
    out["f_user_mean_price"] = up
    out["f_item_mean_price"] = ip
    out["f_price_distance"] = (up - ip).abs()

    out["f_static_age"] = X["raw_u_age"]
    out["f_static_active"] = X["raw_u_active"]
    out["f_static_fn"] = X["raw_u_fn"]
    out["f_static_product_type"] = X["raw_i_product_type_no"]
    out["f_static_department"] = X["raw_i_department_no"]
    out["f_static_index_group"] = X["raw_i_index_group_no"]
    out["f_static_section"] = X["raw_i_section_no"]

    return out.astype(float)
