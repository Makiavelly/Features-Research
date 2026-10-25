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
        "f_user_garment_count", "f_item_product_popularity",
        "f_item_section_popularity", "f_item_price_mean",
    ]
    out = pd.DataFrame(index=X.index)
    h = history
    if h is None or len(h) == 0:
        for n in names:
            out[n] = 0.0
        return out

    d = pd.to_numeric(h["days_ago"], errors="coerce").fillna(9999)
    item = X["article_id"]
    user = X["customer_id"]

    for w in (7, 30, 90):
        out["f_item_count_%dd" % w] = item.map(
            h.loc[d <= w].groupby("article_id").size()
        ).fillna(0)

    all_items = h.groupby("article_id").size()
    total = item.map(all_items).fillna(0)
    out["f_item_popularity"] = np.log1p(total)
    out["f_item_recency"] = item.map(
        h.groupby("article_id")["days_ago"].min()
    ).fillna(365)
    out["f_item_recent_ratio"] = item.map(
        h.loc[d <= 30].groupby("article_id").size()
    ).fillna(0) / (total + 1.0)

    pair = pd.MultiIndex.from_arrays([user, item])
    gp = h.groupby(["customer_id", "article_id"])
    out["f_user_item_count"] = pd.Series(
        pair.map(gp.size()), index=X.index
    ).fillna(0)
    out["f_user_item_recency"] = pd.Series(
        pair.map(gp["days_ago"].min()), index=X.index
    ).fillna(365)
    out["f_user_item_recent"] = pd.Series(
        pair.map(h.loc[d <= 30].groupby(
            ["customer_id", "article_id"]).size()), index=X.index
    ).fillna(0)

    ug = h.groupby("customer_id")
    out["f_customer_recency"] = user.map(ug["days_ago"].min()).fillna(365)
    out["f_user_activity_30d"] = np.log1p(user.map(
        h.loc[d <= 30].groupby("customer_id").size()).fillna(0))
    out["f_user_activity_90d"] = np.log1p(user.map(
        h.loc[d <= 90].groupby("customer_id").size()).fillna(0))

    def add_group(raw, hist, name, recent=None):
        key = pd.MultiIndex.from_arrays([user, X[raw]])
        out[name] = pd.Series(
            key.map(h.groupby(["customer_id", hist]).size()),
            index=X.index).fillna(0)
        if recent:
            out[recent] = pd.Series(
                key.map(h.loc[d <= 30].groupby(
                    ["customer_id", hist]).size()),
                index=X.index).fillna(0)

    add_group("raw_i_product_code", "product_code", "f_user_product_count")
    add_group("raw_i_product_type_no", "product_type_no",
              "f_user_type_count", "f_user_type_recent")
    add_group("raw_i_department_no", "department_no",
              "f_user_department_count")
    add_group("raw_i_section_no", "section_no", "f_user_section_count")
    add_group("raw_i_garment_group_no", "garment_group_no",
              "f_user_garment_count")

    out["f_item_product_popularity"] = np.log1p(
        X["raw_i_product_code"].map(h.groupby("product_code").size()).fillna(0)
    )
    out["f_item_section_popularity"] = np.log1p(
        X["raw_i_section_no"].map(h.groupby("section_no").size()).fillna(0)
    )
    out["f_item_price_mean"] = item.map(
        h.groupby("article_id")["price"].mean()).fillna(0)

    return out.replace([np.inf, -np.inf], np.nan)
