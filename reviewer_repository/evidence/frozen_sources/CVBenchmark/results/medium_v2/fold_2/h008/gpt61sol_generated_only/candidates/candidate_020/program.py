import numpy as np
import pandas as pd


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    u, i = X["customer_id"], X["article_id"]

    def key(a, b):
        return a.astype(str) + "|" + b.astype(str)

    def get(series, keys, default=0.0):
        values = keys.map(series)
        if default is not None:
            values = values.fillna(default)
        return values.to_numpy(dtype=float)

    def put(name, values):
        out[name] = np.asarray(values, dtype=float)

    if history is None or history.empty:
        names = [
            "f_u_n7", "f_u_n30", "f_u_n90", "f_i_n7", "f_i_n30",
            "f_i_n90", "f_pair_n", "f_u_recency", "f_i_recency",
            "f_pair_recency", "f_u_type_aff", "f_u_dept_aff",
            "f_u_garment_aff", "f_u_section_aff", "f_i_decay",
            "f_pair_decay", "f_price_ratio", "f_u_channel1",
            "f_i_product_pop", "f_age"
        ]
        for name in names:
            out[name] = np.nan if name in (
                "f_u_recency", "f_i_recency", "f_pair_recency",
                "f_price_ratio", "f_u_channel1"
            ) else 0.0
        return out

    h = history
    pair_h = key(h["customer_id"], h["article_id"])
    pair_x = key(u, i)

    for days, label in ((7, "7"), (30, "30"), (90, "90")):
        r = h.loc[h["days_ago"] <= days]
        put("f_u_n" + label, np.log1p(get(r.groupby("customer_id").size(), u)))
        if label != "90":
            put("f_i_n" + label, np.log1p(get(r.groupby("article_id").size(), i)))
    r90 = h.loc[h["days_ago"] <= 90]
    put("f_i_n90", np.log1p(get(r90.groupby("article_id").size(), i)))

    put("f_pair_n", np.log1p(get(pair_h.value_counts(), pair_x)))
    put("f_u_recency", get(h.groupby("customer_id")["days_ago"].min(), u, None))
    put("f_i_recency", get(h.groupby("article_id")["days_ago"].min(), i, None))
    put("f_pair_recency", get(h.groupby(pair_h)["days_ago"].min(), pair_x, None))

    den = get(r90.groupby("customer_id").size(), u)
    for col, raw, name in (
        ("product_type_no", "raw_i_product_type_no", "f_u_type_aff"),
        ("department_no", "raw_i_department_no", "f_u_dept_aff"),
        ("garment_group_no", "raw_i_garment_group_no", "f_u_garment_aff"),
        ("section_no", "raw_i_section_no", "f_u_section_aff"),
    ):
        hist_key = key(r90["customer_id"], r90[col])
        cand_key = key(u, X[raw])
        put(name, get(hist_key.value_counts(), cand_key) / (den + 1.0))

    weighted = h.assign(_w=np.exp(-h["days_ago"].to_numpy(dtype=float) / 30.0))
    put("f_i_decay", np.log1p(get(weighted.groupby("article_id")["_w"].sum(), i)))
    put("f_pair_decay", np.log1p(get(weighted.groupby(pair_h)["_w"].sum(), pair_x)))

    ip = get(h.groupby("article_id")["price"].mean(), i, None)
    up = get(h.groupby("customer_id")["price"].mean(), u, None)
    put("f_price_ratio", np.log((ip + 1e-5) / (up + 1e-5)))
    put("f_u_channel1", get(
        h.assign(_c=(h["sales_channel_id"] == 1).astype(float))
         .groupby("customer_id")["_c"].mean(), u, None
    ))
    put("f_i_product_pop", np.log1p(get(h.groupby("product_code").size(),
                                         X["raw_i_product_code"])))
    put("f_age", X["raw_u_age"].to_numpy(dtype=float))
    return out.reindex(index=X.index)
