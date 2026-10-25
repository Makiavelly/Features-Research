import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_pair_7d", "f_pair_30d", "f_pair_90d", "f_pair_all",
        "f_pair_recency", "f_pair_decay",
        "f_customer_7d", "f_customer_30d", "f_customer_90d",
        "f_customer_all", "f_customer_decay",
        "f_item_7d", "f_item_30d", "f_item_90d", "f_item_all",
        "f_item_recency", "f_item_decay",
        "f_product_code_all", "f_product_type_all",
        "f_customer_product_90d", "f_customer_type_90d",
        "f_customer_colour_90d", "f_customer_section_90d",
        "f_customer_garment_90d", "f_customer_index_group_90d",
        "f_customer_department_90d", "f_customer_colour_master_90d",
        "f_item_price_mean", "f_item_price_recent",
        "f_pair_price_mean",
        "f_user_age", "f_user_active", "f_user_club",
        "f_item_product_type", "f_item_section", "f_item_garment"
    ]
    out = pd.DataFrame(index=X.index)
    for n in names:
        out[n] = 0.0

    out["f_user_age"] = pd.to_numeric(
        X["raw_u_age"], errors="coerce").to_numpy()
    out["f_user_active"] = pd.to_numeric(
        X["raw_u_active"], errors="coerce").to_numpy()
    out["f_user_club"] = pd.to_numeric(
        X["raw_u_club_member_status"], errors="coerce").to_numpy()
    out["f_item_product_type"] = pd.to_numeric(
        X["raw_i_product_type_no"], errors="coerce").to_numpy()
    out["f_item_section"] = pd.to_numeric(
        X["raw_i_section_no"], errors="coerce").to_numpy()
    out["f_item_garment"] = pd.to_numeric(
        X["raw_i_garment_group_no"], errors="coerce").to_numpy()

    if history is None or len(history) == 0:
        return out.astype(float)

    h = history.reset_index(drop=True)
    days = pd.to_numeric(h["days_ago"], errors="coerce").fillna(999999)
    c = X["customer_id"]
    a = X["article_id"]

    def key(x, y):
        return (x.astype("string").fillna("<NA>") + "|" +
                y.astype("string").fillna("<NA>"))

    px = key(c, a)
    ph = key(h["customer_id"], h["article_id"])

    def mapped_count(xkey, hkey, mask=None):
        hh = h if mask is None else h.loc[mask]
        kk = hkey if mask is None else hkey.loc[mask]
        return xkey.map(kk.groupby(kk).size()).fillna(0).to_numpy()

    for w, n in ((7, "f_pair_7d"), (30, "f_pair_30d"),
                 (90, "f_pair_90d")):
        m = days <= w
        out[n] = mapped_count(px, ph, m)
    out["f_pair_all"] = mapped_count(px, ph)
    out["f_pair_recency"] = px.map(h.groupby(ph)["days_ago"].min()).to_numpy()
    decay = np.exp(-days.astype(float) / 30.0)
    out["f_pair_decay"] = px.map(
        decay.groupby(ph).sum()).fillna(0).to_numpy()

    for w, n in ((7, "f_customer_7d"), (30, "f_customer_30d"),
                 (90, "f_customer_90d")):
        m = days <= w
        out[n] = c.map(
            h.loc[m].groupby("customer_id").size()).fillna(0).to_numpy()
    out["f_customer_all"] = c.map(
        h.groupby("customer_id").size()).fillna(0).to_numpy()
    out["f_customer_decay"] = c.map(
        decay.groupby(h["customer_id"]).sum()).fillna(0).to_numpy()

    for w, n in ((7, "f_item_7d"), (30, "f_item_30d"),
                 (90, "f_item_90d")):
        m = days <= w
        out[n] = a.map(
            h.loc[m].groupby("article_id").size()).fillna(0).to_numpy()
    out["f_item_all"] = a.map(
        h.groupby("article_id").size()).fillna(0).to_numpy()
    out["f_item_recency"] = a.map(
        h.groupby("article_id")["days_ago"].min()).to_numpy()
    out["f_item_decay"] = a.map(
        decay.groupby(h["article_id"]).sum()).fillna(0).to_numpy()

    for raw, hc, n in (
        ("raw_i_product_code", "product_code", "f_product_code_all"),
        ("raw_i_product_type_no", "product_type_no", "f_product_type_all"),
    ):
        out[n] = X[raw].map(
            h.groupby(hc).size()).fillna(0).to_numpy()

    recent = h.loc[days <= 90]
    for raw, hc, n in (
        ("raw_i_product_code", "product_code", "f_customer_product_90d"),
        ("raw_i_product_type_no", "product_type_no", "f_customer_type_90d"),
        ("raw_i_colour_group_code", "colour_group_code", "f_customer_colour_90d"),
        ("raw_i_section_no", "section_no", "f_customer_section_90d"),
        ("raw_i_garment_group_no", "garment_group_no", "f_customer_garment_90d"),
        ("raw_i_index_group_no", "index_group_no", "f_customer_index_group_90d"),
        ("raw_i_department_no", "department_no", "f_customer_department_90d"),
        ("raw_i_perceived_colour_master_id", "perceived_colour_master_id",
         "f_customer_colour_master_90d"),
    ):
        kh = key(recent["customer_id"], recent[hc])
        kx = key(c, X[raw])
        out[n] = kx.map(kh.groupby(kh).size()).fillna(0).to_numpy()

    price = pd.to_numeric(h["price"], errors="coerce")
    out["f_item_price_mean"] = a.map(
        price.groupby(h["article_id"]).mean()).to_numpy()
    out["f_item_price_recent"] = a.map(
        price.loc[days <= 90].groupby(h.loc[days <= 90, "article_id"]).mean()
    ).to_numpy()
    out["f_pair_price_mean"] = px.map(
        price.groupby(ph).mean()).to_numpy()

    return out.astype(float)
