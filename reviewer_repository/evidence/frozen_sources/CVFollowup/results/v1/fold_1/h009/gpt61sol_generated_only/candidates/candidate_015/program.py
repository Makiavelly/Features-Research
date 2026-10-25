def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_recency",
        "f_item_popularity", "f_user_item_count", "f_user_item_recency",
        "f_user_activity_30d", "f_user_product_count",
        "f_user_type_count", "f_user_department_count",
        "f_user_section_count", "f_item_product_popularity",
        "f_item_section_popularity", "f_item_price_mean",
    ]
    h = history
    if h is None or len(h) == 0:
        for name in names:
            out[name] = 0.0
        return out

    days = pd.to_numeric(h["days_ago"], errors="coerce")
    for window in (7, 30):
        counts = h.loc[days <= window].groupby("article_id").size()
        out["f_item_count_%dd" % window] = X["article_id"].map(counts).fillna(0)

    item_counts = h.groupby("article_id").size()
    out["f_item_popularity"] = np.log1p(X["article_id"].map(item_counts).fillna(0))
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()
    ).fillna(365)

    pair = pd.MultiIndex.from_arrays([X["customer_id"], X["article_id"]])
    out["f_user_item_count"] = pd.Series(
        pair.map(h.groupby(["customer_id", "article_id"]).size()), index=X.index
    ).fillna(0)
    out["f_user_item_recency"] = pd.Series(
        pair.map(h.groupby(["customer_id", "article_id"])["days_ago"].min()),
        index=X.index
    ).fillna(365)
    out["f_user_activity_30d"] = np.log1p(
        X["customer_id"].map(h.loc[days <= 30].groupby("customer_id").size()).fillna(0)
    )

    def user_group_count(raw_col, hist_col, output):
        key = pd.MultiIndex.from_arrays([X["customer_id"], X[raw_col]])
        counts = h.groupby(["customer_id", hist_col]).size()
        out[output] = pd.Series(key.map(counts), index=X.index).fillna(0)

    user_group_count("raw_i_product_code", "product_code", "f_user_product_count")
    user_group_count("raw_i_product_type_no", "product_type_no", "f_user_type_count")
    user_group_count("raw_i_department_no", "department_no", "f_user_department_count")
    user_group_count("raw_i_section_no", "section_no", "f_user_section_count")

    out["f_item_product_popularity"] = np.log1p(
        X["raw_i_product_code"].map(h.groupby("product_code").size()).fillna(0)
    )
    out["f_item_section_popularity"] = np.log1p(
        X["raw_i_section_no"].map(h.groupby("section_no").size()).fillna(0)
    )
    out["f_item_price_mean"] = X["article_id"].map(
        h.groupby("article_id")["price"].mean()
    ).fillna(0)

    return out.replace([np.inf, -np.inf], np.nan)
