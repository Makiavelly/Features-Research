def modify_features(X, history):
    import pandas as pd
    import numpy as np

    static = [
        "raw_u_age", "raw_u_fn", "raw_u_active",
        "raw_u_club_member_status", "raw_u_fashion_news_frequency",
        "raw_i_product_code", "raw_i_product_type_no",
        "raw_i_graphical_appearance_no", "raw_i_colour_group_code",
        "raw_i_perceived_colour_value_id", "raw_i_perceived_colour_master_id",
        "raw_i_department_no", "raw_i_index_group_no",
        "raw_i_section_no", "raw_i_garment_group_no",
    ]
    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_count_all", "f_item_decay", "f_item_recency",
        "f_user_count_7d", "f_user_count_30d", "f_user_count_all",
        "f_user_recency", "f_pair_count_7d", "f_pair_count_all",
        "f_pair_recency", "f_user_type_count_30d",
        "f_user_department_count_30d", "f_user_section_count_30d",
        "f_user_garment_count_30d", "f_user_product_count_30d",
        "f_item_mean_price",
    ] + ["f_" + c.lower() for c in static]

    out = pd.DataFrame(index=X.index)
    for n in names:
        out[n] = 0.0

    for c in static:
        if c in X.columns:
            out["f_" + c.lower()] = pd.to_numeric(
                X[c], errors="coerce"
            ).to_numpy()

    if history is None or len(history) == 0:
        return out[names]

    h = history
    d = pd.to_numeric(h["days_ago"], errors="coerce")
    item = h["article_id"]
    user = h["customer_id"]

    for w in (7, 30, 90):
        s = item.loc[d <= w].value_counts()
        out["f_item_count_%dd" % w] = X["article_id"].map(s).fillna(0).to_numpy()

    all_item = item.value_counts()
    out["f_item_count_all"] = X["article_id"].map(all_item).fillna(0).to_numpy()

    decay = h.assign(_decay=np.exp(-d.clip(lower=0) / 14.0)).groupby(
        "article_id"
    )["_decay"].sum()
    out["f_item_decay"] = X["article_id"].map(decay).fillna(0).to_numpy()

    item_rec = h.groupby("article_id")["days_ago"].min()
    out["f_item_recency"] = X["article_id"].map(item_rec).to_numpy()

    for w in (7, 30):
        s = user.loc[d <= w].value_counts()
        out["f_user_count_%dd" % w] = X["customer_id"].map(s).fillna(0).to_numpy()
    us = user.value_counts()
    out["f_user_count_all"] = X["customer_id"].map(us).fillna(0).to_numpy()
    ur = h.groupby("customer_id")["days_ago"].min()
    out["f_user_recency"] = X["customer_id"].map(ur).to_numpy()

    def pair_values(frame, column):
        g = frame.groupby(["customer_id", "article_id"])[column].agg(
            "size" if column == "_n" else "min"
        )
        k = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        return g.reindex(k).to_numpy()

    h7 = h.loc[d <= 7].copy()
    h7["_n"] = 1
    ha = h.copy()
    ha["_n"] = 1
    out["f_pair_count_7d"] = np.nan_to_num(pair_values(h7, "_n"), nan=0.0)
    out["f_pair_count_all"] = np.nan_to_num(pair_values(ha, "_n"), nan=0.0)
    out["f_pair_recency"] = pair_values(h, "days_ago")

    def user_category(hist_col, raw_col, feature):
        z = h.loc[d <= 30].groupby(["customer_id", hist_col]).size()
        k = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X[raw_col].to_numpy(),
        ])
        out[feature] = z.reindex(k).fillna(0).to_numpy()

    user_category("product_type_no", "raw_i_product_type_no",
                  "f_user_type_count_30d")
    user_category("department_no", "raw_i_department_no",
                  "f_user_department_count_30d")
    user_category("section_no", "raw_i_section_no",
                  "f_user_section_count_30d")
    user_category("garment_group_no", "raw_i_garment_group_no",
                  "f_user_garment_count_30d")
    user_category("product_code", "raw_i_product_code",
                  "f_user_product_count_30d")

    mean_price = h.groupby("article_id")["price"].mean()
    out["f_item_mean_price"] = X["article_id"].map(mean_price).to_numpy()

    return out[names]
