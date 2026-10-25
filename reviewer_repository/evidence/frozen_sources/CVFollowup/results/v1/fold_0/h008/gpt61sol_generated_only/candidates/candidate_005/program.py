def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    days = h["days_ago"]

    def mapped(xcol, values, default=np.nan):
        return X[xcol].map(values).fillna(default).to_numpy()

    def pair_values(grouped, fill=np.nan):
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        return grouped.reindex(keys, fill_value=fill).to_numpy()

    for window in (7, 30, 90):
        hw = h.loc[days <= window]
        out["f_item_popularity_%dd" % window] = mapped(
            "article_id", hw.groupby("article_id").size(), 0
        )
        out["f_user_activity_%dd" % window] = mapped(
            "customer_id", hw.groupby("customer_id").size(), 0
        )

    out["f_item_popularity_all"] = mapped("article_id", h.groupby("article_id").size(), 0)
    out["f_user_activity_all"] = mapped("customer_id", h.groupby("customer_id").size(), 0)

    pair = h.groupby(["customer_id", "article_id"])
    out["f_user_item_recency"] = pair_values(pair["days_ago"].min())
    out["f_user_item_count"] = pair_values(pair.size(), 0)
    recent_pair = h.loc[days <= 30].groupby(["customer_id", "article_id"]).size()
    out["f_user_item_count_30d"] = pair_values(recent_pair, 0)
    out["f_customer_recency"] = mapped(
        "customer_id", h.groupby("customer_id")["days_ago"].min()
    )

    item_price = h.groupby("article_id")["price"].mean()
    user_price = h.groupby("customer_id")["price"].mean()
    candidate_price = mapped("article_id", item_price)
    typical_price = mapped("customer_id", user_price)
    out["f_item_mean_price"] = candidate_price
    out["f_user_price_affinity"] = np.divide(
        candidate_price, typical_price,
        out=np.full(len(X), np.nan, dtype=float),
        where=np.asarray(typical_price, dtype=float) != 0
    )

    category_cols = [
        ("product_code", "raw_i_product_code"),
        ("product_type_no", "raw_i_product_type_no"),
        ("department_no", "raw_i_department_no"),
        ("section_no", "raw_i_section_no"),
    ]
    for hist_col, x_col in category_cols:
        out["f_category_pop_" + hist_col] = mapped(
            x_col, h.groupby(hist_col).size(), 0
        )
        grouped = h.groupby(["customer_id", hist_col]).size()
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[x_col].to_numpy()]
        )
        out["f_user_category_" + hist_col] = grouped.reindex(
            keys, fill_value=0
        ).to_numpy()

    out["f_item_channel1_share"] = mapped(
        "article_id",
        h.assign(_ch=(h["sales_channel_id"] == 1).astype(float))
         .groupby("article_id")["_ch"].mean()
    )
    out["f_item_channel2_share"] = mapped(
        "article_id",
        h.assign(_ch=(h["sales_channel_id"] == 2).astype(float))
         .groupby("article_id")["_ch"].mean()
    )

    for col in (
        "raw_u_age", "raw_u_fn", "raw_u_active",
        "raw_i_product_type_no", "raw_i_index_group_no",
        "raw_i_section_no", "raw_i_garment_group_no",
    ):
        out["f_static_" + col[4:]] = X[col].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan).astype(float)
