import numpy as np
import pandas as pd


def modify_features(X, history):
    names = [
        "f_u_n7", "f_u_n30", "f_i_n7", "f_i_n30",
        "f_pair_n", "f_u_recency", "f_i_recency", "f_pair_recency",
        "f_u_type_aff", "f_u_dept_aff", "f_i_decay", "f_pair_decay",
        "f_price_ratio", "f_u_channel1"
    ]
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def put(name, values, default=0.0):
        if isinstance(values, pd.Series):
            values = values.reindex(X.index)
            if default is not None:
                values = values.fillna(default)
            out[name] = values.to_numpy(dtype=float)
        else:
            out[name] = np.asarray(values, dtype=float)

    def key(a, b):
        return a.astype(str) + "|" + b.astype(str)

    def mapped(series, keys, default=0.0):
        z = keys.map(series)
        if default is not None:
            z = z.fillna(default)
        return z.to_numpy(dtype=float)

    if history is None or history.empty:
        for name in names:
            out[name] = np.zeros(n, dtype=float)
        return out

    h = history
    u = X["customer_id"]
    i = X["article_id"]
    pair_h = key(h["customer_id"], h["article_id"])
    pair_x = key(u, i)

    r7 = h.loc[h["days_ago"] <= 7]
    r30 = h.loc[h["days_ago"] <= 30]
    r90 = h.loc[h["days_ago"] <= 90]

    put("f_u_n7", np.log1p(mapped(r7.groupby("customer_id").size(), u)))
    put("f_u_n30", np.log1p(mapped(r30.groupby("customer_id").size(), u)))
    put("f_i_n7", np.log1p(mapped(r7.groupby("article_id").size(), i)))
    put("f_i_n30", np.log1p(mapped(r30.groupby("article_id").size(), i)))

    put("f_pair_n", np.log1p(mapped(pair_h.value_counts(), pair_x)))
    put("f_u_recency", mapped(h.groupby("customer_id")["days_ago"].min(), u, None))
    put("f_i_recency", mapped(h.groupby("article_id")["days_ago"].min(), i, None))
    put("f_pair_recency", mapped(h.groupby(pair_h)["days_ago"].min(), pair_x, None))

    typ_h = key(r90["customer_id"], r90["product_type_no"])
    typ_x = key(u, X["raw_i_product_type_no"])
    dep_h = key(r90["customer_id"], r90["department_no"])
    dep_x = key(u, X["raw_i_department_no"])
    den = r90.groupby("customer_id").size()
    den_x = mapped(den, u, 0.0)
    put("f_u_type_aff", mapped(typ_h.value_counts(), typ_x) / (den_x + 1.0))
    put("f_u_dept_aff", mapped(dep_h.value_counts(), dep_x) / (den_x + 1.0))

    hh = h.copy()
    hh["_w"] = np.exp(-hh["days_ago"].to_numpy(dtype=float) / 30.0)
    iw = hh.groupby("article_id")["_w"].sum()
    pw = hh.groupby(pair_h)["_w"].sum()
    put("f_i_decay", np.log1p(mapped(iw, i)))
    put("f_pair_decay", np.log1p(mapped(pw, pair_x)))

    ip = mapped(h.groupby("article_id")["price"].mean(), i, None)
    up = mapped(h.groupby("customer_id")["price"].mean(), u, None)
    put("f_price_ratio", np.log((ip + 1e-5) / (up + 1e-5)), None)

    ch = h.assign(_c=(h["sales_channel_id"] == 1).astype(float))
    put("f_u_channel1", mapped(ch.groupby("customer_id")["_c"].mean(), u, None))

    return out.reindex(index=X.index)[names]
