def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)
    h = history

    names = (
        "f_article_rate_14d", "f_article_rate_45d", "f_article_rate_120d",
        "f_article_buyers_45d", "f_article_recency",
        "f_customer_active_14d", "f_customer_active_45d",
        "f_pair_count_45d", "f_pair_recency",
        "f_category_affinity_type", "f_category_affinity_dept",
        "f_category_affinity_section"
    )
    if h is None or len(h) == 0:
        for name in names:
            out[name] = np.zeros(n, dtype=float)
        return out

    def lookup(keys, values):
        left = pd.DataFrame({"_p": np.arange(n)})
        for i, key in enumerate(keys):
            left["_k" + str(i)] = X[key].to_numpy()
        right = values.rename("_v").reset_index()
        right.columns = ["_k" + str(i) for i in range(len(keys))] + ["_v"]
        z = left.merge(
            right,
            on=["_k" + str(i) for i in range(len(keys))],
            how="left",
            sort=False
        )
        return z.sort_values("_p")["_v"].to_numpy()

    for days, name in (
        (14, "f_article_rate_14d"),
        (45, "f_article_rate_45d"),
        (120, "f_article_rate_120d")
    ):
        q = h.loc[h["days_ago"] <= days]
        out[name] = X["article_id"].map(
            q.groupby("article_id").size()).fillna(0).to_numpy()

    q45 = h.loc[h["days_ago"] <= 45]
    out["f_article_buyers_45d"] = X["article_id"].map(
        q45.groupby("article_id")["customer_id"].nunique()).fillna(0).to_numpy()
    out["f_article_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()).to_numpy()

    q14 = h.loc[h["days_ago"] <= 14]
    out["f_customer_active_14d"] = X["customer_id"].map(
        q14.groupby("customer_id")["article_id"].nunique()).fillna(0).to_numpy()
    out["f_customer_active_45d"] = X["customer_id"].map(
        q45.groupby("customer_id")["article_id"].nunique()).fillna(0).to_numpy()

    pair45 = q45.groupby(["customer_id", "article_id"]).size()
    pairrec = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    out["f_pair_count_45d"] = lookup(
        ["customer_id", "article_id"], pair45)
    out["f_pair_recency"] = lookup(
        ["customer_id", "article_id"], pairrec)

    for col, raw, name in (
        ("product_type_no", "raw_i_product_type_no",
         "f_category_affinity_type"),
        ("department_no", "raw_i_department_no",
         "f_category_affinity_dept"),
        ("section_no", "raw_i_section_no",
         "f_category_affinity_section")
    ):
        values = q45.groupby(["customer_id", col]).size()
        out[name] = lookup(["customer_id", raw], values)

    return out.astype(float)
