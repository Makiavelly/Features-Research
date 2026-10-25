import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_count_all", "f_item_users_30d", "f_item_recency",
        "f_item_weighted", "f_user_count_7d", "f_user_count_30d",
        "f_user_count_all", "f_user_recency", "f_pair_count_7d",
        "f_pair_count_30d", "f_pair_count_all", "f_pair_recency",
        "f_pair_weighted", "f_user_product_count_30d",
        "f_user_type_count_30d", "f_user_department_count_30d",
        "f_user_section_count_30d", "f_user_garment_count_30d",
        "f_user_colour_count_30d", "f_user_type_ratio_30d",
        "f_user_department_ratio_30d", "f_type_count_7d",
        "f_department_count_7d", "f_item_mean_price",
        "f_user_mean_price", "f_static_age", "f_static_product_type",
        "f_static_department", "f_static_section", "f_static_garment"
    ]

    out = pd.DataFrame(index=X.index)
    for n in names:
        out[n] = 0.0

    static_cols = (
        ("f_static_age", "raw_u_age"),
        ("f_static_product_type", "raw_i_product_type_no"),
        ("f_static_department", "raw_i_department_no"),
        ("f_static_section", "raw_i_section_no"),
        ("f_static_garment", "raw_i_garment_group_no"),
    )
    for n, c in static_cols:
        out[n] = pd.to_numeric(X[c], errors="coerce").to_numpy()

    if history is None or len(history) == 0:
        return out[names]

    h = history.copy()
    d = pd.to_numeric(h["days_ago"], errors="coerce")
    cid = X["customer_id"].to_numpy()
    aid = X["article_id"].to_numpy()
    pair_key = pd.MultiIndex.from_arrays([cid, aid])

    def pair_map(s, default=0.0):
        return s.reindex(pair_key).fillna(default).to_numpy()

    h7 = h.loc[d <= 7]
    h30 = h.loc[d <= 30]
    h90 = h.loc[d <= 90]

    for frame, label in ((h7, "7d"), (h30, "30d"), (h90, "90d")):
        out["f_item_count_" + label] = X["article_id"].map(
            frame.groupby("article_id").size()
        ).fillna(0).to_numpy()

    out["f_item_count_all"] = X["article_id"].map(
        h.groupby("article_id").size()
    ).fillna(0).to_numpy()

    out["f_item_users_30d"] = X["article_id"].map(
        h30.groupby("article_id")["customer_id"].nunique()
    ).fillna(0).to_numpy()

    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()
    ).to_numpy()

    weight = np.exp(-d.fillna(365.0).to_numpy() / 21.0)
    hw = h[["article_id", "customer_id"]].copy()
    hw["w"] = weight
    out["f_item_weighted"] = X["article_id"].map(
        hw.groupby("article_id")["w"].sum()
    ).fillna(0).to_numpy()

    for frame, label in ((h7, "7d"), (h30, "30d")):
        out["f_user_count_" + label] = X["customer_id"].map(
            frame.groupby("customer_id").size()
        ).fillna(0).to_numpy()

    out["f_user_count_all"] = X["customer_id"].map(
        h.groupby("customer_id").size()
    ).fillna(0).to_numpy()

    out["f_user_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()
    ).to_numpy()

    for frame, label in ((h7, "7d"), (h30, "30d")):
        out["f_pair_count_" + label] = pair_map(
            frame.groupby(["customer_id", "article_id"]).size()
        )

    out["f_pair_count_all"] = pair_map(
        h.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_recency"] = pair_map(
        h.groupby(["customer_id", "article_id"])["days_ago"].min(),
        np.nan
    )

    hw_pair = h[["customer_id", "article_id"]].copy()
    hw_pair["w"] = weight
    out["f_pair_weighted"] = pair_map(
        hw_pair.groupby(["customer_id", "article_id"])["w"].sum()
    )

    prod_key = pd.MultiIndex.from_arrays([
        cid, X["raw_i_product_code"].to_numpy()
    ])
    prod_counts = h30.groupby(["customer_id", "product_code"]).size()
    out["f_user_product_count_30d"] = prod_counts.reindex(
        prod_key
    ).fillna(0).to_numpy()

    categories = (
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
        ("section_no", "raw_i_section_no", "section"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
        ("colour_group_code", "raw_i_colour_group_code", "colour"),
    )
    user30 = h30.groupby("customer_id").size()
    user30_arr = X["customer_id"].map(user30).fillna(0).to_numpy()

    for hc, xc, label in categories:
        k = pd.MultiIndex.from_arrays([cid, X[xc].to_numpy()])
        s = h30.groupby(["customer_id", hc]).size()
        vals = s.reindex(k).fillna(0).to_numpy()
        out["f_user_" + label + "_count_30d"] = vals
        if label in ("type", "department"):
            out["f_user_" + label + "_ratio_30d"] = np.divide(
                vals, user30_arr,
                out=np.zeros(len(X), dtype=float),
                where=user30_arr > 0
            )

    out["f_type_count_7d"] = X["raw_i_product_type_no"].map(
        h7.groupby("product_type_no").size()
    ).fillna(0).to_numpy()

    out["f_department_count_7d"] = X["raw_i_department_no"].map(
        h7.groupby("department_no").size()
    ).fillna(0).to_numpy()

    out["f_item_mean_price"] = X["article_id"].map(
        h.groupby("article_id")["price"].mean()
    ).to_numpy()

    out["f_user_mean_price"] = X["customer_id"].map(
        h.groupby("customer_id")["price"].mean()
    ).to_numpy()

    return out[names]
