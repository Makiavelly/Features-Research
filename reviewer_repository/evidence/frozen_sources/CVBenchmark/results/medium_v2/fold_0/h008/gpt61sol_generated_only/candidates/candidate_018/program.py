import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    c = X["customer_id"]
    a = X["article_id"]

    def mapped_counts(z, key):
        return X[key].map(z.groupby(key).size()).fillna(0)

    def pair_counts(z):
        q = z.groupby(["customer_id", "article_id"]).size()
        k = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return pd.Series(q.reindex(k).to_numpy(), index=X.index).fillna(0)

    def category_counts(z, raw_col, hist_col):
        q = z.assign(_cat=z[hist_col].fillna(-999999)).groupby(
            ["customer_id", "_cat"]
        ).size()
        k = pd.MultiIndex.from_arrays([
            c.to_numpy(), X[raw_col].fillna(-999999).to_numpy()
        ])
        return pd.Series(q.reindex(k).to_numpy(), index=X.index).fillna(0)

    h7 = h.loc[h["days_ago"] <= 7]
    h30 = h.loc[h["days_ago"] <= 30]
    h90 = h.loc[h["days_ago"] <= 90]

    out["f_item_pop_7d"] = a.map(h7.groupby("article_id").size()).fillna(0)
    out["f_item_pop_30d"] = a.map(h30.groupby("article_id").size()).fillna(0)
    out["f_item_pop_all"] = a.map(h.groupby("article_id").size()).fillna(0)
    out["f_user_item_30d"] = pair_counts(h30)
    out["f_user_item_all"] = pair_counts(h)
    out["f_user_recency"] = c.map(h.groupby("customer_id")["days_ago"].min())
    out["f_user_purchases_7d"] = c.map(h7.groupby("customer_id").size()).fillna(0)
    out["f_user_purchases_30d"] = c.map(h30.groupby("customer_id").size()).fillna(0)
    out["f_user_type_30d"] = category_counts(h30, "raw_i_product_type_no", "product_type_no")
    out["f_user_type_all"] = category_counts(h, "raw_i_product_type_no", "product_type_no")
    out["f_user_department_30d"] = category_counts(h30, "raw_i_department_no", "department_no")
    out["f_user_section_30d"] = category_counts(h30, "raw_i_section_no", "section_no")
    out["f_user_colour_90d"] = category_counts(h90, "raw_i_colour_group_code", "colour_group_code")
    out["f_user_product_30d"] = category_counts(h30, "raw_i_product_code", "product_code")

    age = X["raw_u_age"]
    out["f_age"] = age
    out["f_item_unique_buyers"] = a.map(h.groupby("article_id")["customer_id"].nunique()).fillna(0)
    out["f_item_mean_price"] = a.map(h.groupby("article_id")["price"].mean())
    out["f_user_channel1_share"] = c.map(
        h.assign(_ch=(h["sales_channel_id"] == 1).astype(float))
         .groupby("customer_id")["_ch"].mean()
    )
    out["f_user_price_mean"] = c.map(h.groupby("customer_id")["price"].mean())
    return out.replace([np.inf, -np.inf], np.nan)
