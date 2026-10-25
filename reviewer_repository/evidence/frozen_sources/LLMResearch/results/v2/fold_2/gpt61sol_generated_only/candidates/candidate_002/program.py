import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h7 = history[history["days_ago"] <= 7]
    h30 = history[history["days_ago"] <= 30]
    h90 = history[history["days_ago"] <= 90]

    out["f_age"] = X["raw_u_age"]
    out["f_user_active"] = X["raw_u_active"]
    out["f_club"] = X["raw_u_club_member_status"]
    out["f_product_code"] = X["raw_i_product_code"]
    out["f_product_type"] = X["raw_i_product_type_no"]
    out["f_colour"] = X["raw_i_colour_group_code"]
    out["f_colour_master"] = X["raw_i_perceived_colour_master_id"]
    out["f_department"] = X["raw_i_department_no"]
    out["f_index_group"] = X["raw_i_index_group_no"]
    out["f_section"] = X["raw_i_section_no"]
    out["f_garment"] = X["raw_i_garment_group_no"]

    def keymap(frame, cols, value):
        s = frame.groupby(cols).size()
        k = pd.MultiIndex.from_arrays([X[c].to_numpy() for c in cols])
        return s.reindex(k, fill_value=0).to_numpy()

    def recmap(frame, col):
        return X[col].map(frame.groupby(col)["days_ago"].min())

    out["f_item_count_7"] = np.log1p(X["article_id"].map(h7.groupby("article_id").size()).fillna(0))
    out["f_item_count_30"] = np.log1p(X["article_id"].map(h30.groupby("article_id").size()).fillna(0))
    out["f_item_count_all"] = np.log1p(X["article_id"].map(history.groupby("article_id").size()).fillna(0))
    out["f_item_recency"] = recmap(history, "article_id")

    out["f_customer_count_7"] = np.log1p(X["customer_id"].map(h7.groupby("customer_id").size()).fillna(0))
    out["f_customer_count_30"] = np.log1p(X["customer_id"].map(h30.groupby("customer_id").size()).fillna(0))
    out["f_customer_count_all"] = np.log1p(X["customer_id"].map(history.groupby("customer_id").size()).fillna(0))
    out["f_customer_recency"] = recmap(history, "customer_id")

    out["f_pair_count"] = np.log1p(keymap(history, ["customer_id", "article_id"], 1))
    out["f_pair_count_7"] = np.log1p(keymap(h7, ["customer_id", "article_id"], 1))
    out["f_pair_count_30"] = np.log1p(keymap(h30, ["customer_id", "article_id"], 1))
    out["f_pair_recency"] = keymap(history, ["customer_id", "article_id"], 1) * 0.0
    pair_rec = history.groupby(["customer_id", "article_id"])["days_ago"].min()
    pk = pd.MultiIndex.from_arrays([X["customer_id"].to_numpy(), X["article_id"].to_numpy()])
    out["f_pair_recency"] = pair_rec.reindex(pk).to_numpy()

    for raw, hc, nm in [
        ("raw_i_product_code", "product_code", "product"),
        ("raw_i_product_type_no", "product_type_no", "type"),
        ("raw_i_colour_group_code", "colour_group_code", "colour"),
        ("raw_i_department_no", "department_no", "department"),
        ("raw_i_section_no", "section_no", "section"),
        ("raw_i_garment_group_no", "garment_group_no", "garment"),
    ]:
        out["f_affinity_" + nm] = np.log1p(keymap(h90, ["customer_id", hc], 1))

    out["f_item_mean_price"] = X["article_id"].map(history.groupby("article_id")["price"].mean())
    out["f_customer_mean_price"] = X["customer_id"].map(history.groupby("customer_id")["price"].mean())
    return out.replace([np.inf, -np.inf], np.nan)
