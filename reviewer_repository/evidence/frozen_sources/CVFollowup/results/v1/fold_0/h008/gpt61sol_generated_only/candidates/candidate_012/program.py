import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    c = X["customer_id"]
    a = X["article_id"]

    def counts_by_article(days):
        z = h if days is None else h.loc[h["days_ago"] <= days]
        return a.map(z.groupby("article_id").size()).fillna(0)

    def counts_by_customer(days):
        z = h if days is None else h.loc[h["days_ago"] <= days]
        return c.map(z.groupby("customer_id").size()).fillna(0)

    def pair_count(days):
        z = h if days is None else h.loc[h["days_ago"] <= days]
        q = z.groupby(["customer_id", "article_id"]).size()
        k = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return pd.Series(q.reindex(k).to_numpy(), index=X.index).fillna(0)

    def user_category_count(raw_col, hist_col, days):
        z = h if days is None else h.loc[h["days_ago"] <= days]
        z = z.assign(_category_key=z[hist_col].fillna(-999999))
        q = z.groupby(["customer_id", "_category_key"]).size()
        k = pd.MultiIndex.from_arrays([
            c.to_numpy(),
            X[raw_col].fillna(-999999).to_numpy()
        ])
        return pd.Series(q.reindex(k).to_numpy(), index=X.index).fillna(0)

    out["f_item_count_7d"] = counts_by_article(7)
    out["f_item_count_30d"] = counts_by_article(30)
    out["f_item_count_all"] = counts_by_article(None)
    out["f_user_item_count_30d"] = pair_count(30)
    out["f_user_item_count_all"] = pair_count(None)
    out["f_user_recency"] = c.map(h.groupby("customer_id")["days_ago"].min())
    out["f_user_count_7d"] = counts_by_customer(7)
    out["f_user_count_30d"] = counts_by_customer(30)
    out["f_user_type_count_30d"] = user_category_count(
        "raw_i_product_type_no", "product_type_no", 30
    )
    out["f_user_type_count_all"] = user_category_count(
        "raw_i_product_type_no", "product_type_no", None
    )
    out["f_user_department_count_30d"] = user_category_count(
        "raw_i_department_no", "department_no", 30
    )
    return out.replace([np.inf, -np.inf], np.nan)
