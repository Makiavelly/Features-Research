def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    customer = X["customer_id"]
    article = X["article_id"]

    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_all",
        "f_item_recency", "f_item_recent_share",
        "f_customer_count_30d", "f_customer_count_all",
        "f_customer_recency", "f_pair_count_all", "f_pair_count_30d",
        "f_pair_recency", "f_customer_product_count",
        "f_customer_type_count", "f_customer_department_count",
        "f_customer_section_count", "f_product_affinity_30d",
        "f_department_affinity_30d", "f_type_affinity_30d",
        "f_department_popularity_7d", "f_item_price",
        "f_customer_department_price", "f_u_age",
        "f_i_product_type_no", "f_i_department_no",
        "f_i_section_no"
    ]

    if history is None or len(history) == 0:
        for name in names:
            if name.endswith("recency"):
                out[name] = 4000.0
            elif name in ("f_item_price", "f_customer_department_price"):
                out[name] = np.nan
            elif name == "f_u_age":
                out[name] = X["raw_u_age"].to_numpy()
            elif name == "f_i_product_type_no":
                out[name] = X["raw_i_product_type_no"].to_numpy()
            elif name == "f_i_department_no":
                out[name] = X["raw_i_department_no"].to_numpy()
            elif name == "f_i_section_no":
                out[name] = X["raw_i_section_no"].to_numpy()
            else:
                out[name] = 0.0
        return out

    h = history
    r7 = h.loc[h["days_ago"] <= 7]
    r30 = h.loc[h["days_ago"] <= 30]

    def logv(v):
        return np.log1p(pd.Series(v).clip(lower=0).to_numpy(dtype=float))

    def one(values, key, fill=0):
        return key.map(values).fillna(fill).to_numpy()

    def multi(values, keys, fill=0):
        index = pd.MultiIndex.from_arrays(keys)
        return values.reindex(index).fillna(fill).to_numpy()

    def count(frame, keys):
        return frame.groupby(keys, observed=True).size()

    item7 = count(r7, "article_id")
    item30 = count(r30, "article_id")
    itemall = count(h, "article_id")

    out["f_item_count_7d"] = logv(one(item7, article))
    out["f_item_count_30d"] = logv(one(item30, article))
    out["f_item_count_all"] = logv(one(itemall, article))
    out["f_item_recency"] = article.map(
        h.groupby("article_id", observed=True)["days_ago"].min()
    ).fillna(4000).to_numpy()

    item30v = one(item30, article)
    itemallv = one(itemall, article)
    out["f_item_recent_share"] = item30v / np.maximum(itemallv, 1)

    c30 = count(r30, "customer_id")
    call = count(h, "customer_id")
    out["f_customer_count_30d"] = logv(one(c30, customer))
    out["f_customer_count_all"] = logv(one(call, customer))
    out["f_customer_recency"] = customer.map(
        h.groupby("customer_id", observed=True)["days_ago"].min()
    ).fillna(4000).to_numpy()

    pair = h.groupby(["customer_id", "article_id"], observed=True).agg(
        n=("days_ago", "size"),
        recency=("days_ago", "min")
    )
    out["f_pair_count_all"] = logv(multi(pair["n"], [customer, article]))
    out["f_pair_recency"] = multi(pair["recency"], [customer, article], 4000)
    out["f_pair_count_30d"] = logv(
        multi(count(r30, ["customer_id", "article_id"]), [customer, article])
    )

    total30 = one(c30, customer)
    for field, raw, cname, aname in [
        ("product_code", "raw_i_product_code",
         "f_customer_product_count", "f_product_affinity_30d"),
        ("product_type_no", "raw_i_product_type_no",
         "f_customer_type_count", "f_type_affinity_30d"),
        ("department_no", "raw_i_department_no",
         "f_customer_department_count", "f_department_affinity_30d"),
        ("section_no", "raw_i_section_no",
         "f_customer_section_count", None),
    ]:
        all_counts = count(h, ["customer_id", field])
        matched_all = multi(all_counts, [customer, X[raw]])
        out[cname] = logv(matched_all)
        if aname is not None:
            recent_counts = count(r30, ["customer_id", field])
            matched_recent = multi(recent_counts, [customer, X[raw]])
            out[aname] = matched_recent / np.maximum(total30, 1)

    dept7 = count(r7, "department_no")
    out["f_department_popularity_7d"] = logv(
        one(dept7, X["raw_i_department_no"])
    )

    out["f_item_price"] = article.map(
        h.groupby("article_id", observed=True)["price"].mean()
    ).to_numpy()

    dep_price = h.groupby(
        ["customer_id", "department_no"], observed=True
    )["price"].mean()
    out["f_customer_department_price"] = multi(
        dep_price, [customer, X["raw_i_department_no"]], np.nan
    )

    out["f_u_age"] = X["raw_u_age"].to_numpy()
    out["f_i_product_type_no"] = X["raw_i_product_type_no"].to_numpy()
    out["f_i_department_no"] = X["raw_i_department_no"].to_numpy()
    out["f_i_section_no"] = X["raw_i_section_no"].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan)
