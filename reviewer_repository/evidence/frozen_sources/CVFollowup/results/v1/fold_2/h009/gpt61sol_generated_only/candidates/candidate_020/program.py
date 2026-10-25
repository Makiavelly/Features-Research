import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_pair_7d", "f_pair_30d", "f_pair_90d", "f_pair_180d",
        "f_pair_decay", "f_pair_recency", "f_user_7d", "f_user_30d",
        "f_user_180d", "f_user_decay", "f_item_7d", "f_item_30d",
        "f_item_90d", "f_item_180d", "f_item_decay", "f_item_recency",
        "f_user_department", "f_user_section", "f_user_product",
        "f_user_type", "f_user_colour", "f_user_garment",
        "f_user_department_30d", "f_user_section_30d", "f_user_type_30d",
        "f_pair_channel1", "f_pair_channel2", "f_user_total", "f_item_total",
        "f_pair_share_user", "f_pair_share_item", "f_static_product",
        "f_static_type", "f_static_department", "f_static_section",
        "f_static_garment"
    ]
    out = pd.DataFrame(index=X.index)
    h = history

    if len(h) == 0:
        for c in names:
            out[c] = 0.0
        return out

    uid = X["customer_id"].to_numpy()
    aid = X["article_id"].to_numpy()
    pix = pd.MultiIndex.from_arrays(
        [uid, aid], names=["customer_id", "article_id"]
    )

    def pair_count(z):
        s = z.groupby(["customer_id", "article_id"], sort=False).size()
        return s.reindex(pix).to_numpy(dtype=float)

    def user_count(z):
        return X["customer_id"].map(
            z.groupby("customer_id", sort=False).size()
        ).to_numpy(dtype=float)

    def item_count(z):
        return X["article_id"].map(
            z.groupby("article_id", sort=False).size()
        ).to_numpy(dtype=float)

    def affinity(col, raw, z):
        s = z.groupby(["customer_id", col], sort=False).size()
        ix = pd.MultiIndex.from_arrays(
            [uid, X[raw].to_numpy()], names=["customer_id", col]
        )
        return s.reindex(ix).to_numpy(dtype=float)

    r7 = h[h["days_ago"] <= 7]
    r30 = h[h["days_ago"] <= 30]
    r90 = h[h["days_ago"] <= 90]
    r180 = h[h["days_ago"] <= 180]

    out["f_pair_7d"] = pair_count(r7)
    out["f_pair_30d"] = pair_count(r30)
    out["f_pair_90d"] = pair_count(r90)
    out["f_pair_180d"] = pair_count(r180)

    z = h.assign(_w=np.exp(-h["days_ago"].astype(float) / 14.0))
    out["f_pair_decay"] = z.groupby(
        ["customer_id", "article_id"], sort=False
    )["_w"].sum().reindex(pix).to_numpy(dtype=float)
    out["f_user_decay"] = X["customer_id"].map(
        z.groupby("customer_id", sort=False)["_w"].sum()
    ).to_numpy(dtype=float)
    out["f_item_decay"] = X["article_id"].map(
        z.groupby("article_id", sort=False)["_w"].sum()
    ).to_numpy(dtype=float)

    out["f_pair_recency"] = h.groupby(
        ["customer_id", "article_id"], sort=False
    )["days_ago"].min().reindex(pix).to_numpy(dtype=float)
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    ).to_numpy(dtype=float)

    for c, z0 in [
        ("f_user_7d", r7), ("f_user_30d", r30), ("f_user_180d", r180)
    ]:
        out[c] = user_count(z0)
    for c, z0 in [
        ("f_item_7d", r7), ("f_item_30d", r30),
        ("f_item_90d", r90), ("f_item_180d", r180)
    ]:
        out[c] = item_count(z0)

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

    out["f_static_product"] = pd.to_numeric(
        X["raw_i_product_code"], errors="coerce"
    )
    out["f_static_type"] = pd.to_numeric(
        X["raw_i_product_type_no"], errors="coerce"
    )
    out["f_static_department"] = pd.to_numeric(
        X["raw_i_department_no"], errors="coerce"
    )
    out["f_static_section"] = pd.to_numeric(
        X["raw_i_section_no"], errors="coerce"
    )
    out["f_static_garment"] = pd.to_numeric(
        X["raw_i_garment_group_no"], errors="coerce"
    )

    return out.replace([np.inf, -np.inf], np.nan).reindex(index=X.index)
