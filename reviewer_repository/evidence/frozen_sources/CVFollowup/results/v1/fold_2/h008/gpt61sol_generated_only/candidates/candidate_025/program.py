import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    names = [
        "f_pair_7d", "f_pair_30d", "f_pair_90d", "f_pair_all",
        "f_pair_recency", "f_pair_decay",
        "f_customer_7d", "f_customer_30d", "f_customer_90d",
        "f_customer_all", "f_customer_recency", "f_customer_decay",
        "f_item_7d", "f_item_30d", "f_item_90d", "f_item_all",
        "f_item_recency", "f_item_decay",
        "f_customer_type_90d", "f_customer_section_90d",
        "f_customer_colour_90d", "f_customer_garment_90d",
        "f_customer_product_90d", "f_product_type_all",
        "f_product_code_all", "f_item_product_type",
        "f_user_age", "f_user_active"
    ]
    if history is None or len(history) == 0:
        for n in names:
            if n == "f_item_product_type":
                v = X["raw_i_product_type_no"]
            elif n == "f_user_age":
                v = X["raw_u_age"]
            elif n == "f_user_active":
                v = X["raw_u_active"]
            else:
                v = 0.0
            out[n] = pd.to_numeric(v, errors="coerce")
        return out.astype(float)

    h = history.reset_index(drop=True)
    c = X["customer_id"]
    a = X["article_id"]

    def key(x, y):
        return x.astype("string").fillna("<NA>") + "|" + y.astype("string").fillna("<NA>")

    hk_pair = key(h["customer_id"], h["article_id"])
    xk_pair = key(c, a)
    d = pd.to_numeric(h["days_ago"], errors="coerce").fillna(999999.0)
    decay = np.exp(-d / 30.0)

    def mapped(group, keys, default=0.0):
        return keys.map(group).fillna(default).to_numpy()

    for w, n in ((7, "f_pair_7d"), (30, "f_pair_30d"), (90, "f_pair_90d")):
        m = d <= w
        out[n] = mapped(h.loc[m].groupby(hk_pair.loc[m]).size(), xk_pair)
    out["f_pair_all"] = mapped(hk_pair.groupby(hk_pair).size(), xk_pair)
    out["f_pair_recency"] = xk_pair.map(d.groupby(hk_pair).min()).to_numpy()
    out["f_pair_decay"] = mapped(decay.groupby(hk_pair).sum(), xk_pair)

    for w, n in ((7, "f_customer_7d"), (30, "f_customer_30d"),
                 (90, "f_customer_90d")):
        m = d <= w
        out[n] = mapped(h.loc[m].groupby(h["customer_id"].loc[m]).size(), c)
    out["f_customer_all"] = mapped(h.groupby("customer_id").size(), c)
    out["f_customer_recency"] = c.map(d.groupby(h["customer_id"]).min()).to_numpy()
    out["f_customer_decay"] = mapped(decay.groupby(h["customer_id"]).sum(), c)

    for w, n in ((7, "f_item_7d"), (30, "f_item_30d"), (90, "f_item_90d")):
        m = d <= w
        out[n] = mapped(h.loc[m].groupby(h["article_id"].loc[m]).size(), a)
    out["f_item_all"] = mapped(h.groupby("article_id").size(), a)
    out["f_item_recency"] = a.map(d.groupby(h["article_id"]).min()).to_numpy()
    out["f_item_decay"] = mapped(decay.groupby(h["article_id"]).sum(), a)

    recent = d <= 90
    for raw, col, n in (
        ("raw_i_product_type_no", "product_type_no", "f_customer_type_90d"),
        ("raw_i_section_no", "section_no", "f_customer_section_90d"),
        ("raw_i_colour_group_code", "colour_group_code", "f_customer_colour_90d"),
        ("raw_i_garment_group_no", "garment_group_no", "f_customer_garment_90d"),
        ("raw_i_product_code", "product_code", "f_customer_product_90d"),
    ):
        kh = key(h.loc[recent, "customer_id"], h.loc[recent, col])
        kx = key(c, X[raw])
        out[n] = mapped(h.loc[recent].groupby(kh).size(), kx)

    out["f_product_type_all"] = mapped(
        h.groupby("product_type_no").size(), X["raw_i_product_type_no"])
    out["f_product_code_all"] = mapped(
        h.groupby("product_code").size(), X["raw_i_product_code"])
    out["f_item_product_type"] = pd.to_numeric(
        X["raw_i_product_type_no"], errors="coerce").to_numpy()
    out["f_user_age"] = pd.to_numeric(X["raw_u_age"], errors="coerce").to_numpy()
    out["f_user_active"] = pd.to_numeric(
        X["raw_u_active"], errors="coerce").to_numpy()
    return out.astype(float)
