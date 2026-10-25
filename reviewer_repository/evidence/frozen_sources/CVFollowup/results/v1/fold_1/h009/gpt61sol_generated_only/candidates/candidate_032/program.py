def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)
    names = (
        "f_article_3d", "f_article_21d", "f_article_180d",
        "f_article_decay", "f_user_7d", "f_user_45d",
        "f_user_last", "f_pair_45d", "f_pair_last",
        "f_user_garment_45d", "f_user_colour_45d",
        "f_product_code_45d"
    )
    h = history

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
        (3, "f_article_3d"),
        (21, "f_article_21d"),
        (180, "f_article_180d")
    ):
        q = h.loc[h["days_ago"] <= days]
        v = q.groupby("article_id").size()
        out[name] = X["article_id"].map(v).fillna(0).to_numpy()

    decay = np.exp(-h["days_ago"].astype(float) / 18.0)
    decay = pd.Series(decay.to_numpy(), index=h.index)
    out["f_article_decay"] = X["article_id"].map(
        decay.groupby(h["article_id"]).sum()).fillna(0).to_numpy()

    for days, name in ((7, "f_user_7d"), (45, "f_user_45d")):
        q = h.loc[h["days_ago"] <= days]
        v = q.groupby("customer_id").size()
        out[name] = X["customer_id"].map(v).fillna(0).to_numpy()

    out["f_user_last"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()).to_numpy()

    q = h.loc[h["days_ago"] <= 45]
    pair = q.groupby(["customer_id", "article_id"]).size()
    last = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    out["f_pair_45d"] = lookup(["customer_id", "article_id"], pair)
    out["f_pair_last"] = lookup(["customer_id", "article_id"], last)

    garment = q.groupby(["customer_id", "garment_group_no"]).size()
    colour = q.groupby(["customer_id", "colour_group_code"]).size()
    out["f_user_garment_45d"] = lookup(
        ["customer_id", "raw_i_garment_group_no"], garment)
    out["f_user_colour_45d"] = lookup(
        ["customer_id", "raw_i_colour_group_code"], colour)

    product = q.groupby("product_code").size()
    out["f_product_code_45d"] = X["raw_i_product_code"].map(
        product).fillna(0).to_numpy()

    return out.astype(float)
