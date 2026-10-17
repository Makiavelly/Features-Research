def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    if h.empty:
        for name in (
            "f_item_count_30d", "f_item_count_90d", "f_item_count_all",
            "f_item_recency", "f_item_price_mean", "f_user_count_30d",
            "f_user_count_all", "f_user_recency", "f_pair_count_all",
            "f_user_section_count", "f_user_product_count",
            "f_user_colour_count",
        ):
            out[name] = 0
        return out

    h = h.assign(_days=pd.to_numeric(h["days_ago"], errors="coerce"))

    for window, name in ((30, "f_item_count_30d"), (90, "f_item_count_90d")):
        counts = h.loc[h["_days"] <= window].groupby("article_id", observed=True).size()
        out[name] = X["article_id"].map(counts).fillna(0).to_numpy()

    item_counts = h.groupby("article_id", observed=True).size()
    out["f_item_count_all"] = X["article_id"].map(item_counts).fillna(0).to_numpy()
    item_recency = h.groupby("article_id", observed=True)["_days"].min()
    out["f_item_recency"] = X["article_id"].map(item_recency).fillna(-1).to_numpy()

    price = pd.to_numeric(h["price"], errors="coerce")
    item_price = price.groupby(h["article_id"], observed=True).mean()
    out["f_item_price_mean"] = X["article_id"].map(item_price).to_numpy()

    for window, name in ((30, "f_user_count_30d"), (None, "f_user_count_all")):
        source = h if window is None else h.loc[h["_days"] <= window]
        counts = source.groupby("customer_id", observed=True).size()
        out[name] = X["customer_id"].map(counts).fillna(0).to_numpy()

    user_recency = h.groupby("customer_id", observed=True)["_days"].min()
    out["f_user_recency"] = X["customer_id"].map(user_recency).fillna(-1).to_numpy()

    pair = h.groupby(["customer_id", "article_id"], observed=True).size()
    keys = pd.MultiIndex.from_arrays(
        [X["customer_id"].to_numpy(), X["article_id"].to_numpy()],
        names=["customer_id", "article_id"],
    )
    out["f_pair_count_all"] = pair.reindex(keys).fillna(0).to_numpy()

    for raw_col, hist_col, name in (
        ("raw_i_section_no", "section_no", "f_user_section_count"),
        ("raw_i_product_code", "product_code", "f_user_product_count"),
        ("raw_i_colour_group_code", "colour_group_code", "f_user_colour_count"),
    ):
        grouped = h.groupby(["customer_id", hist_col], observed=True).size()
        lookup = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[raw_col].to_numpy()],
            names=["customer_id", hist_col],
        )
        out[name] = grouped.reindex(lookup).fillna(0).to_numpy()

    return out.replace([np.inf, -np.inf], np.nan)
