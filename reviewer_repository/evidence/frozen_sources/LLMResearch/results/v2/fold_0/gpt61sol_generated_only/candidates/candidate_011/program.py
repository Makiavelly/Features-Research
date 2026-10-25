import pandas as pd
import numpy as np

def modify_features(X, history):
    cats = ["product_code", "department_no", "section_no", "garment_group_no"]
    names = [
        "f_item_all", "f_item_7", "f_item_30", "f_item_recency",
        "f_user_all", "f_user_7", "f_user_30", "f_user_recency",
        "f_pair_all", "f_pair_30", "f_pair_recency",
        "f_item_decay", "f_user_decay", "f_price_item", "f_price_user"
    ]
    for c in cats:
        names += ["f_cat_" + c + "_7", "f_cat_" + c + "_30"]
    names += [
        "f_raw_age", "f_raw_active", "f_raw_club", "f_raw_news",
        "f_raw_product", "f_raw_type", "f_raw_department",
        "f_raw_section", "f_raw_garment"
    ]
    n = len(X)
    h = history
    if len(h) == 0:
        return pd.DataFrame(
            {c: np.zeros(n, dtype=float) for c in names}, index=X.index
        )

    h7 = h[h["days_ago"] <= 7]
    h30 = h[h["days_ago"] <= 30]

    def count_map(frame, col):
        return X[col].map(frame.groupby(col).size()).fillna(0).to_numpy()

    out = pd.DataFrame(index=X.index)
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
    pair = h.groupby(["customer_id", "article_id"])
    pair30 = h30.groupby(["customer_id", "article_id"])
    out["f_pair_all"] = pair.size().reindex(key, fill_value=0).to_numpy()
    out["f_pair_30"] = pair30.size().reindex(key, fill_value=0).to_numpy()
    out["f_pair_recency"] = pair["days_ago"].min().reindex(key).to_numpy()

    wh = h.assign(_w=np.exp(-h["days_ago"].to_numpy() / 21.0))
    out["f_item_decay"] = X["article_id"].map(
        wh.groupby("article_id")["_w"].sum()).fillna(0)
    out["f_user_decay"] = X["customer_id"].map(
        wh.groupby("customer_id")["_w"].sum()).fillna(0)
    out["f_price_item"] = X["article_id"].map(
        h.groupby("article_id")["price"].mean())
    out["f_price_user"] = X["customer_id"].map(
        h.groupby("customer_id")["price"].mean())

    for c in cats:
        k = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X["raw_i_" + c].to_numpy()
        ])
        for suffix, frame in [("7", h7), ("30", h30)]:
            v = frame.groupby(["customer_id", c]).size()
            out["f_cat_" + c + "_" + suffix] = v.reindex(
                k, fill_value=0).to_numpy()

    static = {
        "f_raw_age": "raw_u_age",
        "f_raw_active": "raw_u_active",
        "f_raw_club": "raw_u_club_member_status",
        "f_raw_news": "raw_u_fashion_news_frequency",
        "f_raw_product": "raw_i_product_code",
        "f_raw_type": "raw_i_product_type_no",
        "f_raw_department": "raw_i_department_no",
        "f_raw_section": "raw_i_section_no",
        "f_raw_garment": "raw_i_garment_group_no"
    }
    for name, col in static.items():
        out[name] = X[col].to_numpy()

    return out[names].apply(pd.to_numeric, errors="coerce")
