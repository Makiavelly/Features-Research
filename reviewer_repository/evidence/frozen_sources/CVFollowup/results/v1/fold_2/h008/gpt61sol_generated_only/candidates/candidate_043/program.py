import numpy as np
import pandas as pd

def modify_features(X, history):
    names = [
        "f_u_n7", "f_u_n30", "f_i_n7", "f_i_n30",
        "f_pair_n90", "f_u_recency", "f_i_recency", "f_pair_recency",
        "f_u_type_aff", "f_u_dept_aff", "f_u_colour_aff",
        "f_i_decay", "f_pair_decay", "f_price_ratio",
        "f_u_channel1", "f_u_age", "f_i_type", "f_i_dept",
        "f_i_colour", "f_i_section"
    ]
    out = pd.DataFrame(index=X.index)
    n = len(X)

    if history is None or history.empty:
        for z in names:
            out[z] = np.zeros(n, dtype=float)
        out["f_u_recency"] = -1.0
        out["f_i_recency"] = -1.0
        out["f_pair_recency"] = -1.0
        return out[names]

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

    ph = k(h["customer_id"], h["article_id"])
    px = k(u, a)

    r7 = h[h["days_ago"] <= 7]
    r30 = h[h["days_ago"] <= 30]
    r90 = h[h["days_ago"] <= 90]

    out["f_u_n7"] = np.log1p(vals(r7.groupby("customer_id").size(), u))
    out["f_u_n30"] = np.log1p(vals(r30.groupby("customer_id").size(), u))
    out["f_i_n7"] = np.log1p(vals(r7.groupby("article_id").size(), a))
    out["f_i_n30"] = np.log1p(vals(r30.groupby("article_id").size(), a))
    out["f_pair_n90"] = np.log1p(vals(
        r90.assign(_p=k(r90["customer_id"], r90["article_id"]))
           .groupby("_p").size(), px))

    out["f_u_recency"] = vals(h.groupby("customer_id")["days_ago"].min(), u, -1.0)
    out["f_i_recency"] = vals(h.groupby("article_id")["days_ago"].min(), a, -1.0)
    out["f_pair_recency"] = vals(h.groupby(ph)["days_ago"].min(), px, -1.0)

    den = r90.groupby("customer_id").size()
    dx = vals(den, u)
    for col, raw, name in [
        ("product_type_no", "raw_i_product_type_no", "f_u_type_aff"),
        ("department_no", "raw_i_department_no", "f_u_dept_aff"),
        ("colour_group_code", "raw_i_colour_group_code", "f_u_colour_aff")
    ]:
        kh = k(r90["customer_id"], r90[col])
        kx = k(u, X[raw])
        out[name] = vals(kh.value_counts(), kx) / (dx + 1.0)

    w = np.exp(-h["days_ago"].to_numpy(dtype=float) / 30.0)
    hw = h.assign(_w=w)
    out["f_i_decay"] = np.log1p(vals(hw.groupby("article_id")["_w"].sum(), a))
    out["f_pair_decay"] = np.log1p(vals(hw.groupby(ph)["_w"].sum(), px))

    ip = vals(h.groupby("article_id")["price"].mean(), a, np.nan)
    up = vals(h.groupby("customer_id")["price"].mean(), u, np.nan)
    out["f_price_ratio"] = np.log((ip + 1e-5) / (up + 1e-5))

    ch = h.assign(_c=(h["sales_channel_id"] == 1).astype(float))
    out["f_u_channel1"] = vals(
        ch.groupby("customer_id")["_c"].mean(), u, np.nan)

    out["f_u_age"] = X["raw_u_age"].to_numpy(dtype=float)
    out["f_i_type"] = X["raw_i_product_type_no"].to_numpy(dtype=float)
    out["f_i_dept"] = X["raw_i_department_no"].to_numpy(dtype=float)
    out["f_i_colour"] = X["raw_i_colour_group_code"].to_numpy(dtype=float)
    out["f_i_section"] = X["raw_i_section_no"].to_numpy(dtype=float)

    return out.reindex(index=X.index)[names]
