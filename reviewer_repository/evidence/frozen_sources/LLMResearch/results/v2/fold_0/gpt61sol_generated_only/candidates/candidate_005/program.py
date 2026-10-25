import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    cols = [
        "f_pair_recency","f_pair_count","f_pair_7d","f_user_7d","f_user_30d",
        "f_user_all","f_item_7d","f_item_30d","f_item_all","f_user_recency",
        "f_item_recency","f_item_price","f_user_price","f_type_match",
        "f_dept_match","f_section_match","f_garment_match","f_colour_match",
        "f_product_code","f_product_type","f_department","f_section",
        "f_garment_group"
    ]
    if history is None or len(history) == 0:
        for c in cols:
            out[c] = 0.0
        return out

    h = history
    u = X["customer_id"]
    a = X["article_id"]

    def mapu(s, default=0.0):
        return u.map(s).fillna(default).to_numpy()

    def mapa(s, default=0.0):
        return a.map(s).fillna(default).to_numpy()

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(
        rec="min", cnt="size"
    )
    keys = pd.MultiIndex.from_arrays([u.to_numpy(), a.to_numpy()])
    out["f_pair_recency"] = pd.Series(pair["rec"]).reindex(keys).fillna(9999).to_numpy()
    pc = pd.Series(pair["cnt"]).reindex(keys).fillna(0).to_numpy()
    out["f_pair_count"] = np.log1p(pc)
    out["f_pair_7d"] = (out["f_pair_recency"] <= 7).astype(float)

    for d, c in [(7, "f_user_7d"), (30, "f_user_30d")]:
        s = h.loc[h.days_ago <= d].groupby("customer_id").size()
        out[c] = np.log1p(mapu(s))
    out["f_user_all"] = np.log1p(mapu(h.groupby("customer_id").size()))
    out["f_user_recency"] = mapu(h.groupby("customer_id").days_ago.min(), 9999)

    for d, c in [(7, "f_item_7d"), (30, "f_item_30d")]:
        s = h.loc[h.days_ago <= d].groupby("article_id").size()
        out[c] = np.log1p(mapa(s))
    out["f_item_all"] = np.log1p(mapa(h.groupby("article_id").size()))
    out["f_item_recency"] = mapa(h.groupby("article_id").days_ago.min(), 9999)
    out["f_item_price"] = mapa(h.groupby("article_id").price.mean())
    out["f_user_price"] = mapu(h.groupby("customer_id").price.mean())

    def match(hcol, xcol, name):
        z = h.loc[h.days_ago <= 30].groupby(["customer_id", hcol]).size()
        k = pd.MultiIndex.from_arrays([u.to_numpy(), X[xcol].to_numpy()])
        out[name] = np.log1p(pd.Series(z).reindex(k).fillna(0).to_numpy())

    match("product_type_no", "raw_i_product_type_no", "f_type_match")
    match("department_no", "raw_i_department_no", "f_dept_match")
    match("section_no", "raw_i_section_no", "f_section_match")
    match("garment_group_no", "raw_i_garment_group_no", "f_garment_match")
    match("colour_group_code", "raw_i_colour_group_code", "f_colour_match")

    out["f_product_code"] = X["raw_i_product_code"].to_numpy(float)
    out["f_product_type"] = X["raw_i_product_type_no"].to_numpy(float)
    out["f_department"] = X["raw_i_department_no"].to_numpy(float)
    out["f_section"] = X["raw_i_section_no"].to_numpy(float)
    out["f_garment_group"] = X["raw_i_garment_group_no"].to_numpy(float)
    return out.replace([np.inf, -np.inf], np.nan)
