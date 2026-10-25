import numpy as np
import pandas as pd


def modify_features(X, history):
    names = [
        "f_u_n7", "f_u_n30", "f_u_n90",
        "f_i_n7", "f_i_n30", "f_i_n90",
        "f_pair_n", "f_u_recency", "f_i_recency", "f_pair_recency",
        "f_i_decay", "f_pair_decay",
        "f_u_type_aff", "f_u_dept_aff", "f_u_colour_aff",
        "f_u_section_aff", "f_i_product_pop",
        "f_i_product_pop30", "f_price_ratio", "f_u_price",
        "f_i_price", "f_u_channel1", "f_i_channel1",
        "f_u_spend_decay", "f_pair_price"
    ]
    out = pd.DataFrame(index=X.index)
    n = len(X)

    if history is None or history.empty:
        for name in names:
            out[name] = np.zeros(n, dtype=float)
        return out

    h = history
    u = X["customer_id"]
    a = X["article_id"]

    def k(x, y):
        return x.astype(str) + "|" + y.astype(str)

    def vals(s, keys, default=0.0):
        z = keys.map(s)
        if default is not None:
            z = z.fillna(default)
        return z.to_numpy(dtype=float)

    def add(name, x, default=0.0):
        if isinstance(x, pd.Series):
            x = x.reindex(X.index)
            if default is not None:
                x = x.fillna(default)
            x = x.to_numpy(dtype=float)
        else:
            x = np.asarray(x, dtype=float)
        out[name] = x

    ph = k(h["customer_id"], h["article_id"])
    px = k(u, a)

    r7 = h[h["days_ago"] <= 7]
    r30 = h[h["days_ago"] <= 30]
    r90 = h[h["days_ago"] <= 90]

    add("f_u_n7", np.log1p(vals(r7.groupby("customer_id").size(), u)))
    add("f_u_n30", np.log1p(vals(r30.groupby("customer_id").size(), u)))
    add("f_u_n90", np.log1p(vals(r90.groupby("customer_id").size(), u)))
    add("f_i_n7", np.log1p(vals(r7.groupby("article_id").size(), a)))
    add("f_i_n30", np.log1p(vals(r30.groupby("article_id").size(), a)))
    add("f_i_n90", np.log1p(vals(r90.groupby("article_id").size(), a)))
    add("f_pair_n", np.log1p(vals(ph.value_counts(), px)))

    add("f_u_recency", vals(h.groupby("customer_id")["days_ago"].min(), u, None), None)
    add("f_i_recency", vals(h.groupby("article_id")["days_ago"].min(), a, None), None)
    add("f_pair_recency", vals(h.groupby(ph)["days_ago"].min(), px, None), None)

    w = np.exp(-h["days_ago"].to_numpy(dtype=float) / 30.0)
    hw = h.assign(_weight=w, _spend=w * h["price"].to_numpy(dtype=float))
    add("f_i_decay", np.log1p(vals(hw.groupby("article_id")["_weight"].sum(), a)))
    add("f_pair_decay", np.log1p(vals(hw.groupby(ph)["_weight"].sum(), px)))
    add("f_u_spend_decay", np.log1p(vals(hw.groupby("customer_id")["_spend"].sum(), u)))

    total = r90.groupby("customer_id").size()
    den = vals(total, u)
    for name, col, raw in [
        ("f_u_type_aff", "product_type_no", "raw_i_product_type_no"),
        ("f_u_dept_aff", "department_no", "raw_i_department_no"),
        ("f_u_colour_aff", "colour_group_code", "raw_i_colour_group_code"),
        ("f_u_section_aff", "section_no", "raw_i_section_no"),
    ]:
        kh = k(r90["customer_id"], r90[col])
        kx = k(u, X[raw])
        add(name, vals(kh.value_counts(), kx) / (den + 1.0))

    prod = h.groupby("product_code").size()
    prod30 = r30.groupby("product_code").size()
    add("f_i_product_pop", np.log1p(vals(prod, X["raw_i_product_code"])))
    add("f_i_product_pop30", np.log1p(vals(prod30, X["raw_i_product_code"])))

    up = vals(h.groupby("customer_id")["price"].mean(), u, None)
    ip = vals(h.groupby("article_id")["price"].mean(), a, None)
    add("f_u_price", np.log1p(up), None)
    add("f_i_price", np.log1p(ip), None)
    add("f_price_ratio", np.log((ip + 1e-4) / (up + 1e-4)), None)
    add("f_pair_price", vals(h.groupby(ph)["price"].mean(), px, None), None)

    hc = h.assign(_ch=(h["sales_channel_id"] == 1).astype(float))
    add("f_u_channel1", vals(hc.groupby("customer_id")["_ch"].mean(), u, None), None)
    add("f_i_channel1", vals(hc.groupby("article_id")["_ch"].mean(), a, None), None)

    return out.reindex(index=X.index)[names]
