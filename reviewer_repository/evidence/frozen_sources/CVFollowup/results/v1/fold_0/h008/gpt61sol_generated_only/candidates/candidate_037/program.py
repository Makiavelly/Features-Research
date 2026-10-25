def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    n = len(X)
    h = history
    customer = X["customer_id"]
    article = X["article_id"]

    def add_map(name, values, fill=0.0):
        v = values.reindex(X.index) if isinstance(values, pd.Series) else values
        if isinstance(v, pd.Series):
            v = v.fillna(fill).to_numpy()
        else:
            v = np.asarray(v)
            if fill is not None:
                v = np.where(pd.isna(v), fill, v)
        out[name] = v

    def keyed_counts(cols, mask=None):
        z = h if mask is None else h.loc[mask]
        if z.empty:
            return pd.Series(dtype=float)
        return z.groupby(cols).size()

    def pair_values(col, agg, name, fill=np.nan):
        if h.empty:
            out[name] = np.full(n, fill)
            return
        g = h.groupby(["customer_id", "article_id"])[col].agg(agg)
        keys = pd.MultiIndex.from_arrays(
            [customer.to_numpy(), article.to_numpy()],
            names=["customer_id", "article_id"]
        )
        add_map(name, g.reindex(keys), fill)

    if not h.empty:
        d = h["days_ago"]
        for w in (7, 30, 90):
            add_map(
                f"f_item_purchases_{w}d",
                keyed_counts(["article_id"], d <= w).reindex(article),
                0
            )
            add_map(
                f"f_user_purchases_{w}d",
                keyed_counts(["customer_id"], d <= w).reindex(customer),
                0
            )

        add_map(
            "f_item_purchases_all",
            h.groupby("article_id").size().reindex(article),
            0
        )
        add_map(
            "f_user_purchases_all",
            h.groupby("customer_id").size().reindex(customer),
            0
        )
        add_map(
            "f_item_recency",
            h.groupby("article_id")["days_ago"].min().reindex(article)
        )
        add_map(
            "f_user_recency",
            h.groupby("customer_id")["days_ago"].min().reindex(customer)
        )

        pair_values("days_ago", "min", "f_user_item_recency")
        pair_values("price", "mean", "f_user_item_mean_price")
        pair_values("days_ago", "count", "f_user_item_purchases_all", 0)

        add_map(
            "f_item_mean_price",
            h.groupby("article_id")["price"].mean().reindex(article)
        )
        add_map(
            "f_item_mean_price_30d",
            h.loc[d <= 30].groupby("article_id")["price"].mean().reindex(article)
        )

        for hc, rc, nm in (
            ("product_code", "raw_i_product_code", "product_code"),
            ("product_type_no", "raw_i_product_type_no", "product_type"),
            ("department_no", "raw_i_department_no", "department"),
            ("section_no", "raw_i_section_no", "section"),
            ("garment_group_no", "raw_i_garment_group_no", "garment_group"),
        ):
            g = h.groupby(["customer_id", hc]).size()
            keys = pd.MultiIndex.from_arrays(
                [customer.to_numpy(), X[rc].to_numpy()],
                names=["customer_id", hc]
            )
            add_map(f"f_user_{nm}_purchases", g.reindex(keys), 0)
    else:
        for nm in (
            "f_item_purchases_7d", "f_item_purchases_30d",
            "f_item_purchases_90d", "f_user_purchases_7d",
            "f_user_purchases_30d", "f_user_purchases_90d",
            "f_item_purchases_all", "f_user_purchases_all",
            "f_user_item_purchases_all",
            "f_user_product_code_purchases",
            "f_user_product_type_purchases",
            "f_user_department_purchases",
            "f_user_section_purchases",
            "f_user_garment_group_purchases",
        ):
            out[nm] = np.zeros(n)
        for nm in (
            "f_item_recency", "f_user_recency",
            "f_user_item_recency", "f_user_item_mean_price",
            "f_item_mean_price", "f_item_mean_price_30d",
        ):
            out[nm] = np.full(n, np.nan)

    static = (
        ("raw_u_age", "f_user_age"),
        ("raw_u_fn", "f_user_fn"),
        ("raw_u_active", "f_user_active"),
        ("raw_u_club_member_status", "f_user_club_member_status"),
        ("raw_u_fashion_news_frequency", "f_user_fashion_news_frequency"),
        ("raw_i_product_code", "f_article_product_code"),
        ("raw_i_product_type_no", "f_article_product_type"),
        ("raw_i_graphical_appearance_no", "f_article_graphical_appearance"),
        ("raw_i_colour_group_code", "f_article_colour_group"),
        ("raw_i_perceived_colour_value_id", "f_article_perceived_colour_value"),
        ("raw_i_perceived_colour_master_id", "f_article_perceived_colour_master"),
        ("raw_i_department_no", "f_article_department"),
        ("raw_i_index_group_no", "f_article_index_group"),
        ("raw_i_section_no", "f_article_section"),
        ("raw_i_garment_group_no", "f_article_garment_group"),
    )
    for src, dst in static:
        out[dst] = pd.to_numeric(X[src], errors="coerce").to_numpy()

    return out.reindex(X.index)
