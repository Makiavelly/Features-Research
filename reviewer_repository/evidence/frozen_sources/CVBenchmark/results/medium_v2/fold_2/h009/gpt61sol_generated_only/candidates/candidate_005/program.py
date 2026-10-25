import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_pair_7d", "f_pair_30d", "f_pair_180d", "f_pair_decay",
        "f_pair_recency", "f_user_7d", "f_user_30d", "f_user_180d",
        "f_user_decay", "f_item_7d", "f_item_30d", "f_item_180d",
        "f_item_decay", "f_item_recency", "f_user_department",
        "f_user_department_30d", "f_user_section", "f_user_type",
        "f_item_department_30d", "f_item_type_30d"
    ]
    out = pd.DataFrame(index=X.index)
    if len(history) == 0:
        for c in names:
            out[c] = 0.0
        return out

    h = history
    n = len(X)
    uid = X["customer_id"].to_numpy()
    aid = X["article_id"].to_numpy()

    def pair_map(frame, value=None):
        keys = ["customer_id", "article_id"]
        if value is None:
            s = frame.groupby(keys, sort=False).size()
        else:
            s = frame.groupby(keys, sort=False)[value].sum()
        ix = pd.MultiIndex.from_arrays([uid, aid], names=keys)
        return s.reindex(ix).to_numpy(dtype=float)

    def user_map(frame, value=None):
        if value is None:
            s = frame.groupby("customer_id", sort=False).size()
        else:
            s = frame.groupby("customer_id", sort=False)[value].sum()
        return X["customer_id"].map(s).to_numpy(dtype=float)

    def item_map(frame, value=None):
        if value is None:
            s = frame.groupby("article_id", sort=False).size()
        else:
            s = frame.groupby("article_id", sort=False)[value].sum()
        return X["article_id"].map(s).to_numpy(dtype=float)

    r7 = h[h["days_ago"] <= 7]
    r30 = h[h["days_ago"] <= 30]
    r180 = h[h["days_ago"] <= 180]

    out["f_pair_7d"] = pair_map(r7)
    out["f_pair_30d"] = pair_map(r30)
    out["f_pair_180d"] = pair_map(r180)

    hh = h.copy()
    hh["_decay"] = np.exp(-hh["days_ago"].astype(float) / 14.0)
    out["f_pair_decay"] = pair_map(hh, "_decay")
    out["f_user_decay"] = user_map(hh, "_decay")
    out["f_item_decay"] = item_map(hh, "_decay")

    out["f_user_7d"] = user_map(r7)
    out["f_user_30d"] = user_map(r30)
    out["f_user_180d"] = user_map(r180)
    out["f_item_7d"] = item_map(r7)
    out["f_item_30d"] = item_map(r30)
    out["f_item_180d"] = item_map(r180)

    pi = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
    ix = pd.MultiIndex.from_arrays([uid, aid], names=["customer_id", "article_id"])
    out["f_pair_recency"] = pi.reindex(ix).to_numpy(dtype=float)
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    ).to_numpy(dtype=float)

    def user_cat(col, raw, frame):
        s = frame.groupby(["customer_id", col], sort=False).size()
        ix2 = pd.MultiIndex.from_arrays(
            [uid, X[raw].to_numpy()], names=["customer_id", col]
        )
        return s.reindex(ix2).to_numpy(dtype=float)

    out["f_user_department"] = user_cat("department_no", "raw_i_department_no", h)
    out["f_user_department_30d"] = user_cat("department_no", "raw_i_department_no", r30)
    out["f_user_section"] = user_cat("section_no", "raw_i_section_no", h)
    out["f_user_type"] = user_cat("product_type_no", "raw_i_product_type_no", h)

    def item_cat(col, raw):
        s = r30.groupby(col, sort=False).size()
        return X[raw].map(s).to_numpy(dtype=float)

    out["f_item_department_30d"] = item_cat("department_no", "raw_i_department_no")
    out["f_item_type_30d"] = item_cat("product_type_no", "raw_i_product_type_no")

    for c in out.columns:
        out[c] = pd.to_numeric(out[c], errors="coerce").replace(
            [np.inf, -np.inf], np.nan
        )
    return out.reindex(index=X.index)
