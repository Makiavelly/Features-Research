import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    if h is None or len(h) == 0:
        names = [
            "f_pair_all", "f_pair_30d", "f_pair_90d", "f_pair_recency",
            "f_customer_all", "f_customer_30d", "f_customer_recency",
            "f_item_all", "f_item_30d", "f_item_recency",
            "f_customer_product_90d", "f_customer_type_90d",
            "f_customer_colour_90d", "f_customer_section_90d",
            "f_product_popularity", "f_type_popularity",
            "f_customer_channel_90d", "f_item_mean_price"
        ]
        for name in names:
            out[name] = 0.0
        return out

    def map_group(values, groups, agg="size"):
        return values.map(groups).fillna(0).astype(float)

    def pair_key(c, a):
        return pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])

    px = pair_key(X["customer_id"], X["article_id"])
    ph = pair_key(h["customer_id"], h["article_id"])
    out["f_pair_all"] = map_group(px, pd.Series(1, index=ph).groupby(level=[0, 1]).sum())
    for w, name in ((30, "f_pair_30d"), (90, "f_pair_90d")):
        hh = h.loc[h["days_ago"] <= w]
        kk = pair_key(hh["customer_id"], hh["article_id"])
        out[name] = map_group(px, pd.Series(1, index=kk).groupby(level=[0, 1]).sum())
    rec = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    out["f_pair_recency"] = pd.Series(list(zip(X["customer_id"], X["article_id"])), index=X.index).map(rec).fillna(9999)

    for w, name in ((None, "f_customer_all"), (30, "f_customer_30d")):
        hh = h if w is None else h.loc[h["days_ago"] <= w]
        out[name] = X["customer_id"].map(hh.groupby("customer_id").size()).fillna(0)
    out["f_customer_recency"] = X["customer_id"].map(h.groupby("customer_id")["days_ago"].min()).fillna(9999)

    for w, name in ((None, "f_item_all"), (30, "f_item_30d")):
        hh = h if w is None else h.loc[h["days_ago"] <= w]
        out[name] = X["article_id"].map(hh.groupby("article_id").size()).fillna(0)
    out["f_item_recency"] = X["article_id"].map(h.groupby("article_id")["days_ago"].min()).fillna(9999)

    recent = h.loc[h["days_ago"] <= 90]
    for raw, col, name in (
        ("raw_i_product_code", "product_code", "f_customer_product_90d"),
        ("raw_i_product_type_no", "product_type_no", "f_customer_type_90d"),
        ("raw_i_colour_group_code", "colour_group_code", "f_customer_colour_90d"),
        ("raw_i_section_no", "section_no", "f_customer_section_90d"),
    ):
        counts = recent.groupby(["customer_id", col]).size()
        keys = pd.MultiIndex.from_arrays([X["customer_id"].to_numpy(), X[raw].to_numpy()])
        out[name] = pd.Series(keys, index=X.index).map(counts).fillna(0)

    for raw, col, name in (
        ("raw_i_product_code", "product_code", "f_product_popularity"),
        ("raw_i_product_type_no", "product_type_no", "f_type_popularity"),
    ):
        out[name] = X[raw].map(h.groupby(col).size()).fillna(0)

    ch = recent.groupby("customer_id")["sales_channel_id"].agg(
        lambda s: (s == 2).sum() - (s == 1).sum()
    )
    out["f_customer_channel_90d"] = X["customer_id"].map(ch).fillna(0)

    price = h.groupby("article_id")["price"].mean()
    out["f_item_mean_price"] = X["article_id"].map(price).fillna(0)
    return out.astype(float)
