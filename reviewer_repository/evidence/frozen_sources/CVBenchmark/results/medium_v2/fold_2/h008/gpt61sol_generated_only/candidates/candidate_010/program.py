import numpy as np
import pandas as pd


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)
    names = [
        "f_u_n7", "f_u_n30", "f_u_n90", "f_i_n7", "f_i_n30", "f_i_n90",
        "f_pair_n", "f_u_recency", "f_i_recency", "f_pair_recency",
        "f_u_type_n", "f_u_dept_n", "f_u_section_n", "f_i_price",
        "f_u_avg_price", "f_price_ratio", "f_i_channel1", "f_u_age"
    ]

    if history is None or len(history) == 0:
        for name in names:
            out[name] = np.zeros(n, dtype=float)
        return out

    h = history
    u, i = X["customer_id"], X["article_id"]
    hu, hi = h["customer_id"], h["article_id"]

    def mapped(mapping, keys, default=0.0):
        return keys.map(mapping).fillna(default).to_numpy(dtype=float)

    for window in (7, 30, 90):
        r = h.loc[h["days_ago"] <= window]
        suffix = str(window)
        out["f_u_n" + suffix] = np.log1p(mapped(r.groupby("customer_id", sort=False).size(), u))
        out["f_i_n" + suffix] = np.log1p(mapped(r.groupby("article_id", sort=False).size(), i))

    pair_h = pd.MultiIndex.from_arrays([hu.to_numpy(), hi.to_numpy()])
    pair_x = pd.MultiIndex.from_arrays([u.to_numpy(), i.to_numpy()])
    pair_counts = pd.Series(1, index=pair_h).groupby(level=[0, 1], sort=False).sum()
    out["f_pair_n"] = np.log1p(np.asarray(pair_x.map(pair_counts).fillna(0), dtype=float))

    out["f_u_recency"] = mapped(h.groupby("customer_id", sort=False)["days_ago"].min(), u, np.nan)
    out["f_i_recency"] = mapped(h.groupby("article_id", sort=False)["days_ago"].min(), i, np.nan)
    pair_recency = h.groupby([hu, hi], sort=False)["days_ago"].min()
    out["f_pair_recency"] = np.asarray(pair_x.map(pair_recency), dtype=float)

    for col, raw, name in (
        ("product_type_no", "raw_i_product_type_no", "f_u_type_n"),
        ("department_no", "raw_i_department_no", "f_u_dept_n"),
        ("section_no", "raw_i_section_no", "f_u_section_n"),
    ):
        keys_h = pd.MultiIndex.from_arrays([hu.to_numpy(), h[col].to_numpy()])
        keys_x = pd.MultiIndex.from_arrays([u.to_numpy(), X[raw].to_numpy()])
        counts = pd.Series(1, index=keys_h).groupby(level=[0, 1], sort=False).sum()
        out[name] = np.log1p(np.asarray(keys_x.map(counts).fillna(0), dtype=float))

    ip = mapped(h.groupby("article_id", sort=False)["price"].mean(), i, np.nan)
    up = mapped(h.groupby("customer_id", sort=False)["price"].mean(), u, np.nan)
    out["f_i_price"] = ip
    out["f_u_avg_price"] = up
    out["f_price_ratio"] = np.log((ip + 1e-6) / (up + 1e-6))

    channel = h.assign(_c1=(h["sales_channel_id"] == 1).astype(float))
    out["f_i_channel1"] = mapped(channel.groupby("article_id", sort=False)["_c1"].mean(), i, np.nan)
    out["f_u_age"] = pd.to_numeric(X["raw_u_age"], errors="coerce").to_numpy(dtype=float)
    return out.reindex(index=X.index)
