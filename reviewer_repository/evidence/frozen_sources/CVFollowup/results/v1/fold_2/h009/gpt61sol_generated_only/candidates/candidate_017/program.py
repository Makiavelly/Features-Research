import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_pair_7d", "f_pair_30d", "f_pair_180d", "f_pair_decay",
        "f_pair_recency", "f_user_7d", "f_user_30d", "f_user_180d",
        "f_user_decay", "f_item_7d", "f_item_30d", "f_item_180d",
        "f_item_decay", "f_item_recency", "f_user_department",
        "f_user_section", "f_user_product", "f_user_colour",
        "f_user_garment", "f_user_type", "f_user_index_group",
        "f_user_department_30d", "f_user_section_30d",
        "f_pair_channel1", "f_pair_channel2", "f_user_total",
        "f_item_total", "f_pair_share_user", "f_pair_share_item"
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

    def pc(z):
        s = z.groupby(["customer_id", "article_id"], sort=False).size()
        return s.reindex(pix).to_numpy(dtype=float)

    def uc(z):
        return X["customer_id"].map(
            z.groupby("customer_id", sort=False).size()
        ).to_numpy(dtype=float)

    def ic(z):
        return X["article_id"].map(
            z.groupby("article_id", sort=False).size()
        ).to_numpy(dtype=float)

    def cat(col, raw, z):
        s = z.groupby(["customer_id", col], sort=False).size()
        q = pd.MultiIndex.from_arrays(
            [uid, X[raw].to_numpy()], names=["customer_id", col]
        )
        return s.reindex(q).to_numpy(dtype=float)

    r7 = h[h["days_ago"] <= 7]
    r30 = h[h["days_ago"] <= 30]
    r180 = h[h["days_ago"] <= 180]

    out["f_pair_7d"] = pc(r7)
    out["f_pair_30d"] = pc(r30)
    out["f_pair_180d"] = pc(r180)

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

    for c, z in [
        ("f_user_7d", r7), ("f_user_30d", r30), ("f_user_180d", r180)
    ]:
        out[c] = uc(z)
    for c, z in [
        ("f_item_7d", r7), ("f_item_30d", r30), ("f_item_180d", r180)
    ]:
        out[c] = ic(z)

    out["f_user_total"] = uc(h)
    out["f_item_total"] = ic(h)

    out["f_user_department"] = cat(
        "department_no", "raw_i_department_no", h
    )
    out["f_user_section"] = cat("section_no", "raw_i_section_no", h)
    out["f_user_product"] = cat("product_code", "raw_i_product_code", h)
    out["f_user_colour"] = cat(
        "colour_group_code", "raw_i_colour_group_code", h
    )
    out["f_user_garment"] = cat(
        "garment_group_no", "raw_i_garment_group_no", h
    )
    out["f_user_type"] = cat(
        "product_type_no", "raw_i_product_type_no", h
    )
    out["f_user_index_group"] = cat(
        "index_group_no", "raw_i_index_group_no", h
    )
    out["f_user_department_30d"] = cat(
        "department_no", "raw_i_department_no", r30
    )
    out["f_user_section_30d"] = cat(
        "section_no", "raw_i_section_no", r30
    )

    out["f_pair_channel1"] = pc(h[h["sales_channel_id"] == 1])
    out["f_pair_channel2"] = pc(h[h["sales_channel_id"] == 2])

    pair = pc(h)
    user = out["f_user_total"].to_numpy()
    item = out["f_item_total"].to_numpy()
    out["f_pair_share_user"] = pair / (user + 1.0)
    out["f_pair_share_item"] = pair / (item + 1.0)

    return out.replace([np.inf, -np.inf], np.nan).reindex(index=X.index)
