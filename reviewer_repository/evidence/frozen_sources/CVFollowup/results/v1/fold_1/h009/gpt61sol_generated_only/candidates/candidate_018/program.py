def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_popularity",
        "f_item_recency", "f_user_item_count", "f_user_item_recent",
        "f_user_item_recency", "f_customer_recency", "f_user_activity_30d",
        "f_user_product_count", "f_user_type_count", "f_user_type_recent",
        "f_user_section_count", "f_item_product_popularity",
        "f_item_price_mean",
    ]
    h = history
    if h is None or len(h) == 0:
        for name in names:
            out[name] = 0.0
        return out

    days = pd.to_numeric(h["days_ago"], errors="coerce")
    recent30 = h.loc[days <= 30]

    for window in (7, 30):
        counts = h.loc[days <= window].groupby("article_id").size()
        out["f_item_count_%dd" % window] = X["article_id"].map(counts).fillna(0)

    out["f_item_popularity"] = np.log1p(
        X["article_id"].map(h.groupby("article_id").size()).fillna(0)
    )
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()
    ).fillna(365)

    pair = pd.MultiIndex.from_arrays([X["customer_id"], X["article_id"]])
    pair_counts = h.groupby(["customer_id", "article_id"]).size()
    out["f_user_item_count"] = pd.Series(pair.map(pair_counts), index=X.index).fillna(0)
    out["f_user_item_recent"] = pd.Series(
        pair.map(recent30.groupby(["customer_id", "article_id"]).size()),
        index=X.index
    ).fillna(0)
    out["f_user_item_recency"] = pd.Series(
        pair.map(h.groupby(["customer_id", "article_id"])["days_ago"].min()),
        index=X.index
    ).fillna(365)

    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()
    ).fillna(365)
    out["f_user_activity_30d"] = np.log1p(
        X["customer_id"].map(recent30.groupby("customer_id").size()).fillna(0)
    )

    def user_category(raw_name, hist_name, output, recent_output=None):
        key = pd.MultiIndex.from_arrays([X["customer_id"], X[raw_name]])
        out[output] = pd.Series(
            key.map(h.groupby(["customer_id", hist_name]).size()), index=X.index
        ).fillna(0)
        if recent_output:
            out[recent_output] = pd.Series(
                key.map(recent30.groupby(["customer_id", hist_name]).size()),
                index=X.index
            ).fillna(0)

    user_category("raw_i_product_code", "product_code", "f_user_product_count")
    user_category(
        "raw_i_product_type_no", "product_type_no",
        "f_user_type_count", "f_user_type_recent"
    )
    user_category("raw_i_section_no", "section_no", "f_user_section_count")

    out["f_item_product_popularity"] = np.log1p(
        X["raw_i_product_code"].map(h.groupby("product_code").size()).fillna(0)
    )
    out["f_item_price_mean"] = X["article_id"].map(
        h.groupby("article_id")["price"].mean()
    ).fillna(0)

    return out.replace([np.inf, -np.inf], np.nan)
