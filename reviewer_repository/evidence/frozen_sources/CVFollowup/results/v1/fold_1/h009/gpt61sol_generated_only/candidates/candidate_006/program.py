def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_recency", "f_item_popularity", "f_item_recent_share",
        "f_user_item_count", "f_user_item_recency", "f_user_activity_30d",
        "f_user_category_count", "f_user_category_recent", "f_category_popularity",
        "f_product_popularity", "f_item_price_mean",
    ]
    h = history
    if h is None or len(h) == 0:
        for n in names:
            out[n] = 0.0
        return out

    days = pd.to_numeric(h["days_ago"], errors="coerce")
    art = h["article_id"]
    cust = h["customer_id"]

    for window in (7, 30, 90):
        counts = h.loc[days <= window].groupby("article_id").size()
        out["f_item_count_%dd" % window] = X["article_id"].map(counts).fillna(0)

    item_rec = h.groupby("article_id")["days_ago"].min()
    item_total = h.groupby("article_id").size()
    out["f_item_recency"] = X["article_id"].map(item_rec).fillna(365)
    out["f_item_popularity"] = np.log1p(X["article_id"].map(item_total).fillna(0))
    c30 = h.loc[days <= 30].groupby("article_id").size()
    out["f_item_recent_share"] = (
        X["article_id"].map(c30).fillna(0) /
        (X["article_id"].map(item_total).fillna(0) + 1.0)
    )

    ui_count = h.groupby(["customer_id", "article_id"]).size()
    ui_rec = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    pair = pd.MultiIndex.from_arrays([X["customer_id"], X["article_id"]])
    out["f_user_item_count"] = pd.Series(pair.map(ui_count), index=X.index).fillna(0)
    out["f_user_item_recency"] = pd.Series(pair.map(ui_rec), index=X.index).fillna(365)

    user_total = h.groupby("customer_id").size()
    user30 = h.loc[days <= 30].groupby("customer_id").size()
    out["f_user_activity_30d"] = np.log1p(X["customer_id"].map(user30).fillna(0))

    if "raw_i_product_type_no" in X and "product_type_no" in h:
        cat = pd.MultiIndex.from_arrays([X["customer_id"], X["raw_i_product_type_no"]])
        uc = h.groupby(["customer_id", "product_type_no"]).size()
        uc30 = h.loc[days <= 30].groupby(["customer_id", "product_type_no"]).size()
        out["f_user_category_count"] = pd.Series(cat.map(uc), index=X.index).fillna(0)
        out["f_user_category_recent"] = pd.Series(cat.map(uc30), index=X.index).fillna(0)
        cc = h.groupby("product_type_no").size()
        out["f_category_popularity"] = np.log1p(X["raw_i_product_type_no"].map(cc).fillna(0))
    else:
        out["f_user_category_count"] = 0.0
        out["f_user_category_recent"] = 0.0
        out["f_category_popularity"] = 0.0

    if "raw_i_product_code" in X and "product_code" in h:
        pc = h.groupby("product_code").size()
        out["f_product_popularity"] = np.log1p(X["raw_i_product_code"].map(pc).fillna(0))
    else:
        out["f_product_popularity"] = 0.0

    if "price" in h:
        pm = h.groupby("article_id")["price"].mean()
        out["f_item_price_mean"] = X["article_id"].map(pm).fillna(0)
    else:
        out["f_item_price_mean"] = 0.0

    return out.replace([np.inf, -np.inf], np.nan)
