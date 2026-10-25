import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_pair_recency","f_pair_count","f_pair_7d","f_user_7d","f_user_30d",
        "f_user_all","f_user_recency","f_item_7d","f_item_30d","f_item_90d",
        "f_item_all","f_item_recency","f_item_price","f_user_price",
        "f_type_7d","f_type_30d","f_dept_30d","f_section_30d","f_garment_30d",
        "f_colour_30d","f_value_30d","f_master_30d","f_product_code",
        "f_product_type","f_department","f_section","f_garment_group",
        "f_graphical","f_colour","f_value","f_master_colour","f_index_group",
        "f_user_age","f_user_fn","f_user_active","f_user_club"
    ]
    out = pd.DataFrame(index=X.index)
    if history is None or len(history) == 0:
        for c in names:
            out[c] = 0.0
        return out

    h = history
    u, a = X["customer_id"], X["article_id"]

    def umap(s, default=0.0):
        return u.map(s).fillna(default).to_numpy()

    def amap(s, default=0.0):
        return a.map(s).fillna(default).to_numpy()

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(
        rec="min", cnt="size"
    )
    keys = pd.MultiIndex.from_arrays([u.to_numpy(), a.to_numpy()])
    out["f_pair_recency"] = pd.Series(pair["rec"]).reindex(keys).fillna(9999).to_numpy()
    out["f_pair_count"] = np.log1p(
        pd.Series(pair["cnt"]).reindex(keys).fillna(0).to_numpy()
    )
    out["f_pair_7d"] = (out["f_pair_recency"] <= 7).astype(float)

    for d, c in [(7, "f_user_7d"), (30, "f_user_30d")]:
        out[c] = np.log1p(umap(
            h.loc[h["days_ago"] <= d].groupby("customer_id").size()
        ))
    out["f_user_all"] = np.log1p(umap(h.groupby("customer_id").size()))
    out["f_user_recency"] = umap(h.groupby("customer_id")["days_ago"].min(), 9999)

    for d, c in [(7, "f_item_7d"), (30, "f_item_30d"), (90, "f_item_90d")]:
        out[c] = np.log1p(amap(
            h.loc[h["days_ago"] <= d].groupby("article_id").size()
        ))
    out["f_item_all"] = np.log1p(amap(h.groupby("article_id").size()))
    out["f_item_recency"] = amap(h.groupby("article_id")["days_ago"].min(), 9999)
    out["f_item_price"] = amap(h.groupby("article_id")["price"].mean())
    out["f_user_price"] = umap(h.groupby("customer_id")["price"].mean())

    def match(hc, xc, name, days):
        z = h.loc[h["days_ago"] <= days].groupby(["customer_id", hc]).size()
        k = pd.MultiIndex.from_arrays([u.to_numpy(), X[xc].to_numpy()])
        out[name] = np.log1p(pd.Series(z).reindex(k).fillna(0).to_numpy())

    match("product_type_no", "raw_i_product_type_no", "f_type_7d", 7)
    match("product_type_no", "raw_i_product_type_no", "f_type_30d", 30)
    match("department_no", "raw_i_department_no", "f_dept_30d", 30)
    match("section_no", "raw_i_section_no", "f_section_30d", 30)
    match("garment_group_no", "raw_i_garment_group_no", "f_garment_30d", 30)
    match("colour_group_code", "raw_i_colour_group_code", "f_colour_30d", 30)
    match("perceived_colour_value_id", "raw_i_perceived_colour_value_id",
          "f_value_30d", 30)
    match("perceived_colour_master_id", "raw_i_perceived_colour_master_id",
          "f_master_30d", 30)

    out["f_product_code"] = X["raw_i_product_code"].to_numpy(float)
    out["f_product_type"] = X["raw_i_product_type_no"].to_numpy(float)
    out["f_department"] = X["raw_i_department_no"].to_numpy(float)
    out["f_section"] = X["raw_i_section_no"].to_numpy(float)
    out["f_garment_group"] = X["raw_i_garment_group_no"].to_numpy(float)
    out["f_graphical"] = X["raw_i_graphical_appearance_no"].to_numpy(float)
    out["f_colour"] = X["raw_i_colour_group_code"].to_numpy(float)
    out["f_value"] = X["raw_i_perceived_colour_value_id"].to_numpy(float)
    out["f_master_colour"] = X["raw_i_perceived_colour_master_id"].to_numpy(float)
    out["f_index_group"] = X["raw_i_index_group_no"].to_numpy(float)
    out["f_user_age"] = X["raw_u_age"].to_numpy(float)
    out["f_user_fn"] = X["raw_u_fn"].to_numpy(float)
    out["f_user_active"] = X["raw_u_active"].to_numpy(float)
    out["f_user_club"] = X["raw_u_club_member_status"].to_numpy(float)
    return out.replace([np.inf, -np.inf], np.nan)
