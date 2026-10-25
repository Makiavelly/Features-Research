import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    c = X["customer_id"]
    a = X["article_id"]

    def mapped(keys, values, default=0):
        return keys.map(values).fillna(default)

    def pair_lookup(z, value=None, agg="size"):
        if z.empty:
            return pd.Series(0.0, index=X.index)
        if value is None:
            s = z.groupby(["customer_id", "article_id"]).size()
        else:
            s = z.groupby(["customer_id", "article_id"])[value].agg(agg)
        idx = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return pd.Series(s.reindex(idx).to_numpy(), index=X.index).fillna(0)

    def category_lookup(z, raw_col, hist_col):
        if z.empty:
            return pd.Series(0.0, index=X.index)
        sentinel = -999999
        values = z[hist_col].fillna(sentinel)
        s = z.assign(_cat=values).groupby(["customer_id", "_cat"]).size()
        idx = pd.MultiIndex.from_arrays([
            c.to_numpy(), X[raw_col].fillna(sentinel).to_numpy()
        ])
        return pd.Series(s.reindex(idx).to_numpy(), index=X.index).fillna(0)

    h7 = h.loc[h["days_ago"] <= 7]
    h30 = h.loc[h["days_ago"] <= 30]
    h90 = h.loc[h["days_ago"] <= 90]

    out["f_item_pop_7d"] = mapped(a, h7.groupby("article_id").size())
    out["f_item_pop_30d"] = mapped(a, h30.groupby("article_id").size())
    out["f_item_pop_90d"] = mapped(a, h90.groupby("article_id").size())
    out["f_item_pop_all"] = mapped(a, h.groupby("article_id").size())
    out["f_item_buyers_all"] = mapped(
        a, h.groupby("article_id")["customer_id"].nunique()
    )
    out["f_item_recency"] = mapped(
        a, h.groupby("article_id")["days_ago"].min(), default=np.nan
    )

    out["f_pair_count_30d"] = pair_lookup(h30)
    out["f_pair_count_all"] = pair_lookup(h)
    out["f_pair_recency"] = pair_lookup(h, "days_ago", "min")

    out["f_user_recency"] = mapped(
        c, h.groupby("customer_id")["days_ago"].min(), default=np.nan
    )
    out["f_user_purchases_7d"] = mapped(c, h7.groupby("customer_id").size())
    out["f_user_purchases_30d"] = mapped(c, h30.groupby("customer_id").size())
    out["f_user_purchases_90d"] = mapped(c, h90.groupby("customer_id").size())

    out["f_user_type_30d"] = category_lookup(h30, "raw_i_product_type_no", "product_type_no")
    out["f_user_type_all"] = category_lookup(h, "raw_i_product_type_no", "product_type_no")
    out["f_user_department_30d"] = category_lookup(h30, "raw_i_department_no", "department_no")
    out["f_user_section_30d"] = category_lookup(h30, "raw_i_section_no", "section_no")
    out["f_user_colour_90d"] = category_lookup(h90, "raw_i_colour_group_code", "colour_group_code")
    out["f_user_product_30d"] = category_lookup(h30, "raw_i_product_code", "product_code")

    out["f_item_mean_price"] = mapped(a, h.groupby("article_id")["price"].mean(), default=np.nan)
    out["f_user_mean_price"] = mapped(c, h.groupby("customer_id")["price"].mean(), default=np.nan)
    out["f_user_channel1_share"] = mapped(
        c, h.assign(_ch=(h["sales_channel_id"] == 1).astype(float))
            .groupby("customer_id")["_ch"].mean(), default=np.nan
    )
    out["f_age"] = X["raw_u_age"]
    return out.replace([np.inf, -np.inf], np.nan)
