import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)

    def make_key(a, b):
        return a.astype("string").fillna("<NA>") + "|" + b.astype("string").fillna("<NA>")

    h = history
    if h is None or len(h) == 0:
        for name in (
            "f_pair_30d", "f_pair_90d", "f_pair_all", "f_pair_recency",
            "f_customer_30d", "f_customer_90d", "f_customer_recency",
            "f_item_30d", "f_item_90d", "f_item_recency",
            "f_customer_product_90d", "f_customer_section_90d"
        ):
            out[name] = 0.0
        return out

    pair_x = make_key(X["customer_id"], X["article_id"])
    pair_h = make_key(h["customer_id"], h["article_id"])

    for window, name in ((30, "f_pair_30d"), (90, "f_pair_90d")):
        recent = h.loc[h["days_ago"] <= window]
        counts = pair_h.loc[recent.index].value_counts()
        out[name] = pair_x.map(counts).fillna(0).astype(float)

    out["f_pair_all"] = pair_x.map(pair_h.value_counts()).fillna(0).astype(float)
    out["f_pair_recency"] = pair_x.map(
        h.assign(_pair=pair_h).groupby("_pair")["days_ago"].min()
    )

    for window, name in ((30, "f_customer_30d"), (90, "f_customer_90d")):
        recent = h.loc[h["days_ago"] <= window]
        out[name] = X["customer_id"].map(
            recent.groupby("customer_id").size()
        ).fillna(0).astype(float)

    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()
    )

    for window, name in ((30, "f_item_30d"), (90, "f_item_90d")):
        recent = h.loc[h["days_ago"] <= window]
        out[name] = X["article_id"].map(
            recent.groupby("article_id").size()
        ).fillna(0).astype(float)

    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()
    )

    recent = h.loc[h["days_ago"] <= 90]
    for raw, col, name in (
        ("raw_i_product_code", "product_code", "f_customer_product_90d"),
        ("raw_i_section_no", "section_no", "f_customer_section_90d"),
    ):
        kh = make_key(recent["customer_id"], recent[col])
        kx = make_key(X["customer_id"], X[raw])
        out[name] = kx.map(kh.value_counts()).fillna(0).astype(float)

    return out.astype(float)
