def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def mapped(series, keys, fill=None):
        if len(series) == 0:
            return np.full(n, np.nan if fill is None else fill, dtype=float)
        if isinstance(keys, str):
            return X["article_id" if keys == "article_id" else "customer_id"].map(series).to_numpy()
        idx = pd.MultiIndex.from_frame(X[list(keys)])
        values = series.reindex(idx).to_numpy(dtype=float)
        if fill is not None:
            values = np.where(np.isnan(values), fill, values)
        return values

    def grouped(keys, column=None, agg="size", mask=None):
        z = h if mask is None else h.loc[mask]
        if z.empty:
            return pd.Series(dtype=float)
        if agg == "min":
            return z.groupby(keys, sort=False)["days_ago"].min()
        if column is None:
            return z.groupby(keys, sort=False).size()
        return z.groupby(keys, sort=False)[column].size()

    out["f_user_item_count"] = mapped(grouped(["customer_id", "article_id"]), ["customer_id", "article_id"], 0)
    out["f_user_item_recency"] = mapped(
        h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
        if not h.empty else pd.Series(dtype=float),
        ["customer_id", "article_id"]
    )
    for days in (7, 30):
        out["f_item_pop_%dd" % days] = mapped(
            grouped("article_id", mask=h["days_ago"] <= days), "article_id", 0
        )
    for days in (30, 90):
        out["f_user_activity_%dd" % days] = mapped(
            grouped("customer_id", mask=h["days_ago"] <= days), "customer_id", 0
        )
    if not h.empty:
        out["f_item_recency"] = mapped(h.groupby("article_id", sort=False)["days_ago"].min(), "article_id")
    else:
        out["f_item_recency"] = np.full(n, np.nan)

    for col, raw in (
        ("department_no", "raw_i_department_no"),
        ("product_type_no", "raw_i_product_type_no"),
        ("colour_group_code", "raw_i_colour_group_code"),
    ):
        keys = ["customer_id", col]
        counts = grouped(keys)
        cand = X[["customer_id"]].copy()
        cand[col] = X[raw].to_numpy()
        idx = pd.MultiIndex.from_frame(cand[keys])
        vals = counts.reindex(idx).to_numpy(dtype=float) if len(counts) else np.full(n, np.nan)
        out["f_user_%s_count" % col.replace("_no", "").replace("_code", "")] = np.nan_to_num(vals, nan=0.0)

    keys = ["customer_id", "department_no"]
    recent = h.loc[h["days_ago"] <= 30]
    counts = grouped(keys, mask=h["days_ago"] <= 30)
    cand = X[["customer_id"]].copy()
    cand["department_no"] = X["raw_i_department_no"].to_numpy()
    vals = counts.reindex(pd.MultiIndex.from_frame(cand[keys])).to_numpy(dtype=float) if len(counts) else np.zeros(n)
    out["f_user_department_30d"] = np.nan_to_num(vals, nan=0.0)
    return out.replace([np.inf, -np.inf], np.nan)
