import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    c = X["customer_id"]
    a = X["article_id"]
    static_fields = [
        "raw_u_age", "raw_u_fn", "raw_u_active",
        "raw_u_club_member_status", "raw_u_fashion_news_frequency",
        "raw_i_product_code", "raw_i_product_type_no",
        "raw_i_graphical_appearance_no", "raw_i_colour_group_code",
        "raw_i_perceived_colour_value_id", "raw_i_perceived_colour_master_id",
        "raw_i_department_no", "raw_i_index_group_no", "raw_i_section_no",
        "raw_i_garment_group_no"
    ]
    for field in static_fields:
        out["f_" + field] = pd.to_numeric(X[field], errors="coerce").to_numpy()

    item_windows = (7, 30, 90)
    user_windows = (7, 30, 90)
    pair_windows = (7, 30, 90)
    for w in item_windows:
        out[f"f_item_purchases_{w}d"] = 0.0
    for w in user_windows:
        out[f"f_user_purchases_{w}d"] = 0.0
    for w in pair_windows:
        out[f"f_user_item_purchases_{w}d"] = 0.0
    for name in ("f_item_purchases_all", "f_item_recency", "f_item_mean_price",
                 "f_user_purchases_all", "f_user_recency",
                 "f_user_distinct_articles", "f_user_item_purchases_all",
                 "f_user_item_recency", "f_user_item_share"):
        out[name] = np.nan if "recency" in name else 0.0
    for name in ("f_user_department_purchases", "f_user_product_type_purchases",
                 "f_user_colour_purchases", "f_user_section_purchases"):
        out[name] = 0.0

    if history.empty:
        return out.reindex(X.index)

    h = history
    d = h["days_ago"]

    def map_item(s):
        return a.map(s).fillna(0).to_numpy()

    def map_user(s):
        return c.map(s).fillna(0).to_numpy()

    keys = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])

    def map_pair(s):
        return s.reindex(keys).fillna(0).to_numpy()

    for w in (7, 30, 90):
        q = h.loc[d <= w]
        out[f"f_item_purchases_{w}d"] = map_item(q.groupby("article_id").size())
        out[f"f_user_purchases_{w}d"] = map_user(q.groupby("customer_id").size())
        out[f"f_user_item_purchases_{w}d"] = map_pair(
            q.groupby(["customer_id", "article_id"]).size()
        )

    ig = h.groupby("article_id")
    ug = h.groupby("customer_id")
    pg = h.groupby(["customer_id", "article_id"])
    out["f_item_purchases_all"] = map_item(ig.size())
    out["f_item_recency"] = a.map(ig["days_ago"].min()).to_numpy()
    out["f_item_mean_price"] = a.map(ig["price"].mean()).to_numpy()
    out["f_user_purchases_all"] = map_user(ug.size())
    out["f_user_recency"] = c.map(ug["days_ago"].min()).to_numpy()
    out["f_user_distinct_articles"] = map_user(ug["article_id"].nunique())
    pair_counts = pg.size()
    out["f_user_item_purchases_all"] = map_pair(pair_counts)
    out["f_user_item_recency"] = map_pair(pg["days_ago"].min())
    out["f_user_item_share"] = map_pair(pair_counts) / np.maximum(
        map_user(ug.size()), 1
    )

    for hc, xc, name in (
        ("department_no", "raw_i_department_no", "f_user_department_purchases"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_type_purchases"),
        ("colour_group_code", "raw_i_colour_group_code", "f_user_colour_purchases"),
        ("section_no", "raw_i_section_no", "f_user_section_purchases"),
    ):
        cat_keys = pd.MultiIndex.from_arrays([c.to_numpy(), X[xc].to_numpy()])
        counts = h.groupby(["customer_id", hc]).size()
        out[name] = counts.reindex(cat_keys).fillna(0).to_numpy()

    return out.reindex(X.index)
