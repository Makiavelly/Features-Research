import numpy as np
import pandas as pd


def modify_features(X, history):
    names = [
        "f_u_n7", "f_u_n30", "f_u_n90",
        "f_i_n7", "f_i_n30", "f_i_n90",
        "f_pair_n", "f_u_recency", "f_i_recency", "f_pair_recency",
        "f_u_type_aff", "f_u_dept_aff", "f_u_colour_aff",
        "f_i_decay", "f_pair_decay", "f_price_ratio",
        "f_u_channel1"
    ]
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def key(a, b):
        return a.astype(str) + "|" + b.astype(str)

    def values(series, keys, default=0.0):
        z = keys.map(series)
        if default is not None:
            z = z.fillna(default)
        return z.to_numpy(dtype=float)

    def put(name, value):
        if isinstance(value, pd.Series):
            value = value.to_numpy(dtype=float)
        out[name] = np.asarray(value, dtype=float)

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

    put("f_u_n7", np.log1p(values(r7.groupby("customer_id").size(), u)))
    put("f_u_n30", np.log1p(values(r30.groupby("customer_id").size(), u)))
    put("f_u_n90", np.log1p(values(r90.groupby("customer_id").size(), u)))
    put("f_i_n7", np.log1p(values(r7.groupby("article_id").size(), i)))
    put("f_i_n30", np.log1p(values(r30.groupby("article_id").size(), i)))
    put("f_i_n90", np.log1p(values(r90.groupby("article_id").size(), i)))
    put("f_pair_n", np.log1p(values(pair_h.value_counts(), pair_x)))

    put("f_u_recency", values(
        h.groupby("customer_id")["days_ago"].min(), u, None))
    put("f_i_recency", values(
        h.groupby("article_id")["days_ago"].min(), i, None))
    put("f_pair_recency", values(
        h.groupby(pair_h)["days_ago"].min(), pair_x, None))

    den = r90.groupby("customer_id").size()
    den_x = values(den, u)
    type_h = key(r90["customer_id"], r90["product_type_no"])
    type_x = key(u, X["raw_i_product_type_no"])
    dept_h = key(r90["customer_id"], r90["department_no"])
    dept_x = key(u, X["raw_i_department_no"])
    colour_h = key(r90["customer_id"], r90["colour_group_code"])
    colour_x = key(u, X["raw_i_colour_group_code"])

    put("f_u_type_aff",
        values(type_h.value_counts(), type_x) / (den_x + 1.0))
    put("f_u_dept_aff",
        values(dept_h.value_counts(), dept_x) / (den_x + 1.0))
    put("f_u_colour_aff",
        values(colour_h.value_counts(), colour_x) / (den_x + 1.0))

    w = np.exp(-h["days_ago"].to_numpy(dtype=float) / 30.0)
    iw = h.assign(_w=w).groupby("article_id")["_w"].sum()
    pw = h.assign(_w=w).groupby(pair_h)["_w"].sum()
    put("f_i_decay", np.log1p(values(iw, i)))
    put("f_pair_decay", np.log1p(values(pw, pair_x)))

    item_price = values(h.groupby("article_id")["price"].mean(), i, None)
    user_price = values(h.groupby("customer_id")["price"].mean(), u, None)
    put("f_price_ratio", np.log(
        (item_price + 1e-5) / (user_price + 1e-5)))

    channel = h.assign(_c=(h["sales_channel_id"] == 1).astype(float))
    put("f_u_channel1", values(
        channel.groupby("customer_id")["_c"].mean(), u, None))

    return out.reindex(index=X.index)[names]
