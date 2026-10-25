def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def single_map(series, key, fill=0.0):
        if len(series) == 0:
            return np.full(n, fill, dtype=float)
        return X[key].map(series).fillna(fill).to_numpy(dtype=float)

    def pair_map(series, customer_key, history_key, raw_key, fill=0.0):
        if len(series) == 0:
            return np.full(n, fill, dtype=float)
        keys = pd.MultiIndex.from_arrays(
            [X[customer_key].to_numpy(), X[raw_key].to_numpy()]
        )
        return series.reindex(keys).fillna(fill).to_numpy(dtype=float)

    if not h.empty:
        out["f_user_item_count"] = pair_map(
            h.groupby(["customer_id", "article_id"], sort=False).size(),
            "customer_id", "article_id", "article_id"
        )
        out["f_user_item_recency"] = pair_map(
            h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min(),
            "customer_id", "article_id", "article_id", np.nan
        )
        out["f_item_recency"] = single_map(
            h.groupby("article_id", sort=False)["days_ago"].min(), "article_id", np.nan
        )
        for days in (7, 30, 90):
            recent = h.loc[h["days_ago"] <= days]
            out["f_item_pop_%dd" % days] = single_map(
                recent.groupby("article_id", sort=False).size(), "article_id"
            )
            out["f_user_activity_%dd" % days] = single_map(
                recent.groupby("customer_id", sort=False).size(), "customer_id"
            )
        out["f_item_buyer_count_90d"] = single_map(
            h.loc[h["days_ago"] <= 90].groupby("article_id", sort=False)["customer_id"].nunique(),
            "article_id"
        )
        out["f_user_total_count"] = single_map(
            h.groupby("customer_id", sort=False).size(), "customer_id"
        )

        categories = (
            ("product_code", "raw_i_product_code"),
            ("product_type_no", "raw_i_product_type_no"),
            ("department_no", "raw_i_department_no"),
            ("section_no", "raw_i_section_no"),
            ("garment_group_no", "raw_i_garment_group_no"),
            ("index_group_no", "raw_i_index_group_no"),
            ("colour_group_code", "raw_i_colour_group_code"),
        )
        for hist_col, raw_col in categories:
            counts = h.groupby(["customer_id", hist_col], sort=False).size()
            name = hist_col.replace("_no", "").replace("_code", "")
            vals = pair_map(counts, "customer_id", hist_col, raw_col)
            out["f_user_%s_count" % name] = vals
            totals = out["f_user_total_count"].to_numpy(dtype=float)
            out["f_user_%s_share" % name] = np.divide(
                vals, totals, out=np.zeros(n, dtype=float), where=totals > 0
            )

        for days in (30, 90):
            recent = h.loc[h["days_ago"] <= days]
            counts = recent.groupby(["customer_id", "department_no"], sort=False).size()
            out["f_user_department_%dd" % days] = pair_map(
                counts, "customer_id", "department_no", "raw_i_department_no"
            )
        out["f_user_mean_price"] = single_map(
            h.groupby("customer_id", sort=False)["price"].mean(), "customer_id", np.nan
        )
        out["f_item_mean_price"] = single_map(
            h.groupby("article_id", sort=False)["price"].mean(), "article_id", np.nan
        )
        out["f_user_channel1_share"] = single_map(
            h.assign(_c1=(h["sales_channel_id"] == 1).astype(float))
             .groupby("customer_id", sort=False)["_c1"].mean(),
            "customer_id", np.nan
        )
    else:
        for name in (
            "f_user_item_count", "f_user_item_recency", "f_item_recency",
            "f_item_pop_7d", "f_user_activity_7d", "f_item_pop_30d",
            "f_user_activity_30d", "f_item_pop_90d", "f_user_activity_90d",
            "f_item_buyer_count_90d", "f_user_total_count",
            "f_user_product_count", "f_user_product_share",
            "f_user_product_type_count", "f_user_product_type_share",
            "f_user_department_count", "f_user_department_share",
            "f_user_section_count", "f_user_section_share",
            "f_user_garment_group_count", "f_user_garment_group_share",
            "f_user_index_group_count", "f_user_index_group_share",
            "f_user_colour_group_count", "f_user_colour_group_share",
            "f_user_department_30d", "f_user_department_90d",
            "f_user_mean_price", "f_item_mean_price", "f_user_channel1_share"
        ):
            out[name] = np.nan

    for raw in ("raw_u_age", "raw_i_product_code", "raw_i_product_type_no",
                "raw_i_department_no", "raw_i_section_no"):
        out["f_static_" + raw[4:]] = X[raw].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan)
