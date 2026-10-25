import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_pair_count_7d", "f_pair_count_30d", "f_pair_count_90d",
        "f_pair_recency", "f_customer_count_30d", "f_customer_count_90d",
        "f_customer_recency", "f_item_count_7d", "f_item_count_30d",
        "f_item_count_90d", "f_item_recency", "f_pair_decay",
        "f_customer_decay", "f_item_decay", "f_affinity_type_30d",
        "f_affinity_department_30d", "f_affinity_garment_30d",
        "f_affinity_colour_30d", "f_affinity_section_30d",
        "f_item_channel1_share_30d"
    ]
    out = pd.DataFrame(index=X.index)
    if len(history) == 0:
        for name in names:
            out[name] = 0.0
        return out

    h = history
    days = h["days_ago"].astype(float)
    pair_index = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(),
        X["article_id"].to_numpy()
    ])

    def grouped_size(frame, keys):
        return frame.groupby(keys, sort=False).size()

    for window in (7, 30, 90):
        values = grouped_size(
            h.loc[days <= window],
            ["customer_id", "article_id"]
        )
        out["f_pair_count_%dd" % window] = (
            values.reindex(pair_index).fillna(0).to_numpy()
        )

    out["f_pair_recency"] = h.groupby(
        ["customer_id", "article_id"], sort=False
    )["days_ago"].min().reindex(pair_index).to_numpy()

    for window in (30, 90):
        values = grouped_size(h.loc[days <= window], "customer_id")
        out["f_customer_count_%dd" % window] = (
            X["customer_id"].map(values).fillna(0)
        )

    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id", sort=False)["days_ago"].min()
    )

    for window in (7, 30, 90):
        values = grouped_size(h.loc[days <= window], "article_id")
        out["f_item_count_%dd" % window] = (
            X["article_id"].map(values).fillna(0)
        )

    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    )

    weights = pd.Series(
        np.exp(-days.to_numpy() / 30.0), index=h.index
    )
    out["f_pair_decay"] = weights.groupby(
        [h["customer_id"], h["article_id"]], sort=False
    ).sum().reindex(pair_index).fillna(0).to_numpy()

    out["f_customer_decay"] = X["customer_id"].map(
        weights.groupby(h["customer_id"], sort=False).sum()
    ).fillna(0)

    out["f_item_decay"] = X["article_id"].map(
        weights.groupby(h["article_id"], sort=False).sum()
    ).fillna(0)

    recent = h.loc[days <= 30]

    def affinity(history_column, raw_column):
        values = grouped_size(
            recent, ["customer_id", history_column]
        )
        index = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X[raw_column].to_numpy()
        ])
        return values.reindex(index).fillna(0).to_numpy()

    out["f_affinity_type_30d"] = affinity(
        "product_type_no", "raw_i_product_type_no"
    )
    out["f_affinity_department_30d"] = affinity(
        "department_no", "raw_i_department_no"
    )
    out["f_affinity_garment_30d"] = affinity(
        "garment_group_no", "raw_i_garment_group_no"
    )
    out["f_affinity_colour_30d"] = affinity(
        "colour_group_code", "raw_i_colour_group_code"
    )
    out["f_affinity_section_30d"] = affinity(
        "section_no", "raw_i_section_no"
    )

    channel_share = recent.groupby(
        "article_id", sort=False
    )["sales_channel_id"].apply(lambda values: (values == 1).mean())
    out["f_item_channel1_share_30d"] = X["article_id"].map(channel_share)

    return out[names].astype(float)
