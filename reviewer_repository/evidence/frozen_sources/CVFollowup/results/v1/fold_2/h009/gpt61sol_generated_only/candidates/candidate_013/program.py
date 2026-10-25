import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    c = X["customer_id"].to_numpy()
    a = X["article_id"].to_numpy()
    keys = pd.MultiIndex.from_arrays([c, a])

    def pair_count(h, name):
        if len(h):
            s = h.groupby(["customer_id", "article_id"], sort=False).size()
            out[name] = s.reindex(keys).to_numpy()
        else:
            out[name] = np.nan

    def mapped(h, col, name, key):
        if len(h):
            s = h.groupby(key, sort=False).size()
            out[name] = X[col].map(s).to_numpy()
        else:
            out[name] = np.nan

    h7 = history.loc[history["days_ago"] <= 7]
    h30 = history.loc[history["days_ago"] <= 30]
    h90 = history.loc[history["days_ago"] <= 90]
    h365 = history.loc[history["days_ago"] <= 365]

    pair_count(h7, "f_pair_7d")
    pair_count(h30, "f_pair_30d")
    pair_count(h90, "f_pair_90d")
    pair_count(history, "f_pair_all")

    mapped(h7, "customer_id", "f_user_7d", "customer_id")
    mapped(h30, "customer_id", "f_user_30d", "customer_id")
    mapped(h90, "customer_id", "f_user_90d", "customer_id")
    mapped(h30, "article_id", "f_item_30d", "article_id")
    mapped(h90, "article_id", "f_item_90d", "article_id")

    if len(history):
        g = history.groupby(["customer_id", "article_id"], sort=False)
        rec = g["days_ago"].min()
        out["f_pair_recency"] = rec.reindex(keys).to_numpy()
        out["f_pair_decay"] = np.exp(-rec.reindex(keys).to_numpy(dtype=float) / 21.0)

        weighted = history.assign(
            _w=np.exp(-history["days_ago"].to_numpy(dtype=float) / 35.0)
        )
        s = weighted.groupby(
            ["customer_id", "article_id"], sort=False
        )["_w"].sum()
        out["f_pair_weighted"] = s.reindex(keys).to_numpy()

        ur = history.groupby("customer_id", sort=False)["days_ago"].min()
        out["f_user_recency"] = X["customer_id"].map(ur).to_numpy()

        for raw, col, name in [
            ("raw_i_product_type_no", "product_type_no", "f_user_type"),
            ("raw_i_department_no", "department_no", "f_user_department"),
            ("raw_i_section_no", "section_no", "f_user_section"),
            ("raw_i_garment_group_no", "garment_group_no", "f_user_garment"),
            ("raw_i_colour_group_code", "colour_group_code", "f_user_colour"),
            ("raw_i_product_code", "product_code", "f_user_product"),
        ]:
            s = h365.groupby(["customer_id", col], sort=False).size()
            k = pd.MultiIndex.from_arrays([c, X[raw].to_numpy()])
            out[name] = s.reindex(k).to_numpy()

        for raw, col, name in [
            ("raw_i_product_type_no", "product_type_no", "f_type_30d"),
            ("raw_i_department_no", "department_no", "f_department_30d"),
            ("raw_i_section_no", "section_no", "f_section_30d"),
            ("raw_i_garment_group_no", "garment_group_no", "f_garment_30d"),
            ("raw_i_product_code", "product_code", "f_product_code_30d"),
        ]:
            s = h30.groupby(col, sort=False).size()
            out[name] = X[raw].map(s).to_numpy()

        out["f_user_unique_articles"] = X["customer_id"].map(
            history.groupby("customer_id", sort=False)["article_id"].nunique()
        ).to_numpy()
        out["f_item_unique_users"] = X["article_id"].map(
            history.groupby("article_id", sort=False)["customer_id"].nunique()
        ).to_numpy()
    else:
        for name in [
            "f_pair_recency", "f_pair_decay", "f_pair_weighted",
            "f_user_recency", "f_user_type", "f_user_department",
            "f_user_section", "f_user_garment", "f_user_colour",
            "f_user_product", "f_type_30d", "f_department_30d",
            "f_section_30d", "f_garment_30d", "f_product_code_30d",
            "f_user_unique_articles", "f_item_unique_users"
        ]:
            out[name] = np.nan

    return out.astype(float)
