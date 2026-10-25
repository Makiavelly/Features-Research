import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    c, a, h = X["customer_id"], X["article_id"], history

    def mp(s, k, fill=0):
        return k.map(s).fillna(fill).to_numpy()

    def kp(s, k1, k2, fill=0):
        d = dict(zip(s.index.tolist(), s.to_numpy()))
        z = pd.Series(list(zip(k1.to_numpy(), k2.to_numpy())), index=X.index)
        return z.map(d).fillna(fill).to_numpy()

    names = [
        "f_user_count","f_item_count","f_pair_count","f_user_unique",
        "f_item_unique","f_user_recency","f_item_recency","f_pair_recency",
        "f_user_7d","f_item_7d","f_pair_7d","f_user_30d","f_item_30d",
        "f_pair_30d","f_user_90d","f_item_90d","f_pair_90d",
        "f_user_decay","f_item_decay","f_pair_decay","f_item_recent",
        "f_product_pop","f_type_pop","f_department_pop","f_section_pop",
        "f_garment_pop","f_user_product","f_user_type","f_user_department",
        "f_user_section","f_user_garment","f_item_price","f_user_price",
        "f_age","f_active"
    ]
    for n in names:
        out[n] = 0.0
    out["f_age"] = X["raw_u_age"].fillna(-1).to_numpy()
    out["f_active"] = X["raw_u_active"].fillna(-1).to_numpy()
    if len(h) == 0:
        return out

    ug = h.groupby("customer_id", sort=False)
    ig = h.groupby("article_id", sort=False)
    pg = h.groupby(["customer_id", "article_id"], sort=False)

    out["f_user_count"] = mp(ug.size(), c)
    out["f_item_count"] = mp(ig.size(), a)
    out["f_pair_count"] = kp(pg.size(), c, a)
    out["f_user_unique"] = mp(ug["article_id"].nunique(), c)
    out["f_item_unique"] = mp(ig["customer_id"].nunique(), a)
    out["f_user_recency"] = mp(ug["days_ago"].min(), c, 9999)
    out["f_item_recency"] = mp(ig["days_ago"].min(), a, 9999)
    out["f_pair_recency"] = kp(pg["days_ago"].min(), c, a, 9999)

    q = h.copy()
    q["_w"] = np.exp(-q["days_ago"].clip(lower=0).to_numpy() / 30.0)
    out["f_user_decay"] = mp(q.groupby("customer_id")["_w"].sum(), c)
    out["f_item_decay"] = mp(q.groupby("article_id")["_w"].sum(), a)
    out["f_pair_decay"] = kp(q.groupby(["customer_id", "article_id"])["_w"].sum(), c, a)

    for d, t in ((7, "7d"), (30, "30d"), (90, "90d")):
        z = h.loc[h["days_ago"] <= d]
        out["f_user_" + t] = mp(z.groupby("customer_id").size(), c)
        out["f_item_" + t] = mp(z.groupby("article_id").size(), a)
        out["f_pair_" + t] = kp(z.groupby(["customer_id", "article_id"]).size(), c, a)

    recent = h.loc[h["days_ago"] <= 30].groupby("article_id").size()
    out["f_item_recent"] = mp(recent, a) / np.maximum(mp(ig.size(), a), 1)

    specs = [
        ("raw_i_product_code", "product_code", "product"),
        ("raw_i_product_type_no", "product_type_no", "type"),
        ("raw_i_department_no", "department_no", "department"),
        ("raw_i_section_no", "section_no", "section"),
        ("raw_i_garment_group_no", "garment_group_no", "garment")
    ]
    for raw, hc, tag in specs:
        v = X[raw]
        out["f_" + tag + "_pop"] = np.log1p(mp(h.groupby(hc).size(), v))
        out["f_user_" + tag] = kp(h.groupby(["customer_id", hc]).size(), c, v)

    mean_price = float(h["price"].mean())
    out["f_item_price"] = mp(ig["price"].mean(), a, mean_price)
    out["f_user_price"] = mp(ug["price"].mean(), c, mean_price)
    return out
