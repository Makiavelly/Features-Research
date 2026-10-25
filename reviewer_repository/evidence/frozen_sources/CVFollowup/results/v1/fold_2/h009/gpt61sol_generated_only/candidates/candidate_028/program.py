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
            s = h.groupby("customer_id", sort=False).size()
            out[name] = X["customer_id"].map(s).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    def item(h, name):
        if len(h):
            s = h.groupby("article_id", sort=False).size()
            out[name] = X["article_id"].map(s).fillna(0).to_numpy()
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
        r = g["days_ago"].min().reindex(keys).to_numpy(dtype=float)
        p30 = h30.groupby(
            ["customer_id", "article_id"], sort=False
        ).size().reindex(keys).fillna(0).to_numpy(dtype=float)
        u30 = X["customer_id"].map(
            h30.groupby("customer_id", sort=False).size()
        ).fillna(0).to_numpy(dtype=float)
        i30 = X["article_id"].map(
            h30.groupby("article_id", sort=False).size()
        ).fillna(0).to_numpy(dtype=float)

        out["f_recency"] = r
        out["f_decay"] = np.exp(-r / 28.0)
        wh = history.assign(
            _w=np.exp(-history["days_ago"].to_numpy(dtype=float) / 21.0)
        )
        out["f_pair_weighted"] = wh.groupby(
            ["customer_id", "article_id"], sort=False
        )["_w"].sum().reindex(keys).fillna(0).to_numpy()
        out["f_user_recency"] = X["customer_id"].map(
            history.groupby("customer_id", sort=False)["days_ago"].min()
        ).to_numpy()
        out["f_pair_user_share"] = p30 / np.maximum(u30, 1.0)
        out["f_pair_item_share"] = p30 / np.maximum(i30, 1.0)

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
        ]:
            out[name] = X[raw].map(
                h90.groupby(col, sort=False).size()
            ).fillna(0).to_numpy()

        out["f_user_items"] = X["customer_id"].map(
            history.groupby("customer_id", sort=False)["article_id"].nunique()
        ).fillna(0).to_numpy()
        out["f_item_users"] = X["article_id"].map(
            history.groupby("article_id", sort=False)["customer_id"].nunique()
        ).fillna(0).to_numpy()
        out["f_pair_channels"] = g["sales_channel_id"].nunique().reindex(
            keys
        ).fillna(0).to_numpy()
        out["f_user_mean_price"] = X["customer_id"].map(
            h365.groupby("customer_id", sort=False)["price"].mean()
        ).to_numpy()
        out["f_item_mean_price"] = X["article_id"].map(
            h365.groupby("article_id", sort=False)["price"].mean()
        ).to_numpy()
    else:
        for name in [
            "f_recency", "f_decay", "f_pair_weighted", "f_user_recency",
            "f_pair_user_share", "f_pair_item_share", "f_user_product",
            "f_user_type", "f_user_department", "f_user_section",
            "f_user_garment", "f_user_colour", "f_pop_product", "f_pop_type",
            "f_pop_department", "f_pop_section", "f_pop_garment",
            "f_user_items", "f_item_users", "f_pair_channels",
            "f_user_mean_price", "f_item_mean_price"
        ]:
            out[name] = 0.0

    out["f_static_product"] = X["raw_i_product_code"].to_numpy(dtype=float)
    out["f_static_type"] = X["raw_i_product_type_no"].to_numpy(dtype=float)
    out["f_static_department"] = X["raw_i_department_no"].to_numpy(dtype=float)
    out["f_static_section"] = X["raw_i_section_no"].to_numpy(dtype=float)
    out["f_static_garment"] = X["raw_i_garment_group_no"].to_numpy(dtype=float)
    out["f_static_colour"] = X["raw_i_colour_group_code"].to_numpy(dtype=float)

    return out.astype(float)
