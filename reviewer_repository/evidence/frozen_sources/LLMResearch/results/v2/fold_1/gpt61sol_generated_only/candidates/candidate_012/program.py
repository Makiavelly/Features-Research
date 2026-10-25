import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    c = X["customer_id"]
    a = X["article_id"]
    h = history

    def one(s, k, default=0.0):
        return k.map(s).fillna(default).to_numpy()

    def pair_values(s, default=0.0):
        k = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return pd.Series(s.reindex(k).to_numpy(), index=X.index).fillna(default).to_numpy()

    cols = [
        "f_user_count", "f_item_count", "f_pair_count",
        "f_user_recency", "f_item_recency", "f_pair_recency",
        "f_user_weight", "f_item_weight", "f_pair_weight",
        "f_user_count_7d", "f_item_count_7d",
        "f_user_count_30d", "f_item_count_30d",
        "f_item_recent_share", "f_user_mean_price", "f_item_mean_price",
        "f_product_popularity", "f_type_popularity", "f_department_popularity",
        "f_section_popularity", "f_garment_popularity",
        "f_user_product_affinity", "f_user_type_affinity",
        "f_user_department_affinity", "f_user_section_affinity",
        "f_user_garment_affinity"
    ]
    for z in cols:
        out[z] = 0.0

    if len(h) == 0:
        return out

    ug = h.groupby("customer_id", sort=False)
    ig = h.groupby("article_id", sort=False)
    pg = h.groupby(["customer_id", "article_id"], sort=False)

    out["f_user_count"] = one(ug.size(), c)
    out["f_item_count"] = one(ig.size(), a)
    out["f_pair_count"] = pair_values(pg.size())
    out["f_user_recency"] = one(ug["days_ago"].min(), c, 9999)
    out["f_item_recency"] = one(ig["days_ago"].min(), a, 9999)
    out["f_pair_recency"] = pair_values(pg["days_ago"].min(), 9999)

    hw = h.copy()
    hw["_w"] = np.exp(-hw["days_ago"].clip(lower=0).to_numpy() / 30.0)
    uw = hw.groupby("customer_id")["_w"].sum()
    iw = hw.groupby("article_id")["_w"].sum()
    pw = hw.groupby(["customer_id", "article_id"])["_w"].sum()
    out["f_user_weight"] = one(uw, c)
    out["f_item_weight"] = one(iw, a)
    out["f_pair_weight"] = pair_values(pw)

    for d, tag in ((7, "7d"), (30, "30d")):
        q = h.loc[h["days_ago"] <= d]
        if len(q):
            out["f_user_count_" + tag] = one(q.groupby("customer_id").size(), c)
            out["f_item_count_" + tag] = one(q.groupby("article_id").size(), a)

    total = ig.size()
    recent = h.loc[h["days_ago"] <= 30].groupby("article_id").size()
    out["f_item_recent_share"] = one(recent, a) / np.maximum(one(total, a), 1)

    meanp = float(h["price"].mean())
    out["f_user_mean_price"] = one(ug["price"].mean(), c, meanp)
    out["f_item_mean_price"] = one(ig["price"].mean(), a, meanp)

    specs = [
        ("raw_i_product_code", "product_code", "product"),
        ("raw_i_product_type_no", "product_type_no", "type"),
        ("raw_i_department_no", "department_no", "department"),
        ("raw_i_section_no", "section_no", "section"),
        ("raw_i_garment_group_no", "garment_group_no", "garment")
    ]
    for raw, hc, tag in specs:
        v = X[raw]
        out["f_" + tag + "_popularity"] = np.log1p(
            one(h.groupby(hc).size(), v)
        )
        aff = h.groupby(["customer_id", hc]).size()
        kk = pd.MultiIndex.from_arrays([c.to_numpy(), v.to_numpy()])
        out["f_user_" + tag + "_affinity"] = pd.Series(
            aff.reindex(kk).to_numpy(), index=X.index
        ).fillna(0).to_numpy()

    return out
