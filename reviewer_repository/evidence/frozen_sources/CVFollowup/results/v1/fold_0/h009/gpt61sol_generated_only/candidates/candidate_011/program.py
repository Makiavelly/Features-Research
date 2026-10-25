def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)
    user = X["customer_id"].to_numpy()
    item = X["article_id"].to_numpy()

    names = (
        "f_pair_count", "f_pair_count_30d", "f_pair_count_180d",
        "f_pair_recency", "f_user_count_30d", "f_user_count_365d",
        "f_item_count_7d", "f_item_count_30d", "f_item_count_365d",
        "f_item_recency", "f_user_product_pref", "f_user_department_pref",
        "f_user_type_pref", "f_user_section_pref", "f_user_colour_pref",
        "f_user_garment_pref", "f_user_channel_pref", "f_item_popularity",
    )
    if h is None or len(h) == 0:
        for name in names:
            out[name] = np.nan if "recency" in name else 0.0
        return out

    days = pd.to_numeric(h["days_ago"], errors="coerce")
    windows = {d: h.loc[days <= d] for d in (7, 30, 180, 365)}

    def pair_count(hist):
        if len(hist) == 0:
            return np.zeros(n)
        s = hist.groupby(["customer_id", "article_id"], sort=False).size()
        return s.reindex(pd.MultiIndex.from_arrays([user, item])).fillna(0).to_numpy()

    out["f_pair_count"] = pair_count(h)
    out["f_pair_count_30d"] = pair_count(windows[30])
    out["f_pair_count_180d"] = pair_count(windows[180])

    rec = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
    out["f_pair_recency"] = rec.reindex(
        pd.MultiIndex.from_arrays([user, item])
    ).to_numpy()

    for d, label in ((30, "30d"), (365, "365d")):
        out["f_user_count_" + label] = X["customer_id"].map(
            windows[d].groupby("customer_id", sort=False).size()
        ).fillna(0).to_numpy()

    for d, label in ((7, "7d"), (30, "30d"), (365, "365d")):
        out["f_item_count_" + label] = X["article_id"].map(
            windows[d].groupby("article_id", sort=False).size()
        ).fillna(0).to_numpy()

    item_counts = h.groupby("article_id", sort=False).size()
    out["f_item_popularity"] = X["article_id"].map(item_counts).fillna(0).to_numpy()
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    ).to_numpy()

    def preference(hist, hist_col, raw_col, feature):
        if len(hist) == 0 or raw_col not in X.columns:
            out[feature] = 0.0
            return
        s = hist.groupby(["customer_id", hist_col], sort=False).size()
        ix = pd.MultiIndex.from_arrays([user, X[raw_col].to_numpy()])
        out[feature] = s.reindex(ix).fillna(0).to_numpy()

    preference(h, "product_code", "raw_i_product_code", "f_user_product_pref")
    preference(windows[180], "department_no", "raw_i_department_no", "f_user_department_pref")
    preference(windows[180], "product_type_no", "raw_i_product_type_no", "f_user_type_pref")
    preference(windows[180], "section_no", "raw_i_section_no", "f_user_section_pref")
    preference(windows[180], "colour_group_code", "raw_i_colour_group_code", "f_user_colour_pref")
    preference(windows[180], "garment_group_no", "raw_i_garment_group_no", "f_user_garment_pref")
    preference(windows[180], "sales_channel_id", "raw_i_department_no", "f_user_channel_pref")

    return out.replace([np.inf, -np.inf], np.nan)
