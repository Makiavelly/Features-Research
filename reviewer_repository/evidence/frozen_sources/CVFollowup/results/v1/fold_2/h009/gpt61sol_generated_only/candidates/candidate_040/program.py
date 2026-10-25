import pandas as pd
import numpy as np

def modify_features(X, history):
    cols = [
        "f_pair_7d","f_pair_14d","f_pair_30d","f_pair_180d",
        "f_pair_decay","f_pair_recency","f_user_7d","f_user_30d",
        "f_user_180d","f_user_decay","f_item_7d","f_item_14d",
        "f_item_30d","f_item_180d","f_item_decay","f_item_recency",
        "f_user_total","f_item_total","f_user_department",
        "f_user_section","f_user_product","f_user_type","f_user_colour",
        "f_user_garment","f_user_department_30d","f_user_section_30d",
        "f_user_type_30d","f_pair_channel1","f_pair_channel2",
        "f_pair_share_user","f_pair_share_item","f_item_growth",
        "f_user_activity","f_user_product_decay","f_user_type_decay",
        "f_user_department_decay"
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

    def pc(z):
        return z.groupby(
            ["customer_id", "article_id"], sort=False
        ).size().reindex(pidx).to_numpy(dtype=float)

    def uc(z):
        return X["customer_id"].map(
            z.groupby("customer_id", sort=False).size()
        ).to_numpy(dtype=float)

    def ic(z):
        return X["article_id"].map(
            z.groupby("article_id", sort=False).size()
        ).to_numpy(dtype=float)

    def aff(col, raw, z, value=None):
        if value is None:
            s = z.groupby(["customer_id", col], sort=False).size()
        else:
            s = z.groupby(["customer_id", col], sort=False)[value].sum()
        q = pd.MultiIndex.from_arrays(
            [uid, X[raw].to_numpy()], names=["customer_id", col]
        )
        return s.reindex(q).to_numpy(dtype=float)

    r7 = h[h["days_ago"] <= 7]
    r14 = h[h["days_ago"] <= 14]
    r30 = h[h["days_ago"] <= 30]
    r180 = h[h["days_ago"] <= 180]

    out["f_pair_7d"] = pc(r7)
    out["f_pair_14d"] = pc(r14)
    out["f_pair_30d"] = pc(r30)
    out["f_pair_180d"] = pc(r180)

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

    out["f_user_7d"] = uc(r7)
    out["f_user_30d"] = uc(r30)
    out["f_user_180d"] = uc(r180)
    out["f_item_7d"] = ic(r7)
    out["f_item_14d"] = ic(r14)
    out["f_item_30d"] = ic(r30)
    out["f_item_180d"] = ic(r180)
    out["f_user_total"] = uc(h)
    out["f_item_total"] = ic(h)

    for name, col, raw, frame in [
        ("f_user_department","department_no","raw_i_department_no",h),
        ("f_user_section","section_no","raw_i_section_no",h),
        ("f_user_product","product_code","raw_i_product_code",h),
        ("f_user_type","product_type_no","raw_i_product_type_no",h),
        ("f_user_colour","colour_group_code","raw_i_colour_group_code",h),
        ("f_user_garment","garment_group_no","raw_i_garment_group_no",h),
        ("f_user_department_30d","department_no","raw_i_department_no",r30),
        ("f_user_section_30d","section_no","raw_i_section_no",r30),
        ("f_user_type_30d","product_type_no","raw_i_product_type_no",r30)
    ]:
        out[name] = aff(col, raw, frame)

    out["f_user_product_decay"] = aff(
        "product_code", "raw_i_product_code", z, "_w"
    )
    out["f_user_type_decay"] = aff(
        "product_type_no", "raw_i_product_type_no", z, "_w"
    )
    out["f_user_department_decay"] = aff(
        "department_no", "raw_i_department_no", z, "_w"
    )

    out["f_pair_channel1"] = pc(h[h["sales_channel_id"] == 1])
    out["f_pair_channel2"] = pc(h[h["sales_channel_id"] == 2])

    pair = pc(h)
    out["f_pair_share_user"] = pair / (out["f_user_total"].to_numpy() + 1.0)
    out["f_pair_share_item"] = pair / (out["f_item_total"].to_numpy() + 1.0)
    out["f_item_growth"] = out["f_item_7d"] / (out["f_item_180d"] + 1.0)
    out["f_user_activity"] = out["f_user_7d"] / (out["f_user_180d"] + 1.0)
    return out.replace([np.inf, -np.inf], np.nan).reindex(index=X.index)
