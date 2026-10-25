def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    names = (
        "f_pair_count", "f_pair_count_30d", "f_pair_recency",
        "f_user_count_30d", "f_user_count_365d",
        "f_item_count_30d", "f_item_count_365d",
        "f_user_product_pref", "f_user_department_pref",
        "f_user_type_pref", "f_item_recency", "f_pair_count_180d",
    )
    if h is None or len(h) == 0:
        for name in names:
            out[name] = np.nan if name.endswith("recency") else 0.0
        return out

    days = pd.to_numeric(h["days_ago"], errors="coerce")
    h30 = h.loc[days <= 30]
    h180 = h.loc[days <= 180]
    h365 = h.loc[days <= 365]

    def pair_values(hist, col, keys, default=0):
        if len(hist) == 0:
            return np.full(n, default, dtype=float)
        s = hist.groupby(["customer_id", col], sort=False).size()
        ix = pd.MultiIndex.from_arrays(keys)
        return s.reindex(ix).fillna(default).to_numpy()

    user_ids = X["customer_id"].to_numpy()
    item_ids = X["article_id"].to_numpy()

    out["f_pair_count"] = pair_values(
        h, "article_id", [user_ids, item_ids]
    )
    out["f_pair_count_30d"] = pair_values(
        h30, "article_id", [user_ids, item_ids]
    )
    out["f_pair_count_180d"] = pair_values(
        h180, "article_id", [user_ids, item_ids]
    )

    rec = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
    out["f_pair_recency"] = rec.reindex(
        pd.MultiIndex.from_arrays([user_ids, item_ids])
    ).to_numpy()

    for window, hh in ((30, h30), (365, h365)):
        out[f"f_user_count_{window}d"] = (
            X["customer_id"].map(hh.groupby("customer_id", sort=False).size())
            .fillna(0).to_numpy()
        )
        out[f"f_item_count_{window}d"] = (
            X["article_id"].map(hh.groupby("article_id", sort=False).size())
            .fillna(0).to_numpy()
        )

    item_rec = h.groupby("article_id", sort=False)["days_ago"].min()
    out["f_item_recency"] = X["article_id"].map(item_rec).to_numpy()

    def pref(hist, hist_col, raw_col, feature):
        if raw_col not in X.columns or hist_col not in hist.columns or len(hist) == 0:
            out[feature] = 0.0
            return
        s = hist.groupby(["customer_id", hist_col], sort=False).size()
        ix = pd.MultiIndex.from_arrays(
            [user_ids, X[raw_col].to_numpy()]
        )
        out[feature] = s.reindex(ix).fillna(0).to_numpy()

    pref(h, "product_code", "raw_i_product_code", "f_user_product_pref")
    pref(h180, "department_no", "raw_i_department_no", "f_user_department_pref")
    pref(h180, "product_type_no", "raw_i_product_type_no", "f_user_type_pref")

    out.replace([np.inf, -np.inf], np.nan, inplace=True)
    return out
