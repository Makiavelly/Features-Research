import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    c = X["customer_id"]
    a = X["article_id"]

    def window(n):
        if n is None:
            return h
        return h.loc[h["days_ago"] <= n]

    def mapped_count(key, n=None, value=None):
        z = window(n)
        if value is None:
            s = z.groupby(key).size()
            return X[key if key in X.columns else "article_id"].map(s).fillna(0)
        s = z.groupby(key)[value].size()
        return X[key].map(s).fillna(0)

    def pair_count(n=None):
        z = window(n)
        q = z.groupby(["customer_id", "article_id"]).size()
        k = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return pd.Series(q.reindex(k).to_numpy(), index=X.index).fillna(0)

    def pair_recency():
        q = h.groupby(["customer_id", "article_id"])["days_ago"].min()
        k = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return pd.Series(q.reindex(k).to_numpy(), index=X.index)

    def user_cat(raw, hist, n=30):
        z = window(n)
        q = z.groupby(["customer_id", hist]).size()
        k = pd.MultiIndex.from_arrays([
            c.to_numpy(),
            X[raw].to_numpy()
        ])
        return pd.Series(q.reindex(k).to_numpy(), index=X.index).fillna(0)

    def code_pop(raw, hist, n=30):
        z = window(n)
        q = z.groupby(hist).size()
        return X[raw].map(q).fillna(0)

    out["f_item_purchases_7d"] = a.map(window(7).groupby("article_id").size()).fillna(0)
    out["f_item_purchases_30d"] = a.map(window(30).groupby("article_id").size()).fillna(0)
    out["f_item_purchases_all"] = a.map(h.groupby("article_id").size()).fillna(0)

    out["f_item_recency"] = a.map(h.groupby("article_id")["days_ago"].min())
    out["f_item_unique_customers_30d"] = a.map(
        window(30).groupby("article_id")["customer_id"].nunique()
    ).fillna(0)

    out["f_user_purchases_7d"] = c.map(window(7).groupby("customer_id").size()).fillna(0)
    out["f_user_purchases_30d"] = c.map(window(30).groupby("customer_id").size()).fillna(0)
    out["f_user_purchases_all"] = c.map(h.groupby("customer_id").size()).fillna(0)

    out["f_user_item_purchases_30d"] = pair_count(30)
    out["f_user_item_purchases_all"] = pair_count(None)
    out["f_user_item_recency"] = pair_recency()

    out["f_user_product_type_purchases_30d"] = user_cat(
        "raw_i_product_type_no", "product_type_no", 30
    )
    out["f_user_department_purchases_30d"] = user_cat(
        "raw_i_department_no", "department_no", 30
    )

    out["f_product_code_purchases_30d"] = code_pop(
        "raw_i_product_code", "product_code", 30
    )
    out["f_product_type_purchases_30d"] = code_pop(
        "raw_i_product_type_no", "product_type_no", 30
    )

    return out.replace([np.inf, -np.inf], np.nan)
