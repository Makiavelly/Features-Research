def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    names = (
        "f_ui_count", "f_ui_recency", "f_item_pop_7d", "f_item_pop_30d",
        "f_item_recency", "f_item_decay_pop", "f_user_activity_30d",
        "f_user_recency", "f_user_product_count", "f_user_product_recency",
        "f_user_department_count", "f_user_department_recency",
        "f_user_section_count"
    )

    if h.empty:
        for name in names:
            out[name] = 0.0
        return out

    def one_map(series, key, fill=0.0):
        return X[key].map(series).fillna(fill).to_numpy(dtype=float)

    def pair_index(raw_col):
        return pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[raw_col].to_numpy()]
        )

    def pair_map(series, raw_col, fill=0.0):
        vals = series.reindex(pair_index(raw_col)).to_numpy(dtype=float)
        return np.nan_to_num(vals, nan=fill, posinf=fill, neginf=fill)

    ui = h.groupby(["customer_id", "article_id"], sort=False)
    item = h.groupby("article_id", sort=False)
    user = h.groupby("customer_id", sort=False)

    out["f_ui_count"] = pair_map(ui.size(), "article_id", 0.0)
    out["f_ui_recency"] = pair_map(ui["days_ago"].min(), "article_id", 999.0)

    h7 = h.loc[h["days_ago"] <= 7]
    h30 = h.loc[h["days_ago"] <= 30]
    h90 = h.loc[h["days_ago"] <= 90]

    out["f_item_pop_7d"] = one_map(
        h7.groupby("article_id", sort=False).size(), "article_id", 0.0
    )
    out["f_item_pop_30d"] = one_map(
        h30.groupby("article_id", sort=False).size(), "article_id", 0.0
    )
    out["f_item_recency"] = one_map(item["days_ago"].min(), "article_id", 999.0)

    decay = np.exp(-h["days_ago"].to_numpy(dtype=float) / 21.0)
    decay_pop = pd.Series(decay, index=h["article_id"].to_numpy()).groupby(level=0).sum()
    out["f_item_decay_pop"] = one_map(decay_pop, "article_id", 0.0)

    out["f_user_activity_30d"] = one_map(
        h30.groupby("customer_id", sort=False).size(), "customer_id", 0.0
    )
    out["f_user_recency"] = one_map(
        user["days_ago"].min(), "customer_id", 999.0
    )

    product_counts = h90.groupby(["customer_id", "product_code"], sort=False).size()
    product_recency = h.groupby(
        ["customer_id", "product_code"], sort=False
    )["days_ago"].min()
    out["f_user_product_count"] = pair_map(
        product_counts, "raw_i_product_code", 0.0
    )
    out["f_user_product_recency"] = pair_map(
        product_recency, "raw_i_product_code", 999.0
    )

    dept_counts = h90.groupby(["customer_id", "department_no"], sort=False).size()
    dept_recency = h.groupby(
        ["customer_id", "department_no"], sort=False
    )["days_ago"].min()
    out["f_user_department_count"] = pair_map(
        dept_counts, "raw_i_department_no", 0.0
    )
    out["f_user_department_recency"] = pair_map(
        dept_recency, "raw_i_department_no", 999.0
    )

    section_counts = h90.groupby(["customer_id", "section_no"], sort=False).size()
    out["f_user_section_count"] = pair_map(
        section_counts, "raw_i_section_no", 0.0
    )

    return out.replace([np.inf, -np.inf], np.nan)
