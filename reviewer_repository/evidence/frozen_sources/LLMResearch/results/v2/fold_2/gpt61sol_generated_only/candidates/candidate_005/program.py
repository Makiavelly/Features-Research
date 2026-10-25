def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    h7 = h[h["days_ago"] <= 7]
    h30 = h[h["days_ago"] <= 30]
    h90 = h[h["days_ago"] <= 90]

    def cnt(frame, left, right=None):
        if right is None:
            return X[left].map(frame.groupby(left).size()).fillna(0).to_numpy()
        s = frame.groupby([left, right]).size()
        ix = pd.MultiIndex.from_arrays([X[left].to_numpy(), X[right].to_numpy()])
        return s.reindex(ix).fillna(0).to_numpy()

    def minimum(frame, left, right=None):
        if right is None:
            return X[left].map(frame.groupby(left)["days_ago"].min()).to_numpy()
        s = frame.groupby([left, right])["days_ago"].min()
        ix = pd.MultiIndex.from_arrays([X[left].to_numpy(), X[right].to_numpy()])
        return s.reindex(ix).to_numpy()

    out["f_repeat_count"] = np.log1p(cnt(h, "customer_id", "article_id"))
    out["f_repeat_30"] = np.log1p(cnt(h30, "customer_id", "article_id"))
    out["f_repeat_age"] = minimum(h, "customer_id", "article_id")

    out["f_item_7"] = np.log1p(cnt(h7, "article_id"))
    out["f_item_30"] = np.log1p(cnt(h30, "article_id"))
    out["f_item_90"] = np.log1p(cnt(h90, "article_id"))
    out["f_item_age"] = minimum(h, "article_id")

    out["f_user_7"] = np.log1p(cnt(h7, "customer_id"))
    out["f_user_30"] = np.log1p(cnt(h30, "customer_id"))
    out["f_user_age"] = minimum(h, "customer_id")

    for raw, hist, name in [
        ("raw_i_department_no", "department_no", "dep"),
        ("raw_i_product_type_no", "product_type_no", "type"),
        ("raw_i_colour_group_code", "colour_group_code", "colour"),
        ("raw_i_garment_group_no", "garment_group_no", "garment"),
    ]:
        s7 = h7.groupby(["customer_id", hist]).size()
        s30 = h30.groupby(["customer_id", hist]).size()
        ix = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[raw].to_numpy()]
        )
        out["f_user_" + name + "_7"] = np.log1p(s7.reindex(ix).fillna(0).to_numpy())
        out["f_user_" + name + "_30"] = np.log1p(s30.reindex(ix).fillna(0).to_numpy())

    ip = h30.groupby("article_id")["price"].mean()
    up = h30.groupby("customer_id")["price"].mean()
    item_price = X["article_id"].map(ip)
    user_price = X["customer_id"].map(up)
    out["f_price_gap_30"] = np.abs(item_price - user_price)
    out["f_raw_type"] = X["raw_i_product_type_no"]
    out["f_raw_department"] = X["raw_i_department_no"]
    out["f_raw_section"] = X["raw_i_section_no"]
    return out
