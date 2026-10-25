import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_all",
        "f_item_recency", "f_customer_count_7d", "f_customer_count_30d",
        "f_customer_count_all", "f_customer_recency", "f_pair_count_7d",
        "f_pair_count_30d", "f_pair_count_all", "f_pair_recency",
        "f_customer_product_count", "f_customer_type_count",
        "f_customer_department_count", "f_customer_section_count",
        "f_product_affinity", "f_department_affinity",
        "f_product_recency", "f_department_recency",
        "f_item_recent_share", "f_item_channel_2_share"
    ]
    out = pd.DataFrame(index=X.index)
    customer = X["customer_id"]
    article = X["article_id"]

    if history is None or len(history) == 0:
        for name in names:
            out[name] = 4000.0 if "recency" in name else 0.0
        return out

    h = history
    d = h["days_ago"]

    def log_values(v):
        a = np.asarray(v, dtype=float)
        return np.log1p(np.maximum(a, 0))

    def one_map(series, key):
        return key.map(series).fillna(0).to_numpy()

    def two_map(series, k1, k2):
        idx = pd.MultiIndex.from_arrays([k1.to_numpy(), k2.to_numpy()])
        return pd.Series(series.reindex(idx).to_numpy(), index=X.index)

    def counts(frame, key):
        return frame.groupby(key, observed=True).size()

    recent7 = h.loc[d <= 7]
    recent30 = h.loc[d <= 30]

    for name, frame in (
        ("f_item_count_7d", recent7),
        ("f_item_count_30d", recent30),
        ("f_item_count_all", h),
    ):
        out[name] = log_values(one_map(counts(frame, "article_id"), article))

    out["f_item_recency"] = article.map(
        h.groupby("article_id", observed=True)["days_ago"].min()
    ).fillna(4000).to_numpy()

    for name, frame in (
        ("f_customer_count_7d", recent7),
        ("f_customer_count_30d", recent30),
        ("f_customer_count_all", h),
    ):
        out[name] = log_values(one_map(counts(frame, "customer_id"), customer))

    out["f_customer_recency"] = customer.map(
        h.groupby("customer_id", observed=True)["days_ago"].min()
    ).fillna(4000).to_numpy()

    pair_all = h.groupby(
        ["customer_id", "article_id"], observed=True
    ).agg(count=("days_ago", "size"), recency=("days_ago", "min"))
    pair7 = counts(recent7, ["customer_id", "article_id"])
    pair30 = counts(recent30, ["customer_id", "article_id"])

    out["f_pair_count_7d"] = log_values(
        two_map(pair7, customer, article).fillna(0)
    )
    out["f_pair_count_30d"] = log_values(
        two_map(pair30, customer, article).fillna(0)
    )
    out["f_pair_count_all"] = log_values(
        two_map(pair_all["count"], customer, article).fillna(0)
    )
    out["f_pair_recency"] = two_map(
        pair_all["recency"], customer, article
    ).fillna(4000).to_numpy()

    category_specs = (
        ("product_code", "raw_i_product_code", "f_customer_product_count"),
        ("product_type_no", "raw_i_product_type_no", "f_customer_type_count"),
        ("department_no", "raw_i_department_no", "f_customer_department_count"),
        ("section_no", "raw_i_section_no", "f_customer_section_count"),
    )
    for field, raw, name in category_specs:
        s = counts(h, ["customer_id", field])
        out[name] = log_values(
            two_map(s, customer, X[raw]).fillna(0)
        )

    total = customer.map(counts(h, "customer_id")).fillna(0).to_numpy()
    for field, raw, name in (
        ("product_code", "raw_i_product_code", "f_product_affinity"),
        ("department_no", "raw_i_department_no", "f_department_affinity"),
    ):
        matched = two_map(
            counts(h, ["customer_id", field]), customer, X[raw]
        ).fillna(0).to_numpy()
        out[name] = matched / np.maximum(total, 1)

    for field, raw, name in (
        ("product_code", "raw_i_product_code", "f_product_recency"),
        ("department_no", "raw_i_department_no", "f_department_recency"),
    ):
        rec = h.groupby(
            ["customer_id", field], observed=True
        )["days_ago"].min()
        out[name] = two_map(rec, customer, X[raw]).fillna(4000).to_numpy()

    item30 = one_map(counts(recent30, "article_id"), article)
    itemall = one_map(counts(h, "article_id"), article)
    out["f_item_recent_share"] = item30 / np.maximum(itemall, 1)

    channel2 = h.loc[h["sales_channel_id"] == 2]
    c2 = one_map(counts(channel2, "article_id"), article)
    out["f_item_channel_2_share"] = c2 / np.maximum(itemall, 1)

    return out.replace([np.inf, -np.inf], np.nan)
