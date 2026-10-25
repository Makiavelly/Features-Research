import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    names = [
        "f_pair_14d", "f_pair_60d", "f_pair_all", "f_pair_recency",
        "f_pair_decay", "f_user_14d", "f_user_60d", "f_user_all",
        "f_user_recency", "f_user_decay", "f_user_unique_items",
        "f_item_14d", "f_item_60d", "f_item_all", "f_item_recency",
        "f_item_decay", "f_item_channel2", "f_user_channel2",
        "f_type_60d", "f_section_60d", "f_garment_60d",
        "f_colour_60d", "f_department_60d", "f_type_share_60d",
        "f_product_code_all", "f_product_type_all", "f_section_all",
        "f_item_age_match", "f_user_age", "f_item_product_type"
    ]
    if history is None or len(history) == 0:
        for n in names:
            if n == "f_user_age":
                out[n] = pd.to_numeric(X["raw_u_age"], errors="coerce")
            elif n == "f_item_product_type":
                out[n] = pd.to_numeric(X["raw_i_product_type_no"], errors="coerce")
            else:
                out[n] = 0.0
        return out.astype(float)

    h = history.reset_index(drop=True)
    d = pd.to_numeric(h["days_ago"], errors="coerce").fillna(9999.0)
    c = X["customer_id"]
    a = X["article_id"]

    def key(x, y):
        return x.astype("string").fillna("<na>") + "|" + y.astype("string").fillna("<na>")

    def mapped(values, groups, target, fill=0.0):
        z = target.map(values)
        return z.fillna(fill)

    pair_h = key(h["customer_id"], h["article_id"])
    pair_x = key(c, a)
    decay = np.exp(-d.astype(float) / 30.0)

    m14 = d <= 14
    m60 = d <= 60

    out["f_pair_14d"] = mapped(h.loc[m14].groupby(pair_h.loc[m14]).size(), pair_h, pair_x)
    out["f_pair_60d"] = mapped(h.loc[m60].groupby(pair_h.loc[m60]).size(), pair_h, pair_x)
    out["f_pair_all"] = mapped(h.groupby(pair_h).size(), pair_h, pair_x)
    out["f_pair_recency"] = pair_x.map(h.groupby(pair_h)["days_ago"].min())
    out["f_pair_decay"] = mapped(decay.groupby(pair_h).sum(), pair_h, pair_x)

    out["f_user_14d"] = mapped(h.loc[m14].groupby("customer_id").size(), h["customer_id"], c)
    out["f_user_60d"] = mapped(h.loc[m60].groupby("customer_id").size(), h["customer_id"], c)
    out["f_user_all"] = mapped(h.groupby("customer_id").size(), h["customer_id"], c)
    out["f_user_recency"] = c.map(h.groupby("customer_id")["days_ago"].min())
    out["f_user_decay"] = mapped(decay.groupby(h["customer_id"]).sum(), h["customer_id"], c)
    out["f_user_unique_items"] = mapped(
        h.groupby("customer_id")["article_id"].nunique(), h["customer_id"], c
    )

    out["f_item_14d"] = mapped(h.loc[m14].groupby("article_id").size(), h["article_id"], a)
    out["f_item_60d"] = mapped(h.loc[m60].groupby("article_id").size(), h["article_id"], a)
    out["f_item_all"] = mapped(h.groupby("article_id").size(), h["article_id"], a)
    out["f_item_recency"] = a.map(h.groupby("article_id")["days_ago"].min())
    out["f_item_decay"] = mapped(decay.groupby(h["article_id"]).sum(), h["article_id"], a)

    ch2 = (pd.to_numeric(h["sales_channel_id"], errors="coerce") == 2).astype(float)
    out["f_item_channel2"] = a.map(ch2.groupby(h["article_id"]).mean()).fillna(0.0)
    out["f_user_channel2"] = c.map(ch2.groupby(h["customer_id"]).mean()).fillna(0.0)

    recent = h.loc[m60]
    for raw, col, name in (
        ("raw_i_product_type_no", "product_type_no", "f_type_60d"),
        ("raw_i_section_no", "section_no", "f_section_60d"),
        ("raw_i_garment_group_no", "garment_group_no", "f_garment_60d"),
        ("raw_i_colour_group_code", "colour_group_code", "f_colour_60d"),
        ("raw_i_department_no", "department_no", "f_department_60d"),
    ):
        kh = key(recent["customer_id"], recent[col])
        kx = key(c, X[raw])
        out[name] = mapped(recent.groupby(kh).size(), kh, kx)

    user60 = h.loc[m60].groupby("customer_id").size()
    type_key_h = key(recent["customer_id"], recent["product_type_no"])
    type_key_x = key(c, X["raw_i_product_type_no"])
    type_count = mapped(recent.groupby(type_key_h).size(), type_key_h, type_key_x)
    out["f_type_share_60d"] = type_count / c.map(user60).fillna(0.0).replace(0.0, np.nan)

    out["f_product_code_all"] = X["raw_i_product_code"].map(
        h.groupby("product_code").size()
    ).fillna(0.0)
    out["f_product_type_all"] = X["raw_i_product_type_no"].map(
        h.groupby("product_type_no").size()
    ).fillna(0.0)
    out["f_section_all"] = X["raw_i_section_no"].map(
        h.groupby("section_no").size()
    ).fillna(0.0)

    age = pd.to_numeric(X["raw_u_age"], errors="coerce")
    hist_age = pd.to_numeric(h["customer_age"], errors="coerce")
    item_age = h.assign(_age=hist_age).groupby("article_id")["_age"].mean()
    out["f_item_age_match"] = age - a.map(item_age)
    out["f_user_age"] = age
    out["f_item_product_type"] = pd.to_numeric(
        X["raw_i_product_type_no"], errors="coerce"
    )
    return out.astype(float)
