import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    c, a = X["customer_id"], X["article_id"]

    def mapped(keys, values, fill=0):
        return keys.map(values).fillna(fill)

    def pair_count(z):
        counts = z.groupby(["customer_id", "article_id"]).size()
        keys = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return pd.Series(counts.reindex(keys).to_numpy(), index=X.index).fillna(0)

    def category_count(z, raw_col, hist_col):
        sentinel = -999999
        cats = z[hist_col].fillna(sentinel)
        counts = z.assign(_cat=cats).groupby(["customer_id", "_cat"]).size()
        keys = pd.MultiIndex.from_arrays([
            c.to_numpy(), X[raw_col].fillna(sentinel).to_numpy()
        ])
        return pd.Series(counts.reindex(keys).to_numpy(), index=X.index).fillna(0)

    h7 = h.loc[h["days_ago"] <= 7]
    h30 = h.loc[h["days_ago"] <= 30]
    h90 = h.loc[h["days_ago"] <= 90]

    out["f_item_pop_7d"] = mapped(a, h7.groupby("article_id").size())
    out["f_item_pop_30d"] = mapped(a, h30.groupby("article_id").size())
    out["f_item_pop_90d"] = mapped(a, h90.groupby("article_id").size())
    out["f_item_pop_all"] = mapped(a, h.groupby("article_id").size())
    out["f_item_unique_buyers"] = mapped(
        a, h.groupby("article_id")["customer_id"].nunique()
    )
    out["f_item_recency"] = mapped(
        a, h.groupby("article_id")["days_ago"].min(), np.nan
    )

    out["f_user_item_30d"] = pair_count(h30)
    out["f_user_item_all"] = pair_count(h)
    pair_recent = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    pair_keys = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
    out["f_user_item_recency"] = pd.Series(
        pair_recent.reindex(pair_keys).to_numpy(), index=X.index
    )

    out["f_user_recency"] = mapped(
        c, h.groupby("customer_id")["days_ago"].min(), np.nan
    )
    out["f_user_purchases_7d"] = mapped(c, h7.groupby("customer_id").size())
    out["f_user_purchases_30d"] = mapped(c, h30.groupby("customer_id").size())
    out["f_user_purchases_90d"] = mapped(c, h90.groupby("customer_id").size())

    out["f_user_type_30d"] = category_count(
        h30, "raw_i_product_type_no", "product_type_no"
    )
    out["f_user_type_all"] = category_count(
        h, "raw_i_product_type_no", "product_type_no"
    )
    out["f_user_department_30d"] = category_count(
        h30, "raw_i_department_no", "department_no"
    )
    out["f_user_section_30d"] = category_count(
        h30, "raw_i_section_no", "section_no"
    )
    out["f_user_colour_90d"] = category_count(
        h90, "raw_i_colour_group_code", "colour_group_code"
    )

    out["f_item_mean_price"] = mapped(a, h.groupby("article_id")["price"].mean(), np.nan)
    out["f_user_price_mean"] = mapped(c, h.groupby("customer_id")["price"].mean(), np.nan)
    out["f_user_channel1_share"] = mapped(
        c, h.assign(_ch=(h["sales_channel_id"] == 1).astype(float))
        .groupby("customer_id")["_ch"].mean(), np.nan
    )
    out["f_age"] = X["raw_u_age"]
    return out.replace([np.inf, -np.inf], np.nan)
