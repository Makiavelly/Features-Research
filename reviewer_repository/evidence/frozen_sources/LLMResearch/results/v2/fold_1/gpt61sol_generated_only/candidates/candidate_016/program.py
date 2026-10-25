import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_user_count_7d", "f_user_count_30d", "f_user_count_all",
        "f_item_count_7d", "f_item_count_30d", "f_item_count_all",
        "f_user_item_count", "f_user_item_recent", "f_customer_recency",
        "f_code_count_30d", "f_type_affinity", "f_type_affinity_30d",
        "f_dept_affinity", "f_dept_affinity_30d",
        "f_user_weighted_activity", "f_item_weighted_activity",
        "f_raw_product_code", "f_raw_product_type", "f_raw_department",
        "f_raw_section", "f_raw_garment", "f_raw_colour",
        "f_raw_index_group", "f_user_age"
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
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])
    pair_count = h.groupby(["customer_id", "article_id"]).size()
    pair_recent = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    out["f_user_item_count"] = pair_count.reindex(keys).fillna(0).to_numpy()
    out["f_user_item_recent"] = pair_recent.reindex(keys).fillna(-1).to_numpy()

    rec = h.groupby("customer_id")["days_ago"].min()
    out["f_customer_recency"] = X["customer_id"].map(rec).fillna(-1).to_numpy()

    code = h30.groupby("product_code").size()
    out["f_code_count_30d"] = X["raw_i_product_code"].map(code).fillna(0).to_numpy()

    uw = h.assign(_w=np.exp(-h["days_ago"].astype(float) / 30.0))
    us = uw.groupby("customer_id")["_w"].sum()
    it = uw.groupby("article_id")["_w"].sum()
    out["f_user_weighted_activity"] = X["customer_id"].map(us).fillna(0).to_numpy()
    out["f_item_weighted_activity"] = X["article_id"].map(it).fillna(0).to_numpy()

    def affinity(raw_col, hist_col, prefix):
        k = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X[raw_col].to_numpy()
        ])
        a = h.groupby(["customer_id", hist_col]).size()
        b = h30.groupby(["customer_id", hist_col]).size()
        out[prefix] = a.reindex(k).fillna(0).to_numpy()
        out[prefix + "_30d"] = b.reindex(k).fillna(0).to_numpy()

    affinity("raw_i_product_type_no", "product_type_no", "f_type_affinity")
    affinity("raw_i_department_no", "department_no", "f_dept_affinity")

    for raw, name in [
        ("raw_i_product_code", "f_raw_product_code"),
        ("raw_i_product_type_no", "f_raw_product_type"),
        ("raw_i_department_no", "f_raw_department"),
        ("raw_i_section_no", "f_raw_section"),
        ("raw_i_garment_group_no", "f_raw_garment"),
        ("raw_i_colour_group_code", "f_raw_colour"),
        ("raw_i_index_group_no", "f_raw_index_group")
    ]:
        out[name] = pd.to_numeric(X[raw], errors="coerce").to_numpy()

    age = h.groupby("customer_id")["customer_age"].last()
    out["f_user_age"] = X["customer_id"].map(age).fillna(
        X["raw_u_age"]
    ).to_numpy()

    return out[names].replace([np.inf, -np.inf], np.nan)
