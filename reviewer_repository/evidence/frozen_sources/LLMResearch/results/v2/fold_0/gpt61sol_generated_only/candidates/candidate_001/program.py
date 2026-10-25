import pandas as pd
import numpy as np

def modify_features(X, history):
    n = len(X)
    out = pd.DataFrame(index=X.index)

    if history is None or len(history) == 0:
        for c in [
            "f_pair_recency", "f_pair_count", "f_user_count_7d",
            "f_user_count_30d", "f_user_count_all", "f_item_count_7d",
            "f_item_count_30d", "f_item_count_90d", "f_item_count_all",
            "f_user_recency", "f_item_recency", "f_article_price",
            "f_user_price", "f_user_type_count", "f_user_section_count",
            "f_product_code", "f_product_type", "f_department",
            "f_section", "f_garment_group"
        ]:
            out[c] = 0.0
        return out

    h = history
    cust = X["customer_id"]
    item = X["article_id"]

    def mp(series, key, default=0.0):
        return key.map(series).fillna(default).to_numpy()

    pair = h.groupby(["customer_id", "article_id"])["days_ago"].agg(
        pair_recency="min", pair_count="size"
    )
    pair_keys = pd.MultiIndex.from_arrays([cust.to_numpy(), item.to_numpy()])
    out["f_pair_recency"] = pd.Series(pair_recency_map := pair["pair_recency"], index=pair.index).reindex(pair_keys).fillna(9999).to_numpy()
    out["f_pair_count"] = pd.Series(pair["pair_count"], index=pair.index).reindex(pair_keys).fillna(0).to_numpy()

    for d, name in [(7, "f_user_count_7d"), (30, "f_user_count_30d")]:
        s = h.loc[h["days_ago"] <= d].groupby("customer_id").size()
        out[name] = mp(s, cust)

    s = h.groupby("customer_id").size()
    out["f_user_count_all"] = mp(s, cust)

    for d, name in [(7, "f_item_count_7d"), (30, "f_item_count_30d"), (90, "f_item_count_90d")]:
        s = h.loc[h["days_ago"] <= d].groupby("article_id").size()
        out[name] = mp(s, item)

    s = h.groupby("article_id").size()
    out["f_item_count_all"] = mp(s, item)

    out["f_user_recency"] = mp(h.groupby("customer_id")["days_ago"].min(), cust, 9999)
    out["f_item_recency"] = mp(h.groupby("article_id")["days_ago"].min(), item, 9999)

    out["f_article_price"] = mp(h.groupby("article_id")["price"].mean(), item)
    out["f_user_price"] = mp(h.groupby("customer_id")["price"].mean(), cust)

    def category_feature(hist_col, raw_col, name, window=30):
        hh = h.loc[h["days_ago"] <= window]
        g = hh.groupby(["customer_id", hist_col]).size()
        keys = pd.MultiIndex.from_arrays([
            cust.to_numpy(), X[raw_col].to_numpy()
        ])
        out[name] = pd.Series(g).reindex(keys).fillna(0).to_numpy()

    category_feature("product_type_no", "raw_i_product_type_no",
                     "f_user_type_count", 30)
    category_feature("section_no", "raw_i_section_no",
                     "f_user_section_count", 30)

    out["f_product_code"] = X["raw_i_product_code"].to_numpy(dtype=float)
    out["f_product_type"] = X["raw_i_product_type_no"].to_numpy(dtype=float)
    out["f_department"] = X["raw_i_department_no"].to_numpy(dtype=float)
    out["f_section"] = X["raw_i_section_no"].to_numpy(dtype=float)
    out["f_garment_group"] = X["raw_i_garment_group_no"].to_numpy(dtype=float)

    out["f_item_count_7d"] = np.log1p(out["f_item_count_7d"])
    out["f_item_count_30d"] = np.log1p(out["f_item_count_30d"])
    out["f_item_count_90d"] = np.log1p(out["f_item_count_90d"])
    out["f_item_count_all"] = np.log1p(out["f_item_count_all"])
    out["f_user_count_7d"] = np.log1p(out["f_user_count_7d"])
    out["f_user_count_30d"] = np.log1p(out["f_user_count_30d"])
    out["f_user_count_all"] = np.log1p(out["f_user_count_all"])
    out["f_pair_count"] = np.log1p(out["f_pair_count"])
    return out.replace([np.inf, -np.inf], np.nan)
