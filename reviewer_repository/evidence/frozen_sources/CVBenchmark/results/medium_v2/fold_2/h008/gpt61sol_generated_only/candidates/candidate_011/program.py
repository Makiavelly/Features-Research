import pandas as pd
import numpy as np


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    # Static candidate attributes are useful both directly and for interactions
    # with the history-derived preference features below.
    for raw in (
        "raw_u_age", "raw_u_fn", "raw_u_active", "raw_u_club_member_status",
        "raw_u_fashion_news_frequency", "raw_i_product_code",
        "raw_i_product_type_no", "raw_i_graphical_appearance_no",
        "raw_i_colour_group_code", "raw_i_perceived_colour_value_id",
        "raw_i_perceived_colour_master_id", "raw_i_department_no",
        "raw_i_index_group_no", "raw_i_section_no", "raw_i_garment_group_no",
    ):
        out["f_" + raw[4:]] = pd.to_numeric(X[raw], errors="coerce")

    def map_group(grouped, key):
        return X[key].map(grouped).fillna(0.0)

    def map_pair(grouped, left, right):
        keys = pd.MultiIndex.from_arrays(
            [X[left].to_numpy(), X[right].to_numpy()]
        )
        return pd.Series(keys.map(grouped), index=X.index).fillna(0.0)

    if h.empty:
        for name in (
            "f_user_count_30d", "f_user_count_180d", "f_item_count_7d",
            "f_item_count_30d", "f_item_count_180d", "f_pair_count_180d",
            "f_pair_recency", "f_user_recency", "f_item_unique_users",
            "f_user_type_count", "f_user_department_count",
            "f_user_product_count", "f_user_colour_count",
            "f_user_section_count", "f_user_type_count_30d",
            "f_user_department_count_30d",
        ):
            out[name] = 0.0
        return out.astype(float)

    for days, tag in ((30, "30d"), (180, "180d")):
        z = h.loc[h["days_ago"] <= days]
        out["f_user_count_" + tag] = map_group(
            z.groupby("customer_id", sort=False).size(), "customer_id"
        )

    for days, tag in ((7, "7d"), (30, "30d"), (180, "180d")):
        z = h.loc[h["days_ago"] <= days]
        out["f_item_count_" + tag] = map_group(
            z.groupby("article_id", sort=False).size(), "article_id"
        )

    z = h.loc[h["days_ago"] <= 180]
    out["f_pair_count_180d"] = map_pair(
        z.groupby(["customer_id", "article_id"], sort=False).size(),
        "customer_id", "article_id"
    )
    pair_rec = h.groupby(["customer_id", "article_id"], sort=False)[
        "days_ago"
    ].min()
    out["f_pair_recency"] = map_pair(
        pair_rec, "customer_id", "article_id"
    )
    out["f_user_recency"] = map_group(
        h.groupby("customer_id", sort=False)["days_ago"].min(), "customer_id"
    )
    out["f_item_unique_users"] = map_group(
        h.groupby("article_id", sort=False)["customer_id"].nunique(), "article_id"
    )

    for col, feat in (
        ("product_type_no", "f_user_type_count"),
        ("department_no", "f_user_department_count"),
        ("product_code", "f_user_product_count"),
        ("colour_group_code", "f_user_colour_count"),
        ("section_no", "f_user_section_count"),
    ):
        grouped = h.groupby(["customer_id", col], sort=False).size()
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()]
        )
        out[feat] = pd.Series(keys.map(grouped), index=X.index).fillna(0.0)

    for col, feat in (
        ("product_type_no", "f_user_type_count_30d"),
        ("department_no", "f_user_department_count_30d"),
    ):
        z = h.loc[h["days_ago"] <= 30]
        grouped = z.groupby(["customer_id", col], sort=False).size()
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()]
        )
        out[feat] = pd.Series(keys.map(grouped), index=X.index).fillna(0.0)

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
