import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_user_count_7d", "f_user_count_30d", "f_user_count_all",
        "f_item_count_7d", "f_item_count_30d", "f_item_count_all",
        "f_user_item_count", "f_user_item_recent", "f_customer_recency",
        "f_code_count_30d", "f_type_affinity", "f_type_affinity_30d",
        "f_dept_affinity", "f_dept_affinity_30d"
    ]
    out = pd.DataFrame(index=X.index)
    n = len(X)

    if history is None or len(history) == 0:
        for name in names:
            out[name] = np.zeros(n, dtype=float)
        return out

    h = history
    h7 = h.loc[h["days_ago"] <= 7]
    h30 = h.loc[h["days_ago"] <= 30]

    def counts(frame, col):
        s = frame.groupby(col).size()
        return X[col].map(s).fillna(0).to_numpy()

    out["f_user_count_7d"] = counts(h7, "customer_id")
    out["f_user_count_30d"] = counts(h30, "customer_id")
    out["f_user_count_all"] = counts(h, "customer_id")
    out["f_item_count_7d"] = counts(h7, "article_id")
    out["f_item_count_30d"] = counts(h30, "article_id")
    out["f_item_count_all"] = counts(h, "article_id")

    keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(),
        X["article_id"].to_numpy()
    ])
    pair_count = h.groupby(["customer_id", "article_id"]).size()
    pair_recent = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    out["f_user_item_count"] = pair_count.reindex(keys).fillna(0).to_numpy()
    out["f_user_item_recent"] = pair_recent.reindex(keys).fillna(-1).to_numpy()

    recency = h.groupby("customer_id")["days_ago"].min()
    out["f_customer_recency"] = X["customer_id"].map(recency).fillna(-1).to_numpy()

    code_count = h30.groupby("product_code").size()
    out["f_code_count_30d"] = (
        X["raw_i_product_code"].map(code_count).fillna(0).to_numpy()
    )

    def affinity(raw_col, hist_col, prefix):
        k = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X[raw_col].to_numpy()
        ])
        all_counts = h.groupby(["customer_id", hist_col]).size()
        recent_counts = h30.groupby(["customer_id", hist_col]).size()
        out[prefix] = all_counts.reindex(k).fillna(0).to_numpy()
        out[prefix + "_30d"] = recent_counts.reindex(k).fillna(0).to_numpy()

    affinity("raw_i_product_type_no", "product_type_no", "f_type_affinity")
    affinity("raw_i_department_no", "department_no", "f_dept_affinity")

    return out[names].replace([np.inf, -np.inf], np.nan)
