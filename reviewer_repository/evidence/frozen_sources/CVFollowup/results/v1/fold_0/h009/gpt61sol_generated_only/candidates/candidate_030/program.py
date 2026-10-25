def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)
    users = X["customer_id"].to_numpy()
    items = X["article_id"].to_numpy()

    names = (
        "f_pair_weighted", "f_pair_recent_count", "f_user_weighted",
        "f_item_weighted", "f_item_count_90d", "f_item_recency",
        "f_user_type_recent", "f_user_section_recent", "f_user_colour_recent",
        "f_user_department_recent", "f_user_product_recent",
    )
    if h is None or len(h) == 0:
        for name in names:
            out[name] = np.nan if name.endswith("recency") else 0.0
        return out

    days = pd.to_numeric(h["days_ago"], errors="coerce")
    decay = np.exp(-days.fillna(100000).to_numpy(dtype=float) / 45.0)
    hw = h.assign(_weight=decay)
    recent = h.loc[days <= 21]
    recent_w = hw.loc[days <= 90]

    pair_w = hw.groupby(["customer_id", "article_id"], sort=False)["_weight"].sum()
    pair_idx = pd.MultiIndex.from_arrays([users, items])
    out["f_pair_weighted"] = pair_w.reindex(pair_idx).fillna(0).to_numpy()

    recent_pairs = recent.groupby(["customer_id", "article_id"], sort=False).size()
    out["f_pair_recent_count"] = recent_pairs.reindex(pair_idx).fillna(0).to_numpy()

    out["f_user_weighted"] = X["customer_id"].map(
        hw.groupby("customer_id", sort=False)["_weight"].sum()
    ).fillna(0).to_numpy()
    out["f_item_weighted"] = X["article_id"].map(
        hw.groupby("article_id", sort=False)["_weight"].sum()
    ).fillna(0).to_numpy()
    out["f_item_count_90d"] = X["article_id"].map(
        h.loc[days <= 90].groupby("article_id", sort=False).size()
    ).fillna(0).to_numpy()
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    ).to_numpy()

    def category_affinity(hist, col, raw_col, name):
        if len(hist) == 0 or col not in hist.columns or raw_col not in X.columns:
            out[name] = 0.0
            return
        g = hist.groupby(["customer_id", col], sort=False)["_weight"].sum()
        idx = pd.MultiIndex.from_arrays([users, X[raw_col].to_numpy()])
        out[name] = g.reindex(idx).fillna(0).to_numpy()

    category_affinity(recent_w, "product_type_no", "raw_i_product_type_no", "f_user_type_recent")
    category_affinity(recent_w, "section_no", "raw_i_section_no", "f_user_section_recent")
    category_affinity(recent_w, "colour_group_code", "raw_i_colour_group_code", "f_user_colour_recent")
    category_affinity(recent_w, "department_no", "raw_i_department_no", "f_user_department_recent")
    category_affinity(recent_w, "product_code", "raw_i_product_code", "f_user_product_recent")

    return out.replace([np.inf, -np.inf], np.nan)
