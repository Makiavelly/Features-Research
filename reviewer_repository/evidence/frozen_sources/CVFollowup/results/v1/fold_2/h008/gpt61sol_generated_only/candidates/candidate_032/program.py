import numpy as np
import pandas as pd


def modify_features(X, history):
    names = [
        "f_u_n7", "f_u_n30", "f_u_n90",
        "f_i_n7", "f_i_n30", "f_i_n90",
        "f_pair_n7", "f_pair_n30", "f_pair_n",
        "f_u_recency", "f_i_recency", "f_pair_recency",
        "f_u_type_aff", "f_u_dept_aff", "f_u_section_aff",
        "f_u_garment_aff", "f_i_decay", "f_pair_decay",
        "f_price_ratio", "f_u_channel1",
        "f_u_age", "f_i_product_code", "f_i_product_type",
        "f_i_colour_group", "f_i_department", "f_i_section",
        "f_i_garment_group"
    ]
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def key(a, b):
        return a.astype(str) + "|" + b.astype(str)

    def mapped(s, k, default=0.0):
        z = k.map(s)
        if default is not None:
            z = z.fillna(default)
        return z.to_numpy(dtype=float)

    def put(name, value):
        if isinstance(value, pd.Series):
            value = value.reindex(X.index).to_numpy(dtype=float)
        else:
            value = np.asarray(value, dtype=float)
        out[name] = value

    put("f_u_age", X["raw_u_age"])
    put("f_i_product_code", X["raw_i_product_code"])
    put("f_i_product_type", X["raw_i_product_type_no"])
    put("f_i_colour_group", X["raw_i_colour_group_code"])
    put("f_i_department", X["raw_i_department_no"])
    put("f_i_section", X["raw_i_section_no"])
    put("f_i_garment_group", X["raw_i_garment_group_no"])

    if history is None or history.empty:
        for name in names[:20]:
            out[name] = np.zeros(n, dtype=float)
        return out[names]

    h = history
    u = X["customer_id"]
    i = X["article_id"]
    ph = key(h["customer_id"], h["article_id"])
    px = key(u, i)

    r7 = h.loc[h["days_ago"] <= 7]
    r30 = h.loc[h["days_ago"] <= 30]
    r90 = h.loc[h["days_ago"] <= 90]

    for name, frame, col in [
        ("f_u_n7", r7, "customer_id"),
        ("f_u_n30", r30, "customer_id"),
        ("f_u_n90", r90, "customer_id")
    ]:
        put(name, np.log1p(mapped(frame.groupby(col).size(), u)))

    for name, frame, col in [
        ("f_i_n7", r7, "article_id"),
        ("f_i_n30", r30, "article_id"),
        ("f_i_n90", r90, "article_id")
    ]:
        put(name, np.log1p(mapped(frame.groupby(col).size(), i)))

    for name, frame in [
        ("f_pair_n7", r7), ("f_pair_n30", r30)
    ]:
        k = key(frame["customer_id"], frame["article_id"])
        put(name, np.log1p(mapped(k.value_counts(), px)))
    put("f_pair_n", np.log1p(mapped(ph.value_counts(), px)))

    put("f_u_recency", mapped(h.groupby("customer_id")["days_ago"].min(), u, None))
    put("f_i_recency", mapped(h.groupby("article_id")["days_ago"].min(), i, None))
    put("f_pair_recency", mapped(h.groupby(ph)["days_ago"].min(), px, None))

    den = r90.groupby("customer_id").size()
    dx = mapped(den, u)
    for name, col, raw in [
        ("f_u_type_aff", "product_type_no", "raw_i_product_type_no"),
        ("f_u_dept_aff", "department_no", "raw_i_department_no"),
        ("f_u_section_aff", "section_no", "raw_i_section_no"),
        ("f_u_garment_aff", "garment_group_no", "raw_i_garment_group_no")
    ]:
        kh = key(r90["customer_id"], r90[col])
        kx = key(u, X[raw])
        put(name, mapped(kh.value_counts(), kx) / (dx + 1.0))

    w = np.exp(-h["days_ago"].to_numpy(dtype=float) / 30.0)
    iw = h.assign(_w=w).groupby("article_id")["_w"].sum()
    pw = h.assign(_w=w).groupby(ph)["_w"].sum()
    put("f_i_decay", np.log1p(mapped(iw, i)))
    put("f_pair_decay", np.log1p(mapped(pw, px)))

    ip = mapped(h.groupby("article_id")["price"].mean(), i, None)
    up = mapped(h.groupby("customer_id")["price"].mean(), u, None)
    put("f_price_ratio", np.log((ip + 1e-5) / (up + 1e-5)))

    channel = h.assign(_c=(h["sales_channel_id"] == 1).astype(float))
    put("f_u_channel1",
        mapped(channel.groupby("customer_id")["_c"].mean(), u, None))

    return out[names]
