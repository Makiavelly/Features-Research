import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)
    h = history
    cats = ["product_code", "department_no", "section_no", "garment_group_no"]
    names = [
        "f_item_all", "f_item_7", "f_item_30", "f_item_recency",
        "f_user_all", "f_user_7", "f_user_30", "f_user_recency",
        "f_pair_all", "f_pair_30", "f_item_decay", "f_user_decay",
        "f_price_item", "f_price_user"
    ]
    for cat in cats:
        names.append("f_cat_" + cat + "_7")
        names.append("f_cat_" + cat + "_30")

    if len(h) == 0:
        return pd.DataFrame({c: np.zeros(n, dtype=float) for c in names},
                            index=X.index)

    h7 = h[h["days_ago"] <= 7]
    h30 = h[h["days_ago"] <= 30]

    def mapped_count(frame, key):
        s = frame.groupby(key).size()
        return X[key].map(s).fillna(0).to_numpy()

    out["f_item_all"] = mapped_count(h, "article_id")
    out["f_item_7"] = mapped_count(h7, "article_id")
    out["f_item_30"] = mapped_count(h30, "article_id")
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()
    )

    out["f_user_all"] = mapped_count(h, "customer_id")
    out["f_user_7"] = mapped_count(h7, "customer_id")
    out["f_user_30"] = mapped_count(h30, "customer_id")
    out["f_user_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()
    )

    pair_keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(),
        X["article_id"].to_numpy()
    ])
    out["f_pair_all"] = h.groupby(
        ["customer_id", "article_id"]
    ).size().reindex(pair_keys, fill_value=0).to_numpy()
    out["f_pair_30"] = h30.groupby(
        ["customer_id", "article_id"]
    ).size().reindex(pair_keys, fill_value=0).to_numpy()

    weighted = h.assign(_w=np.exp(-h["days_ago"].to_numpy() / 21.0))
    out["f_item_decay"] = X["article_id"].map(
        weighted.groupby("article_id")["_w"].sum()
    ).fillna(0)
    out["f_user_decay"] = X["customer_id"].map(
        weighted.groupby("customer_id")["_w"].sum()
    ).fillna(0)

    out["f_price_item"] = X["article_id"].map(
        h.groupby("article_id")["price"].mean()
    )
    out["f_price_user"] = X["customer_id"].map(
        h.groupby("customer_id")["price"].mean()
    )

    for cat in cats:
        key = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X["raw_i_" + cat].to_numpy()
        ])
        for suffix, frame in [("7", h7), ("30", h30)]:
            values = frame.groupby(["customer_id", cat]).size()
            out["f_cat_" + cat + "_" + suffix] = values.reindex(
                key, fill_value=0
            ).to_numpy()

    return out[names].apply(pd.to_numeric, errors="coerce")
