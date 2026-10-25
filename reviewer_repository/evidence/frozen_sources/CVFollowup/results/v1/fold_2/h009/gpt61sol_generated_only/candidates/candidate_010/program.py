import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    ck = X["customer_id"].to_numpy()
    ak = X["article_id"].to_numpy()
    pk = pd.MultiIndex.from_arrays([ck, ak])

    def pair_count(frame, name):
        if len(frame):
            s = frame.groupby(["customer_id", "article_id"], sort=False).size()
            out[name] = s.reindex(pk).to_numpy()
        else:
            out[name] = np.nan

    def user_count(frame, name):
        if len(frame):
            s = frame.groupby("customer_id", sort=False).size()
            out[name] = X["customer_id"].map(s).to_numpy()
        else:
            out[name] = np.nan

    def item_count(frame, name):
        if len(frame):
            s = frame.groupby("article_id", sort=False).size()
            out[name] = X["article_id"].map(s).to_numpy()
        else:
            out[name] = np.nan

    h7 = history.loc[history["days_ago"] <= 7]
    h30 = history.loc[history["days_ago"] <= 30]
    h90 = history.loc[history["days_ago"] <= 90]
    h365 = history.loc[history["days_ago"] <= 365]

    pair_count(h7, "f_pair_7")
    pair_count(h30, "f_pair_30")
    pair_count(h90, "f_pair_90")
    pair_count(history, "f_pair_all")
    user_count(h30, "f_user_30")
    user_count(h90, "f_user_90")
    item_count(h30, "f_item_30")
    item_count(h90, "f_item_90")

    if len(history):
        g = history.groupby(["customer_id", "article_id"], sort=False)
        r = g["days_ago"].min()
        out["f_pair_recency"] = r.reindex(pk).to_numpy()
        out["f_pair_last_decay"] = np.exp(
            -r.reindex(pk).to_numpy(dtype=float) / 35.0
        )
        out["f_user_recency"] = X["customer_id"].map(
            history.groupby("customer_id", sort=False)["days_ago"].min()
        ).to_numpy()

        w = np.exp(-history["days_ago"].to_numpy(dtype=float) / 28.0)
        hw = history.assign(_weight=w)
        ws = hw.groupby(["customer_id", "article_id"], sort=False)["_weight"].sum()
        out["f_pair_weighted"] = ws.reindex(pk).to_numpy()

        cu = history.groupby("customer_id", sort=False)["article_id"].nunique()
        ai = history.groupby("article_id", sort=False)["customer_id"].nunique()
        out["f_user_unique_items"] = X["customer_id"].map(cu).to_numpy()
        out["f_item_unique_users"] = X["article_id"].map(ai).to_numpy()

        for raw, hist, name in [
            ("raw_i_product_type_no", "product_type_no", "f_user_type"),
            ("raw_i_department_no", "department_no", "f_user_department"),
            ("raw_i_section_no", "section_no", "f_user_section"),
            ("raw_i_garment_group_no", "garment_group_no", "f_user_garment"),
            ("raw_i_colour_group_code", "colour_group_code", "f_user_colour"),
        ]:
            s = h365.groupby(["customer_id", hist], sort=False).size()
            k = pd.MultiIndex.from_arrays([ck, X[raw].to_numpy()])
            out[name] = s.reindex(k).to_numpy()

        for raw, hist, name in [
            ("raw_i_product_type_no", "product_type_no", "f_type_popularity"),
            ("raw_i_department_no", "department_no", "f_department_popularity"),
            ("raw_i_section_no", "section_no", "f_section_popularity"),
            ("raw_i_garment_group_no", "garment_group_no", "f_garment_popularity"),
        ]:
            s = h90.groupby(hist, sort=False).size()
            out[name] = X[raw].map(s).to_numpy()

        up = history.groupby("customer_id", sort=False)["price"].mean()
        ip = history.groupby("article_id", sort=False)["price"].mean()
        out["f_user_mean_price"] = X["customer_id"].map(up).to_numpy()
        out["f_item_mean_price"] = X["article_id"].map(ip).to_numpy()
    else:
        for name in [
            "f_pair_recency", "f_pair_last_decay", "f_user_recency",
            "f_pair_weighted", "f_user_unique_items", "f_item_unique_users",
            "f_user_type", "f_user_department", "f_user_section",
            "f_user_garment", "f_user_colour", "f_type_popularity",
            "f_department_popularity", "f_section_popularity",
            "f_garment_popularity", "f_user_mean_price", "f_item_mean_price"
        ]:
            out[name] = np.nan

    return out.astype(float)
