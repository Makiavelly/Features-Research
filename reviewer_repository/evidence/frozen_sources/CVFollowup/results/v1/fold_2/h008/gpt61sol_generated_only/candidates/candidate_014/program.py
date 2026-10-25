import numpy as np
import pandas as pd


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def mapped(series, keys, default=0.0):
        return keys.map(series).fillna(default).to_numpy(dtype=float)

    def pair_keys(a, b):
        return a.astype(str) + "|" + b.astype(str)

    if history is None or history.empty:
        for name in (
            "f_u_n7", "f_u_n30", "f_u_n90", "f_i_n7", "f_i_n30",
            "f_pair_n", "f_u_recency", "f_i_recency", "f_pair_recency",
            "f_u_type_n", "f_u_dept_n", "f_u_section_n", "f_i_price",
            "f_u_avg_price", "f_price_ratio", "f_u_channel1"
        ):
            out[name] = np.zeros(n, dtype=float)
        return out

    h = history
    u, i = X["customer_id"], X["article_id"]

    for window, label in ((7, "7"), (30, "30"), (90, "90")):
        recent = h.loc[h["days_ago"] <= window]
        out["f_u_n" + label] = np.log1p(mapped(recent.groupby("customer_id").size(), u))
        if window != 90:
            out["f_i_n" + label] = np.log1p(mapped(recent.groupby("article_id").size(), i))

    hp = pair_keys(h["customer_id"], h["article_id"])
    xp = pair_keys(u, i)
    out["f_pair_n"] = np.log1p(mapped(hp.value_counts(), xp))
    out["f_u_recency"] = mapped(h.groupby("customer_id")["days_ago"].min(), u, np.nan)
    out["f_i_recency"] = mapped(h.groupby("article_id")["days_ago"].min(), i, np.nan)
    out["f_pair_recency"] = mapped(h.groupby(hp)["days_ago"].min(), xp, np.nan)

    for hist_col, raw_col, name in (
        ("product_type_no", "raw_i_product_type_no", "f_u_type_n"),
        ("department_no", "raw_i_department_no", "f_u_dept_n"),
        ("section_no", "raw_i_section_no", "f_u_section_n"),
    ):
        keys = pair_keys(h["customer_id"], h[hist_col])
        candidates = pair_keys(u, X[raw_col])
        out[name] = np.log1p(mapped(keys.value_counts(), candidates))

    ip = mapped(h.groupby("article_id")["price"].mean(), i, np.nan)
    up = mapped(h.groupby("customer_id")["price"].mean(), u, np.nan)
    out["f_i_price"] = ip
    out["f_u_avg_price"] = up
    out["f_price_ratio"] = np.log((ip + 1e-6) / (up + 1e-6))
    out["f_u_channel1"] = mapped(
        h.assign(_ch1=(h["sales_channel_id"] == 1).astype(float))
        .groupby("customer_id")["_ch1"].mean(),
        u, np.nan
    )
    return out.reindex(index=X.index)
