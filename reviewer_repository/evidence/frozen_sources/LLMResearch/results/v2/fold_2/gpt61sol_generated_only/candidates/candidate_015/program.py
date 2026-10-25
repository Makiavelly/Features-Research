import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h7 = history[history["days_ago"] <= 7]
    h30 = history[history["days_ago"] <= 30]
    h90 = history[history["days_ago"] <= 90]

    for a, b in [
        ("f_age", "raw_u_age"),
        ("f_user_active", "raw_u_active"),
        ("f_club", "raw_u_club_member_status"),
        ("f_product_code", "raw_i_product_code"),
        ("f_product_type", "raw_i_product_type_no"),
        ("f_colour", "raw_i_colour_group_code"),
        ("f_colour_master", "raw_i_perceived_colour_master_id"),
        ("f_department", "raw_i_department_no"),
        ("f_index_group", "raw_i_index_group_no"),
        ("f_section", "raw_i_section_no"),
        ("f_garment", "raw_i_garment_group_no"),
    ]:
        out[a] = X[b]

    def lookup(frame, xcol, hcol, stat="size"):
        if stat == "min":
            s = frame.groupby(["customer_id", hcol])["days_ago"].min()
        else:
            s = frame.groupby(["customer_id", hcol]).size()
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[xcol].to_numpy()]
        )
        return s.reindex(keys).to_numpy()

    def pop(frame, col):
        return X[col].map(frame.groupby(col).size()).fillna(0)

    i7 = pop(h7, "article_id")
    i30 = pop(h30, "article_id")
    ia = pop(history, "article_id")
    c7 = pop(h7, "customer_id")
    c30 = pop(h30, "customer_id")
    ca = pop(history, "customer_id")

    out["f_item_count_7"] = np.log1p(i7)
    out["f_item_count_30"] = np.log1p(i30)
    out["f_item_count_all"] = np.log1p(ia)
    out["f_item_recent_ratio"] = i7 / (i30 + 1)
    out["f_item_recency"] = X["article_id"].map(
        history.groupby("article_id")["days_ago"].min()
    )
    out["f_customer_count_7"] = np.log1p(c7)
    out["f_customer_count_30"] = np.log1p(c30)
    out["f_customer_count_all"] = np.log1p(ca)
    out["f_customer_recent_ratio"] = c7 / (c30 + 1)
    out["f_customer_recency"] = X["customer_id"].map(
        history.groupby("customer_id")["days_ago"].min()
    )

    p7 = lookup(h7, "article_id", "article_id")
    p30 = lookup(h30, "article_id", "article_id")
    pa = lookup(history, "article_id", "article_id")
    out["f_pair_count_7"] = np.log1p(np.nan_to_num(p7, nan=0))
    out["f_pair_count_30"] = np.log1p(np.nan_to_num(p30, nan=0))
    out["f_pair_count_all"] = np.log1p(np.nan_to_num(pa, nan=0))
    out["f_pair_recency"] = lookup(history, "article_id", "article_id", "min")

    for raw, hc, name in [
        ("raw_i_product_code", "product_code", "product"),
        ("raw_i_product_type_no", "product_type_no", "type"),
        ("raw_i_colour_group_code", "colour_group_code", "colour"),
        ("raw_i_department_no", "department_no", "department"),
        ("raw_i_section_no", "section_no", "section"),
        ("raw_i_garment_group_no", "garment_group_no", "garment"),
    ]:
        v = lookup(h90, raw, hc)
        out["f_affinity_" + name] = np.log1p(np.nan_to_num(v, nan=0))

    out["f_item_mean_price"] = X["article_id"].map(
        history.groupby("article_id")["price"].mean()
    )
    out["f_customer_mean_price"] = X["customer_id"].map(
        history.groupby("customer_id")["price"].mean()
    )
    return out.replace([np.inf, -np.inf], np.nan)
