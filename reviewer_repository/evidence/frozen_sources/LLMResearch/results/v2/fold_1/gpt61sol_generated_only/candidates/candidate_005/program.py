import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_user_count_7d", "f_user_count_30d", "f_user_count_all",
        "f_user_items_30d", "f_item_count_7d", "f_item_count_30d",
        "f_item_count_all", "f_item_recency", "f_user_item_count",
        "f_user_item_recent", "f_customer_recency", "f_code_count_7d",
        "f_code_count_30d", "f_type_affinity", "f_type_affinity_30d",
        "f_dept_affinity", "f_dept_affinity_30d", "f_section_affinity",
        "f_section_affinity_30d"
    ]
    out = pd.DataFrame(index=X.index)
    n = len(X)

    if history is None or len(history) == 0:
        for c in names:
            out[c] = np.zeros(n, dtype=float)
        return out

    h = history
    h7 = h.loc[h["days_ago"] <= 7]
    h30 = h.loc[h["days_ago"] <= 30]

    def mapped_count(frame, key):
        s = frame.groupby(key).size()
        return X[key].map(s).fillna(0).to_numpy()

    out["f_user_count_7d"] = mapped_count(h7, "customer_id")
    out["f_user_count_30d"] = mapped_count(h30, "customer_id")
    out["f_user_count_all"] = mapped_count(h, "customer_id")

    ud = h30.groupby("customer_id")["article_id"].nunique()
    out["f_user_items_30d"] = X["customer_id"].map(ud).fillna(0).to_numpy()

    out["f_item_count_7d"] = mapped_count(h7, "article_id")
    out["f_item_count_30d"] = mapped_count(h30, "article_id")
    out["f_item_count_all"] = mapped_count(h, "article_id")

    item_rec = h.groupby("article_id")["days_ago"].min()
    out["f_item_recency"] = X["article_id"].map(item_rec).fillna(-1).to_numpy()

    pair_keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])
    pc = h.groupby(["customer_id", "article_id"]).size()
    pr = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    out["f_user_item_count"] = pc.reindex(pair_keys).fillna(0).to_numpy()
    out["f_user_item_recent"] = pr.reindex(pair_keys).fillna(-1).to_numpy()

    ur = h.groupby("customer_id")["days_ago"].min()
    out["f_customer_recency"] = X["customer_id"].map(ur).fillna(-1).to_numpy()

    for window, frame in [("7d", h7), ("30d", h30)]:
        s = frame.groupby("product_code").size()
        out["f_code_count_" + window] = (
            X["raw_i_product_code"].map(s).fillna(0).to_numpy()
        )

    def affinity(raw_col, hist_col, prefix):
        keys = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X[raw_col].to_numpy()
        ])
        a = h.groupby(["customer_id", hist_col]).size()
        b = h30.groupby(["customer_id", hist_col]).size()
        out[prefix] = a.reindex(keys).fillna(0).to_numpy()
        out[prefix + "_30d"] = b.reindex(keys).fillna(0).to_numpy()

    affinity("raw_i_product_type_no", "product_type_no", "f_type_affinity")
    affinity("raw_i_department_no", "department_no", "f_dept_affinity")
    affinity("raw_i_section_no", "section_no", "f_section_affinity")

    return out[names].replace([np.inf, -np.inf], np.nan)
