import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    c, a, h = X["customer_id"], X["article_id"], history

    def pair_key(left, right):
        return left.astype(str) + "\x1f" + right.astype(str)

    for window, label in ((7, "7d"), (30, "30d"), (90, "90d")):
        recent = h.loc[h["days_ago"] <= window]
        out["f_customer_purchases_" + label] = c.map(recent.groupby("customer_id", sort=False).size())
        out["f_article_purchases_" + label] = a.map(recent.groupby("article_id", sort=False).size())

    out["f_customer_purchases_all"] = c.map(h.groupby("customer_id", sort=False).size())
    out["f_article_purchases_all"] = a.map(h.groupby("article_id", sort=False).size())
    out["f_customer_recency"] = c.map(h.groupby("customer_id", sort=False)["days_ago"].min())

    hp = pair_key(h["customer_id"], h["article_id"])
    xp = pair_key(c, a)
    pair_stats = h.assign(_pair=hp).groupby("_pair", sort=False).agg(
        _count=("days_ago", "size"), _recent=("days_ago", "min"))
    out["f_pair_purchases"] = xp.map(pair_stats["_count"])
    out["f_pair_recency"] = xp.map(pair_stats["_recent"])

    recent30 = h.loc[h["days_ago"] <= 30]
    out["f_pair_purchases_30d"] = xp.map(
        recent30.assign(_pair=pair_key(recent30["customer_id"], recent30["article_id"]))
                .groupby("_pair", sort=False).size())

    for raw_col, hist_col, name in (
        ("raw_i_product_type_no", "product_type_no", "product_type"),
        ("raw_i_department_no", "department_no", "department"),
        ("raw_i_section_no", "section_no", "section"),
        ("raw_i_garment_group_no", "garment_group_no", "garment_group"),
    ):
        out["f_customer_" + name + "_purchases"] = pair_key(c, X[raw_col]).map(
            h.assign(_key=pair_key(h["customer_id"], h[hist_col]))
             .groupby("_key", sort=False).size())

    item_stats = h.groupby("article_id", sort=False).agg(
        _price=("price", "mean"), _recency=("days_ago", "min"))
    out["f_item_mean_price"] = a.map(item_stats["_price"])
    out["f_item_recency"] = a.map(item_stats["_recency"])

    for col in (
        "raw_u_age", "raw_u_club_member_status", "raw_u_fashion_news_frequency",
        "raw_i_product_code", "raw_i_product_type_no", "raw_i_section_no",
        "raw_i_garment_group_no"
    ):
        out["f_static_" + col[4:]] = X[col]

    return out.astype(float)
