import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h7 = history[history["days_ago"] <= 7]
    h30 = history[history["days_ago"] <= 30]
    h90 = history[history["days_ago"] <= 90]

    def lookup(frame, left, right, kind="size"):
        if kind == "min":
            s = frame.groupby(["customer_id", right])["days_ago"].min()
        else:
            s = frame.groupby(["customer_id", right]).size()
        ix = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[left].to_numpy()]
        )
        return s.reindex(ix).to_numpy()

    def item(frame):
        return X["article_id"].map(frame.groupby("article_id").size()).fillna(0)

    def cust(frame):
        return X["customer_id"].map(frame.groupby("customer_id").size()).fillna(0)

    out["f_age"] = X["raw_u_age"]
    out["f_product_type"] = X["raw_i_product_type_no"]
    out["f_colour"] = X["raw_i_colour_group_code"]
    out["f_department"] = X["raw_i_department_no"]
    out["f_section"] = X["raw_i_section_no"]
    out["f_garment"] = X["raw_i_garment_group_no"]

    i7 = item(h7)
    i30 = item(h30)
    iall = item(history)
    c7 = cust(h7)
    c30 = cust(h30)
    call = cust(history)
    out["f_item_pop7"] = np.log1p(i7)
    out["f_item_pop30"] = np.log1p(i30)
    out["f_item_popall"] = np.log1p(iall)
    out["f_item_recent_share"] = i7 / (i30 + 1)
    out["f_item_recency"] = X["article_id"].map(
        history.groupby("article_id")["days_ago"].min()
    )
    out["f_customer_buy7"] = np.log1p(c7)
    out["f_customer_buy30"] = np.log1p(c30)
    out["f_customer_buyall"] = np.log1p(call)
    out["f_customer_recent_share"] = c7 / (c30 + 1)
    out["f_customer_recency"] = X["customer_id"].map(
        history.groupby("customer_id")["days_ago"].min()
    )

    pair7 = lookup(h7, "article_id", "article_id")
    pair30 = lookup(h30, "article_id", "article_id")
    pairall = lookup(history, "article_id", "article_id")
    out["f_pair7"] = np.log1p(np.nan_to_num(pair7, nan=0))
    out["f_pair30"] = np.log1p(np.nan_to_num(pair30, nan=0))
    out["f_pairall"] = np.log1p(np.nan_to_num(pairall, nan=0))
    out["f_pair_recency"] = lookup(history, "article_id", "article_id", "min")

    for raw, histcol, name in [
        ("raw_i_product_type_no", "product_type_no", "type"),
        ("raw_i_colour_group_code", "colour_group_code", "colour"),
        ("raw_i_department_no", "department_no", "department"),
        ("raw_i_section_no", "section_no", "section"),
        ("raw_i_garment_group_no", "garment_group_no", "garment"),
    ]:
        a7 = lookup(h7, raw, histcol)
        a30 = lookup(h30, raw, histcol)
        out["f_aff_" + name + "7"] = np.log1p(np.nan_to_num(a7, nan=0))
        out["f_aff_" + name + "30"] = np.log1p(np.nan_to_num(a30, nan=0))

    out["f_item_price"] = X["article_id"].map(
        history.groupby("article_id")["price"].mean()
    )
    return out.replace([np.inf, -np.inf], np.nan)
