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
        "f_affinity_product_30d", "f_item_channel1_share_30d",
        "f_pair_share_customer_30d", "f_pair_share_item_30d",
        "f_category_share_customer_30d"
    ]
    out = pd.DataFrame(index=X.index)
    if len(history) == 0:
        for name in names:
            out[name] = 0.0
        return out

    h = history
    d = h["days_ago"].astype(float)
    customer = X["customer_id"]
    article = X["article_id"]
    pair_index = pd.MultiIndex.from_arrays([
        customer.to_numpy(), article.to_numpy()
    ])

    def sizes(frame, keys):
        return frame.groupby(keys, sort=False).size()

    recent = h.loc[d <= 30]
    pair30 = sizes(recent, ["customer_id", "article_id"])
    customer30 = sizes(recent, "customer_id")
    item30 = sizes(recent, "article_id")

    for window in (7, 30, 90):
        s = sizes(h.loc[d <= window], ["customer_id", "article_id"])
        out["f_pair_count_%dd" % window] = (
            s.reindex(pair_index).fillna(0).to_numpy()
        )

    out["f_pair_recency"] = h.groupby(
        ["customer_id", "article_id"], sort=False
    )["days_ago"].min().reindex(pair_index).to_numpy()

    for window in (30, 90):
        out["f_customer_count_%dd" % window] = customer.map(
            sizes(h.loc[d <= window], "customer_id")
        ).fillna(0)

    out["f_customer_recency"] = customer.map(
        h.groupby("customer_id", sort=False)["days_ago"].min()
    )

    for window in (7, 30, 90):
        out["f_item_count_%dd" % window] = article.map(
            sizes(h.loc[d <= window], "article_id")
        ).fillna(0)

    out["f_item_recency"] = article.map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    )

    weights = pd.Series(np.exp(-d.to_numpy() / 30.0), index=h.index)
    out["f_pair_decay"] = weights.groupby(
        [h["customer_id"], h["article_id"]], sort=False
    ).sum().reindex(pair_index).fillna(0).to_numpy()
    out["f_customer_decay"] = customer.map(
        weights.groupby(h["customer_id"], sort=False).sum()
    ).fillna(0)
    out["f_item_decay"] = article.map(
        weights.groupby(h["article_id"], sort=False).sum()
    ).fillna(0)

    def affinity(history_column, raw_column):
        values = sizes(recent, ["customer_id", history_column])
        index = pd.MultiIndex.from_arrays([
            customer.to_numpy(), X[raw_column].to_numpy()
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
    out["f_affinity_product_30d"] = affinity(
        "product_code", "raw_i_product_code"
    )

    share = recent.groupby(
        "article_id", sort=False
    )["sales_channel_id"].apply(lambda z: (z == 1).mean())
    out["f_item_channel1_share_30d"] = article.map(share)

    pc = pair30.reindex(pair_index).fillna(0).to_numpy()
    cc = customer.map(customer30).fillna(0).to_numpy()
    ic = article.map(item30).fillna(0).to_numpy()
    out["f_pair_share_customer_30d"] = pc / np.maximum(cc, 1.0)
    out["f_pair_share_item_30d"] = pc / np.maximum(ic, 1.0)

    typ = affinity("product_type_no", "raw_i_product_type_no")
    out["f_category_share_customer_30d"] = typ / np.maximum(cc, 1.0)

    return out[names].astype(float)
