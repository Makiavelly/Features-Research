import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    c = X["customer_id"].to_numpy()
    a = X["article_id"].to_numpy()
    keys = pd.MultiIndex.from_arrays([c, a])

    def pair_value(h, value, name, fill=0.0):
        if len(h):
            s = h.groupby(["customer_id", "article_id"], sort=False)[value].agg("sum")
            out[name] = s.reindex(keys).fillna(fill).to_numpy()
        else:
            out[name] = fill

    def pair_size(h, name):
        if len(h):
            s = h.groupby(["customer_id", "article_id"], sort=False).size()
            out[name] = s.reindex(keys).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    def user_size(h, name):
        if len(h):
            s = h.groupby("customer_id", sort=False).size()
            out[name] = X["customer_id"].map(s).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    def item_size(h, name):
        if len(h):
            s = h.groupby("article_id", sort=False).size()
            out[name] = X["article_id"].map(s).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    h14 = history.loc[history["days_ago"] <= 14]
    h45 = history.loc[history["days_ago"] <= 45]
    h120 = history.loc[history["days_ago"] <= 120]
    h240 = history.loc[history["days_ago"] <= 240]

    pair_size(h14, "f_pair_recent")
    pair_size(h45, "f_pair_mid")
    pair_size(h120, "f_pair_long")
    pair_size(h240, "f_pair_history")
    user_size(h14, "f_user_recent")
    user_size(h45, "f_user_mid")
    user_size(h120, "f_user_long")
    item_size(h14, "f_item_recent")
    item_size(h45, "f_item_mid")
    item_size(h120, "f_item_long")

    if len(history):
        g = history.groupby(["customer_id", "article_id"], sort=False)
        last = g["days_ago"].min().reindex(keys).to_numpy(dtype=float)
        out["f_last_seen"] = last
        out["f_last_seen_score"] = 1.0 / (1.0 + last)

        w = np.exp(-history["days_ago"].to_numpy(dtype=float) / 12.0)
        hw = history.assign(_weight=w)
        out["f_recent_weight"] = hw.groupby(
            ["customer_id", "article_id"], sort=False
        )["_weight"].sum().reindex(keys).fillna(0).to_numpy()

        pair_value(h45, "price", "f_pair_spend_45")
        user_price = h120.groupby("customer_id", sort=False)["price"].mean()
        item_price = h120.groupby("article_id", sort=False)["price"].mean()
        out["f_user_price"] = X["customer_id"].map(user_price).to_numpy()
        out["f_item_price"] = X["article_id"].map(item_price).to_numpy()

        for raw, col, name in [
            ("raw_i_product_type_no", "product_type_no", "f_match_type"),
            ("raw_i_department_no", "department_no", "f_match_department"),
            ("raw_i_section_no", "section_no", "f_match_section"),
            ("raw_i_garment_group_no", "garment_group_no", "f_match_garment"),
            ("raw_i_colour_group_code", "colour_group_code", "f_match_colour"),
            ("raw_i_product_code", "product_code", "f_match_product"),
        ]:
            s = h120.groupby(["customer_id", col], sort=False).size()
            k = pd.MultiIndex.from_arrays([c, X[raw].to_numpy()])
            out[name] = s.reindex(k).fillna(0).to_numpy()

        out["f_user_distinct"] = X["customer_id"].map(
            h120.groupby("customer_id", sort=False)["article_id"].nunique()
        ).fillna(0).to_numpy()
        out["f_item_distinct"] = X["article_id"].map(
            h120.groupby("article_id", sort=False)["customer_id"].nunique()
        ).fillna(0).to_numpy()
        out["f_pair_channels"] = g["sales_channel_id"].nunique().reindex(
            keys
        ).fillna(0).to_numpy()
    else:
        for name in [
            "f_last_seen", "f_last_seen_score", "f_recent_weight",
            "f_pair_spend_45", "f_user_price", "f_item_price",
            "f_match_type", "f_match_department", "f_match_section",
            "f_match_garment", "f_match_colour", "f_match_product",
            "f_user_distinct", "f_item_distinct", "f_pair_channels"
        ]:
            out[name] = 0.0

    return out.astype(float)
