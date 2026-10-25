def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    h7 = h[h["days_ago"] <= 7]
    h30 = h[h["days_ago"] <= 30]
    h90 = h[h["days_ago"] <= 90]

    def count1(frame, col, xcol):
        return X[xcol].map(frame.groupby(col).size()).fillna(0).to_numpy()

    def min1(frame, col, xcol):
        return X[xcol].map(frame.groupby(col)["days_ago"].min()).to_numpy()

    def count2(frame, hcol, xcol):
        s = frame.groupby(["customer_id", hcol]).size()
        ix = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[xcol].to_numpy()]
        )
        return s.reindex(ix).fillna(0).to_numpy()

    pair = h.groupby(["customer_id", "article_id"])
    pix = pd.MultiIndex.from_arrays(
        [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
    )
    out["f_repeat_n"] = np.log1p(pair.size().reindex(pix).fillna(0).to_numpy())
    out["f_repeat_recency"] = pair["days_ago"].min().reindex(pix).to_numpy()

    pair7 = h7.groupby(["customer_id", "article_id"]).size()
    pair30 = h30.groupby(["customer_id", "article_id"]).size()
    out["f_repeat_7"] = np.log1p(pair7.reindex(pix).fillna(0).to_numpy())
    out["f_repeat_30"] = np.log1p(pair30.reindex(pix).fillna(0).to_numpy())

    out["f_item_n7"] = np.log1p(count1(h7, "article_id", "article_id"))
    out["f_item_n30"] = np.log1p(count1(h30, "article_id", "article_id"))
    out["f_item_n90"] = np.log1p(count1(h90, "article_id", "article_id"))
    out["f_item_recency"] = min1(h, "article_id", "article_id")

    out["f_user_n7"] = np.log1p(count1(h7, "customer_id", "customer_id"))
    out["f_user_n30"] = np.log1p(count1(h30, "customer_id", "customer_id"))
    out["f_user_recency"] = min1(h, "customer_id", "customer_id")

    out["f_dep_7"] = np.log1p(
        count2(h7, "department_no", "raw_i_department_no")
    )
    out["f_dep_30"] = np.log1p(
        count2(h30, "department_no", "raw_i_department_no")
    )
    out["f_type_30"] = np.log1p(
        count2(h30, "product_type_no", "raw_i_product_type_no")
    )
    out["f_section_30"] = np.log1p(
        count2(h30, "section_no", "raw_i_section_no")
    )
    return out
