import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    item_features = [
        "f_item_purchases_7d", "f_item_purchases_30d",
        "f_item_purchases_90d", "f_item_purchases_all",
        "f_item_recency", "f_item_mean_price"
    ]
    pair_features = [
        "f_user_item_purchases_7d", "f_user_item_purchases_30d",
        "f_user_item_purchases_90d", "f_user_item_purchases_all",
        "f_user_item_recency"
    ]
    user_features = [
        "f_user_purchases_7d", "f_user_purchases_30d",
        "f_user_purchases_90d", "f_user_purchases_all"
    ]
    user_cat_features = [
        "f_user_department_purchases",
        "f_user_product_type_purchases",
        "f_user_colour_purchases",
        "f_user_section_purchases"
    ]
    item_cat_features = [
        "f_item_department_purchases",
        "f_item_product_type_purchases"
    ]
    static_fields = [
        "raw_u_age", "raw_u_fn", "raw_u_active",
        "raw_u_club_member_status", "raw_u_fashion_news_frequency",
        "raw_i_product_code", "raw_i_product_type_no",
        "raw_i_graphical_appearance_no", "raw_i_colour_group_code",
        "raw_i_perceived_colour_value_id",
        "raw_i_perceived_colour_master_id", "raw_i_department_no",
        "raw_i_index_group_no", "raw_i_section_no",
        "raw_i_garment_group_no"
    ]

    for name in item_features + pair_features + user_features + user_cat_features + item_cat_features:
        out[name] = np.nan if name.endswith("recency") else 0.0

    for field in static_fields:
        out["f_" + field] = pd.to_numeric(X[field], errors="coerce").to_numpy()

    if history.empty:
        return out

    h = history
    c = X["customer_id"]
    a = X["article_id"]
    d = h["days_ago"]

    def item_map(series):
        return a.map(series).fillna(0).to_numpy()

    def user_map(series):
        return c.map(series).fillna(0).to_numpy()

    def pair_map(series):
        keys = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return series.reindex(keys).fillna(0).to_numpy()

    for window in (7, 30, 90):
        q = h.loc[d <= window]
        out[f"f_item_purchases_{window}d"] = item_map(q.groupby("article_id").size())
        out[f"f_user_purchases_{window}d"] = user_map(q.groupby("customer_id").size())
        out[f"f_user_item_purchases_{window}d"] = pair_map(
            q.groupby(["customer_id", "article_id"]).size()
        )

    ig = h.groupby("article_id")
    ug = h.groupby("customer_id")
    pg = h.groupby(["customer_id", "article_id"])

    out["f_item_purchases_all"] = item_map(ig.size())
    out["f_item_recency"] = a.map(ig["days_ago"].min()).to_numpy()
    out["f_item_mean_price"] = a.map(ig["price"].mean()).to_numpy()

    out["f_user_purchases_all"] = user_map(ug.size())
    out["f_user_item_purchases_all"] = pair_map(pg.size())
    out["f_user_item_recency"] = pair_map(pg["days_ago"].min())

    for hc, xc, name in (
        ("department_no", "raw_i_department_no", "f_user_department_purchases"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_type_purchases"),
        ("colour_group_code", "raw_i_colour_group_code", "f_user_colour_purchases"),
        ("section_no", "raw_i_section_no", "f_user_section_purchases"),
    ):
        keys = pd.MultiIndex.from_arrays([c.to_numpy(), X[xc].to_numpy()])
        counts = h.groupby(["customer_id", hc]).size()
        out[name] = counts.reindex(keys).fillna(0).to_numpy()

    for hc, xc, name in (
        ("department_no", "raw_i_department_no", "f_item_department_purchases"),
        ("product_type_no", "raw_i_product_type_no", "f_item_product_type_purchases"),
    ):
        out[name] = a.map(h.groupby(hc).size().rename_axis(None)).fillna(0).to_numpy()

    return out.reindex(X.index)
