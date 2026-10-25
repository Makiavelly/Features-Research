import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)
    ck = X["customer_id"].to_numpy()
    ik = X["article_id"].to_numpy()
    keys = pd.MultiIndex.from_arrays([ck, ik])

    def pair_count(frame, name):
        if len(frame):
            s = frame.groupby(["customer_id", "article_id"], sort=False).size()
            out[name] = s.reindex(keys).to_numpy()
        else:
            out[name] = np.nan

    def cust_count(frame, name):
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
    h180 = history.loc[history["days_ago"] <= 180]

    pair_count(h7, "f_pair_count_7d")
    pair_count(h30, "f_pair_count_30d")
    pair_count(h180, "f_pair_count_180d")
    pair_count(history, "f_pair_count_all")

    cust_count(h7, "f_customer_count_7d")
    cust_count(h30, "f_customer_count_30d")
    cust_count(h180, "f_customer_count_180d")
    item_count(h7, "f_item_count_7d")
    item_count(h30, "f_item_count_30d")
    item_count(h180, "f_item_count_180d")

    if len(history):
        last_pair = history.groupby(
            ["customer_id", "article_id"], sort=False
        )["days_ago"].min()
        last_customer = history.groupby(
            "customer_id", sort=False
        )["days_ago"].min()
        out["f_pair_recency"] = last_pair.reindex(keys).to_numpy()
        out["f_customer_recency"] = X["customer_id"].map(last_customer).to_numpy()

        p30 = h30.groupby(["customer_id", "article_id"], sort=False).size()
        c30 = h30.groupby("customer_id", sort=False).size()
        p180 = h180.groupby(["customer_id", "article_id"], sort=False).size()
        c180 = h180.groupby("customer_id", sort=False).size()
        a30 = h30.groupby("article_id", sort=False).size()
        allc = history.groupby("customer_id", sort=False).size()
        alli = history.groupby("article_id", sort=False).size()

        pv30 = p30.reindex(keys).to_numpy(dtype=float)
        cv30 = X["customer_id"].map(c30).to_numpy(dtype=float)
        pv180 = p180.reindex(keys).to_numpy(dtype=float)
        cv180 = X["customer_id"].map(c180).to_numpy(dtype=float)
        av30 = X["article_id"].map(a30).to_numpy(dtype=float)
        ac = X["customer_id"].map(allc).to_numpy(dtype=float)
        ai = X["article_id"].map(alli).to_numpy(dtype=float)

        out["f_pair_share_customer_30d"] = pv30 / np.maximum(cv30, 1)
        out["f_pair_share_customer_180d"] = pv180 / np.maximum(cv180, 1)
        out["f_item_share_30d"] = pv30 / np.maximum(av30, 1)
        out["f_customer_item_affinity"] = (
            pv180 / np.maximum(cv180 * ai / max(float(len(history)), 1), 1e-6)
        )
    else:
        for name in [
            "f_pair_recency", "f_customer_recency",
            "f_pair_share_customer_30d", "f_pair_share_customer_180d",
            "f_item_share_30d", "f_customer_item_affinity"
        ]:
            out[name] = np.nan

    if len(history):
        for raw, hist, name in [
            ("raw_i_product_type_no", "product_type_no", "f_customer_type_180d"),
            ("raw_i_department_no", "department_no", "f_customer_department_180d"),
            ("raw_i_section_no", "section_no", "f_customer_section_180d"),
            ("raw_i_garment_group_no", "garment_group_no", "f_customer_garment_180d"),
        ]:
            s = h180.groupby(["customer_id", hist], sort=False).size()
            k = pd.MultiIndex.from_arrays([ck, X[raw].to_numpy()])
            out[name] = s.reindex(k).to_numpy()
    else:
        for name in [
            "f_customer_type_180d", "f_customer_department_180d",
            "f_customer_section_180d", "f_customer_garment_180d"
        ]:
            out[name] = np.nan

    out["f_item_type"] = X["raw_i_product_type_no"].to_numpy(dtype=float)
    out["f_item_department"] = X["raw_i_department_no"].to_numpy(dtype=float)
    out["f_item_section"] = X["raw_i_section_no"].to_numpy(dtype=float)
    return out.astype(float)
