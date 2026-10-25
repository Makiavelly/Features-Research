import pandas as pd
import numpy as np

def modify_features(X, history):
    n = len(X)
    out = pd.DataFrame(index=X.index)

    def mapped(group, key, name, window=None):
        h = history if window is None else history.loc[history["days_ago"] <= window]
        if len(h):
            s = h.groupby(key).size()
            out[name] = X[key].map(s).fillna(0).to_numpy()
        else:
            out[name] = np.zeros(n)

    def paired(hkey, xkey, name, window=None):
        h = history if window is None else history.loc[history["days_ago"] <= window]
        if not len(h):
            out[name] = np.zeros(n)
            return
        a = h.groupby(["customer_id", hkey]).size().rename("__v").reset_index()
        q = X[["customer_id", xkey]].copy()
        q["__r"] = np.arange(n)
        z = q.merge(
            a, how="left", left_on=["customer_id", xkey],
            right_on=["customer_id", hkey], sort=False
        )
        out[name] = z["__v"].fillna(0).to_numpy()

    mapped(None, "article_id", "f_item_all")
    mapped(None, "customer_id", "f_user_all")
    mapped(None, "article_id", "f_item_7", 7)
    mapped(None, "article_id", "f_item_30", 30)
    mapped(None, "article_id", "f_item_90", 90)
    mapped(None, "customer_id", "f_user_7", 7)
    mapped(None, "customer_id", "f_user_30", 30)
    mapped(None, "customer_id", "f_user_90", 90)

    if len(history):
        out["f_user_recency"] = X["customer_id"].map(
            history.groupby("customer_id")["days_ago"].min()
        ).to_numpy()
        out["f_item_recency"] = X["article_id"].map(
            history.groupby("article_id")["days_ago"].min()
        ).to_numpy()
    else:
        out["f_user_recency"] = np.nan
        out["f_item_recency"] = np.nan

    paired("article_id", "article_id", "f_user_item_all")
    paired("article_id", "article_id", "f_user_item_30", 30)
    paired("product_code", "raw_i_product_code", "f_user_product_all")
    paired("product_code", "raw_i_product_code", "f_user_product_30", 30)
    paired("product_type_no", "raw_i_product_type_no", "f_user_type_all")
    paired("department_no", "raw_i_department_no", "f_user_department_all")
    paired("garment_group_no", "raw_i_garment_group_no", "f_user_garment_all")
    paired("colour_group_code", "raw_i_colour_group_code", "f_user_colour_all")

    for src, dst in [
        ("raw_u_age", "f_age"),
        ("raw_u_active", "f_active"),
        ("raw_u_club_member_status", "f_club"),
        ("raw_i_product_code", "f_product"),
        ("raw_i_product_type_no", "f_type"),
        ("raw_i_department_no", "f_department"),
        ("raw_i_section_no", "f_section"),
        ("raw_i_garment_group_no", "f_garment"),
    ]:
        out[dst] = pd.to_numeric(X[src], errors="coerce").to_numpy()

    return out.replace([np.inf, -np.inf], np.nan)
