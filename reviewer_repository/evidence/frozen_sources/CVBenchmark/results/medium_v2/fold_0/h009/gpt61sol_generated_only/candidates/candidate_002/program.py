def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def mapped(series, keys, default=np.nan):
        if len(series) == 0 or n == 0:
            return np.full(n, default, dtype=float)
        idx = pd.MultiIndex.from_arrays(keys)
        return series.reindex(idx).to_numpy()

    if h is None or len(h) == 0:
        for name in (
            "f_pair_count", "f_pair_count_30d", "f_pair_recency",
            "f_user_count_30d", "f_user_count_365d",
            "f_item_count_30d", "f_item_count_365d",
            "f_user_product_pref", "f_user_department_pref",
            "f_user_type_pref",
        ):
            out[name] = 0.0 if "recency" not in name else np.nan
        return out

    days = pd.to_numeric(h["days_ago"], errors="coerce")
    h30 = h.loc[days <= 30]
    h180 = h.loc[days <= 180]
    h365 = h.loc[days <= 365]

    pair = h.groupby(["customer_id", "article_id"], sort=False).size()
    out["f_pair_count"] = mapped(pair, [X["customer_id"].to_numpy(), X["article_id"].to_numpy()], 0)

    pair30 = h30.groupby(["customer_id", "article_id"], sort=False).size()
    out["f_pair_count_30d"] = mapped(pair30, [X["customer_id"].to_numpy(), X["article_id"].to_numpy()], 0)

    rec = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
    out["f_pair_recency"] = mapped(rec, [X["customer_id"].to_numpy(), X["article_id"].to_numpy()])

    for window, hh in ((30, h30), (365, h365)):
        counts = hh.groupby("customer_id", sort=False).size()
        out[f"f_user_count_{window}d"] = X["customer_id"].map(counts).fillna(0).to_numpy()
        counts = hh.groupby("article_id", sort=False).size()
        out[f"f_item_count_{window}d"] = X["article_id"].map(counts).fillna(0).to_numpy()

    def preference(hist, hist_col, raw_col, feature):
        if hist_col not in h.columns or raw_col not in X.columns:
            out[feature] = 0.0
            return
        counts = hist.groupby(["customer_id", hist_col], sort=False).size()
        out[feature] = mapped(
            counts,
            [X["customer_id"].to_numpy(), X[raw_col].to_numpy()],
            0,
        )

    preference(h, "product_code", "raw_i_product_code", "f_user_product_pref")
    preference(h180, "department_no", "raw_i_department_no", "f_user_department_pref")
    preference(h180, "product_type_no", "raw_i_product_type_no", "f_user_type_pref")

    return out.replace([np.inf, -np.inf], np.nan)
