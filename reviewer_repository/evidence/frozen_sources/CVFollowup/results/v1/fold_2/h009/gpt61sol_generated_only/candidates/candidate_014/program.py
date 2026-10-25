import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    feature_names = [
        "f_pair_7d", "f_pair_30d", "f_pair_180d", "f_pair_decay",
        "f_pair_recency", "f_user_7d", "f_user_30d", "f_user_180d",
        "f_user_decay", "f_item_7d", "f_item_30d", "f_item_180d",
        "f_item_decay", "f_item_recency", "f_user_department",
        "f_user_section", "f_user_product", "f_user_colour",
        "f_user_garment", "f_user_index_group", "f_user_garment_30d",
        "f_user_type_30d"
    ]
    if len(h) == 0:
        for c in feature_names:
            out[c] = 0.0
        return out

    uid = X["customer_id"].to_numpy()
    aid = X["article_id"].to_numpy()
    pair_index = pd.MultiIndex.from_arrays(
        [uid, aid], names=["customer_id", "article_id"]
    )

    def pair_count(frame):
        s = frame.groupby(
            ["customer_id", "article_id"], sort=False
        ).size()
        return s.reindex(pair_index).to_numpy(dtype=float)

    def user_count(frame):
        return X["customer_id"].map(
            frame.groupby("customer_id", sort=False).size()
        ).to_numpy(dtype=float)

    def item_count(frame):
        return X["article_id"].map(
            frame.groupby("article_id", sort=False).size()
        ).to_numpy(dtype=float)

    def user_category(column, raw_column, frame):
        s = frame.groupby(
            ["customer_id", column], sort=False
        ).size()
        ix = pd.MultiIndex.from_arrays(
            [uid, X[raw_column].to_numpy()],
            names=["customer_id", column]
        )
        return s.reindex(ix).to_numpy(dtype=float)

    r7 = h[h["days_ago"] <= 7]
    r30 = h[h["days_ago"] <= 30]
    r180 = h[h["days_ago"] <= 180]

    out["f_pair_7d"] = pair_count(r7)
    out["f_pair_30d"] = pair_count(r30)
    out["f_pair_180d"] = pair_count(r180)

    weights = np.exp(-h["days_ago"].astype(float) / 14.0)
    z = h.assign(_weight=weights)
    out["f_pair_decay"] = z.groupby(
        ["customer_id", "article_id"], sort=False
    )["_weight"].sum().reindex(pair_index).to_numpy(dtype=float)
    out["f_user_decay"] = X["customer_id"].map(
        z.groupby("customer_id", sort=False)["_weight"].sum()
    ).to_numpy(dtype=float)
    out["f_item_decay"] = X["article_id"].map(
        z.groupby("article_id", sort=False)["_weight"].sum()
    ).to_numpy(dtype=float)

    out["f_pair_recency"] = h.groupby(
        ["customer_id", "article_id"], sort=False
    )["days_ago"].min().reindex(pair_index).to_numpy(dtype=float)
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    ).to_numpy(dtype=float)

    out["f_user_7d"] = user_count(r7)
    out["f_user_30d"] = user_count(r30)
    out["f_user_180d"] = user_count(r180)
    out["f_item_7d"] = item_count(r7)
    out["f_item_30d"] = item_count(r30)
    out["f_item_180d"] = item_count(r180)

    out["f_user_department"] = user_category(
        "department_no", "raw_i_department_no", h
    )
    out["f_user_section"] = user_category(
        "section_no", "raw_i_section_no", h
    )
    out["f_user_product"] = user_category(
        "product_code", "raw_i_product_code", h
    )
    out["f_user_colour"] = user_category(
        "colour_group_code", "raw_i_colour_group_code", h
    )
    out["f_user_garment"] = user_category(
        "garment_group_no", "raw_i_garment_group_no", h
    )
    out["f_user_index_group"] = user_category(
        "index_group_no", "raw_i_index_group_no", h
    )
    out["f_user_garment_30d"] = user_category(
        "garment_group_no", "raw_i_garment_group_no", r30
    )
    out["f_user_type_30d"] = user_category(
        "product_type_no", "raw_i_product_type_no", r30
    )

    for c in out.columns:
        out[c] = pd.to_numeric(out[c], errors="coerce").replace(
            [np.inf, -np.inf], np.nan
        )
    return out.reindex(index=X.index)
