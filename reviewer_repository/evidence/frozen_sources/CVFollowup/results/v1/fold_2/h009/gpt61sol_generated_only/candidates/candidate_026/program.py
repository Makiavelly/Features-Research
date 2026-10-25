import pandas as pd
import numpy as np

def modify_features(X, history):
    cols = [
        "f_pair_7d", "f_pair_14d", "f_pair_30d", "f_pair_180d",
        "f_pair_decay", "f_pair_recency", "f_user_7d", "f_user_30d",
        "f_user_180d", "f_user_decay", "f_item_7d", "f_item_14d",
        "f_item_30d", "f_item_180d", "f_item_decay", "f_item_recency",
        "f_user_total", "f_item_total", "f_user_department",
        "f_user_section", "f_user_product", "f_user_type", "f_user_colour",
        "f_user_garment", "f_user_department_30d", "f_user_section_30d",
        "f_user_type_30d", "f_pair_channel1", "f_pair_channel2",
        "f_pair_share_user", "f_pair_share_item", "f_item_growth",
        "f_user_activity"
    ]
    out = pd.DataFrame(index=X.index)
    h = history

    if len(h) == 0:
        for c in cols:
            out[c] = 0.0
        return out

    uid = X["customer_id"].to_numpy()
    aid = X["article_id"].to_numpy()
    pidx = pd.MultiIndex.from_arrays(
        [uid, aid], names=["customer_id", "article_id"]
    )

    def pair_count(z):
        s = z.groupby(["customer_id", "article_id"], sort=False).size()
        return s.reindex(pidx).to_numpy(dtype=float)

    def user_count(z):
        s = z.groupby("customer_id", sort=False).size()
        return X["customer_id"].map(s).to_numpy(dtype=float)

    def item_count(z):
        s = z.groupby("article_id", sort=False).size()
        return X["article_id"].map(s).to_numpy(dtype=float)

    def affinity(col, raw, z):
        s = z.groupby(["customer_id", col], sort=False).size()
        q = pd.MultiIndex.from_arrays(
            [uid, X[raw].to_numpy()], names=["customer_id", col]
        )
        return s.reindex(q).to_numpy(dtype=float)

    r7 = h[h["days_ago"] <= 7]
    r14 = h[h["days_ago"] <= 14]
    r30 = h[h["days_ago"] <= 30]
    r180 = h[h["days_ago"] <= 180]

    out["f_pair_7d"] = pair_count(r7)
    out["f_pair_14d"] = pair_count(r14)
    out["f_pair_30d"] = pair_count(r30)
    out["f_pair_180d"] = pair_count(r180)

    z = h.assign(_w=np.exp(-h["days_ago"].astype(float) / 14.0))
    out["f_pair_decay"] = z.groupby(
        ["customer_id", "article_id"], sort=False
    )["_w"].sum().reindex(pidx).to_numpy(dtype=float)
    out["f_user_decay"] = X["customer_id"].map(
        z.groupby("customer_id", sort=False)["_w"].sum()
    ).to_numpy(dtype=float)
    out["f_item_decay"] = X["article_id"].map(
        z.groupby("article_id", sort=False)["_w"].sum()
    ).to_numpy(dtype=float)

    out["f_pair_recency"] = h.groupby(
        ["customer_id", "article_id"], sort=False
    )["days_ago"].min().reindex(pidx).to_numpy(dtype=float)
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    ).to_numpy(dtype=float)

    out["f_user_7d"] = user_count(r7)
    out["f_user_30d"] = user_count(r30)
    out["f_user_180d"] = user_count(r180)
    out["f_item_7d"] = item_count(r7)
    out["f_item_14d"] = item_count(r14)
    out["f_item_30d"] = item_count(r30)
    out["f_item_180d"] = item_count(r180)
    out["f_user_total"] = user_count(h)
    out["f_item_total"] = item_count(h)

    out["f_user_department"] = affinity(
        "department_no", "raw_i_department_no", h
    )
    out["f_user_section"] = affinity("section_no", "raw_i_section_no", h)
    out["f_user_product"] = affinity("product_code", "raw_i_product_code", h)
    out["f_user_type"] = affinity(
        "product_type_no", "raw_i_product_type_no", h
    )
    out["f_user_colour"] = affinity(
        "colour_group_code", "raw_i_colour_group_code", h
    )
    out["f_user_garment"] = affinity(
        "garment_group_no", "raw_i_garment_group_no", h
    )
    out["f_user_department_30d"] = affinity(
        "department_no", "raw_i_department_no", r30
    )
    out["f_user_section_30d"] = affinity(
        "section_no", "raw_i_section_no", r30
    )
    out["f_user_type_30d"] = affinity(
        "product_type_no", "raw_i_product_type_no", r30
    )

    out["f_pair_channel1"] = pair_count(h[h["sales_channel_id"] == 1])
    out["f_pair_channel2"] = pair_count(h[h["sales_channel_id"] == 2])

    pair = pair_count(h)
    user = out["f_user_total"].to_numpy()
    item = out["f_item_total"].to_numpy()
    out["f_pair_share_user"] = pair / (user + 1.0)
    out["f_pair_share_item"] = pair / (item + 1.0)
    out["f_item_growth"] = out["f_item_7d"] / (out["f_item_180d"] + 1.0)
    out["f_user_activity"] = out["f_user_7d"] / (out["f_user_180d"] + 1.0)

    return out.replace([np.inf, -np.inf], np.nan).reindex(index=X.index)
