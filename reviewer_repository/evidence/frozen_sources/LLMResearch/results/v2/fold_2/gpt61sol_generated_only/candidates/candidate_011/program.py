def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    h7 = h[h["days_ago"] <= 7]
    h30 = h[h["days_ago"] <= 30]
    h90 = h[h["days_ago"] <= 90]

    def c1(frame, hc, xc):
        return X[xc].map(frame.groupby(hc).size()).fillna(0).to_numpy()

    def m1(frame, hc, xc):
        return X[xc].map(frame.groupby(hc)["days_ago"].min()).to_numpy()

    def c2(frame, hc, xc):
        z = frame.groupby(["customer_id", hc]).size()
        ix = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[xc].to_numpy()]
        )
        return z.reindex(ix).fillna(0).to_numpy()

    ix = pd.MultiIndex.from_arrays(
        [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
    )
    p = h.groupby(["customer_id", "article_id"])
    out["f_repeat_n"] = np.log1p(p.size().reindex(ix).fillna(0).to_numpy())
    out["f_repeat_recency"] = p["days_ago"].min().reindex(ix).to_numpy()
    out["f_repeat_30"] = np.log1p(
        h30.groupby(["customer_id", "article_id"]).size().reindex(ix).fillna(0).to_numpy()
    )

    out["f_item_7"] = np.log1p(c1(h7, "article_id", "article_id"))
    out["f_item_30"] = np.log1p(c1(h30, "article_id", "article_id"))
    out["f_item_90"] = np.log1p(c1(h90, "article_id", "article_id"))
    out["f_item_recency"] = m1(h, "article_id", "article_id")
    out["f_user_7"] = np.log1p(c1(h7, "customer_id", "customer_id"))
    out["f_user_30"] = np.log1p(c1(h30, "customer_id", "customer_id"))
    out["f_user_recency"] = m1(h, "customer_id", "customer_id")

    out["f_dep_7"] = np.log1p(c2(h7, "department_no", "raw_i_department_no"))
    out["f_dep_30"] = np.log1p(c2(h30, "department_no", "raw_i_department_no"))
    out["f_type_30"] = np.log1p(c2(h30, "product_type_no", "raw_i_product_type_no"))
    return out
