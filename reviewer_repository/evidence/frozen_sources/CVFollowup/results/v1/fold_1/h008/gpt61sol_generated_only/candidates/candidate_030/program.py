def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    customer = X["customer_id"]
    article = X["article_id"]

    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_all",
        "f_item_recency", "f_item_weighted",
        "f_customer_count_7d", "f_customer_count_30d", "f_customer_count_all",
        "f_customer_recency", "f_customer_weighted",
        "f_pair_count_all", "f_pair_count_30d", "f_pair_recency",
        "f_pair_weighted",
        "f_customer_product_count", "f_customer_type_count",
        "f_customer_department_count", "f_customer_section_count",
        "f_product_affinity", "f_type_affinity",
        "f_department_affinity", "f_section_affinity",
        "f_item_department_count_30d", "f_item_type_count_30d",
        "f_customer_department_price", "f_item_price",
        "f_u_age", "f_u_fn", "f_u_active", "f_i_product_code",
        "f_i_product_type_no", "f_i_department_no", "f_i_section_no",
        "f_i_garment_group_no",
    ]

    if history is None or len(history) == 0:
        for n in names:
            if n.endswith("_recency"):
                out[n] = 4000.0
            elif n in ("f_customer_department_price", "f_item_price"):
                out[n] = np.nan
            elif n.startswith("f_u_") or n.startswith("f_i_"):
                raw = n[2:]
                col = "raw_" + raw
                out[n] = X[col].to_numpy() if col in X else np.nan
            else:
                out[n] = 0.0
        return out

    h = history
    d = h["days_ago"].to_numpy()
    r7 = h.loc[d <= 7]
    r30 = h.loc[d <= 30]

    def lg(v):
        return np.log1p(np.asarray(v, dtype=float).clip(0))

    def one_map(s, key):
        return key.map(s).fillna(0).to_numpy()

    def multi_map(s, keys, fill=0):
        mi = pd.MultiIndex.from_arrays([np.asarray(k) for k in keys])
        return s.reindex(mi).fillna(fill).to_numpy()

    def counts(frame, key):
        return frame.groupby(key, observed=True).size()

    def gcounts(frame, keys):
        return frame.groupby(keys, observed=True).size()

    out["f_item_count_7d"] = lg(one_map(counts(r7, "article_id"), article))
    out["f_item_count_30d"] = lg(one_map(counts(r30, "article_id"), article))
    out["f_item_count_all"] = lg(one_map(counts(h, "article_id"), article))

    item_rec = h.groupby("article_id", observed=True)["days_ago"].min()
    out["f_item_recency"] = article.map(item_rec).fillna(4000).to_numpy()

    hw = h.assign(_w=np.exp(-h["days_ago"].to_numpy() / 30.0))
    iw = hw.groupby("article_id", observed=True)["_w"].sum()
    out["f_item_weighted"] = lg(one_map(iw, article))

    out["f_customer_count_7d"] = lg(one_map(counts(r7, "customer_id"), customer))
    out["f_customer_count_30d"] = lg(one_map(counts(r30, "customer_id"), customer))
    out["f_customer_count_all"] = lg(one_map(counts(h, "customer_id"), customer))

    crec = h.groupby("customer_id", observed=True)["days_ago"].min()
    out["f_customer_recency"] = customer.map(crec).fillna(4000).to_numpy()
    cw = hw.groupby("customer_id", observed=True)["_w"].sum()
    out["f_customer_weighted"] = lg(one_map(cw, customer))

    pair = h.groupby(["customer_id", "article_id"], observed=True).agg(
        n=("days_ago", "size"), rec=("days_ago", "min")
    )
    out["f_pair_count_all"] = lg(multi_map(pair["n"], [customer, article]))
    out["f_pair_recency"] = multi_map(pair["rec"], [customer, article], 4000)
    p30 = gcounts(r30, ["customer_id", "article_id"])
    out["f_pair_count_30d"] = lg(multi_map(p30, [customer, article]))
    pw = hw.groupby(["customer_id", "article_id"], observed=True)["_w"].sum()
    out["f_pair_weighted"] = lg(multi_map(pw, [customer, article]))

    specs = [
        ("product_code", "raw_i_product_code", "f_customer_product_count"),
        ("product_type_no", "raw_i_product_type_no", "f_customer_type_count"),
        ("department_no", "raw_i_department_no", "f_customer_department_count"),
        ("section_no", "raw_i_section_no", "f_customer_section_count"),
    ]
    total = h.groupby("customer_id", observed=True).size()
    den = one_map(total, customer)
    for field, raw, name in specs:
        z = gcounts(h, ["customer_id", field])
        m = multi_map(z, [customer, X[raw]])
        out[name] = lg(m)
        out[name.replace("_count", "_affinity")] = m / np.maximum(den, 1)

    out["f_item_department_count_30d"] = lg(
        multi_map(gcounts(r30, ["article_id", "department_no"]),
                  [article, X["raw_i_department_no"]])
    )
    out["f_item_type_count_30d"] = lg(
        multi_map(gcounts(r30, ["article_id", "product_type_no"]),
                  [article, X["raw_i_product_type_no"]])
    )

    cp = h.groupby(["customer_id", "department_no"], observed=True)["price"].mean()
    out["f_customer_department_price"] = multi_map(
        cp, [customer, X["raw_i_department_no"]], np.nan
    )
    ip = h.groupby("article_id", observed=True)["price"].mean()
    out["f_item_price"] = article.map(ip).to_numpy()

    for raw, name in [
        ("raw_u_age", "f_u_age"), ("raw_u_fn", "f_u_fn"),
        ("raw_u_active", "f_u_active"),
        ("raw_i_product_code", "f_i_product_code"),
        ("raw_i_product_type_no", "f_i_product_type_no"),
        ("raw_i_department_no", "f_i_department_no"),
        ("raw_i_section_no", "f_i_section_no"),
        ("raw_i_garment_group_no", "f_i_garment_group_no"),
    ]:
        out[name] = X[raw].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan)
