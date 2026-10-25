import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    c = X["customer_id"].to_numpy()
    a = X["article_id"].to_numpy()
    keys = pd.MultiIndex.from_arrays([c, a])

    def pair(h, name):
        if len(h):
            s = h.groupby(["customer_id", "article_id"], sort=False).size()
            out[name] = s.reindex(keys).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    def user(h, name):
        if len(h):
            out[name] = X["customer_id"].map(
                h.groupby("customer_id", sort=False).size()
            ).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    def item(h, name):
        if len(h):
            out[name] = X["article_id"].map(
                h.groupby("article_id", sort=False).size()
            ).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    h7 = history.loc[history["days_ago"] <= 7]
    h30 = history.loc[history["days_ago"] <= 30]
    h90 = history.loc[history["days_ago"] <= 90]
    h365 = history.loc[history["days_ago"] <= 365]

    pair(h7, "f_pair_7")
    pair(h30, "f_pair_30")
    pair(h90, "f_pair_90")
    pair(history, "f_pair_all")
    user(h7, "f_user_7")
    user(h30, "f_user_30")
    user(h90, "f_user_90")
    item(h7, "f_item_7")
    item(h30, "f_item_30")
    item(h90, "f_item_90")

    if len(history):
        g = history.groupby(["customer_id", "article_id"], sort=False)
        rec = g["days_ago"].min().reindex(keys)
        rv = rec.to_numpy(dtype=float)
        out["f_recency"] = rv
        out["f_recency_decay"] = np.exp(-rv / 30.0)

        wh = history.assign(
            _w=np.exp(-history["days_ago"].to_numpy(dtype=float) / 21.0)
        )
        ws = wh.groupby(
            ["customer_id", "article_id"], sort=False
        )["_w"].sum()
        out["f_weighted_pair"] = ws.reindex(keys).fillna(0).to_numpy()

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
            ("raw_i_graphical_appearance_no", "graphical_appearance_no", "f_user_graphic"),
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
        ]:
            s = h90.groupby(col, sort=False).size()
            out[name] = X[raw].map(s).fillna(0).to_numpy()

        out["f_user_items"] = X["customer_id"].map(
            history.groupby("customer_id", sort=False)["article_id"].nunique()
        ).fillna(0).to_numpy()
        out["f_item_users"] = X["article_id"].map(
            history.groupby("article_id", sort=False)["customer_id"].nunique()
        ).fillna(0).to_numpy()

        ch = h30.groupby(["customer_id", "article_id"], sort=False)["sales_channel_id"].nunique()
        out["f_pair_channels_30"] = ch.reindex(keys).fillna(0).to_numpy()
    else:
        for name in [
            "f_recency", "f_recency_decay", "f_weighted_pair",
            "f_user_recency", "f_user_product", "f_user_type",
            "f_user_department", "f_user_section", "f_user_garment",
            "f_user_colour", "f_user_graphic", "f_pop_product",
            "f_pop_type", "f_pop_department", "f_pop_section",
            "f_pop_garment", "f_user_items", "f_item_users",
            "f_pair_channels_30"
        ]:
            out[name] = 0.0

    return out.astype(float)
