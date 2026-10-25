import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    ck = X["customer_id"].to_numpy()
    ik = X["article_id"].to_numpy()
    pair_keys = pd.MultiIndex.from_arrays([ck, ik])

    def pair_map(frame, col, name, agg="size"):
        if len(frame) == 0:
            out[name] = np.nan
            return
        g = frame.groupby(["customer_id", "article_id"], sort=False)
        s = g.size() if agg == "size" else g[col].agg(agg)
        out[name] = s.reindex(pair_keys).to_numpy()

    def customer_map(frame, name):
        if len(frame):
            s = frame.groupby("customer_id", sort=False).size()
            out[name] = X["customer_id"].map(s).to_numpy()
        else:
            out[name] = np.nan

    def item_map(frame, name):
        if len(frame):
            s = frame.groupby("article_id", sort=False).size()
            out[name] = X["article_id"].map(s).to_numpy()
        else:
            out[name] = np.nan

    h7 = history.loc[history["days_ago"] <= 7]
    h30 = history.loc[history["days_ago"] <= 30]
    h90 = history.loc[history["days_ago"] <= 90]
    h365 = history.loc[history["days_ago"] <= 365]

    pair_map(h7, None, "f_pair_count_7d")
    pair_map(h30, None, "f_pair_count_30d")
    pair_map(h90, None, "f_pair_count_90d")
    pair_map(history, None, "f_pair_count_all")
    customer_map(h30, "f_customer_count_30d")
    customer_map(h90, "f_customer_count_90d")
    item_map(h30, "f_item_count_30d")
    item_map(h90, "f_item_count_90d")

    if len(history):
        gp = history.groupby(["customer_id", "article_id"], sort=False)
        rec = gp["days_ago"].min()
        out["f_pair_recency"] = rec.reindex(pair_keys).to_numpy()
        out["f_pair_decay"] = np.exp(
            -rec.reindex(pair_keys).to_numpy(dtype=float) / 30.0
        )
        out["f_customer_recency"] = X["customer_id"].map(
            history.groupby("customer_id", sort=False)["days_ago"].min()
        ).to_numpy()

        w = np.exp(-history["days_ago"].to_numpy(dtype=float) / 21.0)
        wh = history.assign(_w=w)
        ws = wh.groupby(["customer_id", "article_id"], sort=False)["_w"].sum()
        out["f_pair_weighted"] = ws.reindex(pair_keys).to_numpy()

        for raw, hist, name in [
            ("raw_i_product_type_no", "product_type_no", "f_customer_type"),
            ("raw_i_department_no", "department_no", "f_customer_department"),
            ("raw_i_section_no", "section_no", "f_customer_section"),
            ("raw_i_garment_group_no", "garment_group_no", "f_customer_garment"),
            ("raw_i_colour_group_code", "colour_group_code", "f_customer_colour"),
        ]:
            s = h365.groupby(["customer_id", hist], sort=False).size()
            k = pd.MultiIndex.from_arrays([ck, X[raw].to_numpy()])
            out[name] = s.reindex(k).to_numpy()
    else:
        for name in [
            "f_pair_recency", "f_pair_decay", "f_customer_recency",
            "f_pair_weighted", "f_customer_type", "f_customer_department",
            "f_customer_section", "f_customer_garment", "f_customer_colour"
        ]:
            out[name] = np.nan

    out["f_item_type_popularity"] = X["raw_i_product_type_no"].map(
        history.groupby("product_type_no", sort=False).size()
    ).to_numpy() if len(history) else np.nan
    out["f_item_department_popularity"] = X["raw_i_department_no"].map(
        history.groupby("department_no", sort=False).size()
    ).to_numpy() if len(history) else np.nan
    out["f_article_code_popularity"] = X["raw_i_product_code"].map(
        history.groupby("product_code", sort=False).size()
    ).to_numpy() if len(history) else np.nan

    return out.astype(float)
