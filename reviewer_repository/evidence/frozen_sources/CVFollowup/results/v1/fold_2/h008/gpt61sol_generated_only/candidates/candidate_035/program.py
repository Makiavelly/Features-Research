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
        "f_customer_product_90d", "f_customer_type_90d",
        "f_customer_colour_90d", "f_customer_section_90d",
        "f_customer_garment_90d", "f_customer_index_90d",
        "f_item_type_90d", "f_item_code_all",
        "f_item_price_mean", "f_customer_price_mean",
        "f_item_channel2_share", "f_user_age",
        "f_item_product_code", "f_item_product_type"
    ]
    out = pd.DataFrame(index=X.index)
    for n in names:
        out[n] = 0.0

    out["f_user_age"] = pd.to_numeric(
        X["raw_u_age"], errors="coerce"
    ).to_numpy()
    out["f_item_product_code"] = pd.to_numeric(
        X["raw_i_product_code"], errors="coerce"
    ).to_numpy()
    out["f_item_product_type"] = pd.to_numeric(
        X["raw_i_product_type_no"], errors="coerce"
    ).to_numpy()

    if history is None or len(history) == 0:
        return out.astype(float)

    h = history.reset_index(drop=True)
    c = X["customer_id"]
    a = X["article_id"]

    def make_key(u, v):
        return (
            u.astype("string").fillna("<NA>") + "|" +
            v.astype("string").fillna("<NA>")
        )

    ph = make_key(h["customer_id"], h["article_id"])
    px = make_key(c, a)
    d = pd.to_numeric(h["days_ago"], errors="coerce").fillna(1e9)
    decay = np.exp(-d / 30.0)

    for window, name in (
        (7, "f_pair_7d"),
        (30, "f_pair_30d"),
        (90, "f_pair_90d"),
    ):
        m = d <= window
        z = ph.loc[m].groupby(ph.loc[m]).size()
        out[name] = px.map(z).fillna(0).to_numpy()

    out["f_pair_all"] = px.map(ph.groupby(ph).size()).fillna(0).to_numpy()
    out["f_pair_recency"] = px.map(d.groupby(ph).min()).to_numpy()
    out["f_pair_decay"] = px.map(
        decay.groupby(ph).sum()
    ).fillna(0).to_numpy()

    hc = h["customer_id"]
    for window, name in (
        (7, "f_customer_7d"),
        (30, "f_customer_30d"),
        (90, "f_customer_90d"),
    ):
        m = d <= window
        z = h.loc[m].groupby("customer_id").size()
        out[name] = c.map(z).fillna(0).to_numpy()

    out["f_customer_all"] = c.map(
        h.groupby("customer_id").size()
    ).fillna(0).to_numpy()
    out["f_customer_decay"] = c.map(
        decay.groupby(hc).sum()
    ).fillna(0).to_numpy()

    for window, name in (
        (7, "f_item_7d"),
        (30, "f_item_30d"),
        (90, "f_item_90d"),
    ):
        m = d <= window
        z = h.loc[m].groupby("article_id").size()
        out[name] = a.map(z).fillna(0).to_numpy()

    out["f_item_all"] = a.map(
        h.groupby("article_id").size()
    ).fillna(0).to_numpy()
    out["f_item_recency"] = a.map(
        d.groupby(h["article_id"]).min()
    ).to_numpy()
    out["f_item_decay"] = a.map(
        decay.groupby(h["article_id"]).sum()
    ).fillna(0).to_numpy()

    recent = d <= 90
    for raw, col, name in (
        ("raw_i_product_code", "product_code", "f_customer_product_90d"),
        ("raw_i_product_type_no", "product_type_no", "f_customer_type_90d"),
        ("raw_i_colour_group_code", "colour_group_code", "f_customer_colour_90d"),
        ("raw_i_section_no", "section_no", "f_customer_section_90d"),
        ("raw_i_garment_group_no", "garment_group_no", "f_customer_garment_90d"),
        ("raw_i_index_group_no", "index_group_no", "f_customer_index_90d"),
    ):
        hk = make_key(h.loc[recent, "customer_id"], h.loc[recent, col])
        xk = make_key(c, X[raw])
        out[name] = xk.map(
            hk.groupby(hk).size()
        ).fillna(0).to_numpy()

    z = h.loc[recent].groupby("product_type_no").size()
    out["f_item_type_90d"] = X["raw_i_product_type_no"].map(
        z
    ).fillna(0).to_numpy()

    out["f_item_code_all"] = X["raw_i_product_code"].map(
        h.groupby("product_code").size()
    ).fillna(0).to_numpy()

    item_price = h.groupby("article_id")["price"].mean()
    user_price = h.groupby("customer_id")["price"].mean()
    out["f_item_price_mean"] = a.map(item_price).to_numpy()
    out["f_customer_price_mean"] = c.map(user_price).to_numpy()

    channel2 = h.assign(
        _channel2=(pd.to_numeric(h["sales_channel_id"], errors="coerce") == 2)
    ).groupby("article_id")["_channel2"].mean()
    out["f_item_channel2_share"] = a.map(channel2).to_numpy()

    return out.astype(float)
