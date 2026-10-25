import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    if len(history) == 0:
        for c in [
            "f_user_count_7d", "f_user_count_30d", "f_user_count_all",
            "f_item_count_7d", "f_item_count_30d", "f_item_count_all",
            "f_user_item_count", "f_user_item_recent",
            "f_customer_recency", "f_code_count_30d", "f_type_affinity",
            "f_dept_affinity"
        ]:
            out[c] = np.zeros(n)
        return out

    h = history
    h7 = h[h["days_ago"] <= 7]
    h30 = h[h["days_ago"] <= 30]

    def map_group(frame, key, col=None, agg="size"):
        if col is None:
            s = frame.groupby(key).size()
        else:
            s = frame.groupby(key)[col].agg(agg)
        return X[key].map(s)

    out["f_user_count_7d"] = map_group(h7, "customer_id").fillna(0)
    out["f_user_count_30d"] = map_group(h30, "customer_id").fillna(0)
    out["f_user_count_all"] = map_group(h, "customer_id").fillna(0)

    out["f_item_count_7d"] = map_group(h7, "article_id").fillna(0)
    out["f_item_count_30d"] = map_group(h30, "article_id").fillna(0)
    out["f_item_count_all"] = map_group(h, "article_id").fillna(0)

    ui = h.groupby(["customer_id", "article_id"]).size()
    keys = pd.MultiIndex.from_arrays([X["customer_id"], X["article_id"]])
    out["f_user_item_count"] = ui.reindex(keys).to_numpy()
    ur = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    out["f_user_item_recent"] = ur.reindex(keys).to_numpy()

    rec = h.groupby("customer_id")["days_ago"].min()
    out["f_customer_recency"] = X["customer_id"].map(rec)

    code30 = h30.groupby("product_code").size()
    out["f_code_count_30d"] = X["raw_i_product_code"].map(code30).fillna(0)

    def affinity(raw_col, hist_col, name):
        g = h.groupby(["customer_id", hist_col]).size()
        k = pd.MultiIndex.from_arrays([X["customer_id"], X[raw_col]])
        out[name] = g.reindex(k).to_numpy()
        g30 = h30.groupby(["customer_id", hist_col]).size()
        out[name + "_30d"] = g30.reindex(k).to_numpy()

    affinity("raw_i_product_type_no", "product_type_no", "f_type_affinity")
    affinity("raw_i_department_no", "department_no", "f_dept_affinity")

    for c in out.columns:
        out[c] = pd.to_numeric(out[c], errors="coerce").replace([np.inf, -np.inf], np.nan)
    return out
