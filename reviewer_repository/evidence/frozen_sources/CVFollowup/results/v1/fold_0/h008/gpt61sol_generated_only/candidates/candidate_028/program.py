def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    customer = X["customer_id"]
    article = X["article_id"]

    def mapped(series, keys):
        return keys.map(series).fillna(0).to_numpy()

    def pair_mapped(series, fill=0):
        keys = pd.MultiIndex.from_arrays(
            [customer.to_numpy(), article.to_numpy()]
        )
        return series.reindex(keys).fillna(fill).to_numpy()

    if h.empty:
        for name in (
            "f_item_purchases_7d", "f_item_purchases_30d",
            "f_item_purchases_90d", "f_item_purchases_all",
            "f_item_recency", "f_item_mean_price", "f_item_decay",
            "f_user_purchases_30d", "f_user_purchases_all",
            "f_user_item_purchases_30d", "f_user_item_purchases_90d",
            "f_user_item_purchases_all", "f_user_item_recency",
            "f_user_item_decay", "f_user_department_purchases",
            "f_user_product_type_purchases", "f_user_product_code_purchases",
            "f_user_section_purchases", "f_item_user_ratio",
            "f_pair_user_ratio",
        ):
            out[name] = np.nan if ("recency" in name or "price" in name) else 0.0
    else:
        days = h["days_ago"]
        item_groups = h.groupby("article_id")
        user_groups = h.groupby("customer_id")
        pair_groups = h.groupby(["customer_id", "article_id"])

        for window in (7, 30, 90):
            recent = h.loc[days <= window]
            out[f"f_item_purchases_{window}d"] = mapped(
                recent.groupby("article_id").size(), article
            )

        out["f_item_purchases_all"] = mapped(item_groups.size(), article)
        out["f_item_recency"] = article.map(item_groups["days_ago"].min()).to_numpy()
        out["f_item_mean_price"] = article.map(item_groups["price"].mean()).to_numpy()
        out["f_item_decay"] = mapped(
            np.exp(-days / 30.0).groupby(h["article_id"]).sum(), article
        )

        for window in (30, 90):
            recent = h.loc[days <= window]
            out[f"f_user_item_purchases_{window}d"] = pair_mapped(
                recent.groupby(["customer_id", "article_id"]).size()
            )

        out["f_user_item_purchases_all"] = pair_mapped(pair_groups.size())
        out["f_user_item_recency"] = pair_mapped(
            pair_groups["days_ago"].min(), np.nan
        )
        out["f_user_item_decay"] = pair_mapped(
            np.exp(-days / 30.0).groupby(
                [h["customer_id"], h["article_id"]]
            ).sum()
        )
        out["f_user_purchases_30d"] = mapped(
            h.loc[days <= 30].groupby("customer_id").size(), customer
        )
        out["f_user_purchases_all"] = mapped(user_groups.size(), customer)

        for history_col, raw_col, feature in (
            ("department_no", "raw_i_department_no", "f_user_department_purchases"),
            ("product_type_no", "raw_i_product_type_no", "f_user_product_type_purchases"),
            ("product_code", "raw_i_product_code", "f_user_product_code_purchases"),
            ("section_no", "raw_i_section_no", "f_user_section_purchases"),
        ):
            keys = pd.MultiIndex.from_arrays(
                [customer.to_numpy(), X[raw_col].to_numpy()]
            )
            counts = h.groupby(["customer_id", history_col]).size()
            out[feature] = counts.reindex(keys).fillna(0).to_numpy()

        out["f_item_user_ratio"] = (
            out["f_item_purchases_all"]
            / (out["f_item_purchases_all"] + out["f_user_purchases_all"] + 1.0)
        )
        out["f_pair_user_ratio"] = (
            out["f_user_item_purchases_all"]
            / (out["f_user_purchases_all"] + 1.0)
        )

    for source, feature in (
        ("raw_u_age", "f_user_age"),
        ("raw_u_fn", "f_user_fashion_news"),
        ("raw_u_active", "f_user_active"),
        ("raw_u_club_member_status", "f_user_club_status"),
        ("raw_u_fashion_news_frequency", "f_user_news_frequency"),
        ("raw_i_product_code", "f_article_product_code"),
        ("raw_i_product_type_no", "f_article_product_type"),
        ("raw_i_graphical_appearance_no", "f_article_graphical"),
        ("raw_i_colour_group_code", "f_article_colour"),
        ("raw_i_perceived_colour_value_id", "f_article_colour_value"),
        ("raw_i_perceived_colour_master_id", "f_article_colour_master"),
        ("raw_i_department_no", "f_article_department"),
        ("raw_i_index_group_no", "f_article_index_group"),
        ("raw_i_section_no", "f_article_section"),
        ("raw_i_garment_group_no", "f_article_garment_group"),
    ):
        out[feature] = X[source].to_numpy()

    return out.reindex(X.index)
