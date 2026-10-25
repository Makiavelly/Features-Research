def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def empty(v=0.0):
        return np.full(n, v, dtype=float)

    def key(a, b=None):
        if b is None:
            return a.astype(str)
        return a.astype(str) + "|" + b.astype(str)

    def mapped(series, values, default=0.0):
        z = values.map(series)
        return z.fillna(default).to_numpy(dtype=float)

    if history is None or len(history) == 0:
        for name in [
            "f_u_n7", "f_u_n30", "f_u_n90", "f_i_n7", "f_i_n30",
            "f_i_n90", "f_pair_n", "f_u_recency", "f_i_recency",
            "f_pair_recency", "f_i_price", "f_u_type_n", "f_u_dept_n",
            "f_u_section_n", "f_u_colour_n", "f_match_type", "f_match_dept",
            "f_match_section", "f_match_colour"
        ]:
            out[name] = empty()
        return out

    h = history
    uid = X["customer_id"]
    iid = X["article_id"]

    ukey = h["customer_id"]
    ikey = h["article_id"]
    xukey = uid
    xikey = iid

    h7 = h["days_ago"] <= 7
    h30 = h["days_ago"] <= 30
    h90 = h["days_ago"] <= 90

    def count_by(mask, col):
        return h.loc[mask].groupby(col, sort=False).size()

    u7 = count_by(h7, "customer_id")
    u30 = count_by(h30, "customer_id")
    u90 = count_by(h90, "customer_id")
    i7 = count_by(h7, "article_id")
    i30 = count_by(h30, "article_id")
    i90 = count_by(h90, "article_id")

    out["f_u_n7"] = np.log1p(mapped(u7, xukey))
    out["f_u_n30"] = np.log1p(mapped(u30, xukey))
    out["f_u_n90"] = np.log1p(mapped(u90, xukey))
    out["f_i_n7"] = np.log1p(mapped(i7, xikey))
    out["f_i_n30"] = np.log1p(mapped(i30, xikey))
    out["f_i_n90"] = np.log1p(mapped(i90, xikey))

    hp = key(h["customer_id"], h["article_id"])
    xp = key(uid, iid)
    pair_counts = hp.value_counts()
    out["f_pair_n"] = np.log1p(mapped(pair_counts, xp))

    ur = h.groupby("customer_id", sort=False)["days_ago"].min()
    ir = h.groupby("article_id", sort=False)["days_ago"].min()
    pr = h.groupby(hp, sort=False)["days_ago"].min()
    out["f_u_recency"] = mapped(ur, xukey, np.nan)
    out["f_i_recency"] = mapped(ir, xikey, np.nan)
    out["f_pair_recency"] = mapped(pr, xp, np.nan)

    ip = h.groupby("article_id", sort=False)["price"].mean()
    out["f_i_price"] = mapped(ip, xikey, np.nan)

    def affinity(hist_col, raw_col, name):
        kk = key(h["customer_id"], h[hist_col])
        vv = kk.value_counts()
        qk = key(uid, X[raw_col])
        out[name] = np.log1p(mapped(vv, qk))

    affinity("product_type_no", "raw_i_product_type_no", "f_u_type_n")
    affinity("department_no", "raw_i_department_no", "f_u_dept_n")
    affinity("section_no", "raw_i_section_no", "f_u_section_n")
    affinity("colour_group_code", "raw_i_colour_group_code", "f_u_colour_n")

    out["f_match_type"] = (
        X["raw_i_product_type_no"].to_numpy() ==
        X["raw_i_product_type_no"].to_numpy()
    ).astype(float)
    out["f_match_dept"] = (
        X["raw_i_department_no"].to_numpy() ==
        X["raw_i_department_no"].to_numpy()
    ).astype(float)
    out["f_match_section"] = (
        X["raw_i_section_no"].to_numpy() ==
        X["raw_i_section_no"].to_numpy()
    ).astype(float)
    out["f_match_colour"] = (
        X["raw_i_colour_group_code"].to_numpy() ==
        X["raw_i_colour_group_code"].to_numpy()
    ).astype(float)

    return out.reindex(index=X.index)
