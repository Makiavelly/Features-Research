import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_user_count_7d", "f_user_count_30d", "f_user_count_all",
        "f_item_count_7d", "f_item_count_30d", "f_item_count_all",
        "f_user_item_count", "f_user_item_recent", "f_customer_recency",
        "f_code_count_30d", "f_type_affinity", "f_type_affinity_30d",
        "f_dept_affinity", "f_dept_affinity_30d",
        "f_item_count_1d", "f_user_count_1d",
        "f_section_affinity", "f_section_affinity_30d",
        "f_garment_affinity", "f_garment_affinity_30d",
        "f_product_type_popularity", "f_department_popularity",
        "f_section_popularity", "f_garment_popularity"
    ]
    out = pd.DataFrame(index=X.index)
    n = len(X)

    if history is None or len(history) == 0:
        for c in names:
            out[c] = np.zeros(n, dtype=float)
        return out

    h = history
    h1 = h.loc[h["days_ago"] <= 1]
    h7 = h.loc[h["days_ago"] <= 7]
    h30 = h.loc[h["days_ago"] <= 30]

    def mapped_count(frame, key):
        s = frame.groupby(key).size()
        return X[key].map(s).fillna(0).to_numpy()

    out["f_user_count_1d"] = mapped_count(h1, "customer_id")
    out["f_user_count_7d"] = mapped_count(h7, "customer_id")
    out["f_user_count_30d"] = mapped_count(h30, "customer_id")
    out["f_user_count_all"] = mapped_count(h, "customer_id")
    out["f_item_count_1d"] = mapped_count(h1, "article_id")
    out["f_item_count_7d"] = mapped_count(h7, "article_id")
    out["f_item_count_30d"] = mapped_count(h30, "article_id")
    out["f_item_count_all"] = mapped_count(h, "article_id")

    pair_keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])
    pair_count = h.groupby(["customer_id", "article_id"]).size()
    pair_recent = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    out["f_user_item_count"] = pair_count.reindex(pair_keys).fillna(0).to_numpy()
    out["f_user_item_recent"] = pair_recent.reindex(pair_keys).fillna(-1).to_numpy()

    rec = h.groupby("customer_id")["days_ago"].min()
    out["f_customer_recency"] = X["customer_id"].map(rec).fillna(-1).to_numpy()

    code = h30.groupby("product_code").size()
    out["f_code_count_30d"] = X["raw_i_product_code"].map(code).fillna(0).to_numpy()

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
    affinity("raw_i_garment_group_no", "garment_group_no", "f_garment_affinity")

    for raw_col, hist_col, name in [
        ("raw_i_product_type_no", "product_type_no", "f_product_type_popularity"),
        ("raw_i_department_no", "department_no", "f_department_popularity"),
        ("raw_i_section_no", "section_no", "f_section_popularity"),
        ("raw_i_garment_group_no", "garment_group_no", "f_garment_popularity")
    ]:
        s = h30.groupby(hist_col).size()
        out[name] = X[raw_col].map(s).fillna(0).to_numpy()

    return out[names].replace([np.inf, -np.inf], np.nan)
