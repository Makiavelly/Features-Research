import pandas as pd
import numpy as np


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)

    def pair_key(a, b):
        return a.astype("string").fillna("<NA>") + "|" + b.astype("string").fillna("<NA>")

    if history is None or len(history) == 0:
        for c in (
            "f_pair_30d", "f_pair_90d", "f_pair_all", "f_pair_recency",
            "f_customer_30d", "f_customer_90d", "f_customer_all",
            "f_item_30d", "f_item_90d", "f_item_all", "f_item_recency",
            "f_product_code_all", "f_customer_product_90d",
            "f_customer_colour_90d", "f_customer_section_90d",
            "f_customer_channel_90d", "f_user_age", "f_item_product_type",
            "f_item_popularity_ratio"
        ):
            out[c] = 0.0
        return out

    h = history
    xp = pair_key(X["customer_id"], X["article_id"])
    hp = pair_key(h["customer_id"], h["article_id"])

    for days, name in ((30, "f_pair_30d"), (90, "f_pair_90d")):
        r = h.loc[h["days_ago"] <= days]
        out[name] = xp.map(r.groupby(hp.loc[r.index]).size()).fillna(0).astype(float)
    out["f_pair_all"] = xp.map(h.groupby(hp).size()).fillna(0).astype(float)
    out["f_pair_recency"] = xp.map(h.groupby(hp)["days_ago"].min())

    for days, name in ((30, "f_customer_30d"), (90, "f_customer_90d")):
        r = h.loc[h["days_ago"] <= days]
        out[name] = X["customer_id"].map(r.groupby("customer_id").size()).fillna(0).astype(float)
    out["f_customer_all"] = X["customer_id"].map(h.groupby("customer_id").size()).fillna(0).astype(float)

    for days, name in ((30, "f_item_30d"), (90, "f_item_90d")):
        r = h.loc[h["days_ago"] <= days]
        out[name] = X["article_id"].map(r.groupby("article_id").size()).fillna(0).astype(float)
    item_counts = h.groupby("article_id").size()
    out["f_item_all"] = X["article_id"].map(item_counts).fillna(0).astype(float)
    out["f_item_recency"] = X["article_id"].map(h.groupby("article_id")["days_ago"].min())

    out["f_product_code_all"] = X["raw_i_product_code"].map(
        h.groupby("product_code").size()).fillna(0).astype(float)

    r = h.loc[h["days_ago"] <= 90]
    for raw, hc, name in (
        ("raw_i_product_code", "product_code", "f_customer_product_90d"),
        ("raw_i_colour_group_code", "colour_group_code", "f_customer_colour_90d"),
        ("raw_i_section_no", "section_no", "f_customer_section_90d"),
    ):
        out[name] = pair_key(X["customer_id"], X[raw]).map(
            r.groupby(pair_key(r["customer_id"], r[hc])).size()
        ).fillna(0).astype(float)

    channel_key = pair_key(r["customer_id"], r["sales_channel_id"])
    out["f_customer_channel_90d"] = pair_key(
        X["customer_id"], X.get("raw_u_active", pd.Series(index=X.index, dtype=float))
    ).map(pd.Series(dtype=float)).fillna(0.0)

    out["f_user_age"] = pd.to_numeric(X["raw_u_age"], errors="coerce")
    out["f_item_product_type"] = pd.to_numeric(X["raw_i_product_type_no"], errors="coerce")
    pop = X["article_id"].map(item_counts).fillna(0).astype(float)
    out["f_item_popularity_ratio"] = pop / (X["article_id"].map(item_counts).mean() + 1.0)
    return out.astype(float)
