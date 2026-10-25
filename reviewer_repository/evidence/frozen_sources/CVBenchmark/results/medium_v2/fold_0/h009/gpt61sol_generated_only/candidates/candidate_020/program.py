def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)
    uid = X["customer_id"].to_numpy()
    aid = X["article_id"].to_numpy()
    pair_index = pd.MultiIndex.from_arrays([uid, aid])

    columns = (
        "f_pair_count", "f_pair_count_30d", "f_pair_count_180d",
        "f_pair_recency", "f_customer_recency", "f_user_count_30d",
        "f_user_count_365d", "f_item_count_7d", "f_item_count_30d",
        "f_item_count_365d", "f_item_recency", "f_user_product_pref",
        "f_user_department_pref", "f_user_type_pref", "f_user_section_pref",
        "f_user_colour_pref",
    )
    if h is None or len(h) == 0:
        for c in columns:
            out[c] = np.nan if "recency" in c else 0.0
        return out

    days = pd.to_numeric(h["days_ago"], errors="coerce")
    h7 = h.loc[days <= 7]
    h30 = h.loc[days <= 30]
    h180 = h.loc[days <= 180]
    h365 = h.loc[days <= 365]

    def pair_count(hist):
        if len(hist) == 0:
            return np.zeros(n, dtype=float)
        counts = hist.groupby(["customer_id", "article_id"], sort=False).size()
        return counts.reindex(pair_index).fillna(0).to_numpy()

    out["f_pair_count"] = pair_count(h)
    out["f_pair_count_30d"] = pair_count(h30)
    out["f_pair_count_180d"] = pair_count(h180)

    out["f_pair_recency"] = h.groupby(
        ["customer_id", "article_id"], sort=False
    )["days_ago"].min().reindex(pair_index).to_numpy()
    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id", sort=False)["days_ago"].min()
    ).to_numpy()

    for hist, label in ((h30, "30d"), (h365, "365d")):
        out["f_user_count_" + label] = X["customer_id"].map(
            hist.groupby("customer_id", sort=False).size()
        ).fillna(0).to_numpy()

    for hist, label in ((h7, "7d"), (h30, "30d"), (h365, "365d")):
        out["f_item_count_" + label] = X["article_id"].map(
            hist.groupby("article_id", sort=False).size()
        ).fillna(0).to_numpy()

    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    ).to_numpy()

    def add_pref(hist, hist_col, raw_col, name):
        if raw_col not in X.columns or len(hist) == 0:
            out[name] = 0.0
            return
        counts = hist.groupby(["customer_id", hist_col], sort=False).size()
        keys = pd.MultiIndex.from_arrays([uid, X[raw_col].to_numpy()])
        out[name] = counts.reindex(keys).fillna(0).to_numpy()

    add_pref(h, "product_code", "raw_i_product_code", "f_user_product_pref")
    add_pref(h30, "department_no", "raw_i_department_no", "f_user_department_pref")
    add_pref(h30, "product_type_no", "raw_i_product_type_no", "f_user_type_pref")
    add_pref(h30, "section_no", "raw_i_section_no", "f_user_section_pref")
    add_pref(h30, "colour_group_code", "raw_i_colour_group_code", "f_user_colour_pref")

    return out.replace([np.inf, -np.inf], np.nan)
