def modify_features(X, history):
    import numpy as np
    import pandas as pd

    out = pd.DataFrame(index=X.index)
    customer = X["customer_id"]
    article = X["article_id"]

    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_all",
        "f_customer_count_30d", "f_customer_count_365d",
        "f_pair_count_all", "f_pair_count_30d", "f_pair_recency",
        "f_customer_product_count", "f_customer_type_count",
        "f_customer_department_count", "f_customer_section_count",
        "f_product_affinity", "f_department_affinity",
        "f_item_recent_share", "f_customer_department_price",
    ]

    if history is None or len(history) == 0:
        for name in names:
            out[name] = 4000.0 if name == "f_pair_recency" else np.nan if name == "f_customer_department_price" else 0.0
        return out

    h = history
    days = h["days_ago"]

    def counts(frame, keys):
        return frame.groupby(keys, observed=True).size()

    def mapped(values, keys):
        idx = pd.MultiIndex.from_arrays(keys)
        return pd.Series(values.reindex(idx).to_numpy(), index=X.index)

    def log_count(values):
        return np.log1p(values.clip(lower=0))

    recent7 = h.loc[days <= 7]
    recent30 = h.loc[days <= 30]
    recent365 = h.loc[days <= 365]

    for name, frame in (
        ("f_item_count_7d", recent7),
        ("f_item_count_30d", recent30),
        ("f_item_count_all", h),
    ):
        out[name] = log_count(article.map(counts(frame, "article_id")).fillna(0)).to_numpy()

    out["f_customer_count_30d"] = log_count(
        customer.map(counts(recent30, "customer_id")).fillna(0)
    ).to_numpy()
    out["f_customer_count_365d"] = log_count(
        customer.map(counts(recent365, "customer_id")).fillna(0)
    ).to_numpy()

    pair = h.groupby(["customer_id", "article_id"], observed=True)["days_ago"].agg(
        count="size", recency="min"
    )
    out["f_pair_count_all"] = log_count(
        mapped(pair["count"], [customer, article]).fillna(0)
    ).to_numpy()
    out["f_pair_count_30d"] = log_count(
        mapped(counts(recent30, ["customer_id", "article_id"]), [customer, article]).fillna(0)
    ).to_numpy()
    out["f_pair_recency"] = mapped(
        pair["recency"], [customer, article]
    ).fillna(4000).to_numpy()

    total = counts(h, "customer_id").reindex(customer).fillna(0).to_numpy()
    for field, raw, name in (
        ("product_code", "raw_i_product_code", "f_customer_product_count"),
        ("product_type_no", "raw_i_product_type_no", "f_customer_type_count"),
        ("department_no", "raw_i_department_no", "f_customer_department_count"),
        ("section_no", "raw_i_section_no", "f_customer_section_count"),
    ):
        matched = mapped(
            counts(h, ["customer_id", field]), [customer, X[raw]]
        ).fillna(0)
        out[name] = log_count(matched).to_numpy()

    for field, raw, name in (
        ("product_code", "raw_i_product_code", "f_product_affinity"),
        ("department_no", "raw_i_department_no", "f_department_affinity"),
    ):
        matched = mapped(
            counts(h, ["customer_id", field]), [customer, X[raw]]
        ).fillna(0).to_numpy()
        out[name] = matched / np.maximum(total, 1)

    item30 = article.map(counts(recent30, "article_id")).fillna(0).to_numpy()
    itemall = article.map(counts(h, "article_id")).fillna(0).to_numpy()
    out["f_item_recent_share"] = item30 / np.maximum(itemall, 1)

    price_mean = h.groupby(
        ["customer_id", "department_no"], observed=True
    )["price"].mean()
    out["f_customer_department_price"] = mapped(
        price_mean, [customer, X["raw_i_department_no"]]
    ).to_numpy()

    return out.replace([np.inf, -np.inf], np.nan)
