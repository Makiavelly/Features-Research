import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_pair_30d", "f_pair_90d", "f_pair_365d", "f_pair_all",
        "f_pair_recency", "f_pair_decay",
        "f_customer_30d", "f_customer_90d", "f_customer_365d",
        "f_customer_all", "f_customer_decay",
        "f_item_30d", "f_item_90d", "f_item_365d", "f_item_all",
        "f_item_recency", "f_item_decay",
        "f_customer_product_90d", "f_customer_type_90d",
        "f_customer_colour_90d", "f_customer_section_90d",
        "f_customer_garment_90d", "f_customer_index_90d",
        "f_product_code_all", "f_product_type_all",
        "f_section_all", "f_garment_all", "f_colour_all",
        "f_article_price", "f_customer_price",
        "f_user_age", "f_user_active", "f_item_product_code",
        "f_item_product_type", "f_item_section", "f_item_colour"
    ]
    out = pd.DataFrame(index=X.index)
    for n in names:
        out[n] = 0.0

    out["f_user_age"] = pd.to_numeric(X["raw_u_age"], errors="coerce").to_numpy()
    out["f_user_active"] = pd.to_numeric(
        X["raw_u_active"], errors="coerce").to_numpy()
    out["f_item_product_code"] = pd.to_numeric(
        X["raw_i_product_code"], errors="coerce").to_numpy()
    out["f_item_product_type"] = pd.to_numeric(
        X["raw_i_product_type_no"], errors="coerce").to_numpy()
    out["f_item_section"] = pd.to_numeric(
        X["raw_i_section_no"], errors="coerce").to_numpy()
    out["f_item_colour"] = pd.to_numeric(
        X["raw_i_colour_group_code"], errors="coerce").to_numpy()

    if history is None or len(history) == 0:
        return out[names].astype(float)

    h = history.reset_index(drop=True)
    age = pd.to_numeric(h["days_ago"], errors="coerce").fillna(10**6)
    c = X["customer_id"]
    a = X["article_id"]

    def key(left, right):
        return (left.astype("string").fillna("<NA>") + "|" +
                right.astype("string").fillna("<NA>"))

    hc = h["customer_id"]
    ha = h["article_id"]
    pair_h = key(hc, ha)
    pair_x = key(c, a)

    def mapped_count(xkey, hkey, mask=None):
        if mask is None:
            return xkey.map(hkey.groupby(hkey).size()).fillna(0).to_numpy()
        return xkey.map(
            hkey.loc[mask].groupby(hkey.loc[mask]).size()
        ).fillna(0).to_numpy()

    for w, n in ((30, "f_pair_30d"), (90, "f_pair_90d"),
                 (365, "f_pair_365d")):
        out[n] = mapped_count(pair_x, pair_h, age <= w)
    out["f_pair_all"] = mapped_count(pair_x, pair_h)
    out["f_pair_recency"] = pair_x.map(
        age.groupby(pair_h).min()).to_numpy()
    decay = np.exp(-age.astype(float) / 30.0)
    out["f_pair_decay"] = pair_x.map(
        decay.groupby(pair_h).sum()).fillna(0).to_numpy()

    for w, n in ((30, "f_customer_30d"), (90, "f_customer_90d"),
                 (365, "f_customer_365d")):
        out[n] = c.map(
            hc.loc[age <= w].groupby(hc.loc[age <= w]).size()
        ).fillna(0).to_numpy()
    out["f_customer_all"] = c.map(hc.groupby(hc).size()).fillna(0).to_numpy()
    out["f_customer_decay"] = c.map(
        decay.groupby(hc).sum()).fillna(0).to_numpy()

    for w, n in ((30, "f_item_30d"), (90, "f_item_90d"),
                 (365, "f_item_365d")):
        out[n] = a.map(
            ha.loc[age <= w].groupby(ha.loc[age <= w]).size()
        ).fillna(0).to_numpy()
    out["f_item_all"] = a.map(ha.groupby(ha).size()).fillna(0).to_numpy()
    out["f_item_recency"] = a.map(age.groupby(ha).min()).to_numpy()
    out["f_item_decay"] = a.map(
        decay.groupby(ha).sum()).fillna(0).to_numpy()

    recent = age <= 90
    for xr, hcname, n in (
        ("raw_i_product_code", "product_code",
         "f_customer_product_90d"),
        ("raw_i_product_type_no", "product_type_no",
         "f_customer_type_90d"),
        ("raw_i_colour_group_code", "colour_group_code",
         "f_customer_colour_90d"),
        ("raw_i_section_no", "section_no",
         "f_customer_section_90d"),
        ("raw_i_garment_group_no", "garment_group_no",
         "f_customer_garment_90d"),
        ("raw_i_index_group_no", "index_group_no",
         "f_customer_index_90d")
    ):
        kh = key(hc.loc[recent], h.loc[recent, hcname])
        kx = key(c, X[xr])
        out[n] = kx.map(kh.groupby(kh).size()).fillna(0).to_numpy()

    for xr, hn, n in (
        ("raw_i_product_code", "product_code", "f_product_code_all"),
        ("raw_i_product_type_no", "product_type_no", "f_product_type_all"),
        ("raw_i_section_no", "section_no", "f_section_all"),
        ("raw_i_garment_group_no", "garment_group_no", "f_garment_all"),
        ("raw_i_colour_group_code", "colour_group_code", "f_colour_all")
    ):
        out[n] = X[xr].map(h.groupby(h[hn]).size()).fillna(0).to_numpy()

    prices = pd.to_numeric(h["price"], errors="coerce")
    out["f_article_price"] = a.map(
        prices.groupby(ha).mean()).to_numpy()
    out["f_customer_price"] = c.map(
        prices.groupby(hc).mean()).to_numpy()

    return out[names].astype(float)
