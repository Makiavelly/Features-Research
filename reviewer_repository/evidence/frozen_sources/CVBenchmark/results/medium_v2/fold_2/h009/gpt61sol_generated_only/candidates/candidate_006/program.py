import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    names = [
        "f_pair_count_7d", "f_pair_count_30d", "f_pair_count_90d",
        "f_pair_recency", "f_customer_count_30d", "f_customer_count_90d",
        "f_customer_recency", "f_item_count_7d", "f_item_count_30d",
        "f_item_count_90d", "f_item_recency", "f_pair_decay",
        "f_customer_decay", "f_item_decay", "f_affinity_type_30d",
        "f_affinity_department_30d", "f_affinity_garment_30d"
    ]
    if len(history) == 0:
        for name in names:
            out[name] = 0.0
        return out

    h = history
    days = h["days_ago"].astype(float)

    def counts(frame, keys):
        return frame.groupby(keys, sort=False).size()

    pair_index = pd.MultiIndex.from_arrays(
        [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
    )

    for window in (7, 30, 90):
        s = counts(h.loc[days <= window], ["customer_id", "article_id"])
        out["f_pair_count_%dd" % window] = s.reindex(pair_index).fillna(0).to_numpy()

    pair_rec = h.groupby(
        ["customer_id", "article_id"], sort=False
    )["days_ago"].min()
    out["f_pair_recency"] = pair_rec.reindex(pair_index).to_numpy()

    for window in (30, 90):
        s = counts(h.loc[days <= window], "customer_id")
        out["f_customer_count_%dd" % window] = X["customer_id"].map(s).fillna(0)

    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id", sort=False)["days_ago"].min()
    )

    for window in (7, 30, 90):
        s = counts(h.loc[days <= window], "article_id")
        out["f_item_count_%dd" % window] = X["article_id"].map(s).fillna(0)

    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    )

    weight = np.exp(-days / 30.0)
    weighted = pd.Series(weight.to_numpy(), index=h.index)
    pair_decay = weighted.groupby(
        [h["customer_id"], h["article_id"]], sort=False
    ).sum()
    out["f_pair_decay"] = pair_decay.reindex(pair_index).fillna(0).to_numpy()
    out["f_customer_decay"] = X["customer_id"].map(
        weighted.groupby(h["customer_id"], sort=False).sum()
    ).fillna(0)
    out["f_item_decay"] = X["article_id"].map(
        weighted.groupby(h["article_id"], sort=False).sum()
    ).fillna(0)

    def affinity(hist_col, raw_col):
        recent = h.loc[days <= 30]
        s = counts(recent, ["customer_id", hist_col])
        idx = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X[raw_col].to_numpy()
        ])
        return s.reindex(idx).fillna(0).to_numpy()

    out["f_affinity_type_30d"] = affinity(
        "product_type_no", "raw_i_product_type_no"
    )
    out["f_affinity_department_30d"] = affinity(
        "department_no", "raw_i_department_no"
    )
    out["f_affinity_garment_30d"] = affinity(
        "garment_group_no", "raw_i_garment_group_no"
    )

    return out.astype(float)
