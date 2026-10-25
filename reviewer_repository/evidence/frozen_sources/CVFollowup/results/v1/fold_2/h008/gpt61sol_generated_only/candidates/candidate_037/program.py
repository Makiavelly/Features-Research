import numpy as np
import pandas as pd

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    h7 = h.loc[h["days_ago"] <= 7]
    h30 = h.loc[h["days_ago"] <= 30]
    h180 = h.loc[h["days_ago"] <= 180]

    def one(series, key, fill=True):
        v = X[key].map(series)
        if fill:
            v = v.fillna(0.0)
        return v.to_numpy()

    def two(series, left, right, fill=True):
        keys = pd.MultiIndex.from_arrays(
            [X[left].to_numpy(), X[right].to_numpy()]
        )
        v = pd.Series(keys.map(series), index=X.index)
        if fill:
            v = v.fillna(0.0)
        return v.to_numpy()

    for z, tag in ((h7, "7d"), (h30, "30d"), (h180, "180d")):
        out["f_user_count_" + tag] = one(
            z.groupby("customer_id", sort=False).size(), "customer_id"
        )
        out["f_item_count_" + tag] = one(
            z.groupby("article_id", sort=False).size(), "article_id"
        )

    out["f_item_count_all"] = one(
        h.groupby("article_id", sort=False).size(), "article_id"
    )
    out["f_item_users_all"] = one(
        h.groupby("article_id", sort=False)["customer_id"].nunique(), "article_id"
    )
    out["f_item_recency"] = one(
        h.groupby("article_id", sort=False)["days_ago"].min(), "article_id", False
    )
    item_all = h.groupby("article_id", sort=False).size()
    item_30 = h30.groupby("article_id", sort=False).size()
    item_7 = h7.groupby("article_id", sort=False).size()
    out["f_item_share_30d"] = one(item_30, "article_id") / (
        one(item_all, "article_id") + 1.0
    )
    out["f_item_share_7d"] = one(item_7, "article_id") / (
        one(item_30, "article_id") + 1.0
    )

    pairs = ["customer_id", "article_id"]
    out["f_pair_count_all"] = two(
        h.groupby(pairs, sort=False).size(), *pairs
    )
    out["f_pair_count_30d"] = two(
        h30.groupby(pairs, sort=False).size(), *pairs
    )
    out["f_pair_count_7d"] = two(
        h7.groupby(pairs, sort=False).size(), *pairs
    )
    out["f_pair_recency"] = two(
        h.groupby(pairs, sort=False)["days_ago"].min(), *pairs, fill=False
    )
    out["f_user_recency"] = one(
        h.groupby("customer_id", sort=False)["days_ago"].min(),
        "customer_id", False
    )

    for col, name in (
        ("product_code", "product"),
        ("product_type_no", "type"),
        ("department_no", "department"),
        ("colour_group_code", "colour"),
        ("section_no", "section"),
    ):
        out["f_user_" + name + "_count30"] = two(
            h30.groupby(["customer_id", col], sort=False).size(),
            "customer_id", "raw_i_" + col
        )

    weighted = h30.assign(
        _w=np.exp(-h30["days_ago"].astype(float) / 14.0)
    )
    for col, name in (
        ("product_type_no", "type"),
        ("department_no", "department"),
    ):
        out["f_user_" + name + "_weight"] = two(
            weighted.groupby(["customer_id", col], sort=False)["_w"].sum(),
            "customer_id", "raw_i_" + col
        )

    user_price = h.groupby("customer_id", sort=False)["price"].mean()
    item_price = h.groupby("article_id", sort=False)["price"].mean()
    up = one(user_price, "customer_id", False)
    ip = one(item_price, "article_id", False)
    out["f_user_mean_price"] = up
    out["f_item_mean_price"] = ip
    out["f_price_distance"] = np.abs(up - ip)

    for raw, name in (
        ("raw_u_age", "age"),
        ("raw_u_fn", "fn"),
        ("raw_u_active", "active"),
        ("raw_u_club_member_status", "club"),
        ("raw_u_fashion_news_frequency", "news"),
        ("raw_i_product_type_no", "item_type"),
        ("raw_i_department_no", "item_department"),
        ("raw_i_section_no", "item_section"),
        ("raw_i_product_code", "item_product"),
        ("raw_i_colour_group_code", "item_colour"),
    ):
        out["f_static_" + name] = X[raw].to_numpy()

    return out.astype(float)
