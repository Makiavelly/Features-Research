import pandas as pd
import numpy as np

def modify_features(X, history):
    cols = [
        "f_pair_7d","f_pair_30d","f_pair_180d","f_pair_decay",
        "f_pair_recency","f_user_7d","f_user_30d","f_user_180d",
        "f_user_decay","f_item_7d","f_item_30d","f_item_180d",
        "f_item_decay","f_item_recency","f_user_department",
        "f_user_department_30d","f_user_section","f_user_section_30d",
        "f_user_type","f_user_colour","f_user_garment","f_item_department_30d",
        "f_item_type_30d","f_item_colour_30d","f_pair_channel1",
        "f_pair_channel2","f_user_recency","f_item_repeat_rate",
        "f_pair_price_mean","f_user_price_mean","f_item_price_mean"
    ]
    out = pd.DataFrame(index=X.index)
    h = history
    if len(h) == 0:
        for c in cols:
            out[c] = 0.0
        return out

    uid = X["customer_id"].to_numpy()
    aid = X["article_id"].to_numpy()
    pix = pd.MultiIndex.from_arrays(
        [uid, aid], names=["customer_id", "article_id"]
    )

    def pair_count(z):
        return z.groupby(["customer_id", "article_id"], sort=False).size().reindex(pix).to_numpy(dtype=float)

    def pair_sum(z, col):
        return z.groupby(["customer_id", "article_id"], sort=False)[col].sum().reindex(pix).to_numpy(dtype=float)

    def user_count(z):
        return X["customer_id"].map(z.groupby("customer_id", sort=False).size()).to_numpy(dtype=float)

    def item_count(z):
        return X["article_id"].map(z.groupby("article_id", sort=False).size()).to_numpy(dtype=float)

    def cat(col, raw, z):
        s = z.groupby(["customer_id", col], sort=False).size()
        ix = pd.MultiIndex.from_arrays(
            [uid, X[raw].to_numpy()], names=["customer_id", col]
        )
        return s.reindex(ix).to_numpy(dtype=float)

    r7 = h[h.days_ago <= 7]
    r30 = h[h.days_ago <= 30]
    r180 = h[h.days_ago <= 180]

    out["f_pair_7d"] = pair_count(r7)
    out["f_pair_30d"] = pair_count(r30)
    out["f_pair_180d"] = pair_count(r180)

    w = np.exp(-h.days_ago.astype(float) / 14.0)
    z = h.assign(_w=w)
    out["f_pair_decay"] = pair_sum(z, "_w")
    out["f_user_decay"] = X.customer_id.map(z.groupby("customer_id")["_w"].sum()).to_numpy(dtype=float)
    out["f_item_decay"] = X.article_id.map(z.groupby("article_id")["_w"].sum()).to_numpy(dtype=float)

    out["f_pair_recency"] = h.groupby(
        ["customer_id","article_id"], sort=False
    ).days_ago.min().reindex(pix).to_numpy(dtype=float)
    out["f_user_recency"] = X.customer_id.map(h.groupby("customer_id").days_ago.min()).to_numpy(dtype=float)
    out["f_item_recency"] = X.article_id.map(h.groupby("article_id").days_ago.min()).to_numpy(dtype=float)

    for c, z in [("f_user_7d",r7),("f_user_30d",r30),("f_user_180d",r180)]:
        out[c] = user_count(z)
    for c, z in [("f_item_7d",r7),("f_item_30d",r30),("f_item_180d",r180)]:
        out[c] = item_count(z)

    out["f_user_department"] = cat("department_no","raw_i_department_no",h)
    out["f_user_department_30d"] = cat("department_no","raw_i_department_no",r30)
    out["f_user_section"] = cat("section_no","raw_i_section_no",h)
    out["f_user_section_30d"] = cat("section_no","raw_i_section_no",r30)
    out["f_user_type"] = cat("product_type_no","raw_i_product_type_no",h)
    out["f_user_colour"] = cat("colour_group_code","raw_i_colour_group_code",h)
    out["f_user_garment"] = cat("garment_group_no","raw_i_garment_group_no",h)

    for name, col in [
        ("f_item_department_30d","department_no"),
        ("f_item_type_30d","product_type_no"),
        ("f_item_colour_30d","colour_group_code")
    ]:
        raw = {"department_no":"raw_i_department_no","product_type_no":"raw_i_product_type_no",
               "colour_group_code":"raw_i_colour_group_code"}[col]
        out[name] = X[raw].map(r30.groupby(col).size()).to_numpy(dtype=float)

    for ch in (1, 2):
        out["f_pair_channel" + str(ch)] = pair_count(h[h.sales_channel_id == ch])

    total = pair_count(h)
    out["f_item_repeat_rate"] = total / (X.article_id.map(h.groupby("article_id").size()).to_numpy(dtype=float) + 1e-6)
    for name, z in [("f_pair_price_mean", h), ("f_user_price_mean", h), ("f_item_price_mean", h)]:
        if name.startswith("f_pair"):
            s = z.groupby(["customer_id","article_id"]).price.mean()
            out[name] = s.reindex(pix).to_numpy(dtype=float)
        elif name.startswith("f_user"):
            out[name] = X.customer_id.map(z.groupby("customer_id").price.mean()).to_numpy(dtype=float)
        else:
            out[name] = X.article_id.map(z.groupby("article_id").price.mean()).to_numpy(dtype=float)

    return out.replace([np.inf, -np.inf], np.nan).reindex(index=X.index)
