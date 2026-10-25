def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)
    users = X["customer_id"].to_numpy()
    items = X["article_id"].to_numpy()

    feature_names = (
        "f_pair_count", "f_pair_count_30d", "f_pair_recency",
        "f_customer_recency", "f_user_count_30d", "f_user_count_365d",
        "f_item_count_7d", "f_item_count_30d", "f_item_count_365d",
        "f_item_recency", "f_user_product_pref", "f_user_department_pref",
        "f_user_type_pref", "f_user_section_pref", "f_user_colour_pref",
        "f_user_garment_pref",
    )
    if h is None or len(h) == 0:
        for name in feature_names:
            out[name] = np.nan if "recency" in name else 0.0
        return out

    days = pd.to_numeric(h["days_ago"], errors="coerce")
    h30 = h.loc[days <= 30]
    h365 = h.loc[days <= 365]

    def pair_counts(hist):
        if len(hist) == 0:
            return np.zeros(n, dtype=float)
        counts = hist.groupby(["customer_id", "article_id"], sort=False).size()
        return counts.reindex(
            pd.MultiIndex.from_arrays([users, items])
        ).fillna(0).to_numpy()

    out["f_pair_count"] = pair_counts(h)
    out["f_pair_count_30d"] = pair_counts(h30)

    pair_rec = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
    out["f_pair_recency"] = pair_rec.reindex(
        pd.MultiIndex.from_arrays([users, items])
    ).to_numpy()

    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id", sort=False)["days_ago"].min()
    ).to_numpy()

    out["f_user_count_30d"] = X["customer_id"].map(
        h30.groupby("customer_id", sort=False).size()
    ).fillna(0).to_numpy()
    out["f_user_count_365d"] = X["customer_id"].map(
        h365.groupby("customer_id", sort=False).size()
    ).fillna(0).to_numpy()

    for window, label in ((7, "7d"), (30, "30d"), (365, "365d")):
        hh = h.loc[days <= window]
        out["f_item_count_" + label] = X["article_id"].map(
            hh.groupby("article_id", sort=False).size()
        ).fillna(0).to_numpy()

    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    ).to_numpy()

    def preference(hist, hist_col, raw_col, feature):
        if len(hist) == 0 or raw_col not in X.columns:
            out[feature] = 0.0
            return
        counts = hist.groupby(["customer_id", hist_col], sort=False).size()
        index = pd.MultiIndex.from_arrays([users, X[raw_col].to_numpy()])
        out[feature] = counts.reindex(index).fillna(0).to_numpy()

    preference(h, "product_code", "raw_i_product_code", "f_user_product_pref")
    preference(h30, "department_no", "raw_i_department_no", "f_user_department_pref")
    preference(h30, "product_type_no", "raw_i_product_type_no", "f_user_type_pref")
    preference(h30, "section_no", "raw_i_section_no", "f_user_section_pref")
    preference(h30, "colour_group_code", "raw_i_colour_group_code", "f_user_colour_pref")
    preference(h30, "garment_group_no", "raw_i_garment_group_no", "f_user_garment_pref")

    return out.replace([np.inf, -np.inf], np.nan)
