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
            out[name] = s.reindex(keys).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    def user_count(h, name):
        if len(h):
            s = h.groupby("customer_id", sort=False).size()
            out[name] = X["customer_id"].map(s).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    def item_count(h, name):
        if len(h):
            s = h.groupby("article_id", sort=False).size()
            out[name] = X["article_id"].map(s).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    h7 = history.loc[history["days_ago"] <= 7]
    h30 = history.loc[history["days_ago"] <= 30]
    h90 = history.loc[history["days_ago"] <= 90]
    h180 = history.loc[history["days_ago"] <= 180]
    h365 = history.loc[history["days_ago"] <= 365]

    pair_count(h7, "f_pair_7d")
    pair_count(h30, "f_pair_30d")
    pair_count(h90, "f_pair_90d")
    pair_count(h180, "f_pair_180d")
    user_count(h7, "f_user_7d")
    user_count(h30, "f_user_30d")
    user_count(h90, "f_user_90d")
    item_count(h7, "f_item_7d")
    item_count(h30, "f_item_30d")
    item_count(h90, "f_item_90d")

    if len(history):
        gp = history.groupby(["customer_id", "article_id"], sort=False)
        rec = gp["days_ago"].min().reindex(keys)
        rv = rec.to_numpy(dtype=float)
        out["f_pair_recency"] = rv
        out["f_pair_decay"] = np.exp(-rv / 28.0)

        w = history.assign(
            _w=np.exp(-history["days_ago"].to_numpy(dtype=float) / 21.0)
        )
        ws = w.groupby(
            ["customer_id", "article_id"], sort=False
        )["_w"].sum()
        out["f_pair_weighted"] = ws.reindex(keys).fillna(0).to_numpy()

        out["f_user_recency"] = X["customer_id"].map(
            history.groupby("customer_id", sort=False)["days_ago"].min()
        ).to_numpy()

        for raw, col, name in [
            ("raw_i_product_code", "product_code", "f_user_product"),
            ("raw_i_product_type_no", "product_type_no", "f_user_type"),
            ("raw_i_department_no", "department_no", "f_user_department"),
            ("raw_i_section_no", "section_no", "f_user_section"),
            ("raw_i_garment_group_no", "garment_group_no", "f_user_garment"),
            ("raw_i_colour_group_code", "colour_group_code", "f_user_colour"),
        ]:
            s = h365.groupby(["customer_id", col], sort=False).size()
            k = pd.MultiIndex.from_arrays([c, X[raw].to_numpy()])
            out[name] = s.reindex(k).fillna(0).to_numpy()

        for raw, col, name in [
            ("raw_i_product_code", "product_code", "f_pop_product"),
            ("raw_i_product_type_no", "product_type_no", "f_pop_type"),
            ("raw_i_department_no", "department_no", "f_pop_department"),
            ("raw_i_section_no", "section_no", "f_pop_section"),
            ("raw_i_garment_group_no", "garment_group_no", "f_pop_garment"),
            ("raw_i_colour_group_code", "colour_group_code", "f_pop_colour"),
        ]:
            s = h90.groupby(col, sort=False).size()
            out[name] = X[raw].map(s).fillna(0).to_numpy()

        out["f_user_unique_items"] = X["customer_id"].map(
            history.groupby("customer_id", sort=False)["article_id"].nunique()
        ).fillna(0).to_numpy()
        out["f_item_unique_users"] = X["article_id"].map(
            history.groupby("article_id", sort=False)["customer_id"].nunique()
        ).fillna(0).to_numpy()

        ch = h30.groupby(
            ["customer_id", "article_id"], sort=False
        )["sales_channel_id"].nunique()
        out["f_pair_channels"] = ch.reindex(keys).fillna(0).to_numpy()

        for raw, col, name in [
            ("raw_i_product_type_no", "product_type_no", "f_type_recency"),
            ("raw_i_department_no", "department_no", "f_department_recency"),
            ("raw_i_section_no", "section_no", "f_section_recency"),
        ]:
            s = h365.groupby(["customer_id", col], sort=False)["days_ago"].min()
            k = pd.MultiIndex.from_arrays([c, X[raw].to_numpy()])
            out[name] = s.reindex(k).to_numpy()
    else:
        for name in [
            "f_pair_recency", "f_pair_decay", "f_pair_weighted",
            "f_user_recency", "f_user_product", "f_user_type",
            "f_user_department", "f_user_section", "f_user_garment",
            "f_user_colour", "f_pop_product", "f_pop_type",
            "f_pop_department", "f_pop_section", "f_pop_garment",
            "f_pop_colour", "f_user_unique_items", "f_item_unique_users",
            "f_pair_channels", "f_type_recency", "f_department_recency",
            "f_section_recency"
        ]:
            out[name] = 0.0

    return out.astype(float)
