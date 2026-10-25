def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)
    u = X["customer_id"].to_numpy()
    a = X["article_id"].to_numpy()

    cols = (
        "f_pair_last7", "f_pair_last60", "f_pair_last365",
        "f_pair_gap", "f_user_active_days", "f_user_unique_items",
        "f_item_unique_users", "f_item_last14", "f_item_last60",
        "f_user_department_rate", "f_user_type_rate",
        "f_user_section_rate", "f_user_product_rate", "f_user_colour_rate",
    )
    if h is None or len(h) == 0:
        for c in cols:
            out[c] = np.nan if c == "f_pair_gap" else 0.0
        return out

    d = pd.to_numeric(h["days_ago"], errors="coerce")
    h7 = h.loc[d <= 7]
    h14 = h.loc[d <= 14]
    h60 = h.loc[d <= 60]
    h365 = h.loc[d <= 365]
    pi = pd.MultiIndex.from_arrays([u, a])

    def pc(z):
        if len(z) == 0:
            return np.zeros(n)
        s = z.groupby(["customer_id", "article_id"], sort=False).size()
        return s.reindex(pi).fillna(0).to_numpy()

    out["f_pair_last7"] = pc(h7)
    out["f_pair_last60"] = pc(h60)
    out["f_pair_last365"] = pc(h365)

    last = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
    out["f_pair_gap"] = last.reindex(pi).to_numpy()

    ug = h365.groupby("customer_id", sort=False)
    out["f_user_active_days"] = X["customer_id"].map(
        ug["days_ago"].nunique()
    ).fillna(0).to_numpy()
    out["f_user_unique_items"] = X["customer_id"].map(
        ug["article_id"].nunique()
    ).fillna(0).to_numpy()

    out["f_item_unique_users"] = X["article_id"].map(
        h365.groupby("article_id", sort=False)["customer_id"].nunique()
    ).fillna(0).to_numpy()
    out["f_item_last14"] = X["article_id"].map(
        h14.groupby("article_id", sort=False).size()
    ).fillna(0).to_numpy()
    out["f_item_last60"] = X["article_id"].map(
        h60.groupby("article_id", sort=False).size()
    ).fillna(0).to_numpy()

    def affinity(z, hc, xc, name):
        if len(z) == 0 or xc not in X.columns:
            out[name] = 0.0
            return
        num = z.groupby(["customer_id", hc], sort=False).size()
        den = z.groupby("customer_id", sort=False).size()
        key = pd.MultiIndex.from_arrays([u, X[xc].to_numpy()])
        nv = num.reindex(key).fillna(0).to_numpy()
        dv = X["customer_id"].map(den).fillna(0).to_numpy()
        out[name] = nv / np.maximum(dv, 1)

    affinity(h60, "department_no", "raw_i_department_no",
             "f_user_department_rate")
    affinity(h60, "product_type_no", "raw_i_product_type_no",
             "f_user_type_rate")
    affinity(h60, "section_no", "raw_i_section_no",
             "f_user_section_rate")
    affinity(h365, "product_code", "raw_i_product_code",
             "f_user_product_rate")
    affinity(h60, "colour_group_code", "raw_i_colour_group_code",
             "f_user_colour_rate")

    return out.replace([np.inf, -np.inf], np.nan)
