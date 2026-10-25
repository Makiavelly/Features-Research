import numpy as np
import pandas as pd


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    def cmap(series, key):
        return X[key].map(series).fillna(0.0)

    def pmap(series, left, right):
        keys = pd.MultiIndex.from_arrays(
            [X[left].to_numpy(), X[right].to_numpy()]
        )
        return pd.Series(keys.map(series), index=X.index).fillna(0.0)

    seven = h.loc[h["days_ago"] <= 7]
    thirty = h.loc[h["days_ago"] <= 30]
    halfyear = h.loc[h["days_ago"] <= 180]

    for frame, tag in (
        (seven, "seven"),
        (thirty, "thirty"),
        (halfyear, "halfyear"),
    ):
        out["f_user_count_" + tag] = cmap(
            frame.groupby("customer_id", sort=False).size(),
            "customer_id",
        )
        out["f_item_count_" + tag] = cmap(
            frame.groupby("article_id", sort=False).size(),
            "article_id",
        )

    item_all = h.groupby("article_id", sort=False).size()
    item_seven = seven.groupby("article_id", sort=False).size()
    item_thirty = thirty.groupby("article_id", sort=False).size()
    item_halfyear = halfyear.groupby("article_id", sort=False).size()

    out["f_item_count_all"] = cmap(item_all, "article_id")
    out["f_item_recency"] = cmap(
        h.groupby("article_id", sort=False)["days_ago"].min(),
        "article_id",
    )
    out["f_item_unique_users"] = cmap(
        h.groupby("article_id", sort=False)["customer_id"].nunique(),
        "article_id",
    )
    out["f_item_share_seven_thirty"] = cmap(
        item_seven, "article_id"
    ) / (cmap(item_thirty, "article_id") + 1.0)
    out["f_item_share_thirty_halfyear"] = cmap(
        item_thirty, "article_id"
    ) / (cmap(item_halfyear, "article_id") + 1.0)

    pair_cols = ["customer_id", "article_id"]
    out["f_pair_count_all"] = pmap(
        h.groupby(pair_cols, sort=False).size(),
        *pair_cols
    )
    out["f_pair_count_thirty"] = pmap(
        thirty.groupby(pair_cols, sort=False).size(),
        *pair_cols
    )
    out["f_pair_count_seven"] = pmap(
        seven.groupby(pair_cols, sort=False).size(),
        *pair_cols
    )
    out["f_pair_recency"] = pmap(
        h.groupby(pair_cols, sort=False)["days_ago"].min(),
        *pair_cols
    )

    decay = h.assign(
        _weight=np.exp(-h["days_ago"].astype(float) / 21.0)
    )
    out["f_pair_decay"] = pmap(
        decay.groupby(pair_cols, sort=False)["_weight"].sum(),
        *pair_cols
    )
    out["f_customer_recency"] = cmap(
        h.groupby("customer_id", sort=False)["days_ago"].min(),
        "customer_id",
    )

    for col, name in (
        ("product_type_no", "type"),
        ("department_no", "department"),
        ("section_no", "section"),
        ("garment_group_no", "garment"),
        ("colour_group_code", "colour"),
        ("product_code", "product"),
    ):
        out["f_user_" + name + "_thirty"] = pmap(
            thirty.groupby(["customer_id", col], sort=False).size(),
            "customer_id",
            "raw_i_" + col,
        )

    for col, name in (
        ("product_type_no", "type"),
        ("department_no", "department"),
    ):
        out["f_user_" + name + "_decay"] = pmap(
            decay.groupby(["customer_id", col], sort=False)["_weight"].sum(),
            "customer_id",
            "raw_i_" + col,
        )

    for raw, name in (
        ("raw_u_age", "f_static_age"),
        ("raw_u_fn", "f_static_fn"),
        ("raw_u_active", "f_static_active"),
        ("raw_u_club_member_status", "f_static_club"),
        ("raw_u_fashion_news_frequency", "f_static_news"),
        ("raw_i_product_type_no", "f_static_type"),
        ("raw_i_department_no", "f_static_department"),
        ("raw_i_section_no", "f_static_section"),
        ("raw_i_garment_group_no", "f_static_garment"),
        ("raw_i_colour_group_code", "f_static_colour"),
        ("raw_i_product_code", "f_static_product"),
    ):
        out[name] = X[raw]

    return out.astype(float)
