def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    if h is None or len(h) == 0:
        for name in (
            "f_item_count_30d", "f_item_count_7d", "f_item_recency",
            "f_user_item_count", "f_user_category_count", "f_item_popularity",
            "f_user_category_affinity", "f_user_channel_affinity",
            "f_item_channel_affinity", "f_item_price_mean",
        ):
            out[name] = 0.0
        return out

    d = pd.to_numeric(h["days_ago"], errors="coerce")
    item = h["article_id"]
    user = h["customer_id"]

    def mapped(grouped, key):
        return key.map(grouped).fillna(0)

    c7 = item.map(h.loc[d <= 7].groupby("article_id").size()).fillna(0)
    c30 = item.map(h.loc[d <= 30].groupby("article_id").size()).fillna(0)
    item_rec = h.groupby("article_id")["days_ago"].min()
    item_total = h.groupby("article_id").size()
    user_item = h.groupby(["customer_id", "article_id"]).size()
    user_cat = h.groupby(["customer_id", "product_type_no"]).size()
    user_total = h.groupby("customer_id").size()
    item_total_by_key = h.groupby("article_id").size()

    out["f_item_count_30d"] = X["article_id"].map(c30.groupby(item).first()).fillna(0)
    out["f_item_count_7d"] = X["article_id"].map(c7.groupby(item).first()).fillna(0)
    out["f_item_recency"] = X["article_id"].map(item_rec).fillna(365)
    out["f_item_popularity"] = np.log1p(X["article_id"].map(item_total).fillna(0))

    ui = pd.MultiIndex.from_arrays([X["customer_id"], X["article_id"]])
    out["f_user_item_count"] = pd.Series(ui.map(user_item).astype(float), index=X.index).fillna(0)

    cat_col = "raw_i_product_type_no"
    if cat_col in X:
        uc = pd.MultiIndex.from_arrays([X["customer_id"], X[cat_col]])
        out["f_user_category_count"] = pd.Series(uc.map(user_cat).astype(float), index=X.index).fillna(0)
        uc_counts = pd.Series(uc.map(user_cat).astype(float), index=X.index).fillna(0)
        u_counts = X["customer_id"].map(user_total).fillna(0)
        out["f_user_category_affinity"] = np.log1p(uc_counts) - np.log1p(u_counts / 100.0)
    else:
        out["f_user_category_count"] = 0.0
        out["f_user_category_affinity"] = 0.0

    # Historical channel preferences and article-channel tendencies.
    if "sales_channel_id" in h:
        uc = h.groupby(["customer_id", "sales_channel_id"]).size()
        ac = h.groupby(["article_id", "sales_channel_id"]).size()
        uall = h.groupby("customer_id").size()
        aall = h.groupby("article_id").size()
        ch1 = X["raw_i_product_type_no"] if False else None
        # Candidate channel is not supplied; use article's dominant historical channel.
        item_ch = h.groupby(["article_id", "sales_channel_id"]).size().unstack(fill_value=0)
        if 1 in item_ch.columns and 2 in item_ch.columns:
            out["f_item_channel_affinity"] = X["article_id"].map(
                (item_ch[1] + 1) / (item_ch[1] + item_ch[2] + 2)
            ).fillna(0.5)
        else:
            out["f_item_channel_affinity"] = 0.5
        out["f_user_channel_affinity"] = X["customer_id"].map(uall).fillna(0).pipe(np.log1p)
    else:
        out["f_item_channel_affinity"] = 0.5
        out["f_user_channel_affinity"] = 0.0

    if "price" in h:
        pmean = h.groupby("article_id")["price"].mean()
        out["f_item_price_mean"] = X["article_id"].map(pmean).fillna(0)
    else:
        out["f_item_price_mean"] = 0.0

    return out.replace([np.inf, -np.inf], np.nan)
