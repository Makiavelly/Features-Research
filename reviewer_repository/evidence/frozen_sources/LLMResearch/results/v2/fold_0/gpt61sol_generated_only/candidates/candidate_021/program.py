import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_item_7d", "f_item_30d", "f_item_all", "f_item_recency",
        "f_item_users_30d", "f_customer_7d", "f_customer_30d",
        "f_customer_all", "f_customer_recency", "f_pair_all",
        "f_pair_30d", "f_pair_recency", "f_product_affinity",
        "f_type_affinity", "f_department_affinity", "f_section_affinity",
        "f_garment_affinity", "f_recent_category_affinity",
        "f_item_price_mean", "f_user_age", "f_user_active",
        "f_item_type", "f_item_department", "f_item_section"
    ]
    out = pd.DataFrame(index=X.index)
    if history is None or len(history) == 0:
        for z in names:
            out[z] = 0.0
        return out

    h = history
    c = X["customer_id"]
    a = X["article_id"]
    h7 = h[h["days_ago"] <= 7]
    h30 = h[h["days_ago"] <= 30]

    def icount(q):
        return a.map(q.groupby("article_id", sort=False).size()).fillna(0)

    out["f_item_7d"] = icount(h7)
    out["f_item_30d"] = icount(h30)
    out["f_item_all"] = icount(h)
    out["f_item_recency"] = a.map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    )
    users = h30.groupby("article_id", sort=False)["customer_id"].nunique()
    out["f_item_users_30d"] = a.map(users).fillna(0)

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

    for hc, xc, nm in [
        ("product_code", "raw_i_product_code", "f_product_affinity"),
        ("product_type_no", "raw_i_product_type_no", "f_type_affinity"),
        ("department_no", "raw_i_department_no", "f_department_affinity"),
        ("section_no", "raw_i_section_no", "f_section_affinity"),
        ("garment_group_no", "raw_i_garment_group_no", "f_garment_affinity")
    ]:
        kh = h["customer_id"].astype(str) + "|" + h[hc].astype(str)
        kx = c.astype(str) + "|" + X[xc].astype(str)
        out[nm] = kx.map(kh.value_counts()).fillna(0)

    rh = h30[["product_code", "product_type_no", "department_no",
              "section_no", "garment_group_no"]].astype(str).agg("|".join, axis=1)
    rx = X[["raw_i_product_code", "raw_i_product_type_no",
            "raw_i_department_no", "raw_i_section_no",
            "raw_i_garment_group_no"]].astype(str).agg("|".join, axis=1)
    out["f_recent_category_affinity"] = (
        c.astype(str) + "|" + rx
    ).map((h30["customer_id"].astype(str) + "|" + rh).value_counts()).fillna(0)

    out["f_item_price_mean"] = a.map(
        h.groupby("article_id", sort=False)["price"].mean()
    )
    out["f_user_age"] = X["raw_u_age"]
    out["f_user_active"] = X["raw_u_active"]
    out["f_item_type"] = X["raw_i_product_type_no"]
    out["f_item_department"] = X["raw_i_department_no"]
    out["f_item_section"] = X["raw_i_section_no"]
    return out.astype(float)
