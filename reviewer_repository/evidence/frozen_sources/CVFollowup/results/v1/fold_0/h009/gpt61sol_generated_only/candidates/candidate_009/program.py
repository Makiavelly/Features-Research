def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    n = len(X)

    static = {
        "f_u_age": "raw_u_age",
        "f_u_fn": "raw_u_fn",
        "f_u_active": "raw_u_active",
        "f_u_club_member_status": "raw_u_club_member_status",
        "f_u_fashion_news_frequency": "raw_u_fashion_news_frequency",
        "f_i_product_code": "raw_i_product_code",
        "f_i_product_type_no": "raw_i_product_type_no",
        "f_i_graphical_appearance_no": "raw_i_graphical_appearance_no",
        "f_i_colour_group_code": "raw_i_colour_group_code",
        "f_i_perceived_colour_value_id": "raw_i_perceived_colour_value_id",
        "f_i_perceived_colour_master_id": "raw_i_perceived_colour_master_id",
        "f_i_department_no": "raw_i_department_no",
        "f_i_index_group_no": "raw_i_index_group_no",
        "f_i_section_no": "raw_i_section_no",
        "f_i_garment_group_no": "raw_i_garment_group_no",
    }
    for name, col in static.items():
        out[name] = X[col].to_numpy()

    h = history
    empty_names = [
        "f_item_count_1d", "f_item_count_7d", "f_item_count_30d",
        "f_item_count_90d", "f_item_recency", "f_customer_recency",
        "f_customer_count_7d", "f_customer_count_30d", "f_customer_count_90d",
        "f_exact_count", "f_exact_recent_count", "f_exact_recency",
        "f_customer_department_count", "f_customer_section_count",
        "f_customer_product_type_count", "f_customer_product_code_count",
        "f_customer_department_recency", "f_customer_section_recency",
        "f_department_popularity", "f_section_popularity", "f_item_mean_price"
    ]
    if h.empty:
        for name in empty_names:
            out[name] = np.nan if name.endswith(("recency", "price")) else 0.0
        return out

    def amap(series, key):
        return X[key].map(series).to_numpy()

    for w in (1, 7, 30, 90):
        g = h.loc[h["days_ago"] <= w].groupby("article_id").size()
        out["f_item_count_" + str(w) + "d"] = amap(g, "article_id")

    out["f_item_recency"] = amap(h.groupby("article_id")["days_ago"].min(), "article_id")
    for w in (7, 30, 90):
        g = h.loc[h["days_ago"] <= w].groupby("customer_id").size()
        out["f_customer_count_" + str(w) + "d"] = amap(g, "customer_id")
    out["f_customer_recency"] = amap(h.groupby("customer_id")["days_ago"].min(), "customer_id")

    keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])
    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(["size", "min"])
    out["f_exact_count"] = pair["size"].reindex(keys).fillna(0).to_numpy()
    out["f_exact_recency"] = pair["min"].reindex(keys).to_numpy()
    recent_pair = h.loc[h["days_ago"] <= 30].groupby(
        ["customer_id", "article_id"]).size()
    out["f_exact_recent_count"] = recent_pair.reindex(keys).fillna(0).to_numpy()

    for col in ("department_no", "section_no", "product_type_no", "product_code"):
        g = h.groupby(["customer_id", col]).size()
        k = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()
        ])
        out["f_customer_" + col.replace("_no", "") + "_count"] = g.reindex(k).fillna(0).to_numpy()

    for col in ("department_no", "section_no"):
        g = h.groupby(["customer_id", col])["days_ago"].min()
        k = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X["raw_i_" + col].to_numpy()
        ])
        out["f_customer_" + col.replace("_no", "") + "_recency"] = g.reindex(k).to_numpy()

    for col in ("department_no", "section_no"):
        g = h.loc[h["days_ago"] <= 30].groupby(col).size()
        out["f_" + col.replace("_no", "") + "_popularity"] = amap(
            g, "raw_i_" + col
        )

    out["f_item_mean_price"] = amap(h.groupby("article_id")["price"].mean(), "article_id")
    return out.replace([np.inf, -np.inf], np.nan)
