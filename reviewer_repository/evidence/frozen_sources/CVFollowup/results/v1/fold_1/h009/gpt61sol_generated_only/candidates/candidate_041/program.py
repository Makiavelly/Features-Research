def modify_features(X, history):
    import pandas as pd
    import numpy as np

    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_recency", "f_item_popularity", "f_item_recent_ratio",
        "f_user_item_count", "f_user_item_recency", "f_user_item_recent",
        "f_customer_recency", "f_user_activity_30d", "f_user_activity_90d",
        "f_user_product_count", "f_user_type_count", "f_user_type_recent",
        "f_user_department_count", "f_user_section_count",
        "f_user_garment_count", "f_user_colour_count",
        "f_item_product_popularity", "f_item_section_popularity",
        "f_item_price_mean", "f_item_buyer_age_mean",
        "f_item_age_distance",
    ]
    out = pd.DataFrame(index=X.index)
    h = history
    if h is None or len(h) == 0:
        for n in names:
            out[n] = 0.0
        return out

    d = pd.to_numeric(h["days_ago"], errors="coerce").fillna(9999)
    user = X["customer_id"]
    item = X["article_id"]
    h30 = h.loc[d <= 30]
    h90 = h.loc[d <= 90]

    for w in (7, 30, 90):
        out["f_item_count_%dd" % w] = item.map(
            h.loc[d <= w].groupby("article_id").size()
        ).fillna(0)

    item_size = h.groupby("article_id").size()
    item_total = item.map(item_size).fillna(0)
    item_30 = item.map(h30.groupby("article_id").size()).fillna(0)
    out["f_item_recency"] = item.map(
        h.groupby("article_id")["days_ago"].min()
    ).fillna(365)
    out["f_item_popularity"] = np.log1p(item_total)
    out["f_item_recent_ratio"] = item_30 / (item_total + 1.0)

    key = pd.MultiIndex.from_arrays([user, item])
    pair = h.groupby(["customer_id", "article_id"])
    out["f_user_item_count"] = pd.Series(
        key.map(pair.size()), index=X.index
    ).fillna(0)
    out["f_user_item_recency"] = pd.Series(
        key.map(pair["days_ago"].min()), index=X.index
    ).fillna(365)
    out["f_user_item_recent"] = pd.Series(
        key.map(h30.groupby(["customer_id", "article_id"]).size()),
        index=X.index
    ).fillna(0)

    ug = h.groupby("customer_id")
    out["f_customer_recency"] = user.map(ug["days_ago"].min()).fillna(365)
    out["f_user_activity_30d"] = np.log1p(
        user.map(h30.groupby("customer_id").size()).fillna(0)
    )
    out["f_user_activity_90d"] = np.log1p(
        user.map(h90.groupby("customer_id").size()).fillna(0)
    )

    def add_group(raw, hist_col, name, recent_name=None):
        k = pd.MultiIndex.from_arrays([user, X[raw]])
        out[name] = pd.Series(
            k.map(h.groupby(["customer_id", hist_col]).size()),
            index=X.index
        ).fillna(0)
        if recent_name is not None:
            out[recent_name] = pd.Series(
                k.map(h30.groupby(["customer_id", hist_col]).size()),
                index=X.index
            ).fillna(0)

    add_group("raw_i_product_code", "product_code", "f_user_product_count")
    add_group("raw_i_product_type_no", "product_type_no",
              "f_user_type_count", "f_user_type_recent")
    add_group("raw_i_department_no", "department_no",
              "f_user_department_count")
    add_group("raw_i_section_no", "section_no", "f_user_section_count")
    add_group("raw_i_garment_group_no", "garment_group_no",
              "f_user_garment_count")
    add_group("raw_i_colour_group_code", "colour_group_code",
              "f_user_colour_count")

    out["f_item_product_popularity"] = np.log1p(
        X["raw_i_product_code"].map(h.groupby("product_code").size()).fillna(0)
    )
    out["f_item_section_popularity"] = np.log1p(
        X["raw_i_section_no"].map(h.groupby("section_no").size()).fillna(0)
    )
    out["f_item_price_mean"] = item.map(
        h.groupby("article_id")["price"].mean()
    ).fillna(0)

    age_mean = h.groupby("article_id")["customer_age"].mean()
    buyer_age = item.map(age_mean)
    out["f_item_buyer_age_mean"] = buyer_age.fillna(0)
    out["f_item_age_distance"] = (
        pd.to_numeric(X["raw_u_age"], errors="coerce") - buyer_age
    ).abs().fillna(0)

    return out.replace([np.inf, -np.inf], np.nan)
