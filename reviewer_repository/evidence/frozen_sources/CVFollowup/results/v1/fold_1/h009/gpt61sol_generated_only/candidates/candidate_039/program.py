def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)
    names = (
        "f_i_10", "f_i_35", "f_i_75", "f_i_365",
        "f_i_users_75", "f_u_gap", "f_u_10",
        "f_pair_10", "f_pair_75", "f_pair_gap",
        "f_u_index_75", "f_u_garment_75"
    )
    h = history
    if h is None or len(h) == 0:
        for name in names:
            out[name] = 0.0
        return out

    def get(keys, values):
        a = pd.DataFrame({"_p": np.arange(n)})
        for j, k in enumerate(keys):
            a["_k" + str(j)] = X[k].to_numpy()
        b = values.rename("_v").reset_index()
        b.columns = ["_k" + str(j) for j in range(len(keys))] + ["_v"]
        a = a.merge(
            b, on=["_k" + str(j) for j in range(len(keys))],
            how="left", sort=False
        )
        return a.sort_values("_p")["_v"].to_numpy()

    for d, name in ((10, "f_i_10"), (35, "f_i_35"),
                    (75, "f_i_75"), (365, "f_i_365")):
        q = h.loc[h["days_ago"] <= d]
        out[name] = X["article_id"].map(
            q.groupby("article_id").size()).fillna(0).to_numpy()

    q75 = h.loc[h["days_ago"] <= 75]
    out["f_i_users_75"] = X["article_id"].map(
        q75.groupby("article_id")["customer_id"].nunique()
    ).fillna(0).to_numpy()

    out["f_u_gap"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()).to_numpy()
    q10 = h.loc[h["days_ago"] <= 10]
    out["f_u_10"] = X["customer_id"].map(
        q10.groupby("customer_id").size()).fillna(0).to_numpy()

    p10 = q10.groupby(["customer_id", "article_id"]).size()
    p75 = q75.groupby(["customer_id", "article_id"]).size()
    out["f_pair_10"] = get(["customer_id", "article_id"], p10)
    out["f_pair_75"] = get(["customer_id", "article_id"], p75)

    out["f_pair_gap"] = get(
        ["customer_id", "article_id"],
        h.groupby(["customer_id", "article_id"])["days_ago"].min()
    )

    ui = q75.groupby(["customer_id", "index_group_no"]).size()
    ug = q75.groupby(["customer_id", "garment_group_no"]).size()
    out["f_u_index_75"] = get(
        ["customer_id", "raw_i_index_group_no"], ui)
    out["f_u_garment_75"] = get(
        ["customer_id", "raw_i_garment_group_no"], ug)

    return out.astype(float)
