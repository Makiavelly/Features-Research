def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    h7 = h[h["days_ago"] <= 7]
    h30 = h[h["days_ago"] <= 30]
    h90 = h[h["days_ago"] <= 90]

    def aligned_count(frame, keys):
        s = frame.groupby(keys).size()
        if len(keys) == 1:
            return X[keys[0]].map(s).fillna(0).to_numpy()
        ix = pd.MultiIndex.from_arrays([X[k].to_numpy() for k in keys])
        return s.reindex(ix).fillna(0).to_numpy()

    def aligned_min(frame, keys):
        s = frame.groupby(keys)["days_ago"].min()
        if len(keys) == 1:
            return X[keys[0]].map(s).to_numpy()
        ix = pd.MultiIndex.from_arrays([X[k].to_numpy() for k in keys])
        return s.reindex(ix).to_numpy()

    out["f_repeat_n"] = np.log1p(aligned_count(h, ["customer_id", "article_id"]))
    out["f_repeat_n_30"] = np.log1p(aligned_count(h30, ["customer_id", "article_id"]))
    out["f_repeat_recency"] = aligned_min(h, ["customer_id", "article_id"])

    out["f_item_n_7"] = np.log1p(aligned_count(h7, ["article_id"]))
    out["f_item_n_30"] = np.log1p(aligned_count(h30, ["article_id"]))
    out["f_item_n_90"] = np.log1p(aligned_count(h90, ["article_id"]))
    out["f_item_recency"] = aligned_min(h, ["article_id"])

    out["f_user_n_7"] = np.log1p(aligned_count(h7, ["customer_id"]))
    out["f_user_n_30"] = np.log1p(aligned_count(h30, ["customer_id"]))
    out["f_user_recency"] = aligned_min(h, ["customer_id"])

    dep7 = h7.groupby(["customer_id", "department_no"]).size()
    dep30 = h30.groupby(["customer_id", "department_no"]).size()
    dix = pd.MultiIndex.from_arrays(
        [X["customer_id"].to_numpy(), X["raw_i_department_no"].to_numpy()]
    )
    out["f_user_dep_7"] = np.log1p(dep7.reindex(dix).fillna(0).to_numpy())
    out["f_user_dep_30"] = np.log1p(dep30.reindex(dix).fillna(0).to_numpy())

    typ30 = h30.groupby(["customer_id", "product_type_no"]).size()
    tix = pd.MultiIndex.from_arrays(
        [X["customer_id"].to_numpy(), X["raw_i_product_type_no"].to_numpy()]
    )
    out["f_user_type_30"] = np.log1p(typ30.reindex(tix).fillna(0).to_numpy())

    return out
