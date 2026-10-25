import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    cols = [
        "f_item_7", "f_item_30", "f_item_90", "f_item_all", "f_item_rec",
        "f_user_7", "f_user_30", "f_user_90", "f_user_all", "f_user_rec",
        "f_type_30", "f_type_90", "f_dept_30", "f_dept_90",
        "f_section_90", "f_garment_90", "f_pair_all", "f_pair_rec",
        "f_item_price", "f_user_price", "f_item_ch2", "f_item_7_share",
        "f_user_7_share", "f_age", "f_type_static", "f_dept_static"
    ]
    if history is None or len(history) == 0:
        for c in cols:
            out[c] = 0.0
        return out

    h = history
    cid = X["customer_id"]
    aid = X["article_id"]

    def cnt(key, days, name, xkey):
        z = h if days is None else h.loc[h["days_ago"] <= days]
        out[name] = X[xkey].map(z.groupby(key).size()).fillna(0).astype(float)

    cnt("article_id", 7, "f_item_7", "article_id")
    cnt("article_id", 30, "f_item_30", "article_id")
    cnt("article_id", 90, "f_item_90", "article_id")
    cnt("article_id", None, "f_item_all", "article_id")
    cnt("customer_id", 7, "f_user_7", "customer_id")
    cnt("customer_id", 30, "f_user_30", "customer_id")
    cnt("customer_id", 90, "f_user_90", "customer_id")
    cnt("customer_id", None, "f_user_all", "customer_id")

    out["f_item_rec"] = aid.map(h.groupby("article_id")["days_ago"].min()).fillna(999.0)
    out["f_user_rec"] = cid.map(h.groupby("customer_id")["days_ago"].min()).fillna(999.0)

    def cross(histcol, xcol, days, name):
        z = h.loc[h["days_ago"] <= days]
        s = z.groupby(["customer_id", histcol]).size().rename(name).reset_index()
        q = pd.DataFrame({"customer_id": cid.to_numpy(), histcol: X[xcol].to_numpy()})
        out[name] = q.merge(s, on=["customer_id", histcol], how="left", sort=False)[name].fillna(0).to_numpy()

    cross("product_type_no", "raw_i_product_type_no", 30, "f_type_30")
    cross("product_type_no", "raw_i_product_type_no", 90, "f_type_90")
    cross("department_no", "raw_i_department_no", 30, "f_dept_30")
    cross("department_no", "raw_i_department_no", 90, "f_dept_90")
    cross("section_no", "raw_i_section_no", 90, "f_section_90")
    cross("garment_group_no", "raw_i_garment_group_no", 90, "f_garment_90")

    s = h.groupby(["customer_id", "article_id"]).size().rename("v").reset_index()
    q = pd.DataFrame({"customer_id": cid.to_numpy(), "article_id": aid.to_numpy()})
    out["f_pair_all"] = q.merge(s, on=["customer_id", "article_id"], how="left", sort=False)["v"].fillna(0).to_numpy()
    r = h.groupby(["customer_id", "article_id"])["days_ago"].min().rename("v").reset_index()
    out["f_pair_rec"] = q.merge(r, on=["customer_id", "article_id"], how="left", sort=False)["v"].fillna(999.0).to_numpy()

    out["f_item_price"] = aid.map(h.groupby("article_id")["price"].mean()).fillna(0.0)
    out["f_user_price"] = cid.map(h.groupby("customer_id")["price"].mean()).fillna(0.0)
    out["f_item_ch2"] = aid.map(h.groupby("article_id")["sales_channel_id"].mean()).fillna(0.0)
    out["f_item_7_share"] = out["f_item_7"] / (1.0 + out["f_item_90"])
    out["f_user_7_share"] = out["f_user_7"] / (1.0 + out["f_user_90"])
    out["f_age"] = X["raw_u_age"].fillna(-1).astype(float)
    out["f_type_static"] = X["raw_i_product_type_no"].fillna(-1).astype(float)
    out["f_dept_static"] = X["raw_i_department_no"].fillna(-1).astype(float)
    return out
