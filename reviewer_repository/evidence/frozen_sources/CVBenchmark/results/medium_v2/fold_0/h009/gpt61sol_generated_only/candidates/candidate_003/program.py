def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def item_stat(column, values):
        if h.empty:
            return np.full(n, np.nan)
        grouped = h.groupby(column, sort=False)["days_ago"].agg(values)
        return X["article_id"].map(grouped).to_numpy()

    def customer_stat(values):
        if h.empty:
            return np.full(n, np.nan)
        grouped = h.groupby("customer_id", sort=False)["days_ago"].agg(values)
        return X["customer_id"].map(grouped).to_numpy()

    def affinity(column):
        if h.empty:
            return np.zeros(n)
        grouped = h.groupby(["customer_id", column], sort=False).size()
        keys = pd.MultiIndex.from_arrays([X["customer_id"].to_numpy(), X["raw_i_" + column].to_numpy()])
        return grouped.reindex(keys).fillna(0).to_numpy()

    if h.empty:
        out["f_item_count_7d"] = np.zeros(n)
        out["f_item_count_30d"] = np.zeros(n)
        out["f_item_recency"] = np.full(n, np.nan)
        out["f_customer_recency"] = np.full(n, np.nan)
        out["f_customer_count_30d"] = np.zeros(n)
        out["f_exact_purchase_count"] = np.zeros(n)
        out["f_exact_purchase_recency"] = np.full(n, np.nan)
        for name in ("department_no", "section_no", "product_type_no", "product_code"):
            out["f_customer_" + name + "_affinity"] = np.zeros(n)
        out["f_department_count_30d"] = np.zeros(n)
        return out

    out["f_item_count_7d"] = X["article_id"].map(
        h.loc[h["days_ago"] <= 7].groupby("article_id").size()
    ).fillna(0).to_numpy()
    out["f_item_count_30d"] = X["article_id"].map(
        h.loc[h["days_ago"] <= 30].groupby("article_id").size()
    ).fillna(0).to_numpy()
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()
    ).to_numpy()
    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()
    ).to_numpy()
    out["f_customer_count_30d"] = X["customer_id"].map(
        h.loc[h["days_ago"] <= 30].groupby("customer_id").size()
    ).fillna(0).to_numpy()

    exact = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].agg(["size", "min"])
    exact_keys = pd.MultiIndex.from_arrays([X["customer_id"].to_numpy(), X["article_id"].to_numpy()])
    out["f_exact_purchase_count"] = exact["size"].reindex(exact_keys).fillna(0).to_numpy()
    out["f_exact_purchase_recency"] = exact["min"].reindex(exact_keys).to_numpy()

    for name in ("department_no", "section_no", "product_type_no", "product_code"):
        out["f_customer_" + name + "_affinity"] = affinity(name)

    dept = h.loc[h["days_ago"] <= 30].groupby("department_no").size()
    out["f_department_count_30d"] = X["raw_i_department_no"].map(dept).fillna(0).to_numpy()
    return out.replace([np.inf, -np.inf], np.nan)
