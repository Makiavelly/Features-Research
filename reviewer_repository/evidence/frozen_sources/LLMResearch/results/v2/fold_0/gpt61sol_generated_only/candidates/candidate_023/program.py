import pandas as pd
import numpy as np

def modify_features(X, history):
    cats = ["product_code", "product_type_no", "department_no", "section_no"]
    names = [
        "f_item_all", "f_item_7", "f_item_30", "f_item_recency",
        "f_user_all", "f_user_7", "f_user_30", "f_user_recency",
        "f_pair_all", "f_pair_7", "f_pair_30", "f_pair_recency",
        "f_item_decay", "f_user_decay", "f_price_item", "f_price_user",
        "f_item_users_7", "f_item_users_30", "f_user_items_7",
        "f_user_items_30"
    ]
    for c in cats:
        names += ["f_cat_" + c + "_7", "f_cat_" + c + "_30"]

    n = len(X)
    h = history
    if len(h) == 0:
        return pd.DataFrame(
            {c: np.zeros(n, dtype=float) for c in names}, index=X.index
        )

    h7 = h[h["days_ago"] <= 7]
    h30 = h[h["days_ago"] <= 30]
    out = pd.DataFrame(index=X.index)

    def count_map(frame, col):
        return X[col].map(frame.groupby(col).size()).fillna(0).to_numpy()

    out["f_item_all"] = count_map(h, "article_id")
    out["f_item_7"] = count_map(h7, "article_id")
    out["f_item_30"] = count_map(h30, "article_id")
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id")["days_ago"].min()
    )
    out["f_user_all"] = count_map(h, "customer_id")
    out["f_user_7"] = count_map(h7, "customer_id")
    out["f_user_30"] = count_map(h30, "customer_id")
    out["f_user_recency"] = X["customer_id"].map(
        h.groupby("customer_id")["days_ago"].min()
    )

    key = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])
    out["f_pair_all"] = h.groupby(
        ["customer_id", "article_id"]
    ).size().reindex(key, fill_value=0).to_numpy()
    out["f_pair_7"] = h7.groupby(
        ["customer_id", "article_id"]
    ).size().reindex(key, fill_value=0).to_numpy()
    out["f_pair_30"] = h30.groupby(
        ["customer_id", "article_id"]
    ).size().reindex(key, fill_value=0).to_numpy()
    out["f_pair_recency"] = h.groupby(
        ["customer_id", "article_id"]
    )["days_ago"].min().reindex(key).to_numpy()

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
    out["f_item_users_7"] = X["article_id"].map(
        h7.groupby("article_id")["customer_id"].nunique()
    ).fillna(0)
    out["f_item_users_30"] = X["article_id"].map(
        h30.groupby("article_id")["customer_id"].nunique()
    ).fillna(0)
    out["f_user_items_7"] = X["customer_id"].map(
        h7.groupby("customer_id")["article_id"].nunique()
    ).fillna(0)
    out["f_user_items_30"] = X["customer_id"].map(
        h30.groupby("customer_id")["article_id"].nunique()
    ).fillna(0)

    for c in cats:
        key = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X["raw_i_" + c].to_numpy()
        ])
        for suffix, frame in [("7", h7), ("30", h30)]:
            values = frame.groupby(["customer_id", c]).size()
            out["f_cat_" + c + "_" + suffix] = values.reindex(
                key, fill_value=0
            ).to_numpy()

    return out[names].apply(pd.to_numeric, errors="coerce")
