import numpy as np
import pandas as pd


def modify_features(X, history):
    names = [
        "f_u_age", "f_u_active", "f_u_club", "f_u_news", "f_u_fn",
        "f_i_type", "f_i_dept", "f_i_colour", "f_i_section",
        "f_u_n7", "f_u_n30", "f_u_n90", "f_i_n7", "f_i_n30",
        "f_pair_n", "f_u_recency", "f_i_recency", "f_pair_recency",
        "f_u_type_aff", "f_u_dept_aff", "f_u_colour_aff",
        "f_i_decay", "f_pair_decay", "f_price_ratio", "f_u_channel1"
    ]
    out = pd.DataFrame(index=X.index)

    def put(name, value, default=np.nan):
        if isinstance(value, pd.Series):
            value = value.reindex(X.index)
            if default is not None:
                value = value.fillna(default)
            out[name] = value.to_numpy(dtype=float)
        else:
            a = np.asarray(value, dtype=float)
            if default is not None:
                a = np.where(np.isfinite(a), a, default)
            out[name] = a

    def key(a, b):
        return a.astype(str) + "|" + b.astype(str)

    def mapped(values, keys, default=0.0):
        z = keys.map(values)
        if default is not None:
            z = z.fillna(default)
        return z.to_numpy(dtype=float)

    put("f_u_age", X["raw_u_age"])
    put("f_u_active", X["raw_u_active"])
    put("f_u_club", X["raw_u_club_member_status"])
    put("f_u_news", X["raw_u_fashion_news_frequency"])
    put("f_u_fn", X["raw_u_fn"])
    put("f_i_type", X["raw_i_product_type_no"])
    put("f_i_dept", X["raw_i_department_no"])
    put("f_i_colour", X["raw_i_colour_group_code"])
    put("f_i_section", X["raw_i_section_no"])

    dynamic = names[9:]
    if history is None or len(history) == 0:
        for name in dynamic:
            out[name] = 0.0
        return out[names]

    h = history
    u = X["customer_id"]
    i = X["article_id"]
    ph = key(h["customer_id"], h["article_id"])
    px = key(u, i)

    r7 = h.loc[h["days_ago"] <= 7]
    r30 = h.loc[h["days_ago"] <= 30]
    r90 = h.loc[h["days_ago"] <= 90]

    put("f_u_n7", np.log1p(mapped(r7.groupby("customer_id").size(), u)))
    put("f_u_n30", np.log1p(mapped(r30.groupby("customer_id").size(), u)))
    put("f_u_n90", np.log1p(mapped(r90.groupby("customer_id").size(), u)))
    put("f_i_n7", np.log1p(mapped(r7.groupby("article_id").size(), i)))
    put("f_i_n30", np.log1p(mapped(r30.groupby("article_id").size(), i)))
    put("f_pair_n", np.log1p(mapped(ph.value_counts(), px)))

    put("f_u_recency", mapped(h.groupby("customer_id")["days_ago"].min(), u, None))
    put("f_i_recency", mapped(h.groupby("article_id")["days_ago"].min(), i, None))
    put("f_pair_recency", mapped(h.groupby(ph)["days_ago"].min(), px, None))

    den = r90.groupby("customer_id").size()
    denx = mapped(den, u)
    for name, col, raw in [
        ("f_u_type_aff", "product_type_no", "raw_i_product_type_no"),
        ("f_u_dept_aff", "department_no", "raw_i_department_no"),
        ("f_u_colour_aff", "colour_group_code", "raw_i_colour_group_code"),
    ]:
        hk = key(r90["customer_id"], r90[col])
        xk = key(u, X[raw])
        val = mapped(hk.value_counts(), xk)
        put(name, val / (denx + 1.0))

    w = np.exp(-h["days_ago"].to_numpy(dtype=float) / 30.0)
    iw = h.assign(_w=w).groupby("article_id")["_w"].sum()
    pw = h.assign(_w=w).groupby(ph)["_w"].sum()
    put("f_i_decay", np.log1p(mapped(iw, i)))
    put("f_pair_decay", np.log1p(mapped(pw, px)))

    ip = mapped(h.groupby("article_id")["price"].mean(), i, None)
    up = mapped(h.groupby("customer_id")["price"].mean(), u, None)
    put("f_price_ratio", np.log((ip + 1e-5) / (up + 1e-5)), None)

    ch = h.assign(_c=(h["sales_channel_id"] == 1).astype(float))
    put("f_u_channel1", mapped(ch.groupby("customer_id")["_c"].mean(), u, None))

    return out[names].reindex(index=X.index)
