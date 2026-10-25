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
        "f_item_price_mean", "f_item_channel2_rate",
        "f_product_code_all", "f_product_type_all",
        "f_customer_product_30d", "f_customer_type_30d",
        "f_customer_colour_30d", "f_customer_section_30d",
        "f_customer_garment_30d", "f_customer_index_group_30d",
        "f_customer_price_mean", "f_customer_channel2_rate",
        "f_user_age", "f_user_active", "f_user_club",
        "f_item_product_type", "f_item_section", "f_item_garment"
    ]
    out = pd.DataFrame(index=X.index)
    for n in names:
        out[n] = 0.0

    out["f_user_age"] = pd.to_numeric(X["raw_u_age"], errors="coerce")
    out["f_user_active"] = pd.to_numeric(X["raw_u_active"], errors="coerce")
    out["f_user_club"] = pd.to_numeric(X["raw_u_club_member_status"], errors="coerce")
    out["f_item_product_type"] = pd.to_numeric(
        X["raw_i_product_type_no"], errors="coerce")
    out["f_item_section"] = pd.to_numeric(X["raw_i_section_no"], errors="coerce")
    out["f_item_garment"] = pd.to_numeric(X["raw_i_garment_group_no"], errors="coerce")

    if history is None or len(history) == 0:
        return out.astype(float)

    h = history.reset_index(drop=True)
    c = X["customer_id"]
    a = X["article_id"]

    def key(x, y):
        return x.astype("string").fillna("<NA>") + "|" + y.astype("string").fillna("<NA>")

    hk_pair = key(h["customer_id"], h["article_id"])
    xk_pair = key(c, a)

    def mapped(group, series, fill=0.0):
        return series.map(group).fillna(fill).to_numpy()

    for w, n in ((7, "f_pair_7d"), (30, "f_pair_30d"), (90, "f_pair_90d")):
        q = h["days_ago"] <= w
        out[n] = mapped(h.loc[q].groupby(hk_pair.loc[q]).size(), xk_pair)
    out["f_pair_all"] = mapped(h.groupby(hk_pair).size(), xk_pair)
    out["f_pair_recency"] = xk_pair.map(h.groupby(hk_pair)["days_ago"].min()).to_numpy()
    d = np.exp(-pd.to_numeric(h["days_ago"], errors="coerce").fillna(9999) / 30.0)
    out["f_pair_decay"] = mapped(d.groupby(hk_pair).sum(), xk_pair)

    for w, n in ((7, "f_customer_7d"), (30, "f_customer_30d"),
                 (90, "f_customer_90d")):
        q = h["days_ago"] <= w
        out[n] = mapped(h.loc[q].groupby(h.loc[q, "customer_id"]).size(), c)
    out["f_customer_all"] = mapped(h.groupby("customer_id").size(), c)
    out["f_customer_decay"] = mapped(d.groupby(h["customer_id"]).sum(), c)

    for w, n in ((7, "f_item_7d"), (30, "f_item_30d"), (90, "f_item_90d")):
        q = h["days_ago"] <= w
        out[n] = mapped(h.loc[q].groupby(h.loc[q, "article_id"]).size(), a)
    out["f_item_all"] = mapped(h.groupby("article_id").size(), a)
    out["f_item_recency"] = a.map(h.groupby("article_id")["days_ago"].min()).to_numpy()
    out["f_item_decay"] = mapped(d.groupby(h["article_id"]).sum(), a)

    out["f_item_price_mean"] = a.map(h.groupby("article_id")["price"].mean()).to_numpy()
    ch = h["sales_channel_id"].eq(2).astype(float)
    out["f_item_channel2_rate"] = a.map(ch.groupby(h["article_id"]).mean()).to_numpy()
    out["f_customer_price_mean"] = c.map(h.groupby("customer_id")["price"].mean()).to_numpy()
    out["f_customer_channel2_rate"] = c.map(ch.groupby(h["customer_id"]).mean()).to_numpy()

    out["f_product_code_all"] = X["raw_i_product_code"].map(
        h.groupby("product_code").size()).fillna(0).to_numpy()
    out["f_product_type_all"] = X["raw_i_product_type_no"].map(
        h.groupby("product_type_no").size()).fillna(0).to_numpy()

    q = h["days_ago"] <= 30
    r = h.loc[q]
    for raw, col, name in (
        ("raw_i_product_code", "product_code", "f_customer_product_30d"),
        ("raw_i_product_type_no", "product_type_no", "f_customer_type_30d"),
        ("raw_i_colour_group_code", "colour_group_code", "f_customer_colour_30d"),
        ("raw_i_section_no", "section_no", "f_customer_section_30d"),
        ("raw_i_garment_group_no", "garment_group_no", "f_customer_garment_30d"),
        ("raw_i_index_group_no", "index_group_no", "f_customer_index_group_30d"),
    ):
        kh = key(r["customer_id"], r[col])
        kx = key(c, X[raw])
        out[name] = mapped(r.groupby(kh).size(), kx)

    return out.astype(float)
