import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)
    h = history

    if len(h) == 0:
        names = [
            "f_item_all", "f_item_7", "f_item_30", "f_item_recency",
            "f_user_all", "f_user_7", "f_user_30", "f_user_recency",
            "f_pair_all", "f_pair_30", "f_item_decay", "f_user_decay",
            "f_price_item", "f_price_user", "f_cat_product_7",
            "f_cat_product_30", "f_cat_department_30", "f_cat_section_30",
            "f_cat_garment_30", "f_raw_age", "f_raw_active"
        ]
        return pd.DataFrame({c: np.zeros(n) for c in names}, index=X.index)

    h7 = h[h["days_ago"] <= 7]
    h30 = h[h["days_ago"] <= 30]

    def counts(frame, key):
        return X[key].map(frame.groupby(key).size()).fillna(0).to_numpy()

    out["f_item_all"] = counts(h, "article_id")
    out["f_item_7"] = counts(h7, "article_id")
    out["f_item_30"] = counts(h30, "article_id")
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()
    )
    out["f_user_all"] = counts(h, "customer_id")
    out["f_user_7"] = counts(h7, "customer_id")
    out["f_user_30"] = counts(h30, "customer_id")
    out["f_user_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()
    )

    keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])
    out["f_pair_all"] = h.groupby(
        ["customer_id", "article_id"]
    ).size().reindex(keys, fill_value=0).to_numpy()
    out["f_pair_30"] = h30.groupby(
        ["customer_id", "article_id"]
    ).size().reindex(keys, fill_value=0).to_numpy()

    decay = np.exp(-h["days_ago"].to_numpy() / 21.0)
    dh = h.assign(_decay=decay)
    out["f_item_decay"] = X["article_id"].map(
        dh.groupby("article_id")["_decay"].sum()
    ).fillna(0)
    out["f_user_decay"] = X["customer_id"].map(
        dh.groupby("customer_id")["_decay"].sum()
    ).fillna(0)

    out["f_price_item"] = X["article_id"].map(
        h.groupby("article_id")["price"].mean()
    )
    out["f_price_user"] = X["customer_id"].map(
        h.groupby("customer_id")["price"].mean()
    )

    for cat in ["product_code", "department_no", "section_no", "garment_group_no"]:
        for suffix, frame in [("7", h7), ("30", h30)]:
            g = frame.groupby(["customer_id", cat]).size()
            k = pd.MultiIndex.from_arrays([
                X["customer_id"].to_numpy(),
                X["raw_i_" + cat].to_numpy()
            ])
            name = "f_cat_" + cat + "_" + suffix
            out[name] = g.reindex(k, fill_value=0).to_numpy()

    out["f_raw_age"] = X["raw_u_age"]
    out["f_raw_active"] = X["raw_u_active"]
    return out.apply(pd.to_numeric, errors="coerce")
