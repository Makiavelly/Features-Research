import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    names = [
        "f_item_7", "f_item_30", "f_item_90", "f_item_all", "f_item_rec",
        "f_user_7", "f_user_30", "f_user_90", "f_user_all", "f_user_rec",
        "f_type_7", "f_type_30", "f_type_90", "f_dept_30", "f_dept_90",
        "f_section_90", "f_garment_90", "f_colour_90", "f_graphic_90",
        "f_product_90", "f_pair_all", "f_pair_rec", "f_pair_30",
        "f_item_price", "f_user_price", "f_price_gap", "f_item_ch2",
        "f_item_7_share", "f_item_trend", "f_user_7_share",
        "f_age", "f_type_static", "f_dept_static", "f_section_static",
        "f_colour_static", "f_graphic_static"
    ]
    for c in names:
        out[c] = 0.0

    out["f_age"] = X["raw_u_age"].fillna(-1).astype(float)
    out["f_type_static"] = X["raw_i_product_type_no"].fillna(-1).astype(float)
    out["f_dept_static"] = X["raw_i_department_no"].fillna(-1).astype(float)
    out["f_section_static"] = X["raw_i_section_no"].fillna(-1).astype(float)
    out["f_colour_static"] = X["raw_i_colour_group_code"].fillna(-1).astype(float)
    out["f_graphic_static"] = X["raw_i_graphical_appearance_no"].fillna(-1).astype(float)
    if history is None or len(history) == 0:
        return out

    h = history
    cid = X["customer_id"]
    aid = X["article_id"]

    def counts(key, days, name, xkey):
        z = h if days is None else h.loc[h["days_ago"] <= days]
        out[name] = X[xkey].map(z.groupby(key).size()).fillna(0).astype(float)

    counts("article_id", 7, "f_item_7", "article_id")
    counts("article_id", 30, "f_item_30", "article_id")
    counts("article_id", 90, "f_item_90", "article_id")
    counts("article_id", None, "f_item_all", "article_id")
    counts("customer_id", 7, "f_user_7", "customer_id")
    counts("customer_id", 30, "f_user_30", "customer_id")
    counts("customer_id", 90, "f_user_90", "customer_id")
    counts("customer_id", None, "f_user_all", "customer_id")
    out["f_item_rec"] = aid.map(h.groupby("article_id")["days_ago"].min()).fillna(999)
    out["f_user_rec"] = cid.map(h.groupby("customer_id")["days_ago"].min()).fillna(999)

    def affinity(hcol, xcol, days, name):
        z = h.loc[h["days_ago"] <= days]
        s = z.groupby(["customer_id", hcol]).size().rename("v").reset_index()
        q = pd.DataFrame({"customer_id": cid.to_numpy(), hcol: X[xcol].to_numpy()})
        out[name] = q.merge(s, on=["customer_id", hcol], how="left", sort=False)["v"].fillna(0).to_numpy()

    affinity("product_type_no", "raw_i_product_type_no", 7, "f_type_7")
    affinity("product_type_no", "raw_i_product_type_no", 30, "f_type_30")
    affinity("product_type_no", "raw_i_product_type_no", 90, "f_type_90")
    affinity("department_no", "raw_i_department_no", 30, "f_dept_30")
    affinity("department_no", "raw_i_department_no", 90, "f_dept_90")
    affinity("section_no", "raw_i_section_no", 90, "f_section_90")
    affinity("garment_group_no", "raw_i_garment_group_no", 90, "f_garment_90")
    affinity("colour_group_code", "raw_i_colour_group_code", 90, "f_colour_90")
    affinity("graphical_appearance_no", "raw_i_graphical_appearance_no", 90, "f_graphic_90")
    affinity("product_code", "raw_i_product_code", 90, "f_product_90")

    def pair(days, name):
        z = h if days is None else h.loc[h["days_ago"] <= days]
        s = z.groupby(["customer_id", "article_id"]).size().rename("v").reset_index()
        q = pd.DataFrame({"customer_id": cid.to_numpy(), "article_id": aid.to_numpy()})
        out[name] = q.merge(s, on=["customer_id", "article_id"], how="left", sort=False)["v"].fillna(0).to_numpy()

    pair(None, "f_pair_all")
    pair(30, "f_pair_30")
    q = pd.DataFrame({"customer_id": cid.to_numpy(), "article_id": aid.to_numpy()})
    r = h.groupby(["customer_id", "article_id"])["days_ago"].min().rename("v").reset_index()
    out["f_pair_rec"] = q.merge(r, on=["customer_id", "article_id"], how="left", sort=False)["v"].fillna(999).to_numpy()

    out["f_item_price"] = aid.map(h.groupby("article_id")["price"].mean()).fillna(0)
    out["f_user_price"] = cid.map(h.groupby("customer_id")["price"].mean()).fillna(0)
    out["f_price_gap"] = (out["f_item_price"] - out["f_user_price"]).abs()
    out["f_item_ch2"] = aid.map(h.groupby("article_id")["sales_channel_id"].mean()).fillna(0)
    out["f_item_7_share"] = out["f_item_7"] / (1 + out["f_item_90"])
    out["f_item_trend"] = out["f_item_7"] / (1 + out["f_item_30"] - out["f_item_7"])
    out["f_user_7_share"] = out["f_user_7"] / (1 + out["f_user_90"])
    return out
