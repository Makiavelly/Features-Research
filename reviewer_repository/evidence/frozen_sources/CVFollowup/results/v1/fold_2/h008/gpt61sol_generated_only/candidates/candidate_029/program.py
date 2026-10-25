import numpy as np
import pandas as pd


def modify_features(X, history):
    names = [
        "f_u_n7", "f_u_n30", "f_u_n90",
        "f_i_n7", "f_i_n30", "f_i_n90",
        "f_pair_n", "f_pair_n30",
        "f_u_recency", "f_i_recency", "f_pair_recency",
        "f_u_type_aff", "f_u_dept_aff", "f_u_colour_aff",
        "f_i_decay", "f_pair_decay",
        "f_price_ratio", "f_u_channel1", "f_i_price"
    ]
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def key(a, b):
        return a.astype(str) + "|" + b.astype(str)

    def vals(s, k, default=0.0):
        z = k.map(s)
        if default is not None:
            z = z.fillna(default)
        return z.to_numpy(dtype=float)

    if history is None or history.empty:
        for name in names:
            out[name] = np.zeros(n, dtype=float)
        return out[names]

    h = history
    u = X["customer_id"]
    i = X["article_id"]
    pair_h = key(h["customer_id"], h["article_id"])
    pair_x = key(u, i)

    r7 = h.loc[h["days_ago"] <= 7]
    r30 = h.loc[h["days_ago"] <= 30]
    r90 = h.loc[h["days_ago"] <= 90]

    out["f_u_n7"] = np.log1p(vals(r7.groupby("customer_id").size(), u))
    out["f_u_n30"] = np.log1p(vals(r30.groupby("customer_id").size(), u))
    out["f_u_n90"] = np.log1p(vals(r90.groupby("customer_id").size(), u))
    out["f_i_n7"] = np.log1p(vals(r7.groupby("article_id").size(), i))
    out["f_i_n30"] = np.log1p(vals(r30.groupby("article_id").size(), i))
    out["f_i_n90"] = np.log1p(vals(r90.groupby("article_id").size(), i))

    out["f_pair_n"] = np.log1p(vals(pair_h.value_counts(), pair_x))
    pair30 = key(r30["customer_id"], r30["article_id"])
    out["f_pair_n30"] = np.log1p(vals(pair30.value_counts(), pair_x))

    out["f_u_recency"] = vals(
        h.groupby("customer_id")["days_ago"].min(), u, None
    )
    out["f_i_recency"] = vals(
        h.groupby("article_id")["days_ago"].min(), i, None
    )
    out["f_pair_recency"] = vals(
        h.groupby(pair_h)["days_ago"].min(), pair_x, None
    )

    den = r90.groupby("customer_id").size()
    dx = vals(den, u)
    typ_h = key(r90["customer_id"], r90["product_type_no"])
    typ_x = key(u, X["raw_i_product_type_no"])
    dep_h = key(r90["customer_id"], r90["department_no"])
    dep_x = key(u, X["raw_i_department_no"])
    col_h = key(r90["customer_id"], r90["colour_group_code"])
    col_x = key(u, X["raw_i_colour_group_code"])

    out["f_u_type_aff"] = vals(typ_h.value_counts(), typ_x) / (dx + 1.0)
    out["f_u_dept_aff"] = vals(dep_h.value_counts(), dep_x) / (dx + 1.0)
    out["f_u_colour_aff"] = vals(col_h.value_counts(), col_x) / (dx + 1.0)

    w = np.exp(-h["days_ago"].to_numpy(dtype=float) / 30.0)
    hw = h.assign(_w=w)
    out["f_i_decay"] = np.log1p(
        vals(hw.groupby("article_id")["_w"].sum(), i)
    )
    out["f_pair_decay"] = np.log1p(
        vals(hw.groupby(pair_h)["_w"].sum(), pair_x)
    )

    ip = vals(h.groupby("article_id")["price"].mean(), i, None)
    up = vals(h.groupby("customer_id")["price"].mean(), u, None)
    out["f_price_ratio"] = np.log((ip + 1e-5) / (up + 1e-5))
    out["f_i_price"] = ip

    ch = h.assign(_c=(h["sales_channel_id"] == 1).astype(float))
    out["f_u_channel1"] = vals(
        ch.groupby("customer_id")["_c"].mean(), u, None
    )

    return out.reindex(index=X.index)[names]
