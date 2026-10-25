import pandas as pd
import numpy as np

def modify_features(X, history):
    static_cols = (
        ("f_static_age", "raw_u_age"),
        ("f_static_fn", "raw_u_fn"),
        ("f_static_active", "raw_u_active"),
        ("f_static_club", "raw_u_club_member_status"),
        ("f_static_news", "raw_u_fashion_news_frequency"),
        ("f_static_product_code", "raw_i_product_code"),
        ("f_static_product_type", "raw_i_product_type_no"),
        ("f_static_graphical", "raw_i_graphical_appearance_no"),
        ("f_static_colour", "raw_i_colour_group_code"),
        ("f_static_colour_value", "raw_i_perceived_colour_value_id"),
        ("f_static_colour_master", "raw_i_perceived_colour_master_id"),
        ("f_static_department", "raw_i_department_no"),
        ("f_static_index_group", "raw_i_index_group_no"),
        ("f_static_section", "raw_i_section_no"),
        ("f_static_garment", "raw_i_garment_group_no"),
    )
    names = [
        x[0] for x in static_cols
    ] + [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_all",
        "f_user_count_7d", "f_user_count_30d", "f_user_count_all",
        "f_pair_count_7d", "f_pair_count_30d", "f_pair_count_all",
        "f_pair_recency", "f_pair_decay",
        "f_user_type_count", "f_user_type_count_30d",
        "f_user_department_count", "f_user_department_count_30d",
        "f_user_section_count", "f_user_section_count_30d",
        "f_user_garment_count", "f_user_garment_count_30d",
        "f_user_colour_count", "f_user_colour_count_30d",
    ]

    out = pd.DataFrame(0.0, index=X.index, columns=names)
    for feature, col in static_cols:
        out[feature] = pd.to_numeric(X[col], errors="coerce").to_numpy()

    if history is None or len(history) == 0:
        return out[names]

    h = history
    d = pd.to_numeric(h["days_ago"], errors="coerce")
    cid = X["customer_id"].to_numpy()
    aid = X["article_id"].to_numpy()
    pair_keys = pd.MultiIndex.from_arrays([cid, aid])

    def pair_map(s, default=0.0):
        return s.reindex(pair_keys).fillna(default).to_numpy()

    h7 = h.loc[d <= 7]
    h30 = h.loc[d <= 30]

    out["f_item_count_7d"] = X["article_id"].map(
        h7.groupby("article_id").size()
    ).fillna(0).to_numpy()
    out["f_item_count_30d"] = X["article_id"].map(
        h30.groupby("article_id").size()
    ).fillna(0).to_numpy()
    out["f_item_count_all"] = X["article_id"].map(
        h.groupby("article_id").size()
    ).fillna(0).to_numpy()

    out["f_user_count_7d"] = X["customer_id"].map(
        h7.groupby("customer_id").size()
    ).fillna(0).to_numpy()
    out["f_user_count_30d"] = X["customer_id"].map(
        h30.groupby("customer_id").size()
    ).fillna(0).to_numpy()
    out["f_user_count_all"] = X["customer_id"].map(
        h.groupby("customer_id").size()
    ).fillna(0).to_numpy()

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
        d.groupby([h["customer_id"], h["article_id"]]).min(),
        np.nan
    )

    weights = np.exp(-d.fillna(9999).to_numpy() / 30.0)
    decay = pd.Series(weights, index=h.index).groupby(
        [h["customer_id"], h["article_id"]]
    ).sum()
    out["f_pair_decay"] = pair_map(decay)

    categories = (
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
        ("section_no", "raw_i_section_no", "section"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
        ("colour_group_code", "raw_i_colour_group_code", "colour"),
    )
    for hc, xc, label in categories:
        keys = pd.MultiIndex.from_arrays([cid, X[xc].to_numpy()])
        all_counts = h.groupby(["customer_id", hc]).size()
        recent_counts = h30.groupby(["customer_id", hc]).size()
        out["f_user_" + label + "_count"] = (
            all_counts.reindex(keys).fillna(0).to_numpy()
        )
        out["f_user_" + label + "_count_30d"] = (
            recent_counts.reindex(keys).fillna(0).to_numpy()
        )

    return out[names]
