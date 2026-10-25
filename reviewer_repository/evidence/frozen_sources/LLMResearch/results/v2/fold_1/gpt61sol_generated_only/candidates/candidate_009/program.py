import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    c = X["customer_id"]
    a = X["article_id"]
    h = history

    def mp(s, key, default=0.0):
        return key.map(s).fillna(default).to_numpy()

    def pair_map(s):
        k = pd.Series(list(zip(c.to_numpy(), a.to_numpy())), index=X.index)
        return k.map(s).fillna(0).to_numpy()

    names = [
        "f_user_n","f_item_n","f_user_unique","f_item_unique",
        "f_user_recency","f_item_recency","f_pair_n","f_pair_recency",
        "f_user_n7","f_item_n7","f_user_n30","f_item_n30",
        "f_user_n90","f_item_n90","f_pair_n30","f_pair_n90",
        "f_item_recent_share","f_item_popularity","f_user_mean_price",
        "f_item_mean_price","f_user_product_affinity","f_user_type_affinity",
        "f_user_department_affinity","f_user_section_affinity",
        "f_user_garment_affinity","f_product_popularity","f_type_popularity",
        "f_department_popularity","f_section_popularity","f_garment_popularity",
        "f_item_product","f_item_type","f_item_department","f_item_section",
        "f_item_garment"
    ]
    for z in names:
        out[z] = 0.0

    if len(h) == 0:
        return out

    ug = h.groupby("customer_id", sort=False)
    ig = h.groupby("article_id", sort=False)

    out["f_user_n"] = mp(ug.size(), c)
    out["f_item_n"] = mp(ig.size(), a)
    out["f_user_unique"] = mp(ug["article_id"].nunique(), c)
    out["f_item_unique"] = mp(ig["customer_id"].nunique(), a)
    out["f_user_recency"] = mp(ug["days_ago"].min(), c, 9999)
    out["f_item_recency"] = mp(ig["days_ago"].min(), a, 9999)

    pairs = h.groupby(["customer_id", "article_id"], sort=False)
    out["f_pair_n"] = pair_map(dict(zip(pairs.size().index, pairs.size().values)))
    out["f_pair_recency"] = pair_map(dict(zip(pairs["days_ago"].min().index,
                                               pairs["days_ago"].min().values)))

    for d, tag in ((7, "7"), (30, "30"), (90, "90")):
        q = h.loc[h["days_ago"] <= d]
        if len(q):
            out["f_user_n" + tag] = mp(q.groupby("customer_id").size(), c)
            out["f_item_n" + tag] = mp(q.groupby("article_id").size(), a)
            if d >= 30:
                pp = q.groupby(["customer_id", "article_id"]).size()
                out["f_pair_n" + tag] = pair_map(dict(zip(pp.index, pp.values)))

    total_item = ig.size()
    recent_item = h.loc[h["days_ago"] <= 30].groupby("article_id").size()
    out["f_item_recent_share"] = (
        mp(recent_item, a) / np.maximum(mp(total_item, a), 1)
    )
    out["f_item_popularity"] = np.log1p(mp(total_item, a))
    out["f_user_mean_price"] = mp(ug["price"].mean(), c, h["price"].mean())
    out["f_item_mean_price"] = mp(ig["price"].mean(), a, h["price"].mean())

    specs = [
        ("raw_i_product_code", "product_code", "product"),
        ("raw_i_product_type_no", "product_type_no", "type"),
        ("raw_i_department_no", "department_no", "department"),
        ("raw_i_section_no", "section_no", "section"),
        ("raw_i_garment_group_no", "garment_group_no", "garment")
    ]
    for raw, hc, tag in specs:
        v = X[raw]
        pop = h.groupby(hc, sort=False).size()
        out["f_" + tag + "_popularity"] = np.log1p(mp(pop, v))
        kk = pd.Series(list(zip(c.to_numpy(), v.to_numpy())), index=X.index)
        aff = h.groupby(["customer_id", hc], sort=False).size()
        dct = dict(zip(aff.index, aff.values))
        out["f_user_" + tag + "_affinity"] = kk.map(dct).fillna(0).to_numpy()
        out["f_item_" + tag] = v.fillna(-1).to_numpy()

    return out
