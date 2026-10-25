import pandas as pd
import numpy as np

def modify_features(X, history):
    static_cols = [
        ("f_u_age", "raw_u_age"),
        ("f_u_fn", "raw_u_fn"),
        ("f_u_active", "raw_u_active"),
        ("f_u_club", "raw_u_club_member_status"),
        ("f_u_news", "raw_u_fashion_news_frequency"),
        ("f_i_product_code", "raw_i_product_code"),
        ("f_i_type", "raw_i_product_type_no"),
        ("f_i_graphical", "raw_i_graphical_appearance_no"),
        ("f_i_colour", "raw_i_colour_group_code"),
        ("f_i_colour_value", "raw_i_perceived_colour_value_id"),
        ("f_i_colour_master", "raw_i_perceived_colour_master_id"),
        ("f_i_department", "raw_i_department_no"),
        ("f_i_index_group", "raw_i_index_group_no"),
        ("f_i_section", "raw_i_section_no"),
        ("f_i_garment", "raw_i_garment_group_no"),
    ]
    names = [a for a, b in static_cols] + [
        "f_pair_count_7d", "f_pair_count_30d", "f_pair_count_all",
        "f_pair_recency", "f_item_count_7d", "f_item_count_30d",
        "f_item_count_all", "f_item_recency", "f_user_count_7d",
        "f_user_count_30d", "f_user_count_all", "f_user_recency",
        "f_user_type_30d", "f_user_department_30d",
        "f_user_section_30d", "f_user_garment_30d",
        "f_user_colour_30d", "f_type_count_7d",
        "f_department_count_7d", "f_item_buyers_30d",
        "f_price_distance"
    ]

    out = pd.DataFrame(0.0, index=X.index, columns=names)
    for name, col in static_cols:
        out[name] = pd.to_numeric(X[col], errors="coerce").to_numpy()

    if history is None or len(history) == 0:
        return out[names]

    h = history
    d = pd.to_numeric(h["days_ago"], errors="coerce")
    xcid = X["customer_id"].to_numpy()
    xaid = X["article_id"].to_numpy()
    pair_key = pd.MultiIndex.from_arrays([xcid, xaid])

    def pair_map(s, default=0.0):
        return s.reindex(pair_key).fillna(default).to_numpy()

    h7 = h.loc[d <= 7]
    h30 = h.loc[d <= 30]

    out["f_pair_count_7d"] = pair_map(
        h7.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_count_30d"] = pair_map(
        h30.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_count_all"] = pair_map(
        h.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_recency"] = pair_map(
        h.groupby(["customer_id", "article_id"])["days_ago"].min(), np.nan
    )

    for label, frame in (("7d", h7), ("30d", h30), ("all", h)):
        out["f_item_count_" + label] = X["article_id"].map(
            frame.groupby("article_id").size()
        ).fillna(0).to_numpy()
        out["f_user_count_" + label] = X["customer_id"].map(
            frame.groupby("customer_id").size()
        ).fillna(0).to_numpy()

    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()
    ).to_numpy()
    out["f_user_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()
    ).to_numpy()

    for hc, xc, label in (
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
        ("section_no", "raw_i_section_no", "section"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
        ("colour_group_code", "raw_i_colour_group_code", "colour"),
    ):
        key = pd.MultiIndex.from_arrays([xcid, X[xc].to_numpy()])
        s = h30.groupby(["customer_id", hc]).size()
        out["f_user_" + label + "_30d"] = s.reindex(key).fillna(0).to_numpy()

    out["f_type_count_7d"] = X["raw_i_product_type_no"].map(
        h7.groupby("product_type_no").size()
    ).fillna(0).to_numpy()
    out["f_department_count_7d"] = X["raw_i_department_no"].map(
        h7.groupby("department_no").size()
    ).fillna(0).to_numpy()

    out["f_item_buyers_30d"] = X["article_id"].map(
        h30.groupby("article_id")["customer_id"].nunique()
    ).fillna(0).to_numpy()

    user_price = X["customer_id"].map(
        h.groupby("customer_id")["price"].mean()
    )
    item_price = X["article_id"].map(
        h.groupby("article_id")["price"].mean()
    )
    out["f_price_distance"] = (user_price - item_price).abs().to_numpy()

    return out[names]
