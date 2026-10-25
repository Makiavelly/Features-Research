import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    c = X["customer_id"]
    a = X["article_id"]

    def article_count(days):
        z = h if days is None else h.loc[h["days_ago"] <= days]
        return a.map(z.groupby("article_id").size()).fillna(0)

    def customer_count(days):
        z = h if days is None else h.loc[h["days_ago"] <= days]
        return c.map(z.groupby("customer_id").size()).fillna(0)

    def user_item_count(days):
        z = h if days is None else h.loc[h["days_ago"] <= days]
        q = z.groupby(["customer_id", "article_id"]).size()
        k = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return pd.Series(q.reindex(k).to_numpy(), index=X.index).fillna(0)

    def user_category_count(raw_col, hist_col, days):
        z = h if days is None else h.loc[h["days_ago"] <= days]
        q = z.groupby(["customer_id", hist_col]).size()
        v = X[raw_col].fillna(-999999).to_numpy()
        hv = z[hist_col].fillna(-999999)
        q = z.assign(_category_key=hv).groupby(
            ["customer_id", "_category_key"]
        ).size()
        k = pd.MultiIndex.from_arrays([c.to_numpy(), v])
        return pd.Series(q.reindex(k).to_numpy(), index=X.index).fillna(0)

    out["f_item_purchases_7d"] = article_count(7)
    out["f_item_purchases_30d"] = article_count(30)
    out["f_item_purchases_all"] = article_count(None)

    out["f_user_item_purchases_7d"] = user_item_count(7)
    out["f_user_item_purchases_30d"] = user_item_count(30)
    out["f_user_item_purchases_all"] = user_item_count(None)

    out["f_user_recency"] = c.map(h.groupby("customer_id")["days_ago"].min())
    out["f_user_purchases_7d"] = customer_count(7)
    out["f_user_purchases_30d"] = customer_count(30)

    out["f_user_type_purchases_30d"] = user_category_count(
        "raw_i_product_type_no", "product_type_no", 30
    )
    out["f_user_type_purchases_all"] = user_category_count(
        "raw_i_product_type_no", "product_type_no", None
    )
    out["f_user_department_purchases_30d"] = user_category_count(
        "raw_i_department_no", "department_no", 30
    )

    return out.replace([np.inf, -np.inf], np.nan)
