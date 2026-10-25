def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_recency", "f_item_popularity", "f_user_item_count",
        "f_user_item_recency", "f_user_activity_30d", "f_user_category_count",
        "f_user_category_recent", "f_category_popularity",
        "f_product_popularity", "f_item_section_popularity",
        "f_user_section_count", "f_item_price_mean",
    ]
    h = history
    if h is None or len(h) == 0:
        for name in names:
            out[name] = 0.0
        return out

    days = pd.to_numeric(h["days_ago"], errors="coerce")
    for window in (7, 30, 90):
        counts = h.loc[days <= window].groupby("article_id").size()
        out["f_item_count_%dd" % window] = X["article_id"].map(counts).fillna(0)

    total = h.groupby("article_id").size()
    out["f_item_popularity"] = np.log1p(X["article_id"].map(total).fillna(0))
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

    if "raw_i_product_type_no" in X:
        cat = pd.MultiIndex.from_arrays([X["customer_id"], X["raw_i_product_type_no"]])
        out["f_user_category_count"] = pd.Series(
            cat.map(h.groupby(["customer_id", "product_type_no"]).size()), index=X.index
        ).fillna(0)
        out["f_user_category_recent"] = pd.Series(
            cat.map(h.loc[days <= 30].groupby(["customer_id", "product_type_no"]).size()),
            index=X.index
        ).fillna(0)
        out["f_category_popularity"] = np.log1p(
            X["raw_i_product_type_no"].map(h.groupby("product_type_no").size()).fillna(0)
        )
    else:
        out["f_user_category_count"] = 0.0
        out["f_user_category_recent"] = 0.0
        out["f_category_popularity"] = 0.0

    if "raw_i_product_code" in X:
        out["f_product_popularity"] = np.log1p(
            X["raw_i_product_code"].map(h.groupby("product_code").size()).fillna(0)
        )
    else:
        out["f_product_popularity"] = 0.0

    if "raw_i_section_no" in X:
        out["f_item_section_popularity"] = np.log1p(
            X["raw_i_section_no"].map(h.groupby("section_no").size()).fillna(0)
        )
        section_pair = pd.MultiIndex.from_arrays(
            [X["customer_id"], X["raw_i_section_no"]]
        )
        out["f_user_section_count"] = pd.Series(
            section_pair.map(h.groupby(["customer_id", "section_no"]).size()),
            index=X.index
        ).fillna(0)
    else:
        out["f_item_section_popularity"] = 0.0
        out["f_user_section_count"] = 0.0

    if "price" in h:
        out["f_item_price_mean"] = X["article_id"].map(
            h.groupby("article_id")["price"].mean()
        ).fillna(0)
    else:
        out["f_item_price_mean"] = 0.0

    return out.replace([np.inf, -np.inf], np.nan)
