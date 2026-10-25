import pandas as pd
import numpy as np

def modify_features(X, history):
    n = len(X)
    out = pd.DataFrame(index=X.index)

    def add_static(src, name):
        out[name] = pd.to_numeric(X[src], errors="coerce").to_numpy()

    def add_single(hcol, xcol, name, frame=None, agg="size"):
        h = history if frame is None else frame
        if len(h) == 0:
            out[name] = np.zeros(n)
            return
        if agg == "size":
            s = h.groupby(hcol).size()
        else:
            s = h.groupby(hcol)[agg[0]].agg(agg[1])
        out[name] = X[xcol].map(s).fillna(0).to_numpy()

    def add_pair(hkeys, xkeys, name, frame=None):
        h = history if frame is None else frame
        if len(h) == 0:
            out[name] = np.zeros(n)
            return
        left = X[list(xkeys)].copy()
        left["__row__"] = np.arange(n)
        right = h[list(hkeys)].copy()
        right["__v__"] = 1
        g = right.groupby(list(hkeys), as_index=False)["__v__"].sum()
        z = left.merge(g, how="left", left_on=list(xkeys), right_on=list(hkeys),
                       sort=False)["__v__"].fillna(0)
        out[name] = z.to_numpy()

    h7 = history.loc[history["days_ago"] <= 7]
    h30 = history.loc[history["days_ago"] <= 30]
    h90 = history.loc[history["days_ago"] <= 90]

    add_single("article_id", "article_id", "f_item_count_all")
    add_single("article_id", "article_id", "f_item_count_7d", h7)
    add_single("article_id", "article_id", "f_item_count_30d", h30)
    add_single("article_id", "article_id", "f_item_count_90d", h90)

    add_single("customer_id", "customer_id", "f_user_count_all")
    add_single("customer_id", "customer_id", "f_user_count_7d", h7)
    add_single("customer_id", "customer_id", "f_user_count_30d", h30)
    add_single("customer_id", "customer_id", "f_user_count_90d", h90)

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

    add_pair(["customer_id", "article_id"], ["customer_id", "article_id"],
             "f_user_item_count")
    add_pair(["customer_id", "article_id"], ["customer_id", "article_id"],
             "f_user_item_count_30d", h30)

    for hc, xc, tag in [
        ("product_code", "raw_i_product_code", "product"),
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
        ("garment_group_no", "raw_i_garment_group_no", "garment"),
        ("colour_group_code", "raw_i_colour_group_code", "colour"),
    ]:
        add_pair(["customer_id", hc], ["customer_id", xc],
                 "f_user_" + tag + "_count")
        add_pair(["customer_id", hc], ["customer_id", xc],
                 "f_user_" + tag + "_count_30d", h30)

    for c in [
        "raw_u_age", "raw_u_fn", "raw_u_active",
        "raw_u_club_member_status", "raw_u_fashion_news_frequency",
        "raw_i_product_code", "raw_i_product_type_no",
        "raw_i_graphical_appearance_no", "raw_i_colour_group_code",
        "raw_i_perceived_colour_value_id",
        "raw_i_perceived_colour_master_id", "raw_i_department_no",
        "raw_i_index_group_no", "raw_i_section_no",
        "raw_i_garment_group_no"
    ]:
        add_static(c, "f_static_" + c[6:])

    return out.replace([np.inf, -np.inf], np.nan)
