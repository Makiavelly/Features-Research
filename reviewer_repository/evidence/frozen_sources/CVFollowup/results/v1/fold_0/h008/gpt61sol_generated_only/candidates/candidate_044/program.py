import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    c, a = X["customer_id"], X["article_id"]

    def mapped(keys, values, default=0.0):
        return keys.map(values).fillna(default).to_numpy()

    def pair_mapped(values, default=0.0):
        keys = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return values.reindex(keys).fillna(default).to_numpy()

    h = history
    if h.empty:
        for name in (
            "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
            "f_item_count_all", "f_item_recency", "f_item_mean_price",
            "f_user_count_30d", "f_user_count_all",
            "f_pair_count_30d", "f_pair_count_all", "f_pair_recency",
            "f_user_department_count", "f_user_type_count",
        ):
            out[name] = np.nan if "recency" in name else 0.0
        return out

    for window in (7, 30, 90):
        q = h.loc[h["days_ago"] <= window]
        out[f"f_item_count_{window}d"] = mapped(a, q.groupby("article_id").size())
    ig = h.groupby("article_id")
    ug = h.groupby("customer_id")
    pg = h.groupby(["customer_id", "article_id"])

    out["f_item_count_all"] = mapped(a, ig.size())
    out["f_item_recency"] = mapped(a, ig["days_ago"].min(), np.nan)
    out["f_item_mean_price"] = mapped(a, ig["price"].mean(), np.nan)

    q = h.loc[h["days_ago"] <= 30]
    out["f_user_count_30d"] = mapped(c, q.groupby("customer_id").size())
    out["f_user_count_all"] = mapped(c, ug.size())
    out["f_pair_count_30d"] = pair_mapped(
        q.groupby(["customer_id", "article_id"]).size()
    )
    out["f_pair_count_all"] = pair_mapped(pg.size())
    out["f_pair_recency"] = pair_mapped(pg["days_ago"].min(), np.nan)

    for hc, xc, name in (
        ("department_no", "raw_i_department_no", "f_user_department_count"),
        ("product_type_no", "raw_i_product_type_no", "f_user_type_count"),
    ):
        counts = h.groupby(["customer_id", hc]).size()
        keys = pd.MultiIndex.from_arrays([c.to_numpy(), X[xc].to_numpy()])
        out[name] = counts.reindex(keys).fillna(0).to_numpy()

    for field in ("raw_u_age", "raw_u_fn", "raw_u_active",
                  "raw_u_club_member_status", "raw_u_fashion_news_frequency",
                  "raw_i_product_code", "raw_i_product_type_no",
                  "raw_i_graphical_appearance_no", "raw_i_colour_group_code",
                  "raw_i_perceived_colour_value_id", "raw_i_perceived_colour_master_id",
                  "raw_i_department_no", "raw_i_index_group_no",
                  "raw_i_section_no", "raw_i_garment_group_no"):
        out["f_" + field] = pd.to_numeric(X[field], errors="coerce").to_numpy()

    return out.reindex(X.index)
