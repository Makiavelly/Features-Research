import pandas as pd
import numpy as np


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    c = X["customer_id"]
    a = X["article_id"]

    def within(days):
        return h.loc[h["days_ago"] <= days]

    def article_count(z):
        return a.map(z.groupby("article_id").size()).fillna(0)

    def customer_count(z):
        return c.map(z.groupby("customer_id").size()).fillna(0)

    def pair_count(z):
        counts = z.groupby(["customer_id", "article_id"]).size()
        keys = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return pd.Series(counts.reindex(keys).to_numpy(), index=X.index).fillna(0)

    def user_category_count(raw_col, hist_col):
        keys_hist = h.assign(_category_key=h[hist_col].fillna(-999999))
        counts = keys_hist.groupby(["customer_id", "_category_key"]).size()
        keys = pd.MultiIndex.from_arrays([
            c.to_numpy(),
            X[raw_col].fillna(-999999).to_numpy()
        ])
        return pd.Series(counts.reindex(keys).to_numpy(), index=X.index).fillna(0)

    h7 = within(7)
    h30 = within(30)

    out["f_item_count_7d"] = article_count(h7)
    out["f_item_count_30d"] = article_count(h30)
    out["f_item_count_all"] = article_count(h)
    out["f_user_item_count_30d"] = pair_count(h30)
    out["f_user_item_count_all"] = pair_count(h)
    out["f_user_count_7d"] = customer_count(h7)
    out["f_user_count_30d"] = customer_count(h30)
    out["f_user_recency"] = c.map(h.groupby("customer_id")["days_ago"].min())
    out["f_item_recency"] = a.map(h.groupby("article_id")["days_ago"].min())
    out["f_user_type_count_all"] = user_category_count(
        "raw_i_product_type_no", "product_type_no"
    )
    out["f_user_department_count_all"] = user_category_count(
        "raw_i_department_no", "department_no"
    )
    out["f_user_section_count_all"] = user_category_count(
        "raw_i_section_no", "section_no"
    )

    return out.replace([np.inf, -np.inf], np.nan)
