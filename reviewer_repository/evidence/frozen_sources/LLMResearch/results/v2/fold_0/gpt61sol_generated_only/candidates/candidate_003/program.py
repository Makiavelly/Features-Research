import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)
    h = history
    windows = {"7": h[h["days_ago"] <= 7], "30": h[h["days_ago"] <= 30]}
    if len(h) == 0:
        cols = [
            "f_item_all", "f_item_7", "f_item_30", "f_item_recency",
            "f_user_all", "f_user_7", "f_user_30", "f_user_recency",
            "f_pair_all", "f_pair_30", "f_price_mean_item", "f_price_mean_user",
            "f_cat_product_code_30", "f_cat_department_no_30",
            "f_cat_section_no_30", "f_cat_garment_group_no_30"
        ]
        return pd.DataFrame({c: np.zeros(n) for c in cols}, index=X.index)

    def map_count(s, key):
        return X[key].map(s).fillna(0).to_numpy()

    ia = h.groupby("article_id").size()
    i7 = windows["7"].groupby("article_id").size()
    i30 = windows["30"].groupby("article_id").size()
    ir = h.groupby("article_id")["days_ago"].min()
    ua = h.groupby("customer_id").size()
    u7 = windows["7"].groupby("customer_id").size()
    u30 = windows["30"].groupby("customer_id").size()
    ur = h.groupby("customer_id")["days_ago"].min()

    out["f_item_all"] = map_count(ia, "article_id")
    out["f_item_7"] = map_count(i7, "article_id")
    out["f_item_30"] = map_count(i30, "article_id")
    out["f_item_recency"] = X["article_id"].map(ir)
    out["f_user_all"] = map_count(ua, "customer_id")
    out["f_user_7"] = map_count(u7, "customer_id")
    out["f_user_30"] = map_count(u30, "customer_id")
    out["f_user_recency"] = X["customer_id"].map(ur)

    keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])
    pa = h.groupby(["customer_id", "article_id"]).size()
    p30 = windows["30"].groupby(["customer_id", "article_id"]).size()
    out["f_pair_all"] = pa.reindex(keys, fill_value=0).to_numpy()
    out["f_pair_30"] = p30.reindex(keys, fill_value=0).to_numpy()

    ip = h.groupby("article_id")["price"].mean()
    up = h.groupby("customer_id")["price"].mean()
    out["f_price_mean_item"] = X["article_id"].map(ip)
    out["f_price_mean_user"] = X["customer_id"].map(up)

    for cat in ["product_code", "department_no", "section_no", "garment_group_no"]:
        g = windows["30"].groupby(["customer_id", cat]).size()
        k = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X["raw_i_" + cat].to_numpy()
        ])
        out["f_cat_" + cat + "_30"] = g.reindex(k, fill_value=0).to_numpy()

    return out.apply(pd.to_numeric, errors="coerce")
