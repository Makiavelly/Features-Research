import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_pair_30d", "f_pair_90d", "f_pair_365d", "f_pair_all",
        "f_pair_recency", "f_pair_decay", "f_pair_channel2",
        "f_customer_30d", "f_customer_90d", "f_customer_all",
        "f_customer_decay", "f_customer_unique_articles",
        "f_item_30d", "f_item_90d", "f_item_all", "f_item_decay",
        "f_item_recency", "f_item_avg_price",
        "f_item_product_code", "f_item_product_type", "f_item_section",
        "f_customer_product", "f_customer_type", "f_customer_colour",
        "f_customer_section", "f_customer_garment", "f_customer_index",
        "f_customer_avg_price", "f_pair_avg_price",
        "f_user_age", "f_user_fn", "f_user_active", "f_user_club",
        "f_user_news", "f_item_product_type_static", "f_item_section_static"
    ]
    out = pd.DataFrame(index=X.index)
    for n in names:
        out[n] = 0.0

    static = {
        "f_user_age": "raw_u_age",
        "f_user_fn": "raw_u_fn",
        "f_user_active": "raw_u_active",
        "f_user_club": "raw_u_club_member_status",
        "f_user_news": "raw_u_fashion_news_frequency",
        "f_item_product_type_static": "raw_i_product_type_no",
        "f_item_section_static": "raw_i_section_no"
    }
    for n, c in static.items():
        out[n] = pd.to_numeric(X[c], errors="coerce").to_numpy()

    if history is None or len(history) == 0:
        return out.astype(float)

    h = history.reset_index(drop=True)
    c = X["customer_id"]
    a = X["article_id"]

    def key(u, v):
        return u.astype("string").fillna("<NA>") + "|" + v.astype("string").fillna("<NA>")

    pcx = key(c, a)
    pch = key(h["customer_id"], h["article_id"])

    def mapped(group, series):
        return series.map(group).fillna(0).to_numpy()

    def cnt(k, mask=None):
        return (k.loc[mask] if mask is not None else k).groupby(
            h.loc[mask, "customer_id"] if False else
            (k.loc[mask] if mask is not None else k)
        ).size()

    def count_map(kh, kx, mask=None):
        z = kh.loc[mask] if mask is not None else kh
        return kx.map(z.groupby(z).size()).fillna(0).to_numpy()

    for w, n in ((30, "f_pair_30d"), (90, "f_pair_90d"), (365, "f_pair_365d")):
        m = h["days_ago"] <= w
        out[n] = count_map(pch, pcx, m)
    out["f_pair_all"] = count_map(pch, pcx)
    out["f_pair_recency"] = pcx.map(h.groupby(pch)["days_ago"].min()).to_numpy()
    d = np.exp(-pd.to_numeric(h["days_ago"], errors="coerce").fillna(9999) / 30.0)
    out["f_pair_decay"] = pcx.map(d.groupby(pch).sum()).fillna(0).to_numpy()
    ch = h["sales_channel_id"].eq(2)
    out["f_pair_channel2"] = pcx.map(ch.groupby(pch).sum()).fillna(0).to_numpy()

    for w, n in ((30, "f_customer_30d"), (90, "f_customer_90d")):
        m = h["days_ago"] <= w
        g = h.loc[m].groupby("customer_id").size()
        out[n] = c.map(g).fillna(0).to_numpy()
    cg = h.groupby("customer_id")
    out["f_customer_all"] = c.map(cg.size()).fillna(0).to_numpy()
    out["f_customer_decay"] = c.map(d.groupby(h["customer_id"]).sum()).fillna(0).to_numpy()
    out["f_customer_unique_articles"] = c.map(
        cg["article_id"].nunique()).fillna(0).to_numpy()

    ag = h.groupby("article_id")
    for w, n in ((30, "f_item_30d"), (90, "f_item_90d")):
        out[n] = a.map(h.loc[h["days_ago"] <= w].groupby("article_id").size()
                        ).fillna(0).to_numpy()
    out["f_item_all"] = a.map(ag.size()).fillna(0).to_numpy()
    out["f_item_decay"] = a.map(d.groupby(h["article_id"]).sum()).fillna(0).to_numpy()
    out["f_item_recency"] = a.map(ag["days_ago"].min()).to_numpy()
    out["f_item_avg_price"] = a.map(ag["price"].mean()).to_numpy()

    for raw, hc, n in (
        ("raw_i_product_code", "product_code", "f_item_product_code"),
        ("raw_i_product_type_no", "product_type_no", "f_item_product_type"),
        ("raw_i_section_no", "section_no", "f_item_section"),
    ):
        out[n] = X[raw].map(h.groupby(hc).size()).fillna(0).to_numpy()

    recent = h.loc[h["days_ago"] <= 90]
    for raw, hc, n in (
        ("raw_i_product_code", "product_code", "f_customer_product"),
        ("raw_i_product_type_no", "product_type_no", "f_customer_type"),
        ("raw_i_colour_group_code", "colour_group_code", "f_customer_colour"),
        ("raw_i_section_no", "section_no", "f_customer_section"),
        ("raw_i_garment_group_no", "garment_group_no", "f_customer_garment"),
        ("raw_i_index_group_no", "index_group_no", "f_customer_index"),
    ):
        kh = key(recent["customer_id"], recent[hc])
        kx = key(c, X[raw])
        out[n] = kx.map(kh.groupby(kh).size()).fillna(0).to_numpy()

    out["f_customer_avg_price"] = c.map(
        h.groupby("customer_id")["price"].mean()).to_numpy()
    out["f_pair_avg_price"] = pcx.map(
        h.groupby(pch)["price"].mean()).to_numpy()
    return out.astype(float)
