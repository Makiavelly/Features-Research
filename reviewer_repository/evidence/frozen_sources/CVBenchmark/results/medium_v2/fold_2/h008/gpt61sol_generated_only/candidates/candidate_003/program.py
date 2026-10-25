import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    def single_map(column, values):
        if len(h) == 0:
            return pd.Series(0.0, index=X.index)
        s = h.groupby(column, sort=False).size()
        return pd.Series(values, index=X.index).map(s).fillna(0.0)

    def pair_map(left_columns, right_columns, values):
        if len(h) == 0:
            return pd.Series(0.0, index=X.index)
        keys_h = pd.MultiIndex.from_frame(h.loc[:, right_columns])
        s = pd.Series(np.asarray(values), index=keys_h).groupby(level=list(range(len(right_columns)))).size()
        keys_x = pd.MultiIndex.from_frame(X.loc[:, left_columns].rename(
            columns=dict(zip(left_columns, right_columns))
        ))
        return pd.Series(keys_x.map(s), index=X.index).fillna(0.0)

    def add_window(days, suffix):
        z = h.loc[h["days_ago"] <= days]
        if len(z) == 0:
            out["f_user_count_" + suffix] = 0.0
            out["f_item_count_" + suffix] = 0.0
            out["f_pair_count_" + suffix] = 0.0
            return
        us = z.groupby("customer_id", sort=False).size()
        it = z.groupby("article_id", sort=False).size()
        out["f_user_count_" + suffix] = X["customer_id"].map(us).fillna(0.0)
        out["f_item_count_" + suffix] = X["article_id"].map(it).fillna(0.0)
        out["f_pair_count_" + suffix] = pair_map(
            ["customer_id", "article_id"],
            ["customer_id", "article_id"],
            z["article_id"]
        )

    add_window(7, "7d")
    add_window(30, "30d")
    add_window(180, "180d")

    if len(h):
        rec = h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
        kx = pd.MultiIndex.from_frame(X[["customer_id", "article_id"]])
        out["f_pair_recency"] = pd.Series(kx.map(rec), index=X.index)
        ur = h.groupby("customer_id", sort=False)["days_ago"].min()
        out["f_customer_recency"] = X["customer_id"].map(ur)

        typ = h.groupby(["customer_id", "product_type_no"], sort=False).size()
        kt = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X["raw_i_product_type_no"].to_numpy()
        ])
        out["f_user_type_count"] = pd.Series(kt.map(typ), index=X.index).fillna(0.0)

        dep = h.groupby(["customer_id", "department_no"], sort=False).size()
        kd = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X["raw_i_department_no"].to_numpy()
        ])
        out["f_user_department_count"] = pd.Series(kd.map(dep), index=X.index).fillna(0.0)

        ch = h.groupby(["customer_id", "product_code"], sort=False).size()
        kc = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X["raw_i_product_code"].to_numpy()
        ])
        out["f_user_product_count"] = pd.Series(kc.map(ch), index=X.index).fillna(0.0)
    else:
        out["f_pair_recency"] = np.nan
        out["f_customer_recency"] = np.nan
        out["f_user_type_count"] = 0.0
        out["f_user_department_count"] = 0.0
        out["f_user_product_count"] = 0.0

    return out.astype(float)
