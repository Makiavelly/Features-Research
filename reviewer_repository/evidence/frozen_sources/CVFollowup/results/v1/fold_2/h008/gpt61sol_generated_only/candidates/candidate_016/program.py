import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)

    names = [
        "f_pair_30d", "f_pair_90d", "f_pair_365d", "f_pair_all",
        "f_pair_recency", "f_pair_decay", "f_customer_30d",
        "f_customer_90d", "f_customer_all", "f_customer_decay",
        "f_item_30d", "f_item_90d", "f_item_all", "f_item_recency",
        "f_item_decay", "f_product_code_all", "f_product_type_all",
        "f_customer_product_90d", "f_customer_type_90d",
        "f_customer_colour_90d", "f_customer_section_90d",
        "f_customer_garment_90d", "f_customer_index_group_90d",
        "f_user_age", "f_item_product_type"
    ]
    if history is None or len(history) == 0:
        for name in names:
            out[name] = pd.to_numeric(
                X["raw_u_age"] if name == "f_user_age" else
                X["raw_i_product_type_no"] if name == "f_item_product_type" else
                pd.Series(0.0, index=X.index), errors="coerce"
            )
        return out

    h = history.reset_index(drop=True)
    c = X["customer_id"]
    a = X["article_id"]

    def composite(left, right):
        return left.astype("string").fillna("<NA>") + "|" + right.astype("string").fillna("<NA>")

    pair_x = composite(c, a)
    pair_h = composite(h["customer_id"], h["article_id"])

    def counts(keys, mask=None):
        if mask is None:
            hh, kk = h, keys
        else:
            hh, kk = h.loc[mask], keys.loc[mask]
        return hh.groupby(kk).size()

    for window, name in ((30, "f_pair_30d"), (90, "f_pair_90d"),
                         (365, "f_pair_365d")):
        mask = h["days_ago"] <= window
        out[name] = pair_x.map(counts(pair_h, mask)).fillna(0).to_numpy()
    out["f_pair_all"] = pair_x.map(counts(pair_h)).fillna(0).to_numpy()
    out["f_pair_recency"] = pair_x.map(h.groupby(pair_h)["days_ago"].min()).to_numpy()
    decay = np.exp(-h["days_ago"].astype(float) / 30.0)
    out["f_pair_decay"] = pair_x.map(decay.groupby(pair_h).sum()).fillna(0).to_numpy()

    for window, name in ((30, "f_customer_30d"), (90, "f_customer_90d")):
        mask = h["days_ago"] <= window
        out[name] = c.map(counts(h["customer_id"], mask)).fillna(0).to_numpy()
    out["f_customer_all"] = c.map(h.groupby("customer_id").size()).fillna(0).to_numpy()
    out["f_customer_decay"] = c.map(decay.groupby(h["customer_id"]).sum()).fillna(0).to_numpy()

    for window, name in ((30, "f_item_30d"), (90, "f_item_90d")):
        mask = h["days_ago"] <= window
        out[name] = a.map(counts(h["article_id"], mask)).fillna(0).to_numpy()
    out["f_item_all"] = a.map(h.groupby("article_id").size()).fillna(0).to_numpy()
    out["f_item_recency"] = a.map(h.groupby("article_id")["days_ago"].min()).to_numpy()
    out["f_item_decay"] = a.map(decay.groupby(h["article_id"]).sum()).fillna(0).to_numpy()

    out["f_product_code_all"] = X["raw_i_product_code"].map(
        h.groupby("product_code").size()).fillna(0).to_numpy()
    out["f_product_type_all"] = X["raw_i_product_type_no"].map(
        h.groupby("product_type_no").size()).fillna(0).to_numpy()

    recent = h.loc[h["days_ago"] <= 90]
    for raw, hc, name in (
        ("raw_i_product_code", "product_code", "f_customer_product_90d"),
        ("raw_i_product_type_no", "product_type_no", "f_customer_type_90d"),
        ("raw_i_colour_group_code", "colour_group_code", "f_customer_colour_90d"),
        ("raw_i_section_no", "section_no", "f_customer_section_90d"),
        ("raw_i_garment_group_no", "garment_group_no", "f_customer_garment_90d"),
        ("raw_i_index_group_no", "index_group_no", "f_customer_index_group_90d"),
    ):
        kh = composite(recent["customer_id"], recent[hc])
        kx = composite(c, X[raw])
        out[name] = kx.map(recent.groupby(kh).size()).fillna(0).to_numpy()

    out["f_user_age"] = pd.to_numeric(X["raw_u_age"], errors="coerce").to_numpy()
    out["f_item_product_type"] = pd.to_numeric(
        X["raw_i_product_type_no"], errors="coerce").to_numpy()
    return out.astype(float)
