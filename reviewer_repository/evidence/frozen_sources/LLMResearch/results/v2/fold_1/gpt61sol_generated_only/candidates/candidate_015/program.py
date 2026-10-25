import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    c = X["customer_id"]
    a = X["article_id"]
    h = history

    def smap(s, k, fill=0.0):
        return k.map(s).fillna(fill).to_numpy()

    def pmap(s, k1=c, k2=a, fill=0.0):
        ix = pd.MultiIndex.from_arrays([k1.to_numpy(), k2.to_numpy()])
        return pd.Series(s.reindex(ix).to_numpy(), index=X.index).fillna(fill).to_numpy()

    names = [
        "f_user_count","f_item_count","f_pair_count",
        "f_user_recency","f_item_recency","f_pair_recency",
        "f_user_7d","f_item_7d","f_user_30d","f_item_30d",
        "f_user_90d","f_item_90d","f_pair_30d","f_pair_90d",
        "f_user_decay","f_item_decay","f_pair_decay",
        "f_item_recent_ratio","f_user_unique_items","f_item_unique_users",
        "f_product_pop","f_type_pop","f_department_pop","f_section_pop",
        "f_garment_pop","f_user_product","f_user_type",
        "f_user_department","f_user_section","f_user_garment",
        "f_user_age","f_item_product","f_item_type",
        "f_item_department","f_item_section","f_item_garment"
    ]
    for z in names:
        out[z] = 0.0
    if len(h) == 0:
        return out

    ug = h.groupby("customer_id", sort=False)
    ag = h.groupby("article_id", sort=False)
    pg = h.groupby(["customer_id", "article_id"], sort=False)

    out["f_user_count"] = smap(ug.size(), c)
    out["f_item_count"] = smap(ag.size(), a)
    out["f_pair_count"] = pmap(pg.size())
    out["f_user_recency"] = smap(ug["days_ago"].min(), c, 9999)
    out["f_item_recency"] = smap(ag["days_ago"].min(), a, 9999)
    out["f_pair_recency"] = pmap(pg["days_ago"].min(), fill=9999)

    out["f_user_unique_items"] = smap(ug["article_id"].nunique(), c)
    out["f_item_unique_users"] = smap(ag["customer_id"].nunique(), a)

    z = h["days_ago"].clip(lower=0).to_numpy()
    q = h.copy()
    q["_decay"] = np.exp(-z / 21.0)
    out["f_user_decay"] = smap(q.groupby("customer_id")["_decay"].sum(), c)
    out["f_item_decay"] = smap(q.groupby("article_id")["_decay"].sum(), a)
    out["f_pair_decay"] = pmap(q.groupby(["customer_id","article_id"])["_decay"].sum())

    for d, tag in ((7, "7d"), (30, "30d"), (90, "90d")):
        q = h.loc[h["days_ago"] <= d]
        if len(q):
            out["f_user_" + tag] = smap(q.groupby("customer_id").size(), c)
            out["f_item_" + tag] = smap(q.groupby("article_id").size(), a)
            if d >= 30:
                out["f_pair_" + tag] = pmap(q.groupby(["customer_id","article_id"]).size())

    all_i = ag.size()
    r_i = h.loc[h["days_ago"] <= 30].groupby("article_id").size()
    out["f_item_recent_ratio"] = smap(r_i, a) / np.maximum(smap(all_i, a), 1)

    specs = [
        ("raw_i_product_code","product_code","product"),
        ("raw_i_product_type_no","product_type_no","type"),
        ("raw_i_department_no","department_no","department"),
        ("raw_i_section_no","section_no","section"),
        ("raw_i_garment_group_no","garment_group_no","garment")
    ]
    for raw, hc, tag in specs:
        v = X[raw]
        out["f_" + tag + "_pop"] = np.log1p(smap(h.groupby(hc).size(), v))
        aff = h.groupby(["customer_id", hc]).size()
        out["f_user_" + tag] = pmap(aff, c, v)
        out["f_item_" + tag] = v.fillna(-1).to_numpy()

    out["f_user_age"] = X["raw_u_age"].fillna(-1).to_numpy()
    return out
