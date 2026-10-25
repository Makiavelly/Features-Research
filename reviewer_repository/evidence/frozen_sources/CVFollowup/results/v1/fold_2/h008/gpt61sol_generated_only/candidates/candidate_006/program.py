import numpy as np
import pandas as pd


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def vals(mapping, keys, default=0.0):
        return keys.map(mapping).fillna(default).to_numpy(dtype=float)

    def pair_key(a, b):
        return a.astype(str) + "|" + b.astype(str)

    if history is None or len(history) == 0:
        for name in (
            "f_u_n7", "f_u_n30", "f_u_n90", "f_i_n7", "f_i_n30",
            "f_i_n90", "f_pair_n", "f_u_recency", "f_i_recency",
            "f_pair_recency", "f_i_price", "f_u_type_n", "f_u_dept_n",
            "f_u_colour_n", "f_u_product_n", "f_u_avg_price",
            "f_price_ratio", "f_u_age"
        ):
            out[name] = np.zeros(n, dtype=float)
        return out

    h = history
    u, i = X["customer_id"], X["article_id"]
    hu, hi = h["customer_id"], h["article_id"]
    days = h["days_ago"]

    for window, label in ((7, "7"), (30, "30"), (90, "90")):
        recent = h.loc[days <= window]
        uc = recent.groupby("customer_id", sort=False).size()
        ic = recent.groupby("article_id", sort=False).size()
        out["f_u_n" + label] = np.log1p(vals(uc, u))
        out["f_i_n" + label] = np.log1p(vals(ic, i))

    hp = pair_key(hu, hi)
    xp = pair_key(u, i)
    pc = hp.value_counts()
    out["f_pair_n"] = np.log1p(vals(pc, xp))

    out["f_u_recency"] = vals(h.groupby("customer_id", sort=False)["days_ago"].min(), u, np.nan)
    out["f_i_recency"] = vals(h.groupby("article_id", sort=False)["days_ago"].min(), i, np.nan)
    out["f_pair_recency"] = vals(h.groupby(hp, sort=False)["days_ago"].min(), xp, np.nan)

    item_price = h.groupby("article_id", sort=False)["price"].mean()
    user_price = h.groupby("customer_id", sort=False)["price"].mean()
    ip = vals(item_price, i, np.nan)
    up = vals(user_price, u, np.nan)
    out["f_i_price"] = ip
    out["f_u_avg_price"] = up
    out["f_price_ratio"] = np.log((ip + 1e-6) / (up + 1e-6))

    def affinity(hist_col, raw_col, name):
        counts = pair_key(hu, h[hist_col]).value_counts()
        out[name] = np.log1p(vals(counts, pair_key(u, X[raw_col])))

    affinity("product_type_no", "raw_i_product_type_no", "f_u_type_n")
    affinity("department_no", "raw_i_department_no", "f_u_dept_n")
    affinity("colour_group_code", "raw_i_colour_group_code", "f_u_colour_n")
    affinity("product_code", "raw_i_product_code", "f_u_product_n")

    out["f_u_age"] = X["raw_u_age"].to_numpy(dtype=float)
    return out.reindex(index=X.index)
