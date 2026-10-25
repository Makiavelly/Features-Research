import pandas as pd
import numpy as np


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)

    def key2(a, b):
        return (a.astype("string").fillna("<NA>") + "|" +
                b.astype("string").fillna("<NA>"))

    if history is None or len(history) == 0:
        names = (
            "f_pair_30d", "f_pair_90d", "f_pair_all", "f_pair_recency",
            "f_customer_30d", "f_customer_90d", "f_customer_all",
            "f_item_30d", "f_item_90d", "f_item_all", "f_item_recency",
            "f_product_code_all", "f_customer_product_90d",
            "f_customer_colour_90d", "f_customer_section_90d",
            "f_customer_channel_90d", "f_user_age", "f_item_product_type",
            "f_item_popularity_ratio"
        )
        for name in names:
            out[name] = 0.0
        return out

    h = history.reset_index(drop=True)
    hp = key2(h["customer_id"], h["article_id"])
    xp = key2(X["customer_id"], X["article_id"])

    for days, name in ((30, "f_pair_30d"), (90, "f_pair_90d")):
        r = h["days_ago"] <= days
        out[name] = xp.map(h.loc[r].groupby(hp.loc[r]).size()).fillna(0).astype(float)
    out["f_pair_all"] = xp.map(h.groupby(hp).size()).fillna(0).astype(float)
    out["f_pair_recency"] = xp.map(h.groupby(hp)["days_ago"].min())

    for days, name in ((30, "f_customer_30d"), (90, "f_customer_90d")):
        r = h["days_ago"] <= days
        out[name] = X["customer_id"].map(
            h.loc[r].groupby("customer_id").size()).fillna(0).astype(float)
    out["f_customer_all"] = X["customer_id"].map(
        h.groupby("customer_id").size()).fillna(0).astype(float)

    for days, name in ((30, "f_item_30d"), (90, "f_item_90d")):
        r = h["days_ago"] <= days
        out[name] = X["article_id"].map(
            h.loc[r].groupby("article_id").size()).fillna(0).astype(float)
    item_counts = h.groupby("article_id").size()
    out["f_item_all"] = X["article_id"].map(item_counts).fillna(0).astype(float)
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min())

    out["f_product_code_all"] = X["raw_i_product_code"].map(
        h.groupby("product_code").size()).fillna(0).astype(float)

    r = h["days_ago"] <= 90
    recent = h.loc[r]
    for raw, hc, name in (
        ("raw_i_product_code", "product_code", "f_customer_product_90d"),
        ("raw_i_colour_group_code", "colour_group_code", "f_customer_colour_90d"),
        ("raw_i_section_no", "section_no", "f_customer_section_90d"),
    ):
        kh = key2(recent["customer_id"], recent[hc])
        kx = key2(X["customer_id"], X[raw])
        out[name] = kx.map(recent.groupby(kh).size()).fillna(0).astype(float)

    kh = key2(recent["customer_id"], recent["sales_channel_id"])
    kx = key2(X["customer_id"], X["raw_u_active"])
    out["f_customer_channel_90d"] = kx.map(recent.groupby(kh).size()).fillna(0).astype(float)

    out["f_user_age"] = pd.to_numeric(X["raw_u_age"], errors="coerce")
    out["f_item_product_type"] = pd.to_numeric(
        X["raw_i_product_type_no"], errors="coerce")

    # Normalize item popularity using the history population, never the candidate batch.
    population_mean = float(item_counts.mean()) if len(item_counts) else 0.0
    out["f_item_popularity_ratio"] = (
        X["article_id"].map(item_counts).fillna(0).astype(float) /
        (population_mean + 1.0)
    )
    return out.astype(float)
