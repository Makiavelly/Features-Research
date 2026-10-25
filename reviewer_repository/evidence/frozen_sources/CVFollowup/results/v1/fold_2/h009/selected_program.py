import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    names = [
        "f_pair_7d", "f_pair_30d", "f_pair_180d", "f_pair_decay",
        "f_pair_recency", "f_user_decay", "f_item_decay", "f_item_30d",
        "f_item_180d", "f_user_department", "f_user_section",
        "f_user_product", "f_user_colour", "f_user_garment"
    ]
    if len(h) == 0:
        for c in names:
            out[c] = 0.0
        return out

    uid = X["customer_id"].to_numpy()
    aid = X["article_id"].to_numpy()
    pair_ix = pd.MultiIndex.from_arrays(
        [uid, aid], names=["customer_id", "article_id"]
    )

    def pair_count(frame):
        s = frame.groupby(["customer_id", "article_id"], sort=False).size()
        return s.reindex(pair_ix).to_numpy(dtype=float)

    def cat_count(col, raw):
        s = h.groupby(["customer_id", col], sort=False).size()
        ix = pd.MultiIndex.from_arrays(
            [uid, X[raw].to_numpy()], names=["customer_id", col]
        )
        return s.reindex(ix).to_numpy(dtype=float)

    r7 = h[h["days_ago"] <= 7]
    r30 = h[h["days_ago"] <= 30]
    r180 = h[h["days_ago"] <= 180]

    out["f_pair_7d"] = pair_count(r7)
    out["f_pair_30d"] = pair_count(r30)
    out["f_pair_180d"] = pair_count(r180)

    decay = np.exp(-h["days_ago"].astype(float) / 14.0)
    decayed = h.assign(_w=decay)
    s = decayed.groupby(["customer_id", "article_id"], sort=False)["_w"].sum()
    out["f_pair_decay"] = s.reindex(pair_ix).to_numpy(dtype=float)
    out["f_user_decay"] = X["customer_id"].map(
        decayed.groupby("customer_id", sort=False)["_w"].sum()
    ).to_numpy(dtype=float)
    out["f_item_decay"] = X["article_id"].map(
        decayed.groupby("article_id", sort=False)["_w"].sum()
    ).to_numpy(dtype=float)

    rec = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
    out["f_pair_recency"] = rec.reindex(pair_ix).to_numpy(dtype=float)
    out["f_item_30d"] = X["article_id"].map(
        r30.groupby("article_id", sort=False).size()
    ).to_numpy(dtype=float)
    out["f_item_180d"] = X["article_id"].map(
        r180.groupby("article_id", sort=False).size()
    ).to_numpy(dtype=float)

    out["f_user_department"] = cat_count("department_no", "raw_i_department_no")
    out["f_user_section"] = cat_count("section_no", "raw_i_section_no")
    out["f_user_product"] = cat_count("product_code", "raw_i_product_code")
    out["f_user_colour"] = cat_count("colour_group_code", "raw_i_colour_group_code")
    out["f_user_garment"] = cat_count("garment_group_no", "raw_i_garment_group_no")

    for c in out.columns:
        out[c] = pd.to_numeric(out[c], errors="coerce").replace(
            [np.inf, -np.inf], np.nan
        )
    return out.reindex(index=X.index)
