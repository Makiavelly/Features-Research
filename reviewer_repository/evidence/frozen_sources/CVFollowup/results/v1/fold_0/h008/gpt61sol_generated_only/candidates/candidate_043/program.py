import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    c, a = X["customer_id"], X["article_id"]

    def mapped(series, keys):
        return keys.map(series).fillna(0)

    def pair_count(z):
        counts = z.groupby(["customer_id", "article_id"]).size()
        keys = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return pd.Series(counts.reindex(keys).to_numpy(), index=X.index).fillna(0)

    def category_count(z, raw_col, hist_col):
        sentinel = -999999
        cat = z[hist_col].fillna(sentinel)
        counts = z.assign(_cat=cat).groupby(["customer_id", "_cat"]).size()
        keys = pd.MultiIndex.from_arrays([
            c.to_numpy(), X[raw_col].fillna(sentinel).to_numpy()
        ])
        return pd.Series(counts.reindex(keys).to_numpy(), index=X.index).fillna(0)

    h7 = h.loc[h["days_ago"] <= 7]
    h30 = h.loc[h["days_ago"] <= 30]
    h90 = h.loc[h["days_ago"] <= 90]

    for name, z in (("7d", h7), ("30d", h30), ("90d", h90)):
        out["f_item_pop_" + name] = mapped(z.groupby("article_id").size(), a)
    out["f_item_pop_all"] = mapped(h.groupby("article_id").size(), a)
    out["f_item_unique_buyers"] = mapped(
        h.groupby("article_id")["customer_id"].nunique(), a
    )
    out["f_item_recency"] = a.map(h.groupby("article_id")["days_ago"].min())

    out["f_user_item_30d"] = pair_count(h30)
    out["f_user_item_all"] = pair_count(h)
    out["f_user_recency"] = c.map(h.groupby("customer_id")["days_ago"].min())
    for name, z in (("7d", h7), ("30d", h30), ("90d", h90)):
        out["f_user_purchases_" + name] = mapped(z.groupby("customer_id").size(), c)

    out["f_user_type_30d"] = category_count(h30, "raw_i_product_type_no", "product_type_no")
    out["f_user_type_all"] = category_count(h, "raw_i_product_type_no", "product_type_no")
    out["f_user_department_30d"] = category_count(h30, "raw_i_department_no", "department_no")
    out["f_user_section_30d"] = category_count(h30, "raw_i_section_no", "section_no")
    out["f_user_colour_90d"] = category_count(h90, "raw_i_colour_group_code", "colour_group_code")
    out["f_user_product_30d"] = category_count(h30, "raw_i_product_code", "product_code")

    out["f_item_mean_price"] = a.map(h.groupby("article_id")["price"].mean())
    out["f_user_price_mean"] = c.map(h.groupby("customer_id")["price"].mean())
    out["f_user_channel1_share"] = c.map(
        h.assign(_ch=(h["sales_channel_id"] == 1).astype(float))
         .groupby("customer_id")["_ch"].mean()
    )

    for raw, col, label in (
        ("raw_i_product_type_no", "product_type_no", "type"),
        ("raw_i_department_no", "department_no", "department"),
        ("raw_i_section_no", "section_no", "section"),
    ):
        pop = h30.groupby(col).size()
        out["f_item_" + label + "_pop30"] = X[raw].map(pop).fillna(0)

    out["f_age"] = X["raw_u_age"]
    return out.replace([np.inf, -np.inf], np.nan)
