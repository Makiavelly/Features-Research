import pandas as pd
import numpy as np

def modify_features(X, history):
    n = len(X)
    cols = [
        "f_item_7d", "f_item_30d", "f_item_90d", "f_item_all",
        "f_item_recency", "f_customer_7d", "f_customer_30d",
        "f_customer_all", "f_customer_recency", "f_pair_all",
        "f_pair_30d", "f_pair_recency", "f_product_affinity",
        "f_department_affinity", "f_section_affinity",
        "f_garment_affinity", "f_recent_category_affinity"
    ]
    out = pd.DataFrame(index=X.index)
    if history is None or len(history) == 0:
        for z in cols:
            out[z] = 0.0
        return out

    h = history
    c = X["customer_id"]
    a = X["article_id"]

    h7 = h[h["days_ago"] <= 7]
    h30 = h[h["days_ago"] <= 30]
    h90 = h[h["days_ago"] <= 90]

    def count_map(frame, key):
        return a.map(frame.groupby(key, sort=False).size()).fillna(0)

    out["f_item_7d"] = count_map(h7, "article_id")
    out["f_item_30d"] = count_map(h30, "article_id")
    out["f_item_90d"] = count_map(h90, "article_id")
    out["f_item_all"] = count_map(h, "article_id")
    out["f_item_recency"] = a.map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    )

    out["f_customer_7d"] = c.map(h7.groupby("customer_id").size()).fillna(0)
    out["f_customer_30d"] = c.map(h30.groupby("customer_id").size()).fillna(0)
    out["f_customer_all"] = c.map(h.groupby("customer_id").size()).fillna(0)
    out["f_customer_recency"] = c.map(
        h.groupby("customer_id", sort=False)["days_ago"].min()
    )

    hk = h["customer_id"].astype(str) + "|" + h["article_id"].astype(str)
    xk = c.astype(str) + "|" + a.astype(str)
    out["f_pair_all"] = xk.map(hk.value_counts()).fillna(0)

    hk30 = h30["customer_id"].astype(str) + "|" + h30["article_id"].astype(str)
    out["f_pair_30d"] = xk.map(hk30.value_counts()).fillna(0)
    out["f_pair_recency"] = xk.map(
        h.assign(_k=hk).groupby("_k", sort=False)["days_ago"].min()
    )

    pairs = [
        ("product_code", "raw_i_product_code", "f_product_affinity"),
        ("department_no", "raw_i_department_no", "f_department_affinity"),
        ("section_no", "raw_i_section_no", "f_section_affinity"),
        ("garment_group_no", "raw_i_garment_group_no", "f_garment_affinity")
    ]
    for hc, xc, name in pairs:
        kh = h["customer_id"].astype(str) + "|" + h[hc].astype(str)
        kx = c.astype(str) + "|" + X[xc].astype(str)
        out[name] = kx.map(kh.value_counts()).fillna(0)

    catcols = ["product_code", "department_no", "section_no", "garment_group_no"]
    recent = h30.copy()
    recent["_cat"] = recent[catcols].astype(str).agg("|".join, axis=1)
    xcat = X[["raw_i_product_code", "raw_i_department_no",
               "raw_i_section_no", "raw_i_garment_group_no"]].astype(str)
    xcat = xcat.agg("|".join, axis=1)
    kh = recent["customer_id"].astype(str) + "|" + recent["_cat"]
    kx = c.astype(str) + "|" + xcat
    out["f_recent_category_affinity"] = kx.map(kh.value_counts()).fillna(0)

    return out.astype(float)
