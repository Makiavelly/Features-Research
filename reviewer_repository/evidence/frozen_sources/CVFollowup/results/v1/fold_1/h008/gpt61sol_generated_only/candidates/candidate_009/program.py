def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    customer = X["customer_id"]
    article = X["article_id"]

    def mapped(values, keys):
        index = pd.MultiIndex.from_arrays(keys)
        return pd.Series(values.reindex(index).to_numpy(), index=X.index)

    def grouped_count(frame, keys):
        return frame.groupby(keys, observed=True).size()

    def safe_log(values):
        return np.log1p(values.clip(lower=0))

    names = (
        "f_item_count_7d", "f_item_count_30d", "f_item_count_all",
        "f_customer_count_30d", "f_customer_count_365d",
        "f_pair_count_all", "f_pair_count_30d", "f_pair_recency",
        "f_customer_product_count", "f_customer_type_count",
        "f_customer_department_count", "f_customer_section_count",
        "f_product_affinity", "f_department_affinity",
        "f_item_recent_share", "f_customer_department_price",
    )

    if history is None or len(history) == 0:
        for name in names:
            out[name] = 4000.0 if name == "f_pair_recency" else np.nan if name == "f_customer_department_price" else 0.0
        return out

    h = history
    days = h["days_ago"]
    recent7 = h.loc[days <= 7]
    recent30 = h.loc[days <= 30]
    recent365 = h.loc[days <= 365]

    for name, frame in (
        ("f_item_count_7d", recent7),
        ("f_item_count_30d", recent30),
        ("f_item_count_all", h),
    ):
        out[name] = safe_log(article.map(grouped_count(frame, "article_id")).fillna(0)).to_numpy()

    out["f_customer_count_30d"] = safe_log(
        customer.map(grouped_count(recent30, "customer_id")).fillna(0)
    ).to_numpy()
    out["f_customer_count_365d"] = safe_log(
        customer.map(grouped_count(recent365, "customer_id")).fillna(0)
    ).to_numpy()

    pair = h.groupby(["customer_id", "article_id"], observed=True).agg(
        count=("days_ago", "size"), recency=("days_ago", "min")
    )
    out["f_pair_count_all"] = safe_log(
        mapped(pair["count"], [customer, article]).fillna(0)
    ).to_numpy()
    out["f_pair_recency"] = mapped(
        pair["recency"], [customer, article]
    ).fillna(4000).to_numpy()
    pair30 = grouped_count(recent30, ["customer_id", "article_id"])
    out["f_pair_count_30d"] = safe_log(
        mapped(pair30, [customer, article]).fillna(0)
    ).to_numpy()

    for field, raw, name in (
        ("product_code", "raw_i_product_code", "f_customer_product_count"),
        ("product_type_no", "raw_i_product_type_no", "f_customer_type_count"),
        ("department_no", "raw_i_department_no", "f_customer_department_count"),
        ("section_no", "raw_i_section_no", "f_customer_section_count"),
    ):
        counts = grouped_count(h, ["customer_id", field])
        out[name] = safe_log(mapped(counts, [customer, X[raw]]).fillna(0)).to_numpy()

    total = grouped_count(h, "customer_id").reindex(customer).to_numpy()
    for field, raw, name in (
        ("product_code", "raw_i_product_code", "f_product_affinity"),
        ("department_no", "raw_i_department_no", "f_department_affinity"),
    ):
        counts = grouped_count(h, ["customer_id", field])
        matched = mapped(counts, [customer, X[raw]]).fillna(0).to_numpy()
        out[name] = matched / np.maximum(total, 1)

    item30 = article.map(grouped_count(recent30, "article_id")).fillna(0).to_numpy()
    itemall = article.map(grouped_count(h, "article_id")).fillna(0).to_numpy()
    out["f_item_recent_share"] = item30 / np.maximum(itemall, 1)

    if "price" in h.columns and "department_no" in h.columns:
        price_mean = h.groupby(
            ["customer_id", "department_no"], observed=True
        )["price"].mean()
        out["f_customer_department_price"] = mapped(
            price_mean, [customer, X["raw_i_department_no"]]
        ).to_numpy()
    else:
        out["f_customer_department_price"] = np.nan

    return out.replace([np.inf, -np.inf], np.nan)
