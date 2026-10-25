def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history

    def mapped(column, values, default=0):
        return X[column].map(values).fillna(default).to_numpy()

    def pair_mapped(grouped, default=0):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        return grouped.reindex(keys).fillna(default).to_numpy()

    days = h["days_ago"]
    for window in (7, 30, 90):
        hw = h.loc[days <= window]
        out["f_item_popularity_%dd" % window] = mapped(
            "article_id", hw.groupby("article_id").size()
        )
        out["f_user_activity_%dd" % window] = mapped(
            "customer_id", hw.groupby("customer_id").size()
        )

    out["f_item_popularity_all"] = mapped("article_id", h.groupby("article_id").size())

    pair = h.groupby(["customer_id", "article_id"])
    out["f_user_item_count"] = pair_mapped(pair.size())
    out["f_user_item_recency"] = pair_mapped(pair["days_ago"].min(), np.nan)
    out["f_customer_recency"] = mapped(
        "customer_id", h.groupby("customer_id")["days_ago"].min(), np.nan
    )
    out["f_item_recency"] = mapped(
        "article_id", h.groupby("article_id")["days_ago"].min(), np.nan
    )

    for hist_col, x_col in (
        ("product_code", "raw_i_product_code"),
        ("product_type_no", "raw_i_product_type_no"),
        ("section_no", "raw_i_section_no"),
    ):
        out["f_category_pop_" + hist_col] = mapped(
            x_col, h.groupby(hist_col).size()
        )
        user_category = h.groupby(["customer_id", hist_col]).size()
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[x_col].to_numpy()]
        )
        out["f_user_category_" + hist_col] = (
            user_category.reindex(keys).fillna(0).to_numpy()
        )

    item_price = h.groupby("article_id")["price"].mean()
    user_price = h.groupby("customer_id")["price"].mean()
    candidate_price = mapped("article_id", item_price, np.nan)
    typical_price = mapped("customer_id", user_price, np.nan)
    out["f_item_mean_price"] = candidate_price
    out["f_user_item_price_ratio"] = np.divide(
        candidate_price,
        typical_price,
        out=np.full(len(X), np.nan, dtype=float),
        where=np.asarray(typical_price, dtype=float) != 0,
    )

    for col in (
        "raw_u_age",
        "raw_u_fn",
        "raw_u_active",
        "raw_u_club_member_status",
        "raw_u_fashion_news_frequency",
        "raw_i_product_type_no",
        "raw_i_index_group_no",
        "raw_i_section_no",
        "raw_i_garment_group_no",
    ):
        out["f_static_" + col[4:]] = X[col].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
