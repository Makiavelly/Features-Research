def modify_features(X, history):
    import pandas as pd
    import numpy as np

    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_recency", "f_item_popularity", "f_item_decay_score",
        "f_user_item_count", "f_user_item_recency", "f_user_item_decay",
        "f_customer_recency", "f_user_activity_30d", "f_user_type_count",
        "f_user_type_recent", "f_user_section_count", "f_item_price_mean",
    ]
    out = pd.DataFrame(index=X.index)
    h = history
    if h is None or len(h) == 0:
        for n in names:
            out[n] = 0.0
        return out

    days = pd.to_numeric(h["days_ago"], errors="coerce").fillna(9999)
    recent30 = h.loc[days <= 30]
    item = X["article_id"]
    user = X["customer_id"]

    for w in (7, 30, 90):
        c = h.loc[days <= w].groupby("article_id").size()
        out["f_item_count_%dd" % w] = item.map(c).fillna(0)

    item_counts = h.groupby("article_id").size()
    out["f_item_popularity"] = np.log1p(item.map(item_counts).fillna(0))
    out["f_item_recency"] = item.map(
        h.groupby("article_id")["days_ago"].min()
    ).fillna(365)

    weight = np.exp(-days / 30.0)
    item_decay = h.assign(_w=weight).groupby("article_id")["_w"].sum()
    out["f_item_decay_score"] = item.map(item_decay).fillna(0)

    pair = pd.MultiIndex.from_arrays([user, item])
    pair_counts = h.groupby(["customer_id", "article_id"]).size()
    pair_rec = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    pair_decay = h.assign(_w=weight).groupby(
        ["customer_id", "article_id"]
    )["_w"].sum()
    out["f_user_item_count"] = pd.Series(
        pair.map(pair_counts), index=X.index
    ).fillna(0)
    out["f_user_item_recency"] = pd.Series(
        pair.map(pair_rec), index=X.index
    ).fillna(365)
    out["f_user_item_decay"] = pd.Series(
        pair.map(pair_decay), index=X.index
    ).fillna(0)

    out["f_customer_recency"] = user.map(
        h.groupby("customer_id")["days_ago"].min()
    ).fillna(365)
    out["f_user_activity_30d"] = np.log1p(
        user.map(recent30.groupby("customer_id").size()).fillna(0)
    )

    type_key = pd.MultiIndex.from_arrays(
        [user, X["raw_i_product_type_no"]]
    )
    type_counts = h.groupby(
        ["customer_id", "product_type_no"]
    ).size()
    type_recent = recent30.groupby(
        ["customer_id", "product_type_no"]
    ).size()
    out["f_user_type_count"] = pd.Series(
        type_key.map(type_counts), index=X.index
    ).fillna(0)
    out["f_user_type_recent"] = pd.Series(
        type_key.map(type_recent), index=X.index
    ).fillna(0)

    section_key = pd.MultiIndex.from_arrays(
        [user, X["raw_i_section_no"]]
    )
    section_counts = h.groupby(["customer_id", "section_no"]).size()
    out["f_user_section_count"] = pd.Series(
        section_key.map(section_counts), index=X.index
    ).fillna(0)

    out["f_item_price_mean"] = item.map(
        h.groupby("article_id")["price"].mean()
    ).fillna(0)

    return out.replace([np.inf, -np.inf], np.nan)
