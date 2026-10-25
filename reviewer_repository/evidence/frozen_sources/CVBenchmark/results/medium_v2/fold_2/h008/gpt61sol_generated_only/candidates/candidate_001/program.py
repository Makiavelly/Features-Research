import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)

    def key2(a, b):
        return a.astype("string").fillna("<NA>") + "|" + b.astype("string").fillna("<NA>")

    def mapped_counts(h, k):
        if len(h) == 0:
            return pd.Series(0.0, index=X.index)
        s = h.groupby(k).size()
        return k.map(s).fillna(0).astype(float)

    if len(history) == 0:
        for name in (
            "f_pair_30d", "f_pair_90d", "f_pair_365d", "f_pair_all",
            "f_pair_recency", "f_customer_30d", "f_customer_90d",
            "f_customer_all", "f_item_30d", "f_item_90d", "f_item_all",
            "f_item_recency", "f_product_code_all", "f_product_type_all",
            "f_customer_product_90d", "f_customer_type_90d",
            "f_customer_colour_90d", "f_customer_section_90d",
            "f_user_age", "f_item_product_type"
        ):
            out[name] = 0.0
        return out

    h = history
    pair_x = key2(X["customer_id"], X["article_id"])
    pair_h = key2(h["customer_id"], h["article_id"])

    for window, name in ((30, "f_pair_30d"), (90, "f_pair_90d"),
                         (365, "f_pair_365d")):
        hh = h.loc[h["days_ago"] <= window]
        out[name] = pair_x.map(hh.groupby(pair_h.loc[hh.index]).size()).fillna(0).astype(float)
    out["f_pair_all"] = pair_x.map(h.groupby(pair_h).size()).fillna(0).astype(float)

    pr = h.groupby(pair_h)["days_ago"].min()
    out["f_pair_recency"] = pair_x.map(pr)

    for window, name in ((30, "f_customer_30d"), (90, "f_customer_90d")):
        hh = h.loc[h["days_ago"] <= window]
        out[name] = X["customer_id"].map(hh.groupby("customer_id").size()).fillna(0).astype(float)
    out["f_customer_all"] = X["customer_id"].map(h.groupby("customer_id").size()).fillna(0).astype(float)

    for window, name in ((30, "f_item_30d"), (90, "f_item_90d")):
        hh = h.loc[h["days_ago"] <= window]
        out[name] = X["article_id"].map(hh.groupby("article_id").size()).fillna(0).astype(float)
    out["f_item_all"] = X["article_id"].map(h.groupby("article_id").size()).fillna(0).astype(float)
    out["f_item_recency"] = X["article_id"].map(h.groupby("article_id")["days_ago"].min())

    out["f_product_code_all"] = X["raw_i_product_code"].map(
        h.groupby("product_code").size()).fillna(0).astype(float)
    out["f_product_type_all"] = X["raw_i_product_type_no"].map(
        h.groupby("product_type_no").size()).fillna(0).astype(float)

    recent = h.loc[h["days_ago"] <= 90]
    for raw, hc, name in (
        ("raw_i_product_code", "product_code", "f_customer_product_90d"),
        ("raw_i_product_type_no", "product_type_no", "f_customer_type_90d"),
        ("raw_i_colour_group_code", "colour_group_code", "f_customer_colour_90d"),
        ("raw_i_section_no", "section_no", "f_customer_section_90d"),
    ):
        kh = key2(recent["customer_id"], recent[hc])
        kx = key2(X["customer_id"], X[raw])
        out[name] = kx.map(recent.groupby(kh).size()).fillna(0).astype(float)

    out["f_user_age"] = pd.to_numeric(X["raw_u_age"], errors="coerce")
    out["f_item_product_type"] = pd.to_numeric(
        X["raw_i_product_type_no"], errors="coerce"
    )
    return out.astype(float)
