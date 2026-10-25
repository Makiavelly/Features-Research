def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    uid = X["customer_id"].to_numpy()
    aid = X["article_id"].to_numpy()
    n = len(X)
    names = (
        "f_pair_14d", "f_pair_45d", "f_pair_120d",
        "f_user_purchases_14d", "f_user_purchases_45d",
        "f_article_purchases_14d", "f_article_purchases_45d",
        "f_article_users_120d", "f_user_department_14d",
        "f_user_type_14d", "f_user_section_45d", "f_user_product_120d",
    )
    if h is None or len(h) == 0:
        for z in names:
            out[z] = 0.0
        return out

    d = pd.to_numeric(h["days_ago"], errors="coerce")
    h14 = h.loc[d <= 14]
    h45 = h.loc[d <= 45]
    h120 = h.loc[d <= 120]
    pi = pd.MultiIndex.from_arrays([uid, aid])

    def pair(z):
        if len(z) == 0:
            return np.zeros(n)
        s = z.groupby(["customer_id", "article_id"], sort=False).size()
        return s.reindex(pi).fillna(0).to_numpy()

    out["f_pair_14d"] = pair(h14)
    out["f_pair_45d"] = pair(h45)
    out["f_pair_120d"] = pair(h120)

    out["f_user_purchases_14d"] = X["customer_id"].map(
        h14.groupby("customer_id", sort=False).size()
    ).fillna(0).to_numpy()
    out["f_user_purchases_45d"] = X["customer_id"].map(
        h45.groupby("customer_id", sort=False).size()
    ).fillna(0).to_numpy()

    out["f_article_purchases_14d"] = X["article_id"].map(
        h14.groupby("article_id", sort=False).size()
    ).fillna(0).to_numpy()
    out["f_article_purchases_45d"] = X["article_id"].map(
        h45.groupby("article_id", sort=False).size()
    ).fillna(0).to_numpy()
    out["f_article_users_120d"] = X["article_id"].map(
        h120.groupby("article_id", sort=False)["customer_id"].nunique()
    ).fillna(0).to_numpy()

    def cat(hist, hc, xc, name):
        if len(hist) == 0 or hc not in hist.columns or xc not in X.columns:
            out[name] = 0.0
            return
        s = hist.groupby(["customer_id", hc], sort=False).size()
        k = pd.MultiIndex.from_arrays([uid, X[xc].to_numpy()])
        out[name] = s.reindex(k).fillna(0).to_numpy()

    cat(h14, "department_no", "raw_i_department_no", "f_user_department_14d")
    cat(h14, "product_type_no", "raw_i_product_type_no", "f_user_type_14d")
    cat(h45, "section_no", "raw_i_section_no", "f_user_section_45d")
    cat(h120, "product_code", "raw_i_product_code", "f_user_product_120d")

    return out.replace([np.inf, -np.inf], np.nan)
