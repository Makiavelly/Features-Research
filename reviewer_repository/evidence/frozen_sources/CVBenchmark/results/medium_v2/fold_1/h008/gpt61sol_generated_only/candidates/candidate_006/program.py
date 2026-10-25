def modify_features(X, history):
    import pandas as pd
    import numpy as np

    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_count_all", "f_user_count_30d", "f_user_count_all",
        "f_pair_count_all", "f_pair_count_30d", "f_pair_recency",
        "f_user_type_count", "f_user_department_count",
        "f_user_type_count_90d", "f_user_department_count_90d",
        "f_item_mean_price", "f_item_channel1_share",
    ]
    out = pd.DataFrame(index=X.index)
    h = history
    if h is None or len(h) == 0:
        for name in names:
            out[name] = np.nan if name in ("f_pair_recency", "f_item_mean_price", "f_item_channel1_share") else 0.0
        return out[names]

    days = pd.to_numeric(h["days_ago"], errors="coerce")
    article = X["article_id"]
    customer = X["customer_id"]

    for window in (7, 30, 90):
        counts = h.loc[days <= window].groupby("article_id").size()
        out["f_item_count_%dd" % window] = article.map(counts).fillna(0).to_numpy()

    all_items = h.groupby("article_id").size()
    out["f_item_count_all"] = article.map(all_items).fillna(0).to_numpy()

    for window, name in ((30, "f_user_count_30d"), (None, "f_user_count_all")):
        hh = h if window is None else h.loc[days <= window]
        counts = hh.groupby("customer_id").size()
        out[name] = customer.map(counts).fillna(0).to_numpy()

    pair_all = h.groupby(["customer_id", "article_id"]).agg(
        count=("days_ago", "size"), recency=("days_ago", "min")
    )
    pair_recent = h.loc[days <= 30].groupby(["customer_id", "article_id"]).size()
    keys = pd.MultiIndex.from_arrays([customer.to_numpy(), article.to_numpy()])
    out["f_pair_count_all"] = pair_all["count"].reindex(keys).fillna(0).to_numpy()
    out["f_pair_count_30d"] = pair_recent.reindex(keys).fillna(0).to_numpy()
    out["f_pair_recency"] = pair_all["recency"].reindex(keys).to_numpy()

    for hist_col, raw_col, name, window in (
        ("product_type_no", "raw_i_product_type_no", "f_user_type_count", None),
        ("department_no", "raw_i_department_no", "f_user_department_count", None),
        ("product_type_no", "raw_i_product_type_no", "f_user_type_count_90d", 90),
        ("department_no", "raw_i_department_no", "f_user_department_count_90d", 90),
    ):
        hh = h if window is None else h.loc[days <= window]
        counts = hh.groupby(["customer_id", hist_col]).size()
        cat_keys = pd.MultiIndex.from_arrays([customer.to_numpy(), X[raw_col].to_numpy()])
        out[name] = counts.reindex(cat_keys).fillna(0).to_numpy()

    mean_price = h.groupby("article_id")["price"].mean()
    out["f_item_mean_price"] = article.map(mean_price).to_numpy()
    channel_share = h.assign(_ch1=(h["sales_channel_id"] == 1).astype(float)).groupby("article_id")["_ch1"].mean()
    out["f_item_channel1_share"] = article.map(channel_share).to_numpy()
    return out[names]
