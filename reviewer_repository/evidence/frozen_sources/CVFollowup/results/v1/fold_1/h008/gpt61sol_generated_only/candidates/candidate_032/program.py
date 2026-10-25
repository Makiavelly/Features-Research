def modify_features(X, history):
    import pandas as pd
    import numpy as np

    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_count_all", "f_user_count_7d", "f_user_count_30d",
        "f_user_count_all", "f_pair_count_7d", "f_pair_count_30d",
        "f_pair_count_all", "f_pair_recency", "f_item_mean_price",
        "f_user_mean_price", "f_user_type_count", "f_user_department_count",
        "f_user_section_count", "f_user_garment_count", "f_user_colour_count",
        "f_user_type_count_30d", "f_user_department_count_30d",
        "f_user_section_count_30d", "f_user_garment_count_30d",
        "f_user_colour_count_30d", "f_type_count_7d", "f_department_count_7d",
        "f_static_age", "f_static_product_code", "f_static_product_type",
        "f_static_department", "f_static_section", "f_static_garment",
    ]
    out = pd.DataFrame(index=X.index)
    for n in names:
        out[n] = 0.0

    static = (
        ("f_static_age", "raw_u_age"),
        ("f_static_product_code", "raw_i_product_code"),
        ("f_static_product_type", "raw_i_product_type_no"),
        ("f_static_department", "raw_i_department_no"),
        ("f_static_section", "raw_i_section_no"),
        ("f_static_garment", "raw_i_garment_group_no"),
    )
    for n, c in static:
        out[n] = pd.to_numeric(X[c], errors="coerce").to_numpy()

    if history is None or len(history) == 0:
        return out[names]

    h = history
    d = pd.to_numeric(h["days_ago"], errors="coerce")
    cid = X["customer_id"].to_numpy()
    aid = X["article_id"].to_numpy()
    keys = pd.MultiIndex.from_arrays([cid, aid])

    def mapped(series, default=0.0):
        return series.reindex(keys).fillna(default).to_numpy()

    for w in (7, 30, 90):
        s = h.loc[d <= w].groupby("article_id").size()
        out["f_item_count_%dd" % w] = X["article_id"].map(s).fillna(0).to_numpy()
    out["f_item_count_all"] = X["article_id"].map(h.groupby("article_id").size()).fillna(0).to_numpy()

    for w, label in ((7, "7d"), (30, "30d")):
        s = h.loc[d <= w].groupby("customer_id").size()
        out["f_user_count_" + label] = X["customer_id"].map(s).fillna(0).to_numpy()
    out["f_user_count_all"] = X["customer_id"].map(h.groupby("customer_id").size()).fillna(0).to_numpy()

    for w, label in ((7, "7d"), (30, "30d")):
        s = h.loc[d <= w].groupby(["customer_id", "article_id"]).size()
        out["f_pair_count_" + label] = mapped(s)
    s = h.groupby(["customer_id", "article_id"]).size()
    out["f_pair_count_all"] = mapped(s)
    out["f_pair_recency"] = mapped(
        h.groupby(["customer_id", "article_id"])["days_ago"].min(),
        np.nan
    )

    out["f_item_mean_price"] = X["article_id"].map(
        h.groupby("article_id")["price"].mean()
    ).to_numpy()
    out["f_user_mean_price"] = X["customer_id"].map(
        h.groupby("customer_id")["price"].mean()
    ).to_numpy()

    categories = (
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
        ("section_no", "raw_i_section_no", "section"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
        ("colour_group_code", "raw_i_colour_group_code", "colour"),
    )
    for hc, xc, label in categories:
        ck = pd.MultiIndex.from_arrays([cid, X[xc].to_numpy()])
        s = h.groupby(["customer_id", hc]).size()
        out["f_user_" + label + "_count"] = s.reindex(ck).fillna(0).to_numpy()

        if label in ("type", "department", "section", "garment", "colour"):
            s30 = h.loc[d <= 30].groupby(["customer_id", hc]).size()
            out["f_user_" + label + "_count_30d"] = s30.reindex(ck).fillna(0).to_numpy()

    for hc, xc, label in (
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
    ):
        s = h.loc[d <= 7].groupby(hc).size()
        out["f_" + label + "_count_7d"] = X[xc].map(s).fillna(0).to_numpy()

    return out[names]
